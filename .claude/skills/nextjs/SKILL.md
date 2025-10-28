---
name: nextjs
description: Guide for implementing Next.js - a React framework for production with server-side rendering, static generation, and modern web features. Use when building Next.js applications, implementing App Router, working with server components, data fetching, routing, or optimizing performance.
license: MIT
version: 1.0.0
---

# Next.js Skill

Next.js is a React framework for building full-stack web applications with server-side rendering, static generation, and powerful optimization features built-in.

## Reference

https://nextjs.org/docs/llms.txt

## When to Use This Skill

Use this skill when:
- Building new Next.js applications (v15+)
- Implementing App Router architecture
- Working with Server Components and Client Components
- Setting up routing, layouts, and navigation
- Implementing data fetching patterns
- Optimizing images, fonts, and performance
- Configuring metadata and SEO
- Setting up API routes and route handlers
- Migrating from Pages Router to App Router
- Deploying Next.js applications

## Core Concepts

### App Router vs Pages Router

**App Router (Recommended for v13+):**
- Modern architecture with React Server Components
- File-system based routing in `app/` directory
- Layouts, loading states, and error boundaries
- Streaming and Suspense support
- Nested routing with layouts

**Pages Router (Legacy):**
- Traditional page-based routing in `pages/` directory
- Uses `getStaticProps`, `getServerSideProps`, `getInitialProps`
- Still supported for existing projects

### Key Architectural Principles

1. **Server Components by Default**: Components in `app/` are Server Components unless marked with `'use client'`
2. **File-based Routing**: File system defines application routes
3. **Nested Layouts**: Share UI across routes with layouts
4. **Progressive Enhancement**: Works without JavaScript when possible
5. **Automatic Optimization**: Images, fonts, scripts auto-optimized

## Installation & Setup

### Create New Project

```bash
npx create-next-app@latest my-app
# or
yarn create next-app my-app
# or
pnpm create next-app my-app
# or
bun create next-app my-app
```

