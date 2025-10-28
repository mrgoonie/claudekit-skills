---
name: turborepo
description: Guide for implementing Turborepo - a high-performance build system for JavaScript and TypeScript monorepos. Use when setting up monorepos, optimizing build performance, implementing task pipelines, configuring caching strategies, or orchestrating tasks across multiple packages.
license: MIT
version: 1.0.0
---

# Turborepo Skill

Turborepo is a high-performance build system optimized for JavaScript and TypeScript monorepos, written in Rust. It provides intelligent caching, task orchestration, and remote execution capabilities to dramatically speed up development workflows.

## Reference

https://turborepo.com/llms.txt

## When to Use This Skill

Use this skill when:
- Setting up a new monorepo with multiple packages
- Optimizing build performance in existing monorepos
- Implementing task pipelines across packages
- Configuring intelligent caching strategies
- Setting up remote caching for teams
- Orchestrating tasks with dependency awareness
- Integrating monorepo with CI/CD pipelines
- Migrating from Lerna, Nx, or other monorepo tools
- Building microfrontends or shared libraries
- Managing workspace dependencies

## Core Concepts

### 1. Monorepo Architecture
Turborepo organizes code into packages within a single repository:
- **Root Package**: Contains workspace configuration
- **Internal Packages**: Shared libraries, utilities, configs
- **Applications**: Frontend apps, backend services, etc.
- **Workspaces**: npm/yarn/pnpm workspace configuration

### 2. Task Pipeline
Tasks are organized in a dependency graph:
- **Task Dependencies**: Define execution order (build before test)
- **Package Dependencies**: Respect internal package relationships
- **Parallel Execution**: Run independent tasks simultaneously
- **Topological Ordering**: Execute tasks in correct dependency order

### 3. Intelligent Caching
Turborepo caches task outputs based on inputs:
- **Local Cache**: Stores outputs on local machine
- **Remote Cache**: Shares cache across team/CI (Vercel or custom)
- **Content-Based Hashing**: Only re-run when inputs change
- **Cache Restoration**: Instant task completion from cache

### 4. Task Outputs
Define what gets cached:
- Build artifacts (dist/, build/)
- Test results
- Generated files
- Type definitions

## Installation

### Prerequisites
```bash
# Requires Node.js 18+ and a package manager
node --version  # v18.0.0+
```

### Global Installation
```bash
# npm
npm install turbo --global

# yarn
yarn global add turbo

# pnpm
pnpm add turbo --global

# bun
bun add turbo --global
```

### Per-Project Installation
```bash
# npm
npm install turbo --save-dev

# yarn
yarn add turbo --dev

# pnpm
pnpm add turbo --save-dev

# bun
bun add turbo --dev
```

## Project Setup

### Create New Monorepo

Using official examples:
```bash
npx create-turbo@latest
```

Interactive prompts will ask:
- Project name
- Package manager (npm/yarn/pnpm/bun)
- Example template selection

### Manual Setup

**1. Initialize workspace:**

```json
// package.json (root)
{
  "name": "my-turborepo",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "test": "turbo run test",
    "lint": "turbo run lint"
  },
  "devDependencies": {
    "turbo": "latest"
  }
}
```

**2. Create directory structure:**
```
my-turborepo/
├── apps/
│   ├── web/              # Next.js app
│   └── docs/             # Documentation site
├── packages/
│   ├── ui/               # Shared UI components
│   ├── config/           # Shared configs (ESLint, TS)
│   └── tsconfig/         # Shared TypeScript configs
├── turbo.json            # Turborepo configuration
└── package.json          # Root package.json
```

**3. Create turbo.json:**
```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**", "dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {},
    "test": {
      "dependsOn": ["build"]
    }
  }
}
```

## Configuration (turbo.json)

### Basic Structure
```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [".env", "tsconfig.json"],
  "globalEnv": ["NODE_ENV"],
  "pipeline": {
    // Task definitions
  }
}
```

