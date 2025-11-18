# Port.io Integration Guide

This guide explains how to automatically sync repositories from your Port.io service catalog to the documentation aggregation system.

## Overview

When configured, this integration will:
- **Automatically discover** all services in your Port.io catalog
- **Extract repository URLs** from service properties
- **Update** `repos-config.yaml` with all repositories
- **Trigger** documentation aggregation
- **Run hourly** to stay in sync with your catalog

## Architecture

```
Port.io Catalog (Services)
    ↓
GitHub Actions (hourly sync)
    ↓
Update repos-config.yaml
    ↓
Trigger docs aggregation
    ↓
Deploy updated docs
```

## Setup Steps

### 1. Get Port.io API Credentials

1. Log in to [Port.io](https://app.getport.io)
2. Go to **Settings** → **API Tokens**
3. Click **Generate API Token**
4. Save the **Client ID** and **Client Secret**

### 2. Add Credentials to GitHub

1. Go to your GitHub repo: `https://github.com/acarter-wl/platform-docs`
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add two secrets:
   - Name: `PORT_CLIENT_ID`, Value: `your_client_id`
   - Name: `PORT_CLIENT_SECRET`, Value: `your_client_secret`

### 3. Configure Port.io Service Blueprint

Your services in Port.io need a `repository` property. If you haven't set this up yet:

#### Option A: Use Existing Property

If your services already have a GitHub URL property, the script will look for:
- `repository`
- `repo`
- `githubRepo`
- `github_repo`

#### Option B: Add New Property

1. In Port.io, go to **Builder** → **Blueprints**
2. Edit your **service** blueprint
3. Add a property:
   ```json
   {
     "identifier": "repository",
     "title": "Repository",
     "type": "string",
     "format": "url",
     "description": "GitHub repository URL"
   }
   ```

4. For each service, set the repository URL:
   - Full URL: `https://github.com/acarter-wl/TheVault`
   - Or short form: `acarter-wl/TheVault`

### 4. Test the Sync

#### Manual Test (Local)

```bash
# Set credentials
export PORT_CLIENT_ID=your_client_id
export PORT_CLIENT_SECRET=your_client_secret

# Run sync
python scripts/sync-from-port.py

# Check the updated config
cat repos-config.yaml
```

#### Manual Test (GitHub Actions)

1. Go to **Actions** tab in GitHub
2. Select **Sync Repositories from Port.io**
3. Click **Run workflow**
4. Monitor the execution

### 5. Verify Automatic Sync

Once set up, the sync runs automatically every hour. Check:

1. **Actions** tab → **Sync Repositories from Port.io**
2. Look for hourly runs
3. Check commit history for automatic updates

## How It Works

### Repository Discovery

The script:
1. Authenticates with Port.io API
2. Queries the `service` blueprint for all entities
3. Extracts repository URLs from properties
4. Generates configuration for each service

### Configuration Format

For each Port.io service, it creates:

```yaml
repos:
  - repo: acarter-wl/service-name
    docs_path: docs
    target_path: services/service-name
    enabled: true
    description: Service Title from Port.io
```

### Documentation Requirements

Each repository must have a `docs/` folder:

```
your-service/
├── src/
└── docs/          # Required
    ├── index.md
    └── ...
```

## Advanced Configuration

### Custom Docs Path

If your services use a different docs folder, add a `docsPath` property in Port.io:

```json
{
  "identifier": "docsPath",
  "title": "Documentation Path",
  "type": "string",
  "default": "docs"
}
```

### Manual Repositories

To add repos manually (not synced from Port.io), add `manual: true`:

```yaml
repos:
  - repo: acarter-wl/special-repo
    docs_path: documentation
    target_path: special/location
    enabled: true
    manual: true  # Won't be removed by Port.io sync
```

### Disable Specific Services

To exclude a service from docs aggregation, add a property in Port.io:

```json
{
  "identifier": "includeDocs",
  "title": "Include in Documentation",
  "type": "boolean",
  "default": true
}
```

Then update the sync script to check this property.

## Port.io Webhook (Optional)

For real-time sync when services are created/updated:

### 1. Create Webhook in Port.io

1. Go to **Settings** → **Webhooks**
2. Click **Add Webhook**
3. Configure:
   - **URL**: `https://api.github.com/repos/acarter-wl/platform-docs/dispatches`
   - **Method**: POST
   - **Headers**:
     - `Accept: application/vnd.github+json`
     - `Authorization: Bearer YOUR_GITHUB_PAT`
   - **Body**:
     ```json
     {
       "event_type": "port-service-created"
     }
     ```
4. **Trigger**: On service created/updated

### 2. Create GitHub PAT

1. Go to GitHub **Settings** → **Developer settings** → **Personal access tokens**
2. Generate token with `repo` scope
3. Use in Port.io webhook header

## Troubleshooting

### No Repositories Found

**Issue**: Script runs but finds no services

**Solutions**:
- Verify blueprint name is `service` (or update script)
- Check services have `repository` property
- Ensure API credentials have read permissions

### Authentication Failed

**Issue**: `401 Unauthorized` error

**Solutions**:
- Verify `PORT_CLIENT_ID` and `PORT_CLIENT_SECRET` are correct
- Check credentials haven't expired
- Ensure they're properly set as GitHub secrets

### Docs Not Appearing

**Issue**: Repos synced but docs don't show up

**Solutions**:
- Verify repository has `docs/` folder
- Check `skip_missing_docs: true` in config
- Run docs aggregation manually to see errors
- Check GitHub Actions logs

### Webhook Not Triggering

**Issue**: Port.io webhook doesn't trigger GitHub Actions

**Solutions**:
- Verify webhook URL is correct
- Check GitHub PAT has proper permissions
- Test webhook manually in Port.io
- Check GitHub Actions logs for incoming webhooks

## Monitoring

### Check Sync Status

```bash
# View last sync
git log --grep="Sync repositories from Port.io" -1

# View current config
cat repos-config.yaml

# Check service count
grep "^  - repo:" repos-config.yaml | wc -l
```

### GitHub Actions Dashboard

Monitor in the Actions tab:
- **Sync Repositories from Port.io** - Runs hourly
- **Aggregate and Deploy Documentation** - Triggered after sync

## FAQ

**Q: How often does it sync?**
A: Every hour automatically, plus on-demand via manual trigger or webhook.

**Q: Can I mix Port.io and manual repos?**
A: Yes! Add `manual: true` to manual entries and they'll be preserved.

**Q: What if a service doesn't have docs?**
A: It's still added to config, but `skip_missing_docs: true` prevents failure. An index.md is auto-generated.

**Q: Can I customize the target path?**
A: Yes, add a `docsPath` property in Port.io or edit the sync script.

**Q: Does it support private repos?**
A: Yes, the docs aggregation uses `DOCS_PAT` or `GITHUB_TOKEN` for authentication.

## Need Help?

- **GitHub Issues**: [Create an issue](https://github.com/acarter-wl/platform-docs/issues)
- **Port.io Docs**: [Port.io Documentation](https://docs.getport.io)