**Interactive Setup Prompts:**
- TypeScript? (Yes recommended)
- ESLint? (Yes recommended)
- Tailwind CSS? (Optional)
- `src/` directory? (Optional)
- App Router? (Yes for new projects)
- Import alias? (Default: @/*)

### Manual Setup

```bash
npm install next@latest react@latest react-dom@latest
```

**package.json scripts:**
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }
}
```

### Project Structure

```
my-app/
├── app/                    # App Router (v13+)
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   ├── loading.tsx        # Loading UI
│   ├── error.tsx          # Error UI
│   ├── not-found.tsx      # 404 page
│   ├── global.css         # Global styles
│   └── [folder]/          # Route segments
├── public/                # Static assets
├── components/            # React components
├── lib/                   # Utility functions
├── next.config.js         # Next.js configuration
├── package.json
└── tsconfig.json
```

## Routing

### File Conventions

- `page.tsx` - Page UI for route
- `layout.tsx` - Shared UI for segment and children
- `loading.tsx` - Loading UI (wraps page in Suspense)
- `error.tsx` - Error UI (wraps page in Error Boundary)
- `not-found.tsx` - 404 UI
- `route.ts` - API endpoint (Route Handler)
- `template.tsx` - Re-rendered layout UI
- `default.tsx` - Parallel route fallback

### Basic Routing

**Static Route:**
```
app/
├── page.tsx              → /
├── about/
│   └── page.tsx         → /about
└── blog/
    └── page.tsx         → /blog
```

**Dynamic Route:**
```tsx
// app/blog/[slug]/page.tsx
export default function BlogPost({ params }: { params: { slug: string } }) {
  return <h1>Post: {params.slug}</h1>
}
```

**Catch-all Route:**
```tsx
// app/shop/[...slug]/page.tsx
export default function Shop({ params }: { params: { slug: string[] } }) {
  return <h1>Category: {params.slug.join('/')}</h1>
}
```

**Optional Catch-all:**
```tsx
// app/docs/[[...slug]]/page.tsx
// Matches /docs, /docs/a, /docs/a/b, etc.
```

### Route Groups

Organize routes without affecting URL:

```
app/
├── (marketing)/          # Group without URL segment
│   ├── about/page.tsx   → /about
│   └── blog/page.tsx    → /blog
└── (shop)/
    ├── products/page.tsx → /products
    └── cart/page.tsx     → /cart
```

### Parallel Routes

Render multiple pages in same layout:

```
app/
├── @team/               # Slot
│   └── page.tsx
├── @analytics/          # Slot
│   └── page.tsx
└── layout.tsx           # Uses both slots
```

```tsx
// app/layout.tsx
export default function Layout({
  children,
  team,
  analytics,
}: {
  children: React.ReactNode
  team: React.ReactNode
  analytics: React.ReactNode
}) {
  return (
    <>
      {children}
      {team}
      {analytics}
    </>
  )
}
```

### Intercepting Routes

Intercept routes to show in modal:

```
app/
├── feed/
│   └── page.tsx
├── photo/
│   └── [id]/
│       └── page.tsx
└── (..)photo/           # Intercepts /photo/[id]
    └── [id]/
        └── page.tsx
```

## Layouts

### Root Layout (Required)

```tsx
// app/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

### Nested Layouts

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <section>
      <nav>Dashboard Nav</nav>
      {children}
    </section>
  )
}
```

**Layouts are:**
- Shared across multiple pages
- Preserve state on navigation
- Do not re-render on navigation
- Can fetch data

## Server and Client Components

### Server Components (Default)

Components in `app/` are Server Components by default:

```tsx
// app/page.tsx (Server Component)
async function getData() {
  const res = await fetch('https://api.example.com/data')
  return res.json()
}

export default async function Page() {
  const data = await getData()
  return <div>{data.title}</div>
}
```

**Benefits:**
- Fetch data on server
- Access backend resources directly
- Keep sensitive data on server
- Reduce client-side JavaScript
- Improve initial page load

**Limitations:**
- Cannot use hooks (useState, useEffect)
- Cannot use browser APIs
- Cannot add event listeners

### Client Components

Mark components with `'use client'` directive:

```tsx
// components/counter.tsx
'use client'

import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  )
}
```

**Use Client Components for:**
- Interactive UI (onClick, onChange)
- State management (useState, useReducer)
- Effects (useEffect, useLayoutEffect)
- Browser APIs (localStorage, navigator)
- Custom hooks
- React class components

### Composition Pattern

```tsx
// app/page.tsx (Server Component)
import { ClientComponent } from './client-component'

export default function Page() {
  return (
    <div>
      <h1>Server-rendered content</h1>
      <ClientComponent />
    </div>
  )
}
```

## Data Fetching

### Server Component Data Fetching

```tsx
// app/posts/page.tsx
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 } // Revalidate every hour
  })

  if (!res.ok) throw new Error('Failed to fetch')

  return res.json()
}

export default async function PostsPage() {
  const posts = await getPosts()

  return (
    <ul>
      {posts.map(post => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

### Caching Strategies

**Force Cache (Default):**
```tsx
fetch('https://api.example.com/data', { cache: 'force-cache' })
```

**No Store (Dynamic):**
```tsx
fetch('https://api.example.com/data', { cache: 'no-store' })
```

**Revalidate:**
```tsx
fetch('https://api.example.com/data', {
  next: { revalidate: 3600 } // Seconds
})
```

**Tag-based Revalidation:**
```tsx
fetch('https://api.example.com/data', {
  next: { tags: ['posts'] }
})

// Revalidate elsewhere:
import { revalidateTag } from 'next/cache'
revalidateTag('posts')
```

### Parallel Data Fetching

```tsx
async function getData() {
  const [posts, users] = await Promise.all([
    fetch('https://api.example.com/posts').then(r => r.json()),
    fetch('https://api.example.com/users').then(r => r.json()),
  ])

  return { posts, users }
}
```

### Sequential Data Fetching

```tsx
async function getData() {
  const post = await fetch(`https://api.example.com/posts/${id}`).then(r => r.json())
  const author = await fetch(`https://api.example.com/users/${post.authorId}`).then(r => r.json())

  return { post, author }
}
```

## Route Handlers (API Routes)

### Basic Route Handler

```tsx
// app/api/hello/route.ts
export async function GET(request: Request) {
  return Response.json({ message: 'Hello' })
}

export async function POST(request: Request) {
  const body = await request.json()
  return Response.json({ received: body })
}
```

### Dynamic Route Handler

```tsx
// app/api/posts/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const post = await getPost(params.id)
  return Response.json(post)
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  await deletePost(params.id)
  return new Response(null, { status: 204 })
}
```

### Request Helpers

```tsx
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')

  const cookies = request.headers.get('cookie')

  return Response.json({ id })
}
```

### Response Types

```tsx
// JSON
return Response.json({ data: 'value' })

// Text
return new Response('Hello', { headers: { 'Content-Type': 'text/plain' } })

// Redirect
return Response.redirect('https://example.com')

// Status codes
return new Response('Not Found', { status: 404 })
```

## Navigation

### Link Component

```tsx
import Link from 'next/link'

export default function Page() {
  return (
    <>
      <Link href="/about">About</Link>
      <Link href="/blog/post-1">Post 1</Link>
      <Link href={{ pathname: '/blog/[slug]', query: { slug: 'post-1' } }}>
        Post 1 (alternative)
      </Link>
    </>
  )
}
```

### useRouter Hook (Client)

```tsx
'use client'

import { useRouter } from 'next/navigation'

export function NavigateButton() {
  const router = useRouter()

  return (
    <button onClick={() => router.push('/dashboard')}>
      Dashboard
    </button>
  )
}
```

**Router Methods:**
- `router.push(href)` - Navigate to route
- `router.replace(href)` - Replace current history
- `router.refresh()` - Refresh current route
- `router.back()` - Navigate back
- `router.forward()` - Navigate forward
- `router.prefetch(href)` - Prefetch route

### Programmatic Navigation (Server)

```tsx
import { redirect } from 'next/navigation'

export default async function Page() {
  const session = await getSession()

  if (!session) {
    redirect('/login')
  }

  return <div>Protected content</div>
}
```

## Metadata & SEO

### Static Metadata

```tsx
// app/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My Page',
  description: 'Page description',
  keywords: ['nextjs', 'react'],
  openGraph: {
    title: 'My Page',
    description: 'Page description',
    images: ['/og-image.jpg'],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'My Page',
    description: 'Page description',
    images: ['/twitter-image.jpg'],
  },
}

export default function Page() {
  return <div>Content</div>
}
```

### Dynamic Metadata

```tsx
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.slug)

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
    },
  }
}
```

### Metadata Files

- `favicon.ico`, `icon.png`, `apple-icon.png` - Favicons
- `opengraph-image.png`, `twitter-image.png` - Social images
- `robots.txt` - Robots file
- `sitemap.xml` - Sitemap

## Image Optimization

### Image Component

```tsx
import Image from 'next/image'

export default function Page() {
  return (
    <>
      {/* Local image */}
      <Image
        src="/profile.png"
        alt="Profile"
        width={500}
        height={500}
      />

      {/* Remote image */}
      <Image
        src="https://example.com/image.jpg"
        alt="Remote"
        width={500}
        height={500}
      />

      {/* Responsive fill */}
      <div style={{ position: 'relative', width: '100%', height: '400px' }}>
        <Image
          src="/hero.jpg"
          alt="Hero"
          fill
          style={{ objectFit: 'cover' }}
        />
      </div>

      {/* Priority loading */}
      <Image
        src="/hero.jpg"
        alt="Hero"
        width={1200}
        height={600}
        priority
      />
    </>
  )
}
```

**Image Props:**
- `src` - Image path (local or URL)
- `alt` - Alt text (required)
- `width`, `height` - Dimensions (required unless fill)
- `fill` - Fill parent container
- `sizes` - Responsive sizes
- `quality` - 1-100 (default 75)
- `priority` - Preload image
- `placeholder` - 'blur' | 'empty'
- `blurDataURL` - Data URL for blur

### Remote Image Configuration

```js
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
        pathname: '/images/**',
      },
    ],
  },
}
```

## Font Optimization

### Google Fonts

```tsx
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
})

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto-mono',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.className} ${robotoMono.variable}`}>
      <body>{children}</body>
    </html>
  )
}
```

### Local Fonts

```tsx
import localFont from 'next/font/local'

