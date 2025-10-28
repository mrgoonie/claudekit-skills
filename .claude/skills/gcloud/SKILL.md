---
name: gcloud
description: Guide for implementing Google Cloud SDK (gcloud CLI) - a command-line tool for managing Google Cloud resources. Use when installing/configuring gcloud, authenticating with Google Cloud, managing projects/configurations, deploying applications, working with Compute Engine/GKE/App Engine/Cloud Storage, scripting gcloud operations, implementing CI/CD pipelines, or troubleshooting Google Cloud deployments.
---

# Google Cloud SDK (gcloud) Skill

Comprehensive guide for working with the Google Cloud SDK (gcloud CLI) - the primary command-line interface for interacting with Google Cloud Platform services, managing resources, and automating cloud operations.

## When to Use This Skill

Use this skill when you need to:
- Install and configure the Google Cloud SDK
- Authenticate with Google Cloud (user accounts, service accounts, ADC)
- Initialize gcloud and set up projects/configurations
- Manage multiple Google Cloud projects and environments
- Deploy applications to GCP (Compute Engine, GKE, App Engine, Cloud Run)
- Work with Cloud Storage, databases, and other GCP services
- Script gcloud commands for automation and CI/CD pipelines
- Troubleshoot authentication, authorization, or deployment issues
- Optimize gcloud command performance and output formatting
- Implement security best practices for cloud operations

## Core Concepts

### The gcloud CLI

**Architecture:**
- **Command Structure:** `gcloud + [release-level] + component + entity + operation + [args] + [flags]`
- **Release Levels:** alpha, beta, GA (general availability)
- **Components:** compute, container, app, sql, iam, config, auth, storage, etc.
- **Global Flags:** `--project`, `--format`, `--filter`, `--quiet`, `--verbosity`

**Key Features:**
- Unified CLI for 100+ Google Cloud services
- Consistent command patterns across all services
- Rich output formatting (JSON, YAML, CSV, table)
- Built-in filtering and server-side query optimization
- Interactive and non-interactive modes for automation

### Authentication vs Authorization

**Authentication** (Who you are):
- User accounts (developers, admins)
- Service accounts (applications, automation)
- Application Default Credentials (ADC)
- OAuth 2.0, API keys, workload/workforce identity federation

**Authorization** (What you can do):
- IAM roles and permissions
- Service account impersonation
- Resource-level access control

### Configuration Management

**Named Configurations:**
- Multiple configuration profiles for different environments
- Each configuration stores: account, project, region, zone, and other properties
- Switch between configurations instantly

**Properties:**
- 50+ configurable properties across 7 categories
- Precedence: CLI flags > env vars > config files > defaults

---

## I. INSTALLATION & SETUP

### A. Installation Methods

#### Linux (Archive Installation)
```bash
# Download (choose architecture)
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz

# Extract
tar -xf google-cloud-cli-linux-x86_64.tar.gz

# Install
./google-cloud-sdk/install.sh

# Initialize
./google-cloud-sdk/bin/gcloud init
```

#### Debian/Ubuntu (Package Manager)
```bash
# Add repo
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Install
sudo apt-get update && sudo apt-get install google-cloud-cli
```

#### macOS
```bash
# Download installer
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-darwin-arm.tar.gz

# Extract and install
tar -xf google-cloud-cli-darwin-arm.tar.gz
./google-cloud-sdk/install.sh
```

#### Windows
```powershell
# Download installer from https://cloud.google.com/sdk/docs/install
# Run GoogleCloudSDKInstaller.exe
# Follow installation wizard
```

### B. Initialization

```bash
# Interactive setup (recommended for first-time)
gcloud init

# What it does:
# 1. Opens browser for OAuth authentication
# 2. Selects or creates a project
# 3. Sets default configuration (region, zone)
# 4. Stores credentials

# Non-interactive (CI/CD environments)
gcloud auth activate-service-account --key-file=key.json
gcloud config set project PROJECT_ID
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a
```

### C. Components

```bash
# List available components
gcloud components list

# Install additional components
gcloud components install kubectl        # Kubernetes CLI
gcloud components install app-engine-python  # App Engine
gcloud components install cloud-sql-proxy    # Cloud SQL Proxy
gcloud components install pubsub-emulator    # Pub/Sub emulator

# Update all components
gcloud components update

# Remove component
gcloud components remove COMPONENT_ID
```

