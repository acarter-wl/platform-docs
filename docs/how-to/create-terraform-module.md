# How to Create a New Terraform Module

## Overview
This guide walks you through creating a new reusable Terraform module in the plt-modules repository, following our team's standards and best practices.

**Time Required:** ~45-60 minutes
**Difficulty:** Intermediate
**Prerequisites:**
- Terraform v1.5+ installed
- Git and GitHub access
- plt-modules repository cloned locally
- Understanding of terraform module basics

## When to Use This
Create a new terraform module when:
- You're building infrastructure that will be reused across multiple accounts/environments
- You want to standardize a common AWS resource pattern
- You need to abstract complexity from module consumers
- You're replacing repetitive terraform code with a reusable component

## Before You Begin

### Tools Required
```bash
# Verify you have required tools
terraform version    # Should be v1.5+
git --version        # Any recent version
gh --version         # GitHub CLI (optional but helpful)

# Check you're in the right repo
pwd
# Should be in: .../plt-modules or plt-modules-main
```

### Required Access
- [ ] GitHub write access to plt-modules repository
- [ ] AWS account access for testing (dev account)
- [ ] Ability to create tags (for versioning)

### Gather Required Information
Before starting, decide:
- **Module Name:** What will you call it? (e.g., `s3-bucket`, `rds-instance`)
- **Module Purpose:** One sentence description
- **Module Category:** Where does it fit? (`aws/`, `compositions/`, `common/`)
- **Required Inputs:** What variables are required?
- **Outputs:** What values should it expose?

## Step-by-Step Instructions

### Step 1: Create Module Directory Structure
Create the directory for your new module.

```bash
# Navigate to plt-modules repo
cd /path/to/plt-modules-main

# Create module directory (example: new S3 bucket module)
mkdir -p aws/s3-private-bucket

cd aws/s3-private-bucket
```

**Module Placement Guidelines:**
- `aws/` - Atomic AWS resources (single-purpose modules)
- `compositions/` - Multi-resource compositions
- `common/` - Shared utilities and data sources

---

### Step 2: Create Core Terraform Files
Every module needs these standard files.

**Create `main.tf`:**
```hcl
# main.tf - Primary resource definitions
resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name

  tags = merge(
    var.tags,
    {
      Name = var.bucket_name
    }
  )
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id

  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Suspended"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "AES256"
      kms_master_key_id = var.kms_key_id
    }
  }
}

resource "aws_s3_bucket_public_access_block" "this" {
  bucket = aws_s3_bucket.this.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

**Create `variables.tf`:**
```hcl
# variables.tf - Input variable definitions
variable "bucket_name" {
  description = "Name of the S3 bucket (must be globally unique)"
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]*[a-z0-9]$", var.bucket_name))
    error_message = "Bucket name must contain only lowercase letters, numbers, and hyphens"
  }
}

variable "enable_versioning" {
  description = "Enable versioning on the S3 bucket"
  type        = bool
  default     = true
}

variable "kms_key_id" {
  description = "KMS key ID for encryption (optional, uses AES256 if not provided)"
  type        = string
  default     = null
}

variable "tags" {
  description = "Additional tags to apply to the bucket"
  type        = map(string)
  default     = {}
}
```

**Create `outputs.tf`:**
```hcl
# outputs.tf - Values exposed to module consumers
output "bucket_id" {
  description = "The ID (name) of the bucket"
  value       = aws_s3_bucket.this.id
}

output "bucket_arn" {
  description = "The ARN of the bucket"
  value       = aws_s3_bucket.this.arn
}

output "bucket_domain_name" {
  description = "The bucket domain name"
  value       = aws_s3_bucket.this.bucket_domain_name
}
```

**Create `providers.tf`:**
```hcl
# providers.tf - Terraform and provider version constraints
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

---

### Step 3: Create Module Documentation
Every module MUST have a comprehensive README.

