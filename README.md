# ClaudeKit - Agent Skills

[**Agent Skills**](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) are specialized workflows that empower Claude to perform complex, multi-step tasks with precision and reliability. They combine mission briefs, guardrails, and integration hints to transform generic AI assistance into disciplined automation.

> Skills leverage Claude's VM environment to provide capabilities beyond what's possible with prompts alone. Claude operates in a virtual machine with filesystem access, allowing Skills to exist as directories containing instructions, executable code, and reference materials, organized like an onboarding guide you'd create for a new team member.
> 
> This filesystem-based architecture enables **progressive disclosure**: Claude loads information in stages as needed, rather than consuming context upfront.

Learn more about Agent Skills: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview

## Update [Nov 2025]: No more context bloat with "mcp-manager" subagent + "mcp-management" skills!

![No more context bloat with "mcp-manager" subagent + "mcp-management" skills](https://github.com/mrgoonie/claudekit-skills/blob/main/assets/mcp-management.jpeg?raw=true)

📖 Read more here: [MCP_MANAGEMENT.md](MCP_MANAGEMENT.md)

## ✨ Skills just got refactored!

📖 Read more here: [REFACTOR.md](REFACTOR.md)

## Skills catalog

### 🔐 Authentication & Security
- **[better-auth](.claude/skills/better-auth)** - Comprehensive TypeScript authentication framework supporting email/password, OAuth, 2FA, passkeys, and multi-tenancy. Works with any framework (Next.js, Nuxt, SvelteKit, etc.).

### 🤖 AI & Agent Development
- **[google-adk-python](.claude/skills/google-adk-python)** - Google's Agent Development Kit (ADK) for building AI agents with tool integration, multi-agent orchestration, workflow patterns (sequential, parallel, loop), and deployment to Vertex AI or custom infrastructure.

### 💻 Backend Development
- **[backend-development](.claude/skills/backend-development)** - Build robust backend systems with modern technologies (Node.js, Python, Go, Rust), frameworks (NestJS, FastAPI, Django), databases (PostgreSQL, MongoDB, Redis), APIs (REST, GraphQL, gRPC), authentication (OAuth 2.1, JWT), testing strategies, security best practices (OWASP Top 10), performance optimization, scalability patterns (microservices, caching, sharding), DevOps practices (Docker, Kubernetes, CI/CD), and monitoring. Use when designing APIs, implementing authentication, optimizing database queries, setting up CI/CD pipelines, handling security vulnerabilities, building microservices, or developing production-ready backend systems.

### 🧠 AI & Machine Learning
- **[ai-multimodal](.claude/skills/ai-multimodal)** - Process and generate multimedia content using Google Gemini API. Capabilities include analyze audio (transcription, summarization up to 9.5 hours), understand images (captioning, object detection, OCR, visual Q&A), process videos (scene detection, Q&A, temporal analysis, YouTube URLs up to 6 hours), extract from documents (PDF tables, forms, charts, diagrams), generate images (text-to-image, editing, composition). Supports Gemini 2.5/2.0 with context windows up to 2M tokens.

### 🎨 Design & Aesthetics
- **[aesthetic](.claude/skills/aesthetic)** - Create aesthetically beautiful interfaces following proven design principles. Use when building UI/UX, analyzing designs from inspiration sites, generating design images with ai-multimodal, implementing visual hierarchy and color theory, adding micro-interactions, or creating design documentation. Includes workflows for capturing and analyzing inspiration screenshots with chrome-devtools and ai-multimodal, iterative design image generation until aesthetic standards are met, and comprehensive design system guidance covering BEAUTIFUL (aesthetic principles), RIGHT (functionality/accessibility), SATISFYING (micro-interactions), and PEAK (storytelling) stages.

### 🌐 Web Development
- **[web-frameworks](.claude/skills/web-frameworks)** - Build modern full-stack web applications with Next.js (App Router, Server Components, RSC, PPR, SSR, SSG, ISR), Turborepo (monorepo management, task pipelines, remote caching, parallel execution), and RemixIcon (3100+ SVG icons). Create React applications, implement server-side rendering, set up monorepos, optimize build performance, manage shared dependencies.
- **[ui-styling](.claude/skills/ui-styling)** - Create beautiful, accessible user interfaces with shadcn/ui components (built on Radix UI + Tailwind), Tailwind CSS utility-first styling, and canvas-based visual designs. Build design systems, create responsive layouts, add accessible components, customize themes, implement dark mode, generate visual designs and posters.
- **[frontend-design](.claude/skills/frontend-design)** - Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
- **[frontend-development](.claude/skills/frontend-development)** - Frontend development guidelines for React/TypeScript applications. Modern patterns including Suspense, lazy loading, useSuspenseQuery, file organization with features directory, MUI v7 styling, TanStack Router, performance optimization, and TypeScript best practices. Use when creating components, pages, features, fetching data, styling, routing, or working with frontend code.

### 🌐 Browser Automation & Testing
- **[chrome-devtools](.claude/skills/chrome-devtools)** - Browser automation, debugging, and performance analysis using Puppeteer CLI scripts. Automate browsers, take screenshots, analyze performance, monitor network traffic, web scraping, and form automation.

### ☁️ Cloud Platforms & DevOps
- **[devops](.claude/skills/devops)** - Deploy and manage cloud infrastructure on Cloudflare (Workers, R2, D1, KV, Pages, Durable Objects, Browser Rendering), Docker containers, and Google Cloud Platform (Compute Engine, GKE, Cloud Run, App Engine, Cloud Storage). Deploy serverless functions to the edge, configure edge computing solutions, manage containers, set up CI/CD pipelines, optimize cloud infrastructure costs.

### 🗄️ Databases
- **[databases](.claude/skills/databases)** - Work with MongoDB (document database, BSON documents, aggregation pipelines, Atlas cloud) and PostgreSQL (relational database, SQL queries, psql CLI, pgAdmin). Design database schemas, write queries and aggregations, optimize indexes, perform migrations, configure replication and sharding, implement backup and restore strategies.

### 🛠️ Development Tools
- **[claude-code](.claude/skills/claude-code)** - Complete guide to Claude Code features: slash commands, hooks, plugins, MCP servers, agent skills, IDE integration, and enterprise deployment.
- **[mcp-builder](.claude/skills/mcp-builder)** - Build high-quality MCP servers in Python (FastMCP) or TypeScript. Includes agent-centric design principles, evaluation harnesses, and best practices.
- **[mcp-management](.claude/skills/mcp-management)** - Manage Model Context Protocol (MCP) servers - discover, analyze, and execute tools/prompts/resources from configured MCP servers. Use when working with MCP integrations, need to discover available MCP capabilities, filter MCP tools for specific tasks, execute MCP tools programmatically, access MCP prompts/resources, or implement MCP client functionality. Supports intelligent tool selection, multi-server management, and context-efficient capability discovery.
- **[repomix](.claude/skills/repomix)** - Package entire repositories into single AI-friendly files (XML, Markdown, JSON). Perfect for codebase analysis, security audits, and LLM context generation.
- **[media-processing](.claude/skills/media-processing)** - Process multimedia files with FFmpeg (video/audio encoding, conversion, streaming, filtering, hardware acceleration) and ImageMagick (image manipulation, format conversion, batch processing, effects, composition). Supports 100+ formats, hardware acceleration (NVENC, QSV), and complex filtergraphs.

### 📚 Documentation & Research
- **[docs-seeker](.claude/skills/docs-seeker)** - Intelligent documentation discovery using llms.txt standard, GitHub repository analysis via Repomix, and parallel exploration agents for comprehensive coverage.

### 🧪 Code Quality & Review
- **[code-review](.claude/skills/code-review)** - Use when receiving code review feedback (especially if unclear or technically questionable), when completing tasks or major features requiring review before proceeding, or before making any completion/success claims. Essential for subagent-driven development, pull requests, and preventing false completion claims.

### 🐛 Debugging & Quality
- **[debugging/defense-in-depth](.claude/skills/debugging/defense-in-depth)** - Validate at every layer data passes through. Make bugs structurally impossible with entry validation, business logic checks, environment guards, and debug logging.
- **[debugging/root-cause-tracing](.claude/skills/debugging/root-cause-tracing)** - Trace bugs backward through the call stack to find original triggers. Fix at the source, not the symptom.
- **[debugging/systematic-debugging](.claude/skills/debugging/systematic-debugging)** - Four-phase framework ensuring root cause investigation before fixes. Never jump to solutions.
- **[debugging/verification-before-completion](.claude/skills/debugging/verification-before-completion)** - Run verification commands and confirm output before claiming success. Evidence before claims, always.

### 📄 Document Processing
- **[document-skills/docx](.claude/skills/document-skills/docx)** - Create, edit, and analyze Word documents with tracked changes, comments, formatting preservation, and redlining workflows for professional documents.
- **[document-skills/pdf](.claude/skills/document-skills/pdf)** - Extract text/tables, create PDFs, merge/split documents, fill forms. Uses pypdf and command-line tools for programmatic PDF processing.
- **[document-skills/pptx](.claude/skills/document-skills/pptx)** - Create and edit PowerPoint presentations with layouts, speaker notes, comments, animations, and design elements.
- **[document-skills/xlsx](.claude/skills/document-skills/xlsx)** - Build spreadsheets with formulas, formatting, data analysis, and visualization. Includes financial modeling standards and zero-error formula requirements.

### 🛍️ E-commerce & Platforms
- **[shopify](.claude/skills/shopify)** - Build Shopify apps, extensions, and themes using GraphQL/REST APIs, Shopify CLI, Polaris UI. Includes checkout extensions, admin customization, Liquid templating, and Shopify Functions.

### 🧠 Problem-Solving Frameworks
- **[problem-solving/collision-zone-thinking](.claude/skills/problem-solving/collision-zone-thinking)** - Force unrelated concepts together to discover emergent properties. "What if we treated X like Y?"
- **[problem-solving/inversion-exercise](.claude/skills/problem-solving/inversion-exercise)** - Flip core assumptions to reveal hidden constraints and alternative approaches. "What if the opposite were true?"
- **[problem-solving/meta-pattern-recognition](.claude/skills/problem-solving/meta-pattern-recognition)** - Spot patterns appearing in 3+ domains to find universal principles worth extracting.
- **[problem-solving/scale-game](.claude/skills/problem-solving/scale-game)** - Test at extremes (1000x bigger/smaller, instant/year-long) to expose fundamental truths hidden at normal scales.
- **[problem-solving/simplification-cascades](.claude/skills/problem-solving/simplification-cascades)** - Find one insight that eliminates multiple components. "If this is true, we don't need X, Y, or Z."
- **[problem-solving/when-stuck](.claude/skills/problem-solving/when-stuck)** - Dispatch to the right problem-solving technique based on your specific type of stuck-ness.

### 🧠 Advanced Reasoning
- **[sequential-thinking](.claude/skills/sequential-thinking)** - Use when complex problems require systematic step-by-step reasoning with ability to revise thoughts, branch into alternative approaches, or dynamically adjust scope. Ideal for multi-stage analysis, design planning, problem decomposition, or tasks with initially unclear scope.

### 🔧 Meta Skills (from Anthropic)
- **[skill-creator](.claude/skills/skill-creator)** - Guide for creating effective skills with specialized workflows, tool integrations, domain expertise, and bundled resources.

## Getting started
- **Install**: Clone this repo or copy selected folders into your own project.
- **Customize**: Edit the instruction files to match your processes, owners, and tools.
- **Run**: Open Claude Code, connect the repository, and select the skill that aligns with your task. Claude will follow the playbook while you supervise the diffs.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=mrgoonie/claudekit-skills&type=date&legend=top-left)](https://www.star-history.com/#mrgoonie/claudekit-skills&type=date&legend=top-left)

## Extend beyond the free tier
This collection covers the essentials. If you need advanced regulated-industry skills, analytics dashboards, or tailored onboarding, explore the full ClaudeKit package at [ClaudeKit.cc](https://claudekit.cc). The commercial bundle stays subtle but unlocks deeper automation while keeping the same transparent workflow philosophy.

**I've been spending 6+ months to dig into every aspect of Claude Code so you don't have to.**

[![ClaudeKit Agent Skills](https://github.com/mrgoonie/claudekit-skills/blob/main/claudekit.png?raw=true)](https://claudekit.cc)

I've basically been sharing everything I learned about Claude Code on Substack: https://faafospecialist.substack.com/

So if you find this collection useful, please consider supporting my product at [ClaudeKit.cc](https://claudekit.cc).

Thanks for your support! 🥰