**Core Components (installed by default):**
- `gcloud` - Main CLI
- `gsutil` - Cloud Storage utility
- `bq` - BigQuery CLI
- `core` - Core libraries

---

## II. AUTHENTICATION & AUTHORIZATION

### A. Authentication Methods

#### 1. User Account (OAuth 2.0)
```bash
# Login with browser
gcloud auth login

# Login without browser (remote/headless)
gcloud auth login --no-browser

# Login with specific account
gcloud auth login user@example.com

# List authenticated accounts
gcloud auth list

# Switch active account
gcloud config set account user@example.com

# Revoke credentials
gcloud auth revoke user@example.com
```

#### 2. Service Account
```bash
# Activate service account with key file
gcloud auth activate-service-account SA_EMAIL --key-file=path/to/key.json

# Create service account
gcloud iam service-accounts create SA_NAME \
  --display-name="Service Account Display Name"

# Create and download key
gcloud iam service-accounts keys create key.json \
  --iam-account=SA_EMAIL

# Grant IAM role
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SA_EMAIL" \
  --role="roles/compute.admin"
```

#### 3. Application Default Credentials (ADC)
```bash
# Setup ADC for client libraries
gcloud auth application-default login

# Setup ADC with service account impersonation
gcloud auth application-default login \
  --impersonate-service-account=SA_EMAIL

# Revoke ADC
gcloud auth application-default revoke

# ADC Search Order:
# 1. GOOGLE_APPLICATION_CREDENTIALS environment variable
# 2. ~/.config/gcloud/application_default_credentials.json
# 3. Metadata server (on GCP resources)
```

#### 4. Service Account Impersonation (Recommended for Production)
```bash
# Impersonate for single command
gcloud compute instances list \
  --impersonate-service-account=SA_EMAIL

# Set default impersonation
gcloud config set auth/impersonate_service_account SA_EMAIL

# Verify impersonation
gcloud config get-value auth/impersonate_service_account

# Clear impersonation
gcloud config unset auth/impersonate_service_account
```

**Why Impersonation?**
- Short-lived temporary credentials (no persistent key risk)
- No need to distribute service account keys
- Centralized permission management
- Easy to audit and rotate

### B. Configuration Profiles

#### Create and Manage Configurations
```bash
# Create new configuration
gcloud config configurations create dev

# List all configurations
gcloud config configurations list

# Activate configuration
gcloud config configurations activate dev

# Switch configuration for single command
gcloud compute instances list --configuration=prod

# Set properties
gcloud config set project my-project-dev
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

# View all properties
gcloud config list

# Unset property
gcloud config unset compute/zone

# Delete configuration
gcloud config configurations delete dev
```

#### Multi-Environment Pattern
```bash
# Development environment
gcloud config configurations create dev
gcloud config set project my-project-dev
gcloud config set account dev@example.com
gcloud config set compute/region us-central1

# Staging environment
gcloud config configurations create staging
gcloud config set project my-project-staging
gcloud config set auth/impersonate_service_account staging-sa@project.iam.gserviceaccount.com

# Production environment
gcloud config configurations create prod
gcloud config set project my-project-prod
gcloud config set auth/impersonate_service_account prod-sa@project.iam.gserviceaccount.com

# Switch environments
gcloud config configurations activate dev
gcloud config configurations activate prod
```

---

## III. COMMON WORKFLOWS

### A. Project Management

```bash
# List projects
gcloud projects list

# Create project
gcloud projects create PROJECT_ID --name="Project Name"

# Set active project
gcloud config set project PROJECT_ID

# Get current project
gcloud config get-value project

# Enable API
gcloud services enable compute.googleapis.com
gcloud services enable container.googleapis.com

# List enabled APIs
gcloud services list

# Describe project
gcloud projects describe PROJECT_ID
```

### B. Compute Engine

```bash
# List instances
gcloud compute instances list

# Create instance
gcloud compute instances create my-instance \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --boot-disk-size=10GB

# SSH into instance
gcloud compute ssh my-instance --zone=us-central1-a

# Copy files
gcloud compute scp local-file.txt my-instance:~/remote-file.txt \
  --zone=us-central1-a

# Stop instance
gcloud compute instances stop my-instance --zone=us-central1-a

# Delete instance
gcloud compute instances delete my-instance --zone=us-central1-a
```