### Pipeline Configuration

**Task with dependencies:**
```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"],
      "env": ["NODE_ENV", "API_URL"]
    }
  }
}
```

**Key properties:**
- `dependsOn`: Tasks to run first
  - `["^build"]`: Run dependencies' build first
  - `["build"]`: Run own build first
  - `["^build", "lint"]`: Run deps' build and own lint
- `outputs`: Files/directories to cache
- `inputs`: Override input detection (default: all tracked files)
- `cache`: Enable/disable caching (default: true)
- `env`: Environment variables that affect output
- `persistent`: Keep task running (for dev servers)
- `outputMode`: Control output display

### Task Dependency Patterns

**Topological (^):**
```json
{
  "build": {
    "dependsOn": ["^build"]  // Run dependencies' build first
  }
}
```

**Regular:**
```json
{
  "deploy": {
    "dependsOn": ["build", "test"]  // Run own build and test first
  }
}
```

**Combined:**
```json
{
  "test": {
    "dependsOn": ["^build", "lint"]  // Deps' build, then own lint
  }
}
```

### Output Modes

```json
{
  "pipeline": {
    "build": {
      "outputMode": "full"        // Show all output
    },
    "dev": {
      "outputMode": "hash-only"   // Show cache hash only
    },
    "test": {
      "outputMode": "new-only"    // Show new output only
    },
    "lint": {
      "outputMode": "errors-only" // Show errors only
    }
  }
}
```

### Environment Variables

**Global environment variables:**
```json
{
  "globalEnv": ["NODE_ENV", "CI"],
  "globalDependencies": [".env", ".env.local"]
}
```

**Per-task environment variables:**
```json
{
  "pipeline": {
    "build": {
      "env": ["NEXT_PUBLIC_API_URL", "DATABASE_URL"],
      "passThroughEnv": ["CUSTOM_VAR"]  // Pass without hashing
    }
  }
}
```

## Commands

### turbo run

Run tasks across packages:

```bash
# Run build in all packages
turbo run build

# Run multiple tasks
turbo run build test lint

# Run in specific packages
turbo run build --filter=web
turbo run build --filter=@myorg/ui

# Run in packages matching pattern
turbo run build --filter='./apps/*'

# Force execution (skip cache)
turbo run build --force

# Run from specific directory
turbo run build --filter='[./apps/web]'

# Run with dependencies
turbo run build --filter='...^web'

# Parallel execution control
turbo run build --concurrency=3
turbo run build --concurrency=50%

# Continue on error
turbo run test --continue

# Dry run
turbo run build --dry-run

# Output control
turbo run build --output-logs=new-only
turbo run build --output-logs=hash-only
turbo run build --output-logs=errors-only
turbo run build --output-logs=full
```

### turbo prune

Create a subset of the monorepo:

```bash
# Prune for specific app
turbo prune --scope=web

# Prune with Docker
turbo prune --scope=api --docker

# Output to custom directory
turbo prune --scope=web --out-dir=./deploy
```

**Use cases:**
- Docker builds (only include necessary packages)
- Deploy specific apps
- Reduce CI/CD context size

### turbo gen

Generate code in your monorepo:

```bash
# Generate new package
turbo gen workspace

# Generate from custom generator
turbo gen my-generator

# List available generators
turbo gen --list
```

### turbo link

Link local repo to remote cache:

```bash
# Link to Vercel
turbo link

# Unlink
turbo unlink
```

### turbo login

Authenticate with Vercel:

```bash
turbo login
```

### turbo ls

List packages in monorepo:

```bash
# List all packages
turbo ls

# JSON output
turbo ls --json
```

## Filtering

### Filter by Package Name

```bash
# Single package
turbo run build --filter=web

# Multiple packages
turbo run build --filter=web --filter=api

# Scoped package
turbo run build --filter=@myorg/ui
```

### Filter by Pattern

```bash
# All apps
turbo run build --filter='./apps/*'

# Pattern matching
turbo run build --filter='*-ui'
```

