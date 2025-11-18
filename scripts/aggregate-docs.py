#!/usr/bin/env python3
"""
Documentation Aggregation Script

This script aggregates documentation from multiple GitHub repositories
into the platform-docs repository for centralized documentation.

Usage:
    python scripts/aggregate-docs.py [--config repos-config.yaml] [--token TOKEN]

Environment Variables:
    GITHUB_TOKEN: GitHub Personal Access Token for private repos
"""

import os
import sys
import yaml
import shutil
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Optional


class DocAggregator:
    def __init__(self, config_path: str, github_token: Optional[str] = None):
        self.config_path = Path(config_path)
        self.github_token = github_token or os.environ.get('GITHUB_TOKEN')
        self.workspace = Path.cwd()
        self.temp_dir = self.workspace / '.temp-repos'
        self.docs_dir = self.workspace / 'docs'

        # Load configuration
        with open(self.config_path) as f:
            self.config = yaml.safe_load(f)

        self.repos = self.config.get('repos', [])
        self.options = self.config.get('config', {})

    def clean_temp_dir(self):
        """Remove temporary clone directory"""
        if self.temp_dir.exists():
            print(f"🧹 Cleaning temporary directory: {self.temp_dir}")
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def clone_repo(self, repo: str) -> Path:
        """Clone a repository to temporary directory"""
        repo_name = repo.split('/')[-1]
        clone_path = self.temp_dir / repo_name

        print(f"📦 Cloning {repo}...")

        # Build clone URL with token if available
        if self.github_token:
            clone_url = f"https://{self.github_token}@github.com/{repo}.git"
        else:
            clone_url = f"https://github.com/{repo}.git"

        try:
            # Clone with minimal depth for speed
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', clone_url, str(clone_path)],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ Cloned {repo}")
            return clone_path
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to clone {repo}: {e.stderr}")
            return None

    def copy_docs(self, source_path: Path, target_path: Path, repo_info: Dict):
        """Copy documentation from source to target"""
        docs_path = source_path / repo_info.get('docs_path', 'docs')
        target_full_path = self.docs_dir / target_path

        # Check if docs folder exists
        if not docs_path.exists():
            if self.options.get('skip_missing_docs', True):
                print(f"⚠️  No docs folder found at {docs_path}, skipping...")
                return
            else:
                raise FileNotFoundError(f"Documentation not found: {docs_path}")

        # Clean target directory if configured
        if self.options.get('clean_before_copy', True) and target_full_path.exists():
            print(f"🧹 Cleaning {target_full_path}")
            shutil.rmtree(target_full_path)

        # Create target directory
        target_full_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy documentation
        print(f"📄 Copying docs from {docs_path} to {target_full_path}")
        shutil.copytree(docs_path, target_full_path, dirs_exist_ok=True)

        # Create index.md if missing
        if self.options.get('create_index_if_missing', True):
            index_file = target_full_path / 'index.md'
            if not index_file.exists():
                print(f"📝 Creating index.md for {repo_info['repo']}")
                self.create_index(index_file, repo_info)

        print(f"✅ Copied docs for {repo_info['repo']}")

    def create_index(self, index_path: Path, repo_info: Dict):
        """Create a basic index.md if one doesn't exist"""
        repo = repo_info['repo']
        description = repo_info.get('description', f'Documentation for {repo}')

        content = f"""# {repo.split('/')[-1]}

{description}

## Overview

This documentation is automatically aggregated from the source repository:
[{repo}](https://github.com/{repo})

## Contents

Browse the documentation using the navigation menu on the left.

---

*Last updated: This documentation is automatically updated every 2-4 hours from the source repository.*
"""
        index_path.write_text(content)

    def aggregate(self):
        """Main aggregation process"""
        print("🚀 Starting documentation aggregation...")
        print(f"📋 Found {len(self.repos)} repositories in configuration")

        # Clean temp directory
        self.clean_temp_dir()

        successful = 0
        failed = 0
        skipped = 0

        for repo_info in self.repos:
            # Check if enabled
            if not repo_info.get('enabled', True):
                print(f"⏭️  Skipping {repo_info['repo']} (disabled)")
                skipped += 1
                continue

            repo = repo_info['repo']
            target_path = repo_info['target_path']

            print(f"\n{'='*60}")
            print(f"Processing: {repo}")
            print(f"{'='*60}")

            # Clone repository
            clone_path = self.clone_repo(repo)
            if not clone_path:
                failed += 1
                continue

            # Copy documentation
            try:
                self.copy_docs(clone_path, target_path, repo_info)
                successful += 1
            except Exception as e:
                print(f"❌ Failed to copy docs from {repo}: {e}")
                failed += 1

        # Cleanup
        print(f"\n{'='*60}")
        print("🧹 Cleaning up temporary files...")
        self.clean_temp_dir()

        # Summary
        print(f"\n{'='*60}")
        print("📊 Aggregation Summary")
        print(f"{'='*60}")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"⏭️  Skipped: {skipped}")
        print(f"{'='*60}")

        if failed > 0:
            print("\n⚠️  Some repositories failed to aggregate. Check logs above.")
            return False

        print("\n🎉 Documentation aggregation completed successfully!")
        return True


def main():
    parser = argparse.ArgumentParser(
        description='Aggregate documentation from multiple repositories'
    )
    parser.add_argument(
        '--config',
        default='repos-config.yaml',
        help='Path to configuration file (default: repos-config.yaml)'
    )
    parser.add_argument(
        '--token',
        help='GitHub token for private repos (default: GITHUB_TOKEN env var)'
    )

    args = parser.parse_args()

    # Check if config exists
    if not Path(args.config).exists():
        print(f"❌ Configuration file not found: {args.config}")
        sys.exit(1)

    # Run aggregation
    aggregator = DocAggregator(args.config, args.token)
    success = aggregator.aggregate()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