### C. Google Kubernetes Engine (GKE)

```bash
# Create cluster
gcloud container clusters create my-cluster \
  --zone=us-central1-a \
  --num-nodes=3 \
  --machine-type=e2-medium

# Get cluster credentials
gcloud container clusters get-credentials my-cluster --zone=us-central1-a

# List clusters
gcloud container clusters list

# Resize cluster
gcloud container clusters resize my-cluster \
  --num-nodes=5 \
  --zone=us-central1-a

# Delete cluster
gcloud container clusters delete my-cluster --zone=us-central1-a
```

### D. Cloud Storage

```bash
# Create bucket
gsutil mb gs://my-bucket-name

# Upload file
gsutil cp local-file.txt gs://my-bucket-name/

# Download file
gsutil cp gs://my-bucket-name/file.txt ./

# List bucket contents
gsutil ls gs://my-bucket-name/

# Sync directory
gsutil rsync -r ./local-dir gs://my-bucket-name/remote-dir

# Set bucket permissions
gsutil iam ch user:user@example.com:objectViewer gs://my-bucket-name

# Delete bucket
gsutil rm -r gs://my-bucket-name
```

### E. App Engine

```bash
# Deploy application
gcloud app deploy app.yaml

# View application
gcloud app browse

# View logs
gcloud app logs tail

# List versions
gcloud app versions list

# Delete version
gcloud app versions delete VERSION_ID

# Set traffic split
gcloud app services set-traffic SERVICE \
  --splits v1=0.5,v2=0.5
```

### F. Cloud Run

```bash
# Deploy container
gcloud run deploy my-service \
  --image=gcr.io/PROJECT_ID/my-image:tag \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated

# List services
gcloud run services list

# Describe service
gcloud run services describe my-service --region=us-central1

# Delete service
gcloud run services delete my-service --region=us-central1
```

---

## IV. SCRIPTING & AUTOMATION

### A. Output Formats

```bash
# JSON (recommended for scripting)
gcloud compute instances list --format=json

# YAML
gcloud compute instances list --format=yaml

# CSV
gcloud compute instances list --format="csv(name,zone,status)"

# Table (default)
gcloud compute instances list --format=table

# Value (single field extraction)
gcloud config get-value project --format="value()"

# Custom format
gcloud compute instances list \
  --format="table(name,zone,machineType,status)"
```

### B. Filtering

```bash
# Server-side filtering (more efficient)
gcloud compute instances list --filter="zone:us-central1-a"
gcloud compute instances list --filter="status=RUNNING"
gcloud compute instances list --filter="name~^web-.*"

# Multiple conditions
gcloud compute instances list \
  --filter="zone:us-central1 AND status=RUNNING"

# Negation
gcloud compute instances list --filter="NOT status=TERMINATED"

# Complex expressions
gcloud compute instances list \
  --filter="(status=RUNNING OR status=STOPPING) AND zone:us-central1"
```

### C. Error Handling

```bash
#!/bin/bash

# Simple error check
if ! gcloud compute instances create my-instance; then
  echo "Failed to create instance"
  exit 1
fi

# Capture exit code
gcloud compute instances describe my-instance
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
  echo "Instance not found or error occurred"
  exit $EXIT_CODE
fi

# Capture stderr
ERROR_OUTPUT=$(gcloud compute instances create my-instance 2>&1)
if [ $? -ne 0 ]; then
  echo "Error: $ERROR_OUTPUT"
  exit 1
fi

# Validate before create (idempotent pattern)
if ! gcloud compute instances describe my-instance &>/dev/null; then
  gcloud compute instances create my-instance
else
  echo "Instance already exists, skipping creation"
fi
```

### D. Retry Logic

```bash
#!/bin/bash

MAX_RETRIES=5
RETRY_DELAY=5

for i in $(seq 1 $MAX_RETRIES); do
  if gcloud compute instances create my-instance; then
    echo "Instance created successfully"
    exit 0
  else
    echo "Attempt $i failed, retrying in ${RETRY_DELAY}s..."
    sleep $RETRY_DELAY
    RETRY_DELAY=$((RETRY_DELAY * 2))  # Exponential backoff
  fi
done

echo "Failed after $MAX_RETRIES attempts"
exit 1
```