**Create `README.md`:**
```markdown
# S3 Private Bucket Module

Creates a private S3 bucket with security best practices enabled:
- Versioning enabled by default
- Server-side encryption (AES256 or KMS)
- Public access completely blocked
- Consistent tagging strategy

## Usage

### Basic Example
\`\`\`hcl
module "my_bucket" {
  source = "git::https://github.com/intelerad-org/plt-modules.git//aws/s3-private-bucket?ref=s3-private-bucket/v1.0.0"

  bucket_name = "my-application-data"

  tags = {
    Environment = "production"
    Application = "my-app"
  }
}
\`\`\`

### With KMS Encryption
\`\`\`hcl
module "encrypted_bucket" {
  source = "git::https://github.com/intelerad-org/plt-modules.git//aws/s3-private-bucket?ref=s3-private-bucket/v1.0.0"

  bucket_name        = "my-encrypted-data"
  enable_versioning  = true
  kms_key_id         = aws_kms_key.my_key.arn

  tags = {
    Environment = "production"
    Compliance  = "PCI"
  }
}
\`\`\`

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket (globally unique) | string | n/a | yes |
| enable_versioning | Enable versioning on the bucket | bool | true | no |
| kms_key_id | KMS key ID for encryption | string | null | no |
| tags | Additional tags to apply | map(string) | {} | no |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID (name) of the bucket |
| bucket_arn | The ARN of the bucket |
| bucket_domain_name | The bucket domain name |

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.5.0 |
| aws | ~> 5.0 |

## Security Features
- ✅ Public access completely blocked
- ✅ Encryption at rest (AES256 or KMS)
- ✅ Versioning enabled by default
- ✅ All buckets tagged consistently

## Breaking Changes

### v2.0.0
- Changed default encryption from AES256 to require KMS
- Removed `lifecycle_rules` variable (use separate module)

### v1.0.0
- Initial release

## Maintainers
Platform Engineering Team (@platform-team)

## License
Internal use only
```

---

### Step 4: Create Example Directory
Provide working examples for users to copy.

```bash
# Create examples directory
mkdir -p examples/basic examples/advanced

# Basic example
cat > examples/basic/main.tf <<EOF
module "basic_bucket" {
  source = "../../"

  bucket_name = "example-basic-bucket"

  tags = {
    Environment = "dev"
    Purpose     = "testing"
  }
}

output "bucket_id" {
  value = module.basic_bucket.bucket_id
}
EOF

# Advanced example
cat > examples/advanced/main.tf <<EOF
module "encrypted_bucket" {
  source = "../../"

  bucket_name       = "example-encrypted-bucket"
  enable_versioning = true
  kms_key_id        = aws_kms_key.example.arn

  tags = {
    Environment = "production"
    Compliance  = "required"
  }
}

resource "aws_kms_key" "example" {
  description = "Example KMS key for S3 encryption"
}

output "bucket_arn" {
  value = module.encrypted_bucket.bucket_arn
}
EOF
```

---

### Step 5: Test the Module Locally
Before committing, test your module works.

```bash
# Navigate to basic example
cd examples/basic

# Initialize terraform
terraform init

# Validate syntax
terraform validate

# Format code
terraform fmt -recursive ../../

# Generate plan (requires AWS access)
terraform plan

# Expected output should show:
# - aws_s3_bucket.this will be created
# - aws_s3_bucket_versioning.this will be created
# - etc.
```

**Testing Checklist:**
- [ ] `terraform init` succeeds
- [ ] `terraform validate` passes
- [ ] `terraform fmt` returns no changes
- [ ] `terraform plan` shows expected resources
- [ ] Optional: `terraform apply` and verify in AWS console

**If you see errors:**
- Missing provider → Check providers.tf
- Invalid variable → Check validation rules in variables.tf
- Syntax error → Run `terraform fmt` and `terraform validate`

---

### Step 6: Commit and Create Pull Request
Follow git best practices for committing.

```bash
# Return to repo root
cd /path/to/plt-modules-main

# Check status
git status

# Add new module files
git add aws/s3-private-bucket/

# Commit with descriptive message
git commit -m "feat(aws): Add s3-private-bucket module

- Creates private S3 bucket with security best practices
- Includes versioning, encryption, public access block
- Provides basic and advanced examples
- Full documentation in README

Closes: PLT-XXXX"

# Push to feature branch
git push origin feature/s3-private-bucket-module

# Create PR using GitHub CLI
gh pr create \
  --title "feat(aws): Add s3-private-bucket module" \
  --body "## Description
Creates a new reusable module for private S3 buckets with security best practices.

## Testing
- ✅ Validated locally with terraform validate
- ✅ Formatted with terraform fmt
- ✅ Tested in dev account
- ✅ Examples provided and tested

## Checklist
- [x] README.md created with usage examples
- [x] All required files present (main.tf, variables.tf, outputs.tf, providers.tf)
- [x] Examples directory with working examples
- [x] Module follows naming conventions
- [x] Variables have descriptions and validation
- [x] Outputs have descriptions"
```

---

### Step 7: Tag the Module for Versioning
After PR is merged, create a version tag.