### Filter by Directory

```bash
# From specific directory
turbo run build --filter='[./apps/web]'
```

### Filter by Git

```bash
# Changed since main
turbo run build --filter='[main]'

# Changed since HEAD~1
turbo run build --filter='[HEAD~1]'

# Changed in working directory
turbo run test --filter='...[HEAD]'
```

### Filter by Dependencies

```bash
# Package and its dependencies
turbo run build --filter='...web'

# Package's dependencies only
turbo run build --filter='...^web'

# Package and its dependents
turbo run test --filter='ui...'

# Package's dependents only
turbo run test --filter='^ui...'
```

## Caching Strategies

### Local Caching

Enabled by default, stores in `./node_modules/.cache/turbo`

**Cache behavior:**
```json
{
  "pipeline": {
    "build": {
      "outputs": ["dist/**"],  // Cache dist directory
      "cache": true            // Enable caching (default)
    },
    "dev": {
      "cache": false           // Disable for dev servers
    }
  }
}
```

**Clear cache:**
```bash
# Clear Turbo cache
rm -rf ./node_modules/.cache/turbo

# Or use turbo command
turbo run build --force  # Skip cache for this run
```

### Remote Caching

Share cache across team and CI:

**1. Link to Vercel (recommended):**
```bash
turbo login
turbo link
```

**2. Custom remote cache:**
```json
// .turbo/config.json
{
  "teamid": "team_123",
  "apiurl": "https://cache.example.com",
  "token": "your-token"
}
```

**Benefits:**
- Share builds across team
- Speed up CI/CD
- Consistent builds
- Reduce compute costs

### Cache Signatures

Cache is invalidated when:
- Source files change
- Dependencies change
- Environment variables change (if specified)
- Global dependencies change
- Task configuration changes

**Control inputs:**
```json
{
  "pipeline": {
    "build": {
      "inputs": ["src/**/*.ts", "!src/**/*.test.ts"],
      "env": ["NODE_ENV"]
    }
  }
}
```

## Workspace Patterns

### Package Types