### E. Batch Operations

```bash
#!/bin/bash

# Parallel instance creation
INSTANCES=("web-1" "web-2" "web-3")

for instance in "${INSTANCES[@]}"; do
  gcloud compute instances create "$instance" \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --async  # Run in background
done

# Wait for all operations to complete
gcloud compute operations list --filter="status=RUNNING" \
  --format="value(name)" | while read op; do
  gcloud compute operations wait "$op" --zone=us-central1-a
done

echo "All instances created"
```

### F. CI/CD Integration

#### GitHub Actions
```yaml
name: Deploy to GCP

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - id: auth
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v1

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy my-service \
            --image=gcr.io/${{ secrets.GCP_PROJECT_ID }}/my-image:${{ github.sha }} \
            --region=us-central1 \
            --platform=managed
```

#### GitLab CI
```yaml
deploy:
  image: google/cloud-sdk:alpine
  script:
    - echo $GCP_SA_KEY | base64 -d > key.json
    - gcloud auth activate-service-account --key-file=key.json
    - gcloud config set project $GCP_PROJECT_ID
    - gcloud app deploy
  only:
    - main
```

---

## V. BEST PRACTICES

### A. Security

**1. Never Commit Credentials**
```bash
# Add to .gitignore
echo "key.json" >> .gitignore
echo ".config/gcloud/" >> .gitignore
echo "application_default_credentials.json" >> .gitignore
```

**2. Use Service Account Impersonation**
```bash
# Prefer impersonation over key files
gcloud config set auth/impersonate_service_account SA_EMAIL

# NOT: gcloud auth activate-service-account --key-file=key.json
```

**3. Principle of Least Privilege**
```bash
# Grant minimal required roles
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SA_EMAIL" \
  --role="roles/compute.instanceAdmin.v1"  # Specific role, not "owner"
```

**4. Rotate Keys Regularly**
```bash
# Create new key
gcloud iam service-accounts keys create new-key.json \
  --iam-account=SA_EMAIL

# Delete old key
gcloud iam service-accounts keys delete KEY_ID \
  --iam-account=SA_EMAIL
```

### B. Performance

**1. Use Server-Side Filtering**
```bash
# Good: Filter on server
gcloud compute instances list --filter="zone:us-central1"

# Bad: Filter locally with grep
gcloud compute instances list | grep us-central1
```

**2. Limit Output**
```bash
# Only fetch what you need
gcloud compute instances list --limit=10

# Project only needed fields
gcloud compute instances list --format="value(name,zone)"
```

**3. Batch Operations**
```bash
# Use --async for parallel operations
gcloud compute instances create instance-1 --async
gcloud compute instances create instance-2 --async
gcloud compute instances create instance-3 --async
```

### C. Maintainability

**1. Use Named Configurations**
```bash
# Separate dev/staging/prod configurations
gcloud config configurations create dev
gcloud config configurations create prod
```

**2. Document Commands**
```bash
#!/bin/bash
# Purpose: Deploy application to Cloud Run
# Usage: ./deploy.sh [environment]
# Example: ./deploy.sh production

ENV=${1:-staging}
gcloud config configurations activate "$ENV"
gcloud run deploy my-service --image=gcr.io/project/image:latest
```

**3. Use Environment Variables**
```bash
# Make scripts portable
PROJECT_ID=${GCP_PROJECT_ID:-default-project}
REGION=${GCP_REGION:-us-central1}

gcloud config set project "$PROJECT_ID"
gcloud config set compute/region "$REGION"
```

### D. Monitoring & Logging

```bash
# Enable audit logging
gcloud logging read "resource.type=gce_instance" \
  --limit=10 \
  --format=json

# Track command history
gcloud info --show-log

# Verbose output for debugging
gcloud compute instances create my-instance --verbosity=debug
```

---

## VI. TROUBLESHOOTING

### Common Issues

**1. Authentication Failures**
```bash
# Check current authentication
gcloud auth list

# Verify credentials
gcloud auth application-default print-access-token

# Re-authenticate
gcloud auth login
gcloud auth application-default login
```

