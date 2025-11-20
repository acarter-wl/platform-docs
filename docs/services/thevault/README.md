# Sample Documentation for Testing

This directory contains sample documentation that you can copy to another repository to test the doc aggregation functionality.

## What's Included

This is a complete, production-ready documentation structure for a fictional "Sample Service" that demonstrates best practices:

```
sample-docs/
├── index.md                           # Main overview page
├── architecture/
│   └── overview.md                    # Architecture documentation
├── api/
│   └── endpoints.md                   # API reference
├── runbooks/
│   └── incident-response.md           # Operational runbooks
└── how-to/
    └── local-development.md           # Step-by-step guides
```

## Features Demonstrated

- **Comprehensive structure**: Shows all major doc types
- **Mermaid diagrams**: Architecture visualizations
- **Code examples**: Multiple languages (TypeScript, Python, Bash, SQL)
- **Tables**: Formatted data presentation
- **Links**: Cross-references between docs
- **Admonitions**: Notes, warnings, tips
- **Real-world content**: Practical, production-ready examples

## How to Use for Testing

### Option 1: Test with a New Repository

1. **Create a test repository on GitHub**:
   ```bash
   # On GitHub, create a new repo (e.g., "test-service-docs")
   ```

2. **Copy these docs to the repo**:
   ```bash
   # Clone your test repo
   git clone https://github.com/your-org/test-service-docs.git
   cd test-service-docs

   # Copy the sample docs
   mkdir docs
   cp -r /path/to/platform-docs/sample-docs/* docs/

   # Commit and push
   git add docs/
   git commit -m "docs: Add sample documentation"
   git push
   ```

3. **Add the repo to platform-docs**:
   Edit `repos-config.yaml` in platform-docs:
   ```yaml
   repos:
     - repo: your-org/test-service-docs
       docs_path: docs
       target_path: services/test-service
       enabled: true
       description: Test service for doc aggregation
   ```

4. **Run the aggregation**:
   ```bash
   # In platform-docs directory
   python scripts/aggregate-docs.py

   # Verify docs were copied
   ls -la docs/services/test-service/

   # Preview the site
   mkdocs serve
   ```

### Option 2: Test with TheVault (Already Configured)

If you have access to TheVault repo, you can copy these docs there:

```bash
# Clone TheVault (if you haven't)
git clone https://github.com/acarter-wl/TheVault.git
cd TheVault

# Create docs directory if it doesn't exist
mkdir -p docs

# Copy sample docs
cp -r /path/to/platform-docs/sample-docs/* docs/

# Commit and push
git add docs/
git commit -m "docs: Add sample documentation for testing"
git push
```

Then run aggregation in platform-docs:
```bash
cd /path/to/platform-docs
python scripts/aggregate-docs.py
```

### Option 3: Test with Different Doc Structures

Modify the sample docs to test edge cases:

**Test: Missing index.md**
```bash
cp -r sample-docs test-no-index
rm test-no-index/index.md
# Should auto-generate index.md
```

**Test: Nested structure**
```bash
cp -r sample-docs test-nested
mkdir test-nested/advanced
mv test-nested/architecture/* test-nested/advanced/
# Test if nested folders work
```

**Test: Minimal docs**
```bash
mkdir test-minimal/docs
echo "# Minimal Test" > test-minimal/docs/index.md
# Test with bare minimum
```

## What to Verify After Aggregation

1. **Files copied correctly**:
   ```bash
   ls -la docs/services/<service-name>/
   ```

2. **Index.md exists** (auto-generated if missing):
   ```bash
   cat docs/services/<service-name>/index.md
   ```

3. **MkDocs builds without errors**:
   ```bash
   mkdocs build --strict
   ```

4. **Site navigation works**:
   ```bash
   mkdocs serve
   # Open http://localhost:8000
   # Navigate to your service docs
   ```

5. **Mermaid diagrams render**:
   - Check architecture/overview.md in the browser
   - Diagrams should display properly

6. **Search functionality**:
   - Use search bar in MkDocs site
   - Search for terms like "PostgreSQL" or "Redis"
   - Should find content in aggregated docs

7. **Links work**:
   - Click internal links between pages
   - All relative links should work

## Expected MkDocs Output

When aggregation succeeds, you should see:

```
🚀 Starting documentation aggregation...
📋 Found 2 repositories in configuration
============================================================
Processing: your-org/test-service-docs
============================================================
📦 Cloning your-org/test-service-docs...
✅ Cloned your-org/test-service-docs
📄 Copying docs from /path/.temp-repos/test-service-docs/docs to /path/docs/services/test-service
✅ Copied docs for your-org/test-service-docs
============================================================
🧹 Cleaning up temporary files...
============================================================
📊 Aggregation Summary
============================================================
✅ Successful: 2
❌ Failed: 0
⏭️  Skipped: 0
============================================================
🎉 Documentation aggregation completed successfully!
```

## Troubleshooting

### Aggregation Script Fails

```bash
# Check Python version
python --version  # Should be 3.11+

# Check dependencies installed
pip install -r requirements.txt

# Check GitHub token
echo $GITHUB_TOKEN

# Run with verbose logging
python scripts/aggregate-docs.py --config repos-config.yaml
```

### Docs Not Showing in Site

```bash
# Check docs were copied
ls -la docs/services/

# Rebuild site
mkdocs build --clean

# Check for errors
mkdocs build --strict --verbose
```

### Links Broken

- Ensure all markdown links use relative paths
- Check that linked files exist in the same repo
- Verify paths in `repos-config.yaml` are correct

## Customizing Sample Docs

Feel free to modify these docs for your specific testing needs:

1. **Change service name**: Search and replace "Sample Service"
2. **Add more pages**: Create new .md files in any folder
3. **Test different formats**: Add images, videos, code samples
4. **Test edge cases**: Unicode, special characters, very long files

## Clean Up After Testing

To remove test docs:

```bash
# Remove aggregated docs
rm -rf docs/services/test-service/

# Or remove all services
rm -rf docs/services/

# Rebuild site
mkdocs build --clean
```

## Next Steps

After verifying aggregation works:

1. Add real service repositories to `repos-config.yaml`
2. Set up GitHub Actions workflow (`.github/workflows/aggregate-docs.yml`)
3. Configure GitHub Pages deployment
4. Set up scheduled runs (every 4 hours)
5. Document process for teams to add their docs

## Questions?

- Check the main [README.md](../README.md) for platform-docs
- Review [aggregate-docs.py](../scripts/aggregate-docs.py) for how it works
- Test locally before pushing to production