**1. Internal packages (packages/*):**
```json
// packages/ui/package.json
{
  "name": "@myorg/ui",
  "version": "0.0.0",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "lint": "eslint ."
  }
}
```

**2. Applications (apps/*):**
```json
// apps/web/package.json
{
  "name": "web",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "@myorg/ui": "*",
    "next": "latest"
  },
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
```

### Dependency Management

**Workspace protocol (pnpm/yarn):**
```json
{
  "dependencies": {
    "@myorg/ui": "workspace:*"
  }
}
```

**Version protocol (npm):**
```json
{
  "dependencies": {
    "@myorg/ui": "*"
  }
}
```

### Shared Configuration

**ESLint config package:**
```js
// packages/eslint-config/index.js
module.exports = {
  extends: ["next", "prettier"],
  rules: {
    // shared rules
  }
}
```

**TypeScript config package:**
```json
// packages/tsconfig/base.json
{
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

**Usage:**
```json
// apps/web/tsconfig.json
{
  "extends": "@myorg/tsconfig/base.json",
  "compilerOptions": {
    "jsx": "preserve"
  }
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 18

      - name: Install dependencies
        run: npm install

      - name: Build
        run: npx turbo run build
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ secrets.TURBO_TEAM }}

      - name: Test
        run: npx turbo run test
```

### GitLab CI

```yaml
image: node:18

cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/
    - .turbo/

build:
  stage: build
  script:
    - npm install
    - npx turbo run build
  variables:
    TURBO_TOKEN: $TURBO_TOKEN
    TURBO_TEAM: $TURBO_TEAM
```

### Docker

```dockerfile
FROM node:18-alpine AS base

# Prune workspace
FROM base AS builder
RUN npm install -g turbo
COPY . .
RUN turbo prune --scope=web --docker

# Install dependencies
FROM base AS installer
COPY --from=builder /app/out/json/ .
COPY --from=builder /app/out/package-lock.json ./package-lock.json
RUN npm install

# Build
COPY --from=builder /app/out/full/ .
RUN npx turbo run build --filter=web

# Runner
FROM base AS runner
COPY --from=installer /app/apps/web/.next/standalone ./
COPY --from=installer /app/apps/web/.next/static ./apps/web/.next/static
COPY --from=installer /app/apps/web/public ./apps/web/public

CMD node apps/web/server.js
```

### Optimization Tips

1. **Use remote caching in CI:**
```yaml
env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ secrets.TURBO_TEAM }}
```

2. **Cache node_modules:**
```yaml
- uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

3. **Run only affected tasks:**
```bash
turbo run build test --filter='...[origin/main]'
```

## Framework Integration

### Next.js

```json
// apps/web/package.json
{
  "name": "web",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "latest",
    "react": "latest"
  }
}
```

**turbo.json:**
```json
{
  "pipeline": {
    "build": {
      "outputs": [".next/**", "!.next/cache/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### Vite

```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### NuxtJS

```json
{
  "pipeline": {
    "build": {
      "outputs": [".output/**", ".nuxt/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

## Development Tools Integration

### TypeScript

```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", "*.tsbuildinfo"]
    },
    "typecheck": {
      "dependsOn": ["^build"]
    }
  }
}
```

### ESLint

```json
{
  "pipeline": {
    "lint": {
      "dependsOn": ["^build"],
      "outputs": []
    }
  }
}
```

### Jest / Vitest

```json
{
  "pipeline": {
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"],
      "cache": true
    }
  }
}
```

### Prisma

```json
{
  "pipeline": {
    "db:generate": {
      "cache": false
    },
    "db:push": {
      "cache": false
    }
  }
}
```

## Best Practices

### 1. Structure Your Monorepo

```
my-monorepo/
├── apps/                    # Applications
│   ├── web/                # Frontend app
│   ├── api/                # Backend API
│   └── docs/               # Documentation
├── packages/               # Shared packages
│   ├── ui/                 # UI components
│   ├── config/             # Shared configs
│   ├── utils/              # Utilities
│   └── tsconfig/           # TS configs
├── tooling/                # Development tools
│   ├── eslint-config/
│   └── prettier-config/
└── turbo.json
```

### 2. Define Clear Task Dependencies

```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["build"]
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "deploy": {
      "dependsOn": ["build", "test", "lint"]
    }
  }
}
```

### 3. Optimize Cache Configuration

- **Cache build outputs, not source files**
- **Include all generated files in outputs**
- **Exclude cache directories** (e.g., `.next/cache`)
- **Disable cache for dev servers**

```json
{
  "pipeline": {
    "build": {
      "outputs": [
        "dist/**",
        ".next/**",
        "!.next/cache/**",
        "storybook-static/**"
      ]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### 4. Use Environment Variables Wisely

```json
{
  "globalEnv": ["NODE_ENV", "CI"],
  "pipeline": {
    "build": {
      "env": ["NEXT_PUBLIC_API_URL"],
      "passThroughEnv": ["DEBUG"]  // Don't affect cache
    }
  }
}
```

### 5. Leverage Remote Caching

- Enable for all team members
- Configure in CI/CD
- Reduces build times significantly
- Especially beneficial for large teams

### 6. Use Filters Effectively

```bash
# Build only changed packages
turbo run build --filter='...[origin/main]'

# Build specific app with dependencies
turbo run build --filter='...web'

# Test only affected packages
turbo run test --filter='...[HEAD^1]'
```

### 7. Organize Scripts Consistently

Root package.json:
```json
{
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "test": "turbo run test",
    "clean": "turbo run clean && rm -rf node_modules"
  }
}
```

### 8. Handle Persistent Tasks

```json
{
  "pipeline": {
    "dev": {
      "cache": false,
      "persistent": true  // Keeps running
    }
  }
}
```

## Common Patterns

### Full-Stack Application

```
apps/
├── web/          # Next.js frontend
│   └── package.json
├── api/          # Express backend
│   └── package.json
└── mobile/       # React Native
    └── package.json

packages/
├── ui/           # Shared UI components
├── database/     # Database client/migrations
├── types/        # Shared TypeScript types
└── config/       # Shared configs
```

### Shared Component Library

```
packages/
├── ui/                    # Component library
│   ├── src/
│   ├── package.json
│   └── tsconfig.json
└── ui-docs/              # Storybook
    ├── .storybook/
    ├── stories/
    └── package.json
```

### Microfrontends

```
apps/
├── shell/        # Container app
├── dashboard/    # Dashboard MFE
└── settings/     # Settings MFE

packages/
├── shared-ui/    # Shared components
└── router/       # Routing logic
```

## Troubleshooting

### Cache Issues

**Problem**: Task not using cache when it should
```bash
# Check what's causing cache miss
turbo run build --dry-run=json

# Force rebuild
turbo run build --force

# Clear cache
rm -rf ./node_modules/.cache/turbo
```

**Problem**: Cache too large
```bash
# Limit cache size in turbo.json
{
  "cacheDir": ".turbo",
  "cacheSize": "50gb"
}
```

### Dependency Issues

**Problem**: Internal package not found
```bash
# Ensure workspace is set up correctly
npm install

# Check package names match
npm ls @myorg/ui

# Rebuild dependencies
turbo run build --filter='...web'
```

### Task Execution Issues

**Problem**: Tasks running in wrong order
- Check `dependsOn` configuration
- Use `^task` for dependency tasks
- Verify task names match package.json scripts

**Problem**: Dev server not starting
```json
{
  "pipeline": {
    "dev": {
      "cache": false,
      "persistent": true  // Add this
    }
  }
}
```

### Performance Issues

**Problem**: Builds taking too long
```bash
# Run with concurrency limit
turbo run build --concurrency=2

# Use filters to build less
turbo run build --filter='...[origin/main]'

# Check for unnecessary dependencies
turbo run build --dry-run
```

**Problem**: Remote cache not working
```bash
# Verify authentication
turbo link

# Check environment variables
echo $TURBO_TOKEN
echo $TURBO_TEAM

# Test connection
turbo run build --output-logs=hash-only
```

## Migration Guide

### From Lerna

1. Replace Lerna with Turborepo:
```bash
npm uninstall lerna
npm install turbo --save-dev
```

2. Convert lerna.json to turbo.json:
```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"]
    }
  }
}
```

3. Update scripts:
```json
{
  "scripts": {
    "build": "turbo run build",
    "test": "turbo run test"
  }
}
```

### From Nx

1. Install Turborepo:
```bash
npm install turbo --save-dev
```

2. Convert nx.json to turbo.json:
- Map targetDefaults to pipeline
- Convert dependsOn syntax
- Configure caching

3. Update workspace configuration
4. Migrate CI/CD scripts

## Resources

- Documentation: https://turbo.build/repo/docs
- Examples: https://github.com/vercel/turbo/tree/main/examples
- Discord: https://turbo.build/discord
- GitHub: https://github.com/vercel/turbo

## Implementation Checklist

When setting up Turborepo:

- [ ] Install Turborepo globally or per-project
- [ ] Set up workspace structure (apps/, packages/)
- [ ] Create turbo.json with pipeline configuration
- [ ] Define task dependencies (build, test, lint)
- [ ] Configure cache outputs for each task
- [ ] Set up global dependencies and environment variables
- [ ] Link to remote cache (Vercel or custom)
- [ ] Configure CI/CD integration
- [ ] Add filtering strategies for large repos
- [ ] Document monorepo structure for team
- [ ] Set up code generation (turbo gen)
- [ ] Configure Docker builds with turbo prune
- [ ] Test caching behavior locally
- [ ] Verify remote cache in CI
- [ ] Optimize concurrency settings