**2. Permission Denied**
```bash
# Check IAM permissions
gcloud projects get-iam-policy PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:user@example.com"

# Check service account permissions
gcloud iam service-accounts get-iam-policy SA_EMAIL
```

**3. Quota Exceeded**
```bash
# Check quota usage
gcloud compute project-info describe --project=PROJECT_ID

# Request quota increase via Cloud Console
```

**4. Network Issues**
```bash
# Check connectivity
gcloud info

# Use proxy
gcloud config set proxy/type http
gcloud config set proxy/address PROXY_HOST
gcloud config set proxy/port PROXY_PORT
```

**5. Configuration Issues**
```bash
# View current configuration
gcloud config list

# Reset configuration
gcloud config configurations delete default
gcloud init
```

---

## VII. QUICK REFERENCE

### Essential Commands

| Task | Command |
|------|---------|
| Initialize gcloud | `gcloud init` |
| Login | `gcloud auth login` |
| Set project | `gcloud config set project PROJECT_ID` |
| List resources | `gcloud [SERVICE] list` |
| Describe resource | `gcloud [SERVICE] describe RESOURCE` |
| Create resource | `gcloud [SERVICE] create RESOURCE` |
| Delete resource | `gcloud [SERVICE] delete RESOURCE` |
| Get help | `gcloud [SERVICE] --help` |
| View configurations | `gcloud config configurations list` |
| Switch configuration | `gcloud config configurations activate CONFIG` |

### Global Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--project` | Override project | `--project=my-project` |
| `--format` | Output format | `--format=json` |
| `--filter` | Server-side filter | `--filter="status=RUNNING"` |
| `--limit` | Limit results | `--limit=10` |
| `--quiet` | Suppress prompts | `--quiet` |
| `--verbosity` | Log level | `--verbosity=debug` |
| `--async` | Don't wait | `--async` |

### Common Properties

```bash
# Core
gcloud config set project PROJECT_ID
gcloud config set account EMAIL
gcloud config set disable_usage_reporting true

# Compute
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

# Container
gcloud config set container/cluster CLUSTER_NAME

# App Engine
gcloud config set app/cloud_build_timeout 1200
```

---

## VIII. RESOURCES

### Official Documentation
- **gcloud CLI Reference:** https://cloud.google.com/sdk/gcloud/reference
- **Installation Guide:** https://cloud.google.com/sdk/docs/install
- **Authentication Guide:** https://cloud.google.com/docs/authentication
- **Cheatsheet:** https://cloud.google.com/sdk/docs/cheatsheet
- **Scripting Guide:** https://cloud.google.com/sdk/docs/scripting-gcloud

### Tools
- **Cloud Console:** https://console.cloud.google.com
- **Cloud Shell:** Browser-based shell with gcloud pre-installed
- **Cloud Code:** IDE extensions (VS Code, IntelliJ)

### Best Practices Summary

1. **Authentication:** Use service account impersonation instead of key files
2. **Configuration:** Use named configurations for multiple environments
3. **Security:** Grant minimal IAM permissions, rotate keys regularly
4. **Performance:** Use server-side filtering, batch operations with --async
5. **Scripting:** Output JSON format, implement error handling and retries
6. **Automation:** Use environment variables, validate before operations
7. **Monitoring:** Enable Cloud Audit Logs, track command history
8. **Maintenance:** Keep SDK updated, document scripts thoroughly

---

## Common Use Cases

### Multi-Environment Deployment
- Separate configurations for dev/staging/prod
- Service account impersonation for each environment
- Automated deployments via CI/CD

### Infrastructure as Code
- Create resources with gcloud in shell scripts
- Export configurations as YAML/JSON
- Version control infrastructure commands

### Data Pipeline Automation
- Scheduled BigQuery jobs
- Cloud Storage file transfers
- Pub/Sub message processing

### Security Compliance
- Audit logging for all operations
- Encrypted data at rest and in transit
- Regular key rotation and access reviews

---

This skill provides comprehensive gcloud CLI knowledge for implementing Google Cloud solutions, from basic authentication to advanced automation workflows. Always refer to official documentation for the latest features and service-specific details.
