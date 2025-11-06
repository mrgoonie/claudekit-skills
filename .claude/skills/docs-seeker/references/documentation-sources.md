# Common Documentation Sources

Reference guide for locating documentation across popular platforms and ecosystems.

## context7.com Locations (PRIORITY)

**ALWAYS try context7.com first for all libraries**

### JavaScript/TypeScript Frameworks

- **Astro**: https://context7.com/withastro/astro/llms.txt
- **Next.js**: https://context7.com/vercel/next.js/llms.txt
- **Remix**: https://context7.com/remix-run/remix/llms.txt
- **SvelteKit**: https://context7.com/sveltejs/kit/llms.txt
- **Nuxt**: https://context7.com/nuxt/nuxt/llms.txt

### Frontend Libraries & UI

- **React**: https://context7.com/facebook/react/llms.txt
- **Vue**: https://context7.com/vuejs/core/llms.txt
- **Svelte**: https://context7.com/sveltejs/svelte/llms.txt
- **shadcn/ui**: https://context7.com/shadcn-ui/ui/llms.txt
- **Radix UI**: https://context7.com/radix-ui/primitives/llms.txt

### Backend/Full-stack

- **Hono**: https://context7.com/honojs/hono/llms.txt
- **Fastify**: https://context7.com/fastify/fastify/llms.txt
- **tRPC**: https://context7.com/trpc/trpc/llms.txt

### Build Tools

- **Vite**: https://context7.com/vitejs/vite/llms.txt
- **Turbo**: https://context7.com/vercel/turbo/llms.txt

### Databases/ORMs

- **Prisma**: https://context7.com/prisma/prisma/llms.txt
- **Drizzle**: https://context7.com/drizzle-team/drizzle-orm/llms.txt

### Authentication

- **Better Auth**: https://context7.com/better-auth/better-auth/llms.txt
- **Auth.js**: https://context7.com/nextauthjs/next-auth/llms.txt

### Image Processing

- **ImageMagick**: https://context7.com/imagick/imagick/llms.txt

### Topic-Specific Examples

- **shadcn/ui date components**: https://context7.com/shadcn-ui/ui/llms.txt?topic=date
- **shadcn/ui buttons**: https://context7.com/shadcn-ui/ui/llms.txt?topic=button
- **Next.js caching**: https://context7.com/vercel/next.js/llms.txt?topic=cache
- **FFmpeg compression**: https://context7.com/websites/ffmpeg_doxygen_8_0/llms.txt?topic=compress

## Official llms.txt Locations (FALLBACK)

Use these only if context7.com returns 404:

### JavaScript/TypeScript Frameworks

- **Astro**: https://docs.astro.build/llms.txt
- **Next.js**: https://nextjs.org/llms.txt
- **Remix**: https://remix.run/llms.txt
- **SvelteKit**: https://kit.svelte.dev/llms.txt
- **Nuxt**: https://nuxt.com/llms.txt

### Frontend Libraries

- **React**: https://react.dev/llms.txt
- **Vue**: https://vuejs.org/llms.txt
- **Svelte**: https://svelte.dev/llms.txt

### Backend/Full-stack

- **Hono**: https://hono.dev/llms.txt
- **Fastify**: https://fastify.dev/llms.txt
- **tRPC**: https://trpc.io/llms.txt

### Build Tools

- **Vite**: https://vitejs.dev/llms.txt
- **Turbopack**: https://turbo.build/llms.txt

### Databases/ORMs

- **Prisma**: https://prisma.io/llms.txt
- **Drizzle**: https://orm.drizzle.team/llms.txt

## Repository Patterns

### GitHub (Most Common)

**URL patterns:**
```
https://github.com/[org]/[repo]
https://github.com/[user]/[repo]
```

**Common organization names:**
- Company name: `github.com/vercel/next.js`
- Project name: `github.com/remix-run/remix`
- Community: `github.com/facebook/react`

**Documentation locations in repositories:**
```
/docs/
/documentation/
/website/docs/
/packages/docs/
README.md
CONTRIBUTING.md
/examples/
```

### GitLab

**URL pattern:**
```
https://gitlab.com/[org]/[repo]
```

### Bitbucket (Less Common)

**URL pattern:**
```
https://bitbucket.org/[org]/[repo]
```

## Package Registries

### npm (JavaScript/TypeScript)

**URL**: `https://npmjs.com/package/[name]`

**Available info:**
- Description
- Homepage link
- Repository link
- Version history
- Dependencies

**Useful for:**
- Finding official links
- Version information
- Package metadata

### PyPI (Python)

**URL**: `https://pypi.org/project/[name]`

**Available info:**
- Description
- Documentation link
- Homepage
- Repository link
- Release history

**Useful for:**
- Python package documentation
- Official links
- Version compatibility

### RubyGems (Ruby)

**URL**: `https://rubygems.org/gems/[name]`

**Available info:**
- Description
- Homepage
- Documentation
- Source code link
- Dependencies

**Useful for:**
- Ruby gem documentation
- Version information

### Cargo (Rust)