const myFont = localFont({
  src: './fonts/my-font.woff2',
  display: 'swap',
  variable: '--font-my-font',
})
```

## Loading States

### Loading File

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <div>Loading dashboard...</div>
}
```

### Streaming with Suspense

```tsx
// app/page.tsx
import { Suspense } from 'react'

async function Posts() {
  const posts = await getPosts()
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}

export default function Page() {
  return (
    <div>
      <h1>My Posts</h1>
      <Suspense fallback={<div>Loading posts...</div>}>
        <Posts />
      </Suspense>
    </div>
  )
}
```

## Error Handling

### Error File

```tsx
// app/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

### Global Error

```tsx
// app/global-error.tsx
'use client'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <html>
      <body>
        <h2>Something went wrong!</h2>
        <button onClick={() => reset()}>Try again</button>
      </body>
    </html>
  )
}
```

### Not Found

```tsx
// app/not-found.tsx
export default function NotFound() {
  return (
    <div>
      <h2>404 - Not Found</h2>
      <p>Could not find requested resource</p>
    </div>
  )
}

// Trigger programmatically
import { notFound } from 'next/navigation'

export default async function Page({ params }) {
  const post = await getPost(params.id)

  if (!post) {
    notFound()
  }

  return <div>{post.title}</div>
}
```

## Middleware

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Authentication check
  const token = request.cookies.get('token')

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Add custom header
  const response = NextResponse.next()
  response.headers.set('x-custom-header', 'value')

  return response
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
}
```

