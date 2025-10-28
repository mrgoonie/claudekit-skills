# ClaudeKit - Agent Skills

[**Agent Skills**](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview.md) are specialized workflows that empower Claude to perform complex, multi-step tasks with precision and reliability. They combine mission briefs, guardrails, and integration hints to transform generic AI assistance into disciplined automation.

> Skills leverage Claude's VM environment to provide capabilities beyond what's possible with prompts alone. Claude operates in a virtual machine with filesystem access, allowing Skills to exist as directories containing instructions, executable code, and reference materials, organized like an onboarding guide you'd create for a new team member.
> 
> This filesystem-based architecture enables **progressive disclosure**: Claude loads information in stages as needed, rather than consuming context upfront.

Learn more about Agent Skills: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview.md

## Repository overview
- **Purpose**: Share the free `.claude/skills/*` folders that power the open ClaudeKit workflows.
- **Source**: Mirrors the Agent Skills shipped with the **Claude Engineer** toolkit stored in [ClaudeKit.cc](https://claudekit.cc).
- **Audience**: Indie builders, startups, and teams who want a starting point for disciplined Claude Code automations.

## What lives inside `.claude/skills/*`
Each folder under `.claude/skills` bundles:
- **Mission brief**: Opinionated instructions that keep Claude focused on shipping real work instead of generic chat.
- **Guardrails**: Step-by-step checklists and fallback actions that make outputs reviewable and auditable.
- **Integration hints**: Suggested MCP connections, file structures, and prompts so you can plug skills directly into your repositories.

The directories are intentionally human-readable. Copy a skill, tweak the text files, and commit it alongside your project—Claude Code will pick it up automatically on the next run.

## Claude Code at a glance
Recent updates make Claude Code an ideal companion for these skills:
- **Parallel web sessions**: Launch multiple coding tasks from the browser, steer them mid-flight, and let Claude open pull requests when it finishes.
- **Security-first sandboxing**: Grant scoped filesystem and network access so Claude can fetch dependencies or run tests without exposing the rest of your infrastructure.
- **On-the-go iteration**: Use the iOS preview to nudge a session while you are away from your laptop.

(See Anthropic’s [Claude Code on the web](https://www.anthropic.com/news/claude-code-on-the-web) announcement and Ars Technica’s coverage of the new sandbox runtime for deeper context.)

[![ClaudeKit Agent Skills](./claudekit.png)](https://claudekit.cc)

## Skills catalog

### 🔐 Authentication & Security
- **`better-auth`** - Comprehensive TypeScript authentication framework supporting email/password, OAuth, 2FA, passkeys, and multi-tenancy. Works with any framework (Next.js, Nuxt, SvelteKit, etc.).

### 🤖 AI & Agent Development
- **`google-adk-python`** - Google's Agent Development Kit (ADK) for building AI agents with tool integration, multi-agent orchestration, workflow patterns (sequential, parallel, loop), and deployment to Vertex AI or custom infrastructure.

### 🎨 Design & Creative
- **`canvas-design`** - Create museum-quality visual art in PDF/PNG using design philosophy. Generates aesthetic movements first, then expresses them visually through masterful composition, typography, and color theory.
- **`remix-icon`** - Open-source icon library with 3,100+ icons in outlined and filled styles. Supports webfonts, SVG, React, Vue, and direct integration. Built on 24x24 pixel grid for perfect alignment.

### 🧠 AI & Machine Learning
- **`gemini-audio`** - Google Gemini API audio capabilities - analyze audio with transcription, summarization, and understanding (up to 9.5 hours), plus generate speech with controllable TTS.
- **`gemini-document-processing`** - Google Gemini API document processing - analyze PDFs with native vision to extract text, images, diagrams, charts, and tables.
- **`gemini-image-gen`** - Google Gemini API image generation - create high-quality images from text prompts using gemini-2.5-flash-image model with text-to-image, editing, and composition.
- **`gemini-video-understanding`** - Google Gemini API video analysis - describe content, answer questions, transcribe audio with visual descriptions, reference timestamps, and process YouTube URLs.
- **`gemini-vision`** - Google Gemini API image understanding - analyze images with captioning, classification, visual QA, object detection, segmentation, and multi-image comparison.

### 🌐 Web Development
- **`nextjs`** - React framework for production with server-side rendering, static generation, App Router, Server Components, and powerful optimization features. Complete guide for Next.js 15+.
- **`shadcn-ui`** - Beautifully-designed, accessible UI components built with Radix UI and Tailwind CSS. Copy-paste components into your codebase with full ownership and customization.
- **`tailwindcss`** - Utility-first CSS framework for rapid UI development with responsive design, dark mode, custom themes, and optimized build-time processing.

### 🌐 Browser Automation & Testing
- **`chrome-devtools`** - Browser automation, debugging, and performance analysis using Puppeteer CLI scripts. Automate browsers, take screenshots, analyze performance, monitor network traffic, web scraping, and form automation.

### ☁️ Cloud Platforms
- **`cloudflare`** - Build applications on Cloudflare's edge platform with serverless functions (Workers), edge databases (D1), storage (R2, KV), real-time apps (Durable Objects), and AI features (Workers AI).
- **`cloudflare-browser-rendering`** - Cloudflare's headless browser automation API for screenshots, PDFs, web scraping, and testing. Supports REST API, Workers Bindings (Puppeteer/Playwright), and AI-powered automation.
- **`cloudflare-r2`** - S3-compatible object storage with zero egress fees. Implement file storage, uploads/downloads, data migration, bucket configuration, and Workers integration.
- **`cloudflare-workers`** - Build serverless applications with Cloudflare Workers. Develop edge functions, configure bindings, implement runtime APIs, use Wrangler CLI, and deploy to production.
- **`gcloud`** - Google Cloud SDK (gcloud CLI) for managing Google Cloud resources. Install/configure gcloud, authenticate, manage projects, deploy applications, work with Compute Engine/GKE/App Engine/Cloud Storage.

### 🐳 Infrastructure & DevOps
- **`docker`** - Containerization platform for building, running, and deploying applications in isolated containers. Create Dockerfiles, use Docker Compose, manage images/containers, configure networking, and optimize builds.

### 🗄️ Databases
- **`mongodb`** - Document database platform with CRUD operations, aggregation pipelines, indexing, replication, sharding, and search capabilities. Works with Atlas, self-managed, or Kubernetes deployments.
- **`postgresql-psql`** - PostgreSQL interactive terminal client (psql) for connecting to databases, executing queries, managing databases/tables, formatting output, writing scripts, and database administration.

### 🛠️ Development Tools
- **`claude-code`** - Complete guide to Claude Code features: slash commands, hooks, plugins, MCP servers, agent skills, IDE integration, and enterprise deployment.
- **`ffmpeg`** - Comprehensive multimedia framework for video/audio encoding, conversion, streaming, and filtering. Supports all major codecs and formats.
- **`imagemagick`** - Command-line image processing for format conversion, resizing, cropping, effects, watermarks, and batch operations across 250+ formats.
- **`mcp-builder`** - Build high-quality MCP servers in Python (FastMCP) or TypeScript. Includes agent-centric design principles, evaluation harnesses, and best practices.
- **`repomix`** - Package entire repositories into single AI-friendly files (XML, Markdown, JSON). Perfect for codebase analysis, security audits, and LLM context generation.
- **`turborepo`** - High-performance build system for JavaScript/TypeScript monorepos. Intelligent caching, task orchestration, and remote execution for dramatically faster builds.

### 📚 Documentation & Research
- **`docs-seeker`** - Intelligent documentation discovery using llms.txt standard, GitHub repository analysis via Repomix, and parallel exploration agents for comprehensive coverage.

### 🐛 Debugging & Quality
- **`debugging/defense-in-depth`** - Validate at every layer data passes through. Make bugs structurally impossible with entry validation, business logic checks, environment guards, and debug logging.
- **`debugging/root-cause-tracing`** - Trace bugs backward through the call stack to find original triggers. Fix at the source, not the symptom.
- **`debugging/systematic-debugging`** - Four-phase framework ensuring root cause investigation before fixes. Never jump to solutions.
- **`debugging/verification-before-completion`** - Run verification commands and confirm output before claiming success. Evidence before claims, always.

### 📄 Document Processing
- **`document-skills/docx`** - Create, edit, and analyze Word documents with tracked changes, comments, formatting preservation, and redlining workflows for professional documents.
- **`document-skills/pdf`** - Extract text/tables, create PDFs, merge/split documents, fill forms. Uses pypdf and command-line tools for programmatic PDF processing.
- **`document-skills/pptx`** - Create and edit PowerPoint presentations with layouts, speaker notes, comments, animations, and design elements.
- **`document-skills/xlsx`** - Build spreadsheets with formulas, formatting, data analysis, and visualization. Includes financial modeling standards and zero-error formula requirements.

### 🛍️ E-commerce & Platforms
- **`shopify`** - Build Shopify apps, extensions, and themes using GraphQL/REST APIs, Shopify CLI, Polaris UI. Includes checkout extensions, admin customization, Liquid templating, and Shopify Functions.

### 🧠 Problem-Solving Frameworks
- **`problem-solving/collision-zone-thinking`** - Force unrelated concepts together to discover emergent properties. "What if we treated X like Y?"
- **`problem-solving/inversion-exercise`** - Flip core assumptions to reveal hidden constraints and alternative approaches. "What if the opposite were true?"
- **`problem-solving/meta-pattern-recognition`** - Spot patterns appearing in 3+ domains to find universal principles worth extracting.
- **`problem-solving/scale-game`** - Test at extremes (1000x bigger/smaller, instant/year-long) to expose fundamental truths hidden at normal scales.
- **`problem-solving/simplification-cascades`** - Find one insight that eliminates multiple components. "If this is true, we don't need X, Y, or Z."
- **`problem-solving/when-stuck`** - Dispatch to the right problem-solving technique based on your specific type of stuck-ness.

### 🔧 Meta Skills
- **`skill-creator`** - Guide for creating effective skills with specialized workflows, tool integrations, domain expertise, and bundled resources.

## Getting started
- **Install**: Clone this repo or copy selected folders into your own project.
- **Customize**: Edit the instruction files to match your processes, owners, and tools.
- **Run**: Open Claude Code, connect the repository, and select the skill that aligns with your task. Claude will follow the playbook while you supervise the diffs.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=mrgoonie/claudekit-skills&type=date&legend=top-left)](https://www.star-history.com/#mrgoonie/claudekit-skills&type=date&legend=top-left)

## Extend beyond the free tier
This collection covers the essentials. If you need advanced regulated-industry skills, analytics dashboards, or tailored onboarding, explore the full ClaudeKit package at [ClaudeKit.cc](https://claudekit.cc). The commercial bundle stays subtle but unlocks deeper automation while keeping the same transparent workflow philosophy.

**I've been spending 6+ months to dig into every aspect of Claude Code so you don't have to.**

[![ClaudeKit Agent Skills](./claudekit.png)](https://claudekit.cc)