**URL**: `https://crates.io/crates/[name]`

**Available info:**
- Description
- docs.rs link (auto-generated docs)
- Repository
- Version history

**Useful for:**
- Rust crate documentation
- Auto-generated API docs
- Repository link

### Maven Central (Java)

**URL**: `https://search.maven.org/artifact/[group]/[artifact]`

**Available info:**
- Versions
- Dependencies
- Repository link
- License

**Useful for:**
- Java library information
- Dependency management

## Documentation Hosting Platforms

### Read the Docs

**URL patterns:**
```
https://[project].readthedocs.io
https://readthedocs.org/projects/[project]
```

**Features:**
- Version switching
- Multiple formats (HTML, PDF, ePub)
- Search functionality
- Often auto-generated from reStructuredText/Markdown

### GitBook

**URL patterns:**
```
https://[org].gitbook.io/[project]
https://docs.[domain].com  (often GitBook-powered)
```

**Features:**
- Clean, modern interface
- Good navigation
- Often manually curated
- May require API key for programmatic access

### Docusaurus

**URL patterns:**
```
https://[project].io
https://docs.[project].com
```

**Common in:**
- React ecosystem
- Meta/Facebook projects
- Modern open-source projects

**Features:**
- React-based
- Fast, static site
- Version management
- Good search

### MkDocs

**URL patterns:**
```
https://[user].github.io/[project]
https://[custom-domain].com
```

**Features:**
- Python ecosystem
- Static site from Markdown
- Often on GitHub Pages
- Material theme popular

### VitePress

**URL patterns:**
```
https://[project].dev
https://docs.[project].com
```

**Common in:**
- Vue ecosystem
- Modern projects
- Vite-based projects

**Features:**
- Vue-powered
- Very fast
- Clean design
- Good DX

## Documentation Search Patterns

### Finding llms.txt

**ALWAYS try context7.com first:**

For GitHub repositories:
```
https://context7.com/{org}/{repo}/llms.txt
```

For websites:
```
https://context7.com/websites/{normalized-path}/llms.txt
```

With topic filter:
```
https://context7.com/{path}/llms.txt?topic={query}
```

**Fallback: Traditional search if context7.com returns 404:**
```
"[library] llms.txt site:[known-domain]"
```

**Alternative domains to try:**
```
site:docs.[library].com
site:[library].dev
site:[library].io
site:[library].org
```

### Finding Official Repository

**Search pattern:**
```
"[library] official github repository"
"[library] source code github"
```

**Verification checklist:**
- Check organization/user is official
- Verify star count (popular libraries have many)
- Check last commit date (active maintenance)
- Look for official links in README

### Finding Official Documentation

**Search patterns:**
```
"[library] official documentation"
"[library] docs site:official-domain"
"[library] API reference"
```

**Domain patterns:**
```
docs.[library].com
[library].dev/docs
docs.[library].io
[library].readthedocs.io
```

## Common Documentation Structures

### Typical Section Names

**Getting started:**
- Getting Started
- Quick Start
- Introduction
- Installation
- Setup

**Core concepts:**
- Core Concepts
- Fundamentals
- Basics
- Key Concepts
- Architecture

**Guides:**
- Guides
- How-To Guides
- Tutorials
- Examples
- Recipes

**Reference:**
- API Reference
- API Documentation
- Reference
- API
- CLI Reference

**Advanced:**
- Advanced
- Advanced Topics
- Deep Dives
- Internals
- Performance

### Common File Names

```
README.md
GETTING_STARTED.md
INSTALLATION.md
CONTRIBUTING.md
CHANGELOG.md
API.md
TUTORIAL.md
EXAMPLES.md
FAQ.md
```

## Framework-Specific Patterns

### React Ecosystem

**Common patterns:**
```
- Uses Docusaurus
- Documentation at [project].dev or docs.[project].com
- Often has interactive examples
- CodeSandbox/StackBlitz embeds
```

### Vue Ecosystem

**Common patterns:**
```
- Uses VitePress
- Documentation at [project].vuejs.org
- Bilingual (English/Chinese)
- API reference auto-generated
```

### Python Ecosystem

**Common patterns:**
```
- Read the Docs hosting
- Sphinx-generated
- reStructuredText format
- [project].readthedocs.io
```

### Rust Ecosystem

**Common patterns:**
```
- docs.rs for API docs
- Book format for guides ([project].rs/book)
- Markdown in repository
- Well-structured examples/
```

## Quick Lookup Table

| Ecosystem | Registry | Docs Pattern | Common Host |
|-----------|----------|--------------|-------------|
| JavaScript/TS | npmjs.com | [name].dev | Docusaurus, VitePress |
| Python | pypi.org | readthedocs.io | Read the Docs |
| Rust | crates.io | docs.rs | docs.rs |
| Ruby | rubygems.org | rubydoc.info | RDoc |
| Go | pkg.go.dev | pkg.go.dev | pkg.go.dev |
| PHP | packagist.org | [name].org | Various |
| Java | maven.org | javadoc | Maven Central |