## Environment Variables

```env
# .env.local
DATABASE_URL=postgresql://...
NEXT_PUBLIC_API_URL=https://api.example.com
```

```tsx
// Server-side only
const dbUrl = process.env.DATABASE_URL

// Client and server (NEXT_PUBLIC_ prefix)
const apiUrl = process.env.NEXT_PUBLIC_API_URL
```

## Configuration

### next.config.js

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // React strict mode
  reactStrictMode: true,

  // Image domains
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'example.com' },
    ],
  },

  // Redirects
  async redirects() {
    return [
      {
        source: '/old-page',
        destination: '/new-page',
        permanent: true,
      },
    ]
  },

  // Rewrites
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://api.example.com/:path*',
      },
    ]
  },

  // Headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
        ],
      },
    ]
  },

  // Environment variables
  env: {
    CUSTOM_KEY: 'value',
  },
}

module.exports = nextConfig
```

## Best Practices

1. **Use Server Components**: Default to Server Components, use Client Components only when needed
2. **Optimize Images**: Always use `next/image` for automatic optimization
3. **Metadata**: Set proper metadata for SEO
4. **Loading States**: Provide loading UI with Suspense
5. **Error Handling**: Implement error boundaries
6. **Route Handlers**: Use for API endpoints instead of separate backend
7. **Caching**: Leverage built-in caching strategies
8. **Layouts**: Use nested layouts to share UI
9. **TypeScript**: Enable TypeScript for type safety
10. **Performance**: Use `priority` for above-fold images, lazy load below-fold

## Common Patterns

### Protected Routes

```tsx
// app/dashboard/layout.tsx
import { redirect } from 'next/navigation'
import { getSession } from '@/lib/auth'

export default async function DashboardLayout({ children }) {
  const session = await getSession()

  if (!session) {
    redirect('/login')
  }

  return <>{children}</>
}
```

### Data Mutations (Server Actions)

```tsx
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'

export async function createPost(formData: FormData) {
  const title = formData.get('title')

  await db.post.create({ data: { title } })

  revalidatePath('/posts')
}

// app/posts/new/page.tsx
import { createPost } from '@/app/actions'

export default function NewPost() {
  return (
    <form action={createPost}>
      <input name="title" type="text" required />
      <button type="submit">Create</button>
    </form>
  )
}
```

### Static Generation

```tsx
// Generate static params for dynamic routes
export async function generateStaticParams() {
  const posts = await getPosts()

  return posts.map(post => ({
    slug: post.slug,
  }))
}

export default async function Post({ params }) {
  const post = await getPost(params.slug)
  return <article>{post.content}</article>
}
```

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Self-Hosting

```bash
# Build
npm run build

# Start production server
npm start
```

**Requirements:**
- Node.js 18.17 or later
- `output: 'standalone'` in next.config.js (optional, reduces size)

### Docker

```dockerfile
FROM node:18-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"]
```

## Troubleshooting

### Common Issues

1. **Hydration errors**
   - Ensure server and client render same content
   - Check for browser-only code in Server Components
   - Verify no conditional rendering based on browser APIs

2. **Images not loading**
   - Add remote domains to `next.config.js`
   - Check image paths (use leading `/` for public)
   - Verify width/height provided

3. **API route 404**
   - Check file is named `route.ts/js` not `index.ts`
   - Verify export named GET/POST not default export
   - Ensure in `app/api/` directory

4. **"use client" errors**
   - Add `'use client'` to components using hooks
   - Import Client Components in Server Components, not vice versa
   - Check event handlers have `'use client'`

5. **Metadata not updating**
   - Clear browser cache
   - Check metadata export is named correctly
   - Verify async generateMetadata returns Promise<Metadata>

## Resources

- Documentation: https://nextjs.org/docs
- Learn Course: https://nextjs.org/learn
- Examples: https://github.com/vercel/next.js/tree/canary/examples
- Blog: https://nextjs.org/blog
- GitHub: https://github.com/vercel/next.js

## Implementation Checklist

When building with Next.js:

- [ ] Create project with `create-next-app`
- [ ] Configure TypeScript and ESLint
- [ ] Set up root layout with metadata
- [ ] Implement routing structure
- [ ] Add loading and error states
- [ ] Configure image optimization
- [ ] Set up font optimization
- [ ] Implement data fetching patterns
- [ ] Add API routes as needed
- [ ] Configure environment variables
- [ ] Set up middleware if needed
- [ ] Optimize for production build
- [ ] Test in production mode
- [ ] Configure deployment platform
- [ ] Set up monitoring and analytics
