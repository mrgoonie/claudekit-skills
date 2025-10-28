# Shopify CLI Commands Reference

Comprehensive guide to Shopify CLI for app and theme development.

## Table of Contents
1. [Installation](#installation)
2. [App Commands](#app-commands)
3. [Theme Commands](#theme-commands)
4. [Extension Commands](#extension-commands)
5. [Configuration Commands](#configuration-commands)
6. [Common Workflows](#common-workflows)
7. [Troubleshooting](#troubleshooting)

## Installation

### Install Shopify CLI
```bash
# Via npm (recommended)
npm install -g @shopify/cli@latest

# Via Homebrew (macOS)
brew tap shopify/shopify
brew install shopify-cli

# Via Ruby Gem (legacy)
gem install shopify-cli
```

### Verify Installation
```bash
shopify version
```

### Update CLI
```bash
npm update -g @shopify/cli
```

## App Commands

### Initialize New App
```bash
shopify app init
```

**Prompts:**
- App name
- Technology stack (Node, Ruby, PHP, Remix)
- Template selection

**Creates:**
- App configuration (`shopify.app.toml`)
- Project structure
- Development dependencies

### Start Development Server
```bash
shopify app dev
```

**What it does:**
- Starts local development server
- Creates tunnel for embedded app testing
- Auto-reloads on file changes
- Provides preview URL

**Options:**
```bash
shopify app dev --reset        # Reset cached state
shopify app dev --store=mystore # Specify store
shopify app dev --port=3000    # Custom port
```

### Deploy App
```bash
shopify app deploy
```

**What it does:**
- Builds production assets
- Uploads extensions to Shopify
- Updates app configuration
- Creates new app version

### Generate Extension
```bash
shopify app generate extension
```

**Extension Types:**
- Checkout UI Extension
- Admin UI Extension (app block, app overlay, link)
- POS UI Extension
- Customer Account UI Extension
- Post-Purchase UI Extension
- Shopify Function (discount, payment, delivery, validation)
- Theme App Extension
- Web Pixel Extension

**Example:**
```bash
shopify app generate extension --type checkout_ui_extension --name gift-message
```

### Generate Schema
```bash
shopify app generate schema
```

Generates TypeScript types from GraphQL schema.

### Build App
```bash
shopify app build
```

Compiles app for production without deploying.

### Info
```bash
shopify app info
```

Displays app configuration and metadata.

### Config Link
```bash
shopify app config link
```

Links local project to app in Partners dashboard.

### Config Use
```bash
shopify app config use
```

Switch between multiple app configurations (staging, production).

### Config Push
```bash
shopify app config push
```

Push local config to Partners dashboard.

### Versions List
```bash
shopify app versions list
```

View all deployed app versions.

## Theme Commands

### Initialize Theme
```bash
shopify theme init
```

**Options:**
- Clone Dawn (Shopify's reference theme)
- Start from scratch
- Clone existing theme

### Pull Theme
```bash
shopify theme pull
```

Download theme files from store.

**Options:**
```bash
shopify theme pull --theme=123456789  # Specific theme ID
shopify theme pull --live              # Pull live theme
shopify theme pull --development       # Pull development theme
shopify theme pull --only=templates    # Specific directory
shopify theme pull --ignore=config/*   # Ignore patterns
```

### Push Theme
```bash
shopify theme push
```

Upload local theme files to store.

**Options:**
```bash
shopify theme push --theme=123456789   # Push to specific theme
shopify theme push --live              # Push to live theme (dangerous!)
shopify theme push --development       # Push to development theme
shopify theme push --unpublished       # Create new unpublished theme
shopify theme push --json              # Only push JSON files
shopify theme push --allow-live        # Allow pushing to live (confirmation)
```

### Theme Dev
```bash
shopify theme dev
```

Start local theme development server with hot reload.

**Options:**
```bash
shopify theme dev --theme=123456789    # Connect to specific theme
shopify theme dev --store=mystore      # Specific store
shopify theme dev --host=0.0.0.0       # Custom host
shopify theme dev --port=9292          # Custom port
shopify theme dev --poll               # Use polling for file changes
```

**Features:**
- Live reload on file changes
- Local preview at `http://localhost:9292`
- Syncs changes to development theme
- Hot Module Replacement (HMR)

### Theme Check
```bash
shopify theme check
```

Lints theme code for best practices and errors.

**Options:**
```bash
shopify theme check --list      # List all checks
shopify theme check --category  # Check specific category
shopify theme check --auto-correct # Fix issues automatically
```

### Theme Share
```bash
shopify theme share
```

Generate shareable preview link for unpublished theme.

### Theme Publish
```bash
shopify theme publish --theme=123456789
```

Set theme as live on store.

### Theme Package
```bash
shopify theme package
```

Create `.zip` file for theme upload or distribution.

### Theme List
```bash
shopify theme list
```

Display all themes on connected store.

### Theme Delete
```bash
shopify theme delete --theme=123456789
```

Remove theme from store.

## Extension Commands

### Extension Build
```bash
shopify extension build
```

Compile extension for production.

### Extension Check
```bash
shopify extension check
```

Validate extension configuration and code.

### Extension Push
```bash
shopify extension push
```

Upload extension to Shopify.

## Configuration Commands

### Login
```bash
shopify login
```

Authenticate with Shopify Partners account.

**Options:**
```bash
shopify login --store=mystore  # Login to specific store
```

### Logout
```bash
shopify logout
```

Remove stored authentication credentials.

### Whoami
```bash
shopify whoami
```

Display current authentication status.

### Store
```bash
shopify store
```

Display current connected store.

### Switch Store
```bash
shopify store switch
```

Change connected development store.

## Common Workflows

### New App Development

1. **Create app:**
```bash
shopify app init
cd my-app
```

2. **Start development:**
```bash
shopify app dev
```

3. **Generate extensions:**
```bash
shopify app generate extension --type checkout_ui_extension
```

4. **Deploy:**
```bash
shopify app deploy
```

### Theme Development

1. **Pull existing theme:**
```bash
shopify theme pull --live
```

2. **Start local development:**
```bash
shopify theme dev
```

3. **Make changes and test:**
   - Edit files in editor
   - See changes at `localhost:9292`

4. **Push to development theme:**
```bash
shopify theme push --development
```

5. **Publish when ready:**
```bash
shopify theme publish --theme=123456789
```

### Working with Multiple Environments

1. **Create app config file per environment:**
```bash
# Development config
shopify app config use dev

# Staging config
shopify app config use staging

# Production config
shopify app config use production
```

2. **Switch between configs:**
```bash
shopify app config use dev
shopify app dev

shopify app config use production
shopify app deploy
```

### Extension Development

1. **Generate extension:**
```bash
shopify app generate extension
```

2. **Select type and configure**

3. **Develop locally:**
```bash
shopify app dev
```

4. **Test in development store**

5. **Deploy:**
```bash
shopify app deploy
```

## Environment Variables

### Required Variables

**For Apps:**
```bash
SHOPIFY_API_KEY=your_api_key
SHOPIFY_API_SECRET=your_api_secret
SCOPES=read_products,write_orders
HOST=https://your-domain.com
```

**For Themes:**
```bash
SHOPIFY_CLI_THEME_TOKEN=shptka_xxx
SHOPIFY_FLAG_STORE=mystore.myshopify.com
```

### `.env` File Example
```bash
# App configuration
SHOPIFY_API_KEY=abc123def456
SHOPIFY_API_SECRET=xyz789uvw012
SCOPES=read_products,write_products,read_orders

# Database
DATABASE_URL=postgresql://localhost/myapp

# Other
NODE_ENV=development
PORT=3000
```

## Flags and Options

### Global Flags
```bash
--help, -h         # Show help
--version, -v      # Show version
--verbose          # Show detailed output
--path             # Specify project directory
--no-color         # Disable colored output
```

### App-Specific Flags
```bash
--reset            # Reset local state
--store            # Target store
--config           # Config file path
--subscription-product-url  # Specify subscription URL
```

### Theme-Specific Flags
```bash
--theme            # Theme ID
--live             # Target live theme
--development      # Target development theme
--unpublished      # Create unpublished theme
--nodelete         # Don't delete files on remote
--only             # Include only specified paths
--ignore           # Exclude specified paths
--json             # JSON output format
```

## Configuration Files

### shopify.app.toml
Main app configuration file.

```toml
# Basic info
name = "my-app"
client_id = "abc123"
application_url = "https://my-app.com"
embedded = true

# Build configuration
[build]
automatically_update_urls_on_dev = true
dev_store_url = "my-dev-store.myshopify.com"

# Access scopes
[access_scopes]
scopes = "read_products,write_products,read_orders"

# Webhooks
[webhooks]
api_version = "2025-01"

[[webhooks.subscriptions]]
topics = ["orders/create"]
uri = "/webhooks/orders/create"

[[webhooks.subscriptions]]
topics = ["app/uninstalled"]
uri = "/webhooks/app/uninstalled"

# App proxy
[app_proxy]
url = "https://my-app.com/proxy"
subpath = "apps/my-app"
prefix = "apps"

# GDPR webhooks (mandatory)
[webhooks.privacy_compliance]
customer_data_request_url = "/webhooks/gdpr/data-request"
customer_deletion_url = "/webhooks/gdpr/customer-deletion"
shop_deletion_url = "/webhooks/gdpr/shop-deletion"
```

### shopify.extension.toml
Extension configuration.

```toml
name = "gift-message"
type = "checkout_ui_extension"
handle = "gift-message"

[extension_points]
api_version = "2025-01"

[[extension_points.targets]]
target = "purchase.checkout.block.render"

[capabilities]
network_access = true
block_progress = false
```

## Troubleshooting

### Common Issues

**1. Authentication Errors**
```bash
# Re-authenticate
shopify logout
shopify login
```

**2. Port Already in Use**
```bash
# Use different port
shopify app dev --port=3001
```

**3. Theme Not Syncing**
```bash
# Reset and restart
shopify theme dev --reset
```

**4. Extension Not Appearing**
```bash
# Rebuild and redeploy
shopify extension build
shopify app deploy
```

**5. Config Issues**
```bash
# Validate config
shopify app info

# Relink config
shopify app config link
```

**6. Build Failures**
```bash
# Clear cache and rebuild
rm -rf node_modules
npm install
shopify app build
```

### Debug Mode

Enable verbose logging:
```bash
SHOPIFY_CLI_STACKTRACE=1 shopify app dev --verbose
```

### Update CLI

Many issues resolved by updating:
```bash
npm update -g @shopify/cli@latest
```

### Check CLI Status
```bash
shopify status
```

## Performance Tips

### Faster Development
```bash
# Only sync specific directories
shopify theme dev --only=sections,snippets

# Ignore large directories
shopify theme dev --ignore=assets/videos
```

### Faster Deployments
```bash
# Deploy only changed files
shopify theme push --only=changed

# Parallel uploads
shopify theme push --concurrent=10
```

## Best Practices

1. **Use version control:** Commit `shopify.app.toml` and extension configs
2. **Environment separation:** Use different configs for dev/staging/prod
3. **Ignore build artifacts:** Add to `.gitignore`:
   ```
   .shopify/
   dist/
   build/
   node_modules/
   .env
   ```
4. **Regular updates:** Keep CLI updated for bug fixes and features
5. **Development stores:** Use dedicated development stores for testing
6. **Backup before pushing:** Always pull before pushing themes to avoid conflicts
7. **Test extensions thoroughly:** Use development stores before production deployment

## Official Resources

- **CLI Documentation:** https://shopify.dev/docs/api/shopify-cli
- **CLI GitHub:** https://github.com/Shopify/cli
- **App Configuration:** https://shopify.dev/docs/apps/build/cli-for-apps/app-configuration
- **Theme Development:** https://shopify.dev/docs/themes/tools/cli
