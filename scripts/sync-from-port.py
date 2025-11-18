#!/usr/bin/env python3
"""
Port.io Repository Sync Script

Syncs service repositories from Port.io catalog to repos-config.yaml.
This script queries Port.io API and automatically updates the configuration
with all services that have a 'repository' property.

Usage:
    python scripts/sync-from-port.py

Environment Variables:
    PORT_CLIENT_ID: Port.io API client ID
    PORT_CLIENT_SECRET: Port.io API client secret
"""

import os
import sys
import yaml
import requests
from pathlib import Path
from typing import List, Dict, Optional


class PortSync:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://api.getport.io/v1"
        self.access_token = None
        self.config_path = Path("repos-config.yaml")

    def authenticate(self) -> bool:
        """Authenticate with Port.io API"""
        print("🔐 Authenticating with Port.io...")

        auth_url = "https://api.getport.io/v1/auth/access_token"
        response = requests.post(
            auth_url,
            json={
                "clientId": self.client_id,
                "clientSecret": self.client_secret
            }
        )

        if response.status_code == 200:
            self.access_token = response.json()["accessToken"]
            print("✅ Authenticated successfully")
            return True
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(response.text)
            return False

    def get_services(self) -> List[Dict]:
        """Get all service entities from Port.io"""
        print("📦 Fetching services from Port.io catalog...")

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        # Query for service blueprint entities
        # Adjust the blueprint name based on your Port.io setup
        response = requests.get(
            f"{self.base_url}/blueprints/service/entities",
            headers=headers,
            params={
                "include": "properties"
            }
        )

        if response.status_code == 200:
            entities = response.json()["entities"]
            print(f"✅ Found {len(entities)} services")
            return entities
        else:
            print(f"❌ Failed to fetch services: {response.status_code}")
            print(response.text)
            return []

    def extract_repo_config(self, service: Dict) -> Optional[Dict]:
        """Extract repository configuration from Port.io service entity"""
        props = service.get("properties", {})

        # Common property names in Port.io for repository
        repo_url = (
            props.get("repository") or
            props.get("repo") or
            props.get("githubRepo") or
            props.get("github_repo")
        )

        if not repo_url:
            return None

        # Extract org/repo from GitHub URL
        # e.g., https://github.com/acarter-wl/TheVault -> acarter-wl/TheVault
        repo = None
        if "github.com" in repo_url:
            parts = repo_url.rstrip("/").split("/")
            if len(parts) >= 2:
                repo = f"{parts[-2]}/{parts[-1]}"
        else:
            # Assume it's already in org/repo format
            repo = repo_url

        if not repo:
            return None

        # Generate target path from service name
        service_name = service.get("identifier", "").lower().replace(" ", "-")

        return {
            "repo": repo,
            "docs_path": props.get("docsPath", "docs"),
            "target_path": f"services/{service_name}",
            "enabled": True,
            "description": service.get("title", service_name)
        }

    def update_config(self, repos: List[Dict]) -> bool:
        """Update repos-config.yaml with Port.io services"""
        print("📝 Updating repos-config.yaml...")

        # Load existing config
        if self.config_path.exists():
            with open(self.config_path) as f:
                config = yaml.safe_load(f)
        else:
            config = {"repos": [], "config": {}}

        # Preserve config options
        config_options = config.get("config", {
            "clean_before_copy": True,
            "skip_missing_docs": True,
            "create_index_if_missing": True,
            "commit_message": "docs: Update aggregated documentation from source repos"
        })

        # Create new repos list
        # Keep manually added repos (those with a 'manual: true' flag)
        manual_repos = [r for r in config.get("repos", []) if r.get("manual", False)]

        # Add Port.io synced repos
        new_repos = manual_repos + repos

        # Update config
        config["repos"] = new_repos
        config["config"] = config_options

        # Write back
        with open(self.config_path, "w") as f:
            f.write("# Repository Documentation Aggregation Configuration\n")
            f.write("# Auto-synced from Port.io - DO NOT EDIT MANUALLY\n")
            f.write("# To add repos manually, add 'manual: true' to the repo entry\n\n")
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        print(f"✅ Updated config with {len(repos)} repositories")
        return True

    def sync(self) -> bool:
        """Main sync process"""
        print("🚀 Starting Port.io sync...\n")

        # Authenticate
        if not self.authenticate():
            return False

        # Get services from Port.io
        services = self.get_services()
        if not services:
            print("⚠️  No services found in Port.io")
            return True

        # Extract repo configurations
        repos = []
        for service in services:
            repo_config = self.extract_repo_config(service)
            if repo_config:
                repos.append(repo_config)
                print(f"  📌 {repo_config['repo']} -> {repo_config['target_path']}")

        print(f"\n📊 Summary: {len(repos)}/{len(services)} services have repositories")

        # Update configuration
        if repos:
            return self.update_config(repos)
        else:
            print("⚠️  No repositories to sync")
            return True


def main():
    # Get Port.io credentials from environment
    client_id = os.environ.get("PORT_CLIENT_ID")
    client_secret = os.environ.get("PORT_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("❌ Error: PORT_CLIENT_ID and PORT_CLIENT_SECRET environment variables required")
        print("\nSet them with:")
        print("  export PORT_CLIENT_ID=your_client_id")
        print("  export PORT_CLIENT_SECRET=your_client_secret")
        sys.exit(1)

    # Run sync
    syncer = PortSync(client_id, client_secret)
    success = syncer.sync()

    if success:
        print("\n🎉 Port.io sync completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Port.io sync failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
