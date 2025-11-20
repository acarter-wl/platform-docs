# GitHub Actions Setup Guide

This guide explains how to configure GitHub Actions to automatically aggregate documentation from other repositories.

## Problem: "Could not read Password" Error

If you see this error in GitHub Actions:

```
fatal: could not read Password for 'https://***@github.com': No such device or address
```

This means the workflow doesn't have the proper authentication to clone your source repositories.

## Solution: Configure GitHub Token

### For Public Repositories

If all your source repositories (like TheVault) are **public**, no additional setup is needed. The default `GITHUB_TOKEN` should work.

### For Private Repositories (RECOMMENDED)

If any of your source repositories are **private**, you need to create a Personal Access Token (PAT):

#### Step 1: Create a Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Or visit: https://github.com/settings/tokens

2. Click "Generate new token (classic)"

3. Configure the token:
   - **Name**: `platform-docs-aggregation`
   - **Expiration**: Choose appropriate expiration (90 days recommended)
   - **Scopes**: Select `repo` (Full control of private repositories)

4. Click "Generate token" and **copy the token** (you won't see it again!)

#### Step 2: Add Token to Repository Secrets

1. Go to your platform-docs repository on GitHub

2. Navigate to: **Settings → Secrets and variables → Actions**

3. Click "New repository secret"

4. Configure the secret:
   - **Name**: `DOCS_PAT`
   - **Secret**: Paste the token you copied in Step 1

5. Click "Add secret"

#### Step 3: Verify Configuration

1. Go to the "Actions" tab in your repository

2. Find the "Aggregate and Deploy Documentation" workflow

3. Click "Run workflow" to manually trigger it

4. Watch the logs to verify it works:
   - ✅ You should see: "GitHub token is configured"
   - ✅ You should see: "Cloning acarter-wl/TheVault..."
   - ✅ You should see: "Documentation aggregation completed successfully!"

## How the Token is Used

The workflow uses the token in this order:

1. **First choice**: `DOCS_PAT` secret (your Personal Access Token)
2. **Fallback**: `GITHUB_TOKEN` (default GitHub Actions token)

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.DOCS_PAT || secrets.GITHUB_TOKEN }}
```

The default `GITHUB_TOKEN` only works for:
- Public repositories
- Private repositories in the same organization (sometimes)

For reliable access to private repositories, always use `DOCS_PAT`.

## Workflow Configuration

The workflow is configured in `.github/workflows/aggregate-docs.yml` and runs:

- **Automatically**: Every 4 hours
- **On push**: When you update `repos-config.yaml` or the workflow file
- **Manually**: Via the Actions tab → "Run workflow" button

## Troubleshooting

### Error: "GitHub token is not set"

This shouldn't happen, as the workflow always has access to `GITHUB_TOKEN`. If you see this, it's a workflow configuration issue.

### Error: "Failed to clone [repo]"

**Cause**: The token doesn't have access to the repository.

**Solution**:
1. Verify the repository name in `repos-config.yaml` is correct
2. If the repo is private, create a `DOCS_PAT` secret (see above)
3. Make sure the PAT has `repo` scope
4. Verify the PAT hasn't expired

### Error: "No changes to commit"

This is **normal** if the documentation hasn't changed since the last run. The workflow will still build and deploy the site.

### Build Warnings About Broken Links

This is **expected** if:
- A source repository's `docs/` folder only contains `index.md` but references other files
- Navigation links point to pages that don't exist yet

These warnings don't stop deployment, but you should fix broken links in your source repositories.

## Testing Locally

Before relying on GitHub Actions, test aggregation locally:

```bash
# Set your GitHub token
export GITHUB_TOKEN=ghp_your_token_here

# Run aggregation
python scripts/aggregate-docs.py

# Build the site
mkdocs build --strict

# Preview locally
mkdocs serve
```

If it works locally but fails in GitHub Actions, the issue is with the `DOCS_PAT` secret configuration.

## Security Best Practices

1. **Use token expiration**: Set PATs to expire (90 days recommended)
2. **Minimal scope**: Only grant `repo` scope, nothing more
3. **Rotate regularly**: Update the token before it expires
4. **Monitor usage**: Check GitHub Actions logs for unexpected cloning
5. **Revoke if compromised**: Immediately revoke and regenerate if exposed

## Token Permissions Needed

The PAT needs these permissions:

| Permission | Why It's Needed |
|------------|-----------------|
| `repo` | Clone private repositories to aggregate their documentation |

The workflow does NOT need:
- ❌ `workflow` - Not modifying workflows in other repos
- ❌ `write:packages` - Not publishing packages
- ❌ `admin:org` - Not managing organization settings

## Alternative: GitHub App

For organizations with many repositories, consider creating a GitHub App instead of using a PAT:

1. More granular permissions
2. Better audit logging
3. Doesn't count against user quota
4. Can be scoped to specific repositories

See: https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps

## Next Steps

After setting up the token:

1. ✅ Verify the workflow runs successfully
2. ✅ Check your documentation site is deployed
3. ✅ Add more repositories to `repos-config.yaml`
4. ✅ Set up notifications for workflow failures
5. ✅ Document the process for your team

## Support

- **Workflow issues**: Check GitHub Actions logs
- **Token issues**: Verify token hasn't expired
- **Repository access**: Confirm PAT has `repo` scope
- **Still stuck?**: Review the logs for specific error messages