```bash
# Pull latest main
git checkout main
git pull origin main

# Create version tag (semantic versioning)
git tag -a s3-private-bucket/v1.0.0 -m "Release v1.0.0 of s3-private-bucket module

Features:
- Private S3 bucket creation
- Versioning support
- KMS/AES256 encryption
- Public access blocking
- Tagging support

Breaking changes: None (initial release)"

# Push tag
git push origin s3-private-bucket/v1.0.0
```

**Versioning Format:** `<module-name>/v<major>.<minor>.<patch>`
- Example: `s3-private-bucket/v1.0.0`
- **Major:** Breaking changes
- **Minor:** New features (backward compatible)
- **Patch:** Bug fixes

---

### Step 8: Update Module Registry/Documentation
Add your module to the team's module registry.

**Option 1: Update plt-modules README**
```bash
# Edit main README.md
# Add your module to the list

## Available Modules

### AWS Modules
- [s3-private-bucket](aws/s3-private-bucket) - Secure private S3 bucket

```

**Option 2: Update Port.io or Internal Wiki**
Document the module in your team's internal catalog.

## Verification Checklist
After completing all steps:

- [ ] Module files created (main.tf, variables.tf, outputs.tf, providers.tf)
- [ ] README.md with usage examples
- [ ] Examples directory with working examples
- [ ] Local testing passed (init, validate, fmt, plan)
- [ ] PR created and reviewed
- [ ] PR merged to main branch
- [ ] Version tag created (e.g., v1.0.0)
- [ ] Module documented in registry/wiki
- [ ] Team notified in Slack

## Troubleshooting

### Problem 1: terraform init fails with "Module not found"
**Cause:** Incorrect source path

**Solution:** Verify your source URL format:
```hcl
# Correct format for modules in same repo
source = "../../aws/s3-private-bucket"

# Correct format for tagged version
source = "git::https://github.com/org/repo.git//path/to/module?ref=tag"
```

---

### Problem 2: terraform validate fails
**Cause:** Syntax error or missing required provider

**Solution:**
```bash
# Run terraform fmt first
terraform fmt -recursive

# Check for syntax errors
terraform validate

# If provider error, check providers.tf exists and is correct
```

---

### Problem 3: Can't push tag
**Cause:** Tag already exists or no permission

**Solution:**
```bash
# Check existing tags
git tag -l "s3-private-bucket/*"

# Delete local tag if needed
git tag -d s3-private-bucket/v1.0.0

# Delete remote tag if needed (careful!)
git push origin :refs/tags/s3-private-bucket/v1.0.0
```

## Best Practices

### Module Design
- ✅ **DO:** Make modules single-purpose and focused
- ✅ **DO:** Use sensible defaults for optional variables
- ✅ **DO:** Include validation rules for variables
- ✅ **DO:** Provide comprehensive examples
- ❌ **DON'T:** Make modules do too many things
- ❌ **DON'T:** Hard-code values (use variables)
- ❌ **DON'T:** Output sensitive values without marking sensitive=true

### Naming Conventions
- **Module names:** Lowercase with hyphens (`s3-bucket`, not `S3_Bucket`)
- **Variable names:** Snake_case (`bucket_name`, not `bucketName`)
- **Resource names:** Use `this` for single resources
- **Output names:** Descriptive and consistent with AWS attribute names

### Versioning
- **Breaking changes:** Bump major version (v1.0.0 → v2.0.0)
- **New features:** Bump minor version (v1.0.0 → v1.1.0)
- **Bug fixes:** Bump patch version (v1.0.0 → v1.0.1)
- **Tag format:** `module-name/vX.Y.Z`

## Related Documentation
- [ADR-002: Terraform Module Structure](../adr/002-terraform-module-structure.md) (if exists)
- [How-To: Release Module Version](release-module-version.md) (if exists)
- [Terraform Module Documentation](https://developer.hashicorp.com/terraform/language/modules)
- [plt-modules Repository](https://github.com/intelerad-org/plt-modules)

## Getting Help
If you're stuck:

1. **Check this guide's troubleshooting section**
2. **Search Slack:** `#platform-team` for "terraform module"
3. **Ask for help:**
   - Slack: #platform-team
   - Tag: @platform-team-lead
4. **Review existing modules:** Look at similar modules in `aws/` directory

---

**Author:** Platform Engineering Team
**Last Updated:** 2025-11-17
**Tested With:**
- Terraform v1.5.0
- AWS Provider v5.25.0
