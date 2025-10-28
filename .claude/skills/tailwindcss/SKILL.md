---
name: tailwindcss
description: Guide for implementing Tailwind CSS - a utility-first CSS framework for rapid UI development. Use when styling applications with responsive design, dark mode, custom themes, or building design systems with Tailwind's utility classes.
license: MIT
version: 1.0.0
---

# Tailwind CSS Skill

Tailwind CSS is a utility-first CSS framework that enables rapid UI development by providing pre-built utility classes. It generates optimized CSS at build-time by scanning your project files, resulting in zero runtime overhead and minimal production bundles.

## When to Use This Skill

Use this skill when:
- Building responsive layouts with mobile-first design
- Implementing dark mode and theme customization
- Creating custom design systems with consistent spacing, colors, and typography
- Styling React, Vue, Svelte, or any web framework components
- Prototyping interfaces with rapid visual feedback
- Building production applications with optimized CSS bundles
- Working with state-based styling (hover, focus, disabled, etc.)
- Creating complex layouts with Grid and Flexbox utilities

## Core Concepts

### Utility-First Approach

Tailwind provides low-level utility classes that you apply directly to HTML elements instead of writing custom CSS:

```html
<!-- Traditional CSS approach -->
<div class="card">
  <h2 class="card-title">Title</h2>
</div>

<!-- Tailwind utility-first approach -->
<div class="bg-white rounded-lg shadow-md p-6">
  <h2 class="text-2xl font-bold text-gray-900">Title</h2>
</div>
```

**Benefits:**
- No CSS file switching - styles live with markup
- No naming conventions needed
- Automatic dead code elimination
- Consistent design tokens across team
- Fast iteration without CSS bloat

### Build-Time Processing

Tailwind scans your source files at build-time and generates only the CSS classes you actually use:

```javascript
// Tailwind analyzes these files
content: [
  "./src/**/*.{js,jsx,ts,tsx}",
  "./app/**/*.{js,jsx,ts,tsx}",
  "./components/**/*.{js,jsx,ts,tsx}"
]
```

Result: Optimized production bundles with zero runtime overhead.

## Installation & Setup

### Modern Setup with Vite

**Step 1: Install dependencies**

```bash
npm install -D tailwindcss @tailwindcss/vite
# or
pnpm add -D tailwindcss @tailwindcss/vite
# or
yarn add -D tailwindcss @tailwindcss/vite
```

**Step 2: Configure Vite**

```javascript
// vite.config.ts
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [tailwindcss()]
})
```

**Step 3: Import in CSS**

```css
/* src/index.css */
@import "tailwindcss";
```

**Step 4: Reference stylesheet in HTML**

```html
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="./src/index.css">
  </head>
  <body>
    <div class="bg-blue-500 text-white p-4">Hello Tailwind!</div>
  </body>
</html>
```

### Framework-Specific Setup

**Next.js (App Router):**
```bash
npx create-next-app@latest --tailwind
```

**Next.js (Manual):**
```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}"
  ]
}
```

**React with Vite:**
```bash
npm create vite@latest my-app -- --template react
npm install -D tailwindcss @tailwindcss/vite
```

**Vue:**
```bash
npm install -D tailwindcss @tailwindcss/vite
```

**Svelte:**
```bash
npm install -D tailwindcss @tailwindcss/vite
```

**Astro:**
```bash
npx astro add tailwind
```

### PostCSS Setup (Alternative)

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

```javascript
// postcss.config.js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {}
  }
}
```

## Design System & Tokens

### Default Design System

Tailwind includes a comprehensive default design system:

- **Colors**: 18 color palettes with 11 shades each (50-950)
- **Spacing**: Consistent scale from 0.25rem to 96rem
- **Typography**: Font sizes, weights, line heights
- **Breakpoints**: Mobile-first responsive system
- **Shadows**: Elevation system for depth
- **Border radius**: Rounded corners at different scales

### Customizing Theme

Use the `@theme` directive in CSS:

```css
@import "tailwindcss";

@theme {
  /* Custom colors */
  --color-brand-50: oklch(0.97 0.02 264);
  --color-brand-500: oklch(0.55 0.22 264);
  --color-brand-900: oklch(0.25 0.15 264);

  /* Custom fonts */
  --font-display: "Satoshi", "Inter", sans-serif;
  --font-body: "Inter", system-ui, sans-serif;

  /* Custom spacing */
  --spacing-18: calc(var(--spacing) * 18);
  --spacing-navbar: 4.5rem;

  /* Custom breakpoints */
  --breakpoint-3xl: 120rem;
  --breakpoint-4xl: 160rem;

  /* Custom shadows */
  --shadow-glow: 0 0 20px rgba(139, 92, 246, 0.3);
}
```

**Usage:**
```html
<div class="bg-brand-500 font-display shadow-glow">
  Custom themed element
</div>
```

### Color System

**Using default colors:**
```html
<div class="bg-blue-500">Background</div>
<p class="text-red-600">Text</p>
<div class="border-green-400">Border</div>
```

**Color scale:**
- 50: Lightest
- 100-400: Light variations
- 500: Base color
- 600-800: Dark variations
- 950: Darkest

**Color opacity modifiers:**
```html
<div class="bg-black/75">75% opacity</div>
<div class="text-blue-500/30">30% opacity</div>
<div class="bg-purple-500/[0.87]">87% opacity</div>
```

## Utility Classes

### Layout

**Display:**
```html
<div class="block">Block</div>
<div class="inline-block">Inline Block</div>
<div class="flex">Flex</div>
<div class="inline-flex">Inline Flex</div>
<div class="grid">Grid</div>
<div class="hidden">Hidden</div>
```

**Flexbox:**
```html
<div class="flex items-center justify-between gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<div class="flex flex-col items-start">
  <div>Vertical stack</div>
</div>
```

**Grid:**
```html
<div class="grid grid-cols-3 gap-4">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>

<div class="grid grid-cols-[1fr_500px_2fr] gap-6">
  <div>Flexible</div>
  <div>Fixed 500px</div>
  <div>More flexible</div>
</div>
```

**Positioning:**
```html
<div class="relative">
  <div class="absolute top-0 right-0">Positioned</div>
</div>

<div class="fixed bottom-4 right-4">Fixed</div>
<div class="sticky top-0">Sticky header</div>
```

### Spacing

**Padding & Margin:**
```html
<div class="p-4">Padding all sides</div>
<div class="px-6 py-3">Padding X and Y</div>
<div class="pt-8 pb-4">Padding top/bottom</div>
<div class="m-4">Margin all sides</div>
<div class="mx-auto">Center horizontally</div>
<div class="-mt-4">Negative margin</div>
```

**Gap (Flexbox/Grid):**
```html
<div class="flex gap-4">Flex with gap</div>
<div class="grid grid-cols-3 gap-x-6 gap-y-4">Grid with X/Y gap</div>
```

### Typography

**Font Size:**
```html
<p class="text-xs">Extra small</p>
<p class="text-sm">Small</p>
<p class="text-base">Base (16px)</p>
<p class="text-lg">Large</p>
<p class="text-xl">Extra large</p>
<p class="text-2xl">2XL</p>
<h1 class="text-4xl font-bold">Heading</h1>
```

**Font Weight:**
```html
<p class="font-light">Light (300)</p>
<p class="font-normal">Normal (400)</p>
<p class="font-medium">Medium (500)</p>
<p class="font-semibold">Semibold (600)</p>
<p class="font-bold">Bold (700)</p>
```

**Text Alignment:**
```html
<p class="text-left">Left aligned</p>
<p class="text-center">Center aligned</p>
<p class="text-right">Right aligned</p>
<p class="text-justify">Justified</p>
```

**Line Height:**
```html
<p class="leading-tight">Tight line height</p>
<p class="leading-normal">Normal line height</p>
<p class="leading-relaxed">Relaxed line height</p>
```

**Combining font utilities:**
```html
<h1 class="text-4xl/tight font-bold">
  Font size 4xl with tight line-height
</h1>
```

### Colors & Backgrounds

**Background colors:**
```html
<div class="bg-white">White background</div>
<div class="bg-gray-100">Gray background</div>
<div class="bg-gradient-to-r from-blue-500 to-purple-600">
  Gradient background
</div>
```

**Text colors:**
```html
<p class="text-gray-900">Dark text</p>
<p class="text-blue-600">Blue text</p>
<a class="text-blue-500 hover:text-blue-700">Link</a>
```

### Borders

```html
<div class="border">Default border</div>
<div class="border-2 border-gray-300">2px border</div>
<div class="border-t border-b-2">Top and bottom borders</div>
<div class="rounded">Rounded corners</div>
<div class="rounded-lg">Large rounded</div>
<div class="rounded-full">Fully rounded</div>
<div class="border border-red-500 rounded-md">Combined</div>
```

### Shadows

```html
<div class="shadow">Small shadow</div>
<div class="shadow-md">Medium shadow</div>
<div class="shadow-lg">Large shadow</div>
<div class="shadow-xl">Extra large shadow</div>
<div class="shadow-none">No shadow</div>
```

## Responsive Design

### Mobile-First Breakpoints

Tailwind uses a mobile-first approach. Base styles apply to all screen sizes, then use breakpoint prefixes to override at larger sizes:

**Breakpoints:**
- `sm:` - 640px and up
- `md:` - 768px and up
- `lg:` - 1024px and up
- `xl:` - 1280px and up
- `2xl:` - 1536px and up

**Example:**
```html
<!-- Mobile: 1 column, Tablet: 2 columns, Desktop: 4 columns -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
  <div>Item 4</div>
</div>

<!-- Hide on mobile, show on desktop -->
<div class="hidden lg:block">Desktop only content</div>

<!-- Show on mobile, hide on desktop -->
<div class="block lg:hidden">Mobile only content</div>

<!-- Responsive text sizes -->
<h1 class="text-2xl md:text-4xl lg:text-6xl">
  Responsive heading
</h1>
```

### Custom Breakpoints

```css
@theme {
  --breakpoint-3xl: 120rem;
  --breakpoint-tablet: 48rem;
}
```

```html
<div class="tablet:grid-cols-2 3xl:grid-cols-6">
  Custom breakpoints
</div>
```

### Max-width Queries

```html
<!-- Only apply styles below 768px -->
<div class="flex max-md:hidden">Hidden on mobile</div>

<!-- Between breakpoints -->
<div class="md:block lg:hidden">Only visible on tablets</div>
```

### Container Queries

Style elements based on parent container width:

```html
<div class="@container">
  <div class="@md:grid-cols-2 @lg:grid-cols-3">
    Responds to parent width
  </div>
</div>
```

## Interactive States

### Hover States

```html
<button class="bg-blue-500 hover:bg-blue-700 text-white">
  Hover me
</button>

<a class="text-blue-600 hover:underline">
  Hover link
</a>

<div class="scale-100 hover:scale-105 transition-transform">
  Scale on hover
</div>
```

### Focus States

```html
<input class="border focus:border-blue-500 focus:ring-2 focus:ring-blue-200" />

<button class="bg-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-300">
  Accessible button
</button>
```

### Active States

```html
<button class="bg-blue-500 active:bg-blue-800">
  Click me
</button>
```

### Disabled States

```html
<button class="bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed" disabled>
  Disabled button
</button>

<input class="disabled:bg-gray-100" disabled />
```

### Form States

```html
<input class="invalid:border-red-500 focus:invalid:ring-red-200" required />

<input class="placeholder:text-gray-400 placeholder:italic" placeholder="Search..." />

<input type="checkbox" class="checked:bg-blue-500" />
```

### Group Hover (Parent State)

```html
<div class="group hover:bg-gray-100">
  <p class="group-hover:text-blue-600">
    Text changes when parent is hovered
  </p>
  <img class="group-hover:opacity-50" src="..." />
</div>
```

### Peer State (Sibling State)

```html
<input type="checkbox" class="peer" id="terms" />
<label for="terms" class="peer-checked:text-blue-600">
  I accept terms
</label>

<input type="email" class="peer" required />
<p class="hidden peer-invalid:block text-red-600">
  Invalid email
</p>
```

## Dark Mode

### Setup Dark Mode

**Media query approach (automatic):**
```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Auto switches based on system preference
</div>
```

**Class-based approach (manual toggle):**

```javascript
// Add .dark class to <html> element
document.documentElement.classList.toggle('dark')
```

### Dark Mode Utilities

```html
<!-- Colors -->
<div class="bg-white dark:bg-slate-900">Background</div>
<p class="text-gray-900 dark:text-gray-100">Text</p>

<!-- Borders -->
<div class="border-gray-200 dark:border-gray-700">Border</div>

<!-- Complete example -->
<div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
  <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
    Dark mode card
  </h2>
  <p class="text-gray-600 dark:text-gray-300">
    Content adapts to theme
  </p>
</div>
```

### Dark Mode Toggle Implementation

```javascript
// Store preference
function toggleDarkMode() {
  const isDark = document.documentElement.classList.toggle('dark')
  localStorage.setItem('theme', isDark ? 'dark' : 'light')
}

// Initialize on load
if (localStorage.theme === 'dark' ||
    (!('theme' in localStorage) &&
     window.matchMedia('(prefers-color-scheme: dark)').matches)) {
  document.documentElement.classList.add('dark')
}
```

## Arbitrary Values

Use square brackets for one-off custom values:

**Pixel values:**
```html
<div class="top-[117px]">Custom position</div>
<p class="text-[22px]">Custom font size</p>
<div class="w-[500px]">Custom width</div>
```

**Colors:**
```html
<div class="bg-[#bada55]">Custom hex color</div>
<div class="text-[rgb(123,45,67)]">RGB color</div>
<div class="bg-[oklch(0.55_0.22_264)]">OKLCH color</div>
```

**CSS variables:**
```html
<div class="bg-[var(--my-brand-color)]">CSS variable</div>
<div class="text-[length:var(--my-font-size)]">Type hint</div>
```

**Complex values:**
```html
<div class="grid-cols-[1fr_500px_2fr]">Custom grid</div>
<div class="content-['>']">Custom content</div>
<div class="[mask-type:luminance]">Custom property</div>
```

## Transitions & Animations

### Transitions

```html
<button class="bg-blue-500 transition-colors hover:bg-blue-700">
  Smooth color transition
</button>

<div class="transform transition-transform hover:scale-110">
  Scale with transition
</div>

<div class="transition-all duration-300 ease-in-out hover:shadow-lg">
  Multiple transitions
</div>

<!-- Duration options -->
<div class="transition duration-150">Fast</div>
<div class="transition duration-300">Normal</div>
<div class="transition duration-500">Slow</div>
```

### Transforms

```html
<!-- Scale -->
<div class="scale-95 hover:scale-100">Scale</div>

<!-- Rotate -->
<div class="rotate-45">Rotate 45deg</div>
<div class="hover:rotate-6">Slight rotation</div>

<!-- Translate -->
<div class="translate-x-4 translate-y-2">Move</div>

<!-- Skew -->
<div class="skew-x-12">Skew</div>

<!-- Combined -->
<div class="transform scale-110 rotate-3 translate-x-2">
  Multiple transforms
</div>
```

### Animations

```html
<div class="animate-spin">Spinning</div>
<div class="animate-ping">Pinging</div>
<div class="animate-pulse">Pulsing</div>
<div class="animate-bounce">Bouncing</div>
```

### Custom Animations

```css
@theme {
  --animate-slide-in: slide-in 0.5s ease-out;
}

@keyframes slide-in {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(0);
  }
}
```

```html
<div class="animate-slide-in">Custom animation</div>
```

## Advanced Patterns

### Custom Utilities

Create reusable utility classes:

```css
@utility content-auto {
  content-visibility: auto;
}

@utility tab-* {
  tab-size: var(--tab-size-*);
}
```

```html
<div class="content-auto">Custom utility</div>
<pre class="tab-4">Custom tab size</pre>
```

### Custom Variants

```css
@custom-variant theme-midnight (&:where([data-theme="midnight"] *));
@custom-variant aria-checked (&[aria-checked="true"]);
```

```html
<div theme-midnight:bg-navy-900>
  Applies when data-theme="midnight"
</div>
```

### Layer Organization

```css
@layer base {
  h1 {
    @apply text-4xl font-bold;
  }

  body {
    @apply bg-white text-gray-900;
  }
}

@layer components {
  .btn {
    @apply px-4 py-2 rounded bg-blue-500 text-white hover:bg-blue-700;
  }

  .card {
    @apply bg-white rounded-lg shadow-md p-6;
  }
}
```

### Apply Directive

Extract repeated utilities into CSS classes:

```css
.btn-primary {
  @apply bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded;
}

.input-field {
  @apply border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500;
}
```

## Component Examples

### Button Component

```html
<!-- Primary button -->
<button class="bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white font-semibold px-6 py-3 rounded-lg shadow-md hover:shadow-lg transform hover:scale-105 transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-blue-300 disabled:opacity-50 disabled:cursor-not-allowed">
  Click me
</button>

<!-- Secondary button -->
<button class="bg-white hover:bg-gray-50 border-2 border-gray-300 text-gray-700 font-semibold px-6 py-3 rounded-lg">
  Secondary
</button>

<!-- Icon button -->
<button class="p-2 rounded-full hover:bg-gray-100 transition-colors">
  <svg class="w-6 h-6">...</svg>
</button>
```

### Card Component

```html
<div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg hover:shadow-xl transition-shadow overflow-hidden">
  <img class="w-full h-48 object-cover" src="..." alt="Card image" />
  <div class="p-6">
    <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
      Card Title
    </h3>
    <p class="text-gray-600 dark:text-gray-300 mb-4">
      Card description text goes here
    </p>
    <button class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded-lg">
      Learn More
    </button>
  </div>
</div>
```

### Form Component

```html
<form class="max-w-md mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-md p-8">
  <div class="mb-6">
    <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2" for="email">
      Email
    </label>
    <input
      type="email"
      id="email"
      class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
      placeholder="you@example.com"
    />
  </div>

  <div class="mb-6">
    <label class="block text-gray-700 dark:text-gray-300 font-semibold mb-2" for="password">
      Password
    </label>
    <input
      type="password"
      id="password"
      class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 invalid:border-red-500 dark:bg-gray-700 dark:text-white"
    />
  </div>

  <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition-colors">
    Sign In
  </button>
</form>
```

### Navigation Component

```html
<nav class="bg-white dark:bg-gray-900 shadow-md sticky top-0 z-50">
  <div class="container mx-auto px-4">
    <div class="flex items-center justify-between h-16">
      <div class="flex items-center gap-8">
        <a href="/" class="text-2xl font-bold text-blue-600">Logo</a>
        <div class="hidden md:flex gap-6">
          <a href="#" class="text-gray-700 dark:text-gray-300 hover:text-blue-600 transition-colors">Home</a>
          <a href="#" class="text-gray-700 dark:text-gray-300 hover:text-blue-600 transition-colors">About</a>
          <a href="#" class="text-gray-700 dark:text-gray-300 hover:text-blue-600 transition-colors">Services</a>
        </div>
      </div>
      <button class="md:hidden p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800">
        <svg class="w-6 h-6">...</svg>
      </button>
    </div>
  </div>
</nav>
```

### Grid Layout

```html
<div class="container mx-auto px-4 py-8">
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
    <div class="bg-white rounded-lg shadow-md p-6">Item 1</div>
    <div class="bg-white rounded-lg shadow-md p-6">Item 2</div>
    <div class="bg-white rounded-lg shadow-md p-6">Item 3</div>
    <div class="bg-white rounded-lg shadow-md p-6">Item 4</div>
  </div>
</div>
```

## Best Practices

### 1. Use Consistent Spacing Scale
```html
<!-- Good: Use spacing scale -->
<div class="p-4 mb-6">

<!-- Avoid: Arbitrary values unless necessary -->
<div class="p-[17px] mb-[23px]">
```

### 2. Leverage Design Tokens
```html
<!-- Good: Use semantic color names -->
<button class="bg-blue-600 hover:bg-blue-700">

<!-- Avoid: One-off colors -->
<button class="bg-[#3B82F6] hover:bg-[#2563EB]">
```

### 3. Mobile-First Responsive Design
```html
<!-- Good: Mobile first, then scale up -->
<div class="text-base md:text-lg lg:text-xl">

<!-- Avoid: Desktop first -->
<div class="text-xl lg:text-base">
```

### 4. Component Extraction
```javascript
// React component with Tailwind
function Button({ children, variant = 'primary' }) {
  const baseClasses = "font-semibold px-6 py-3 rounded-lg transition-colors"
  const variants = {
    primary: "bg-blue-600 hover:bg-blue-700 text-white",
    secondary: "bg-gray-200 hover:bg-gray-300 text-gray-900"
  }

  return (
    <button className={`${baseClasses} ${variants[variant]}`}>
      {children}
    </button>
  )
}
```

### 5. Use @apply for Repeated Patterns
```css
/* Only use @apply for truly repeated patterns */
@layer components {
  .card {
    @apply bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow;
  }
}
```

### 6. Accessibility First
```html
<button class="focus:outline-none focus:ring-4 focus:ring-blue-300">
  Accessible button
</button>

<a class="text-blue-600 hover:underline focus:outline-2 focus:outline-offset-2">
  Accessible link
</a>
```

### 7. Performance Optimization
- Use PurgeCSS in production (automatic with modern setup)
- Avoid dynamic class names: `class={`text-${color}-500`}` won't work
- Use safelist for dynamic classes if needed

### 8. Dark Mode Consistency
```html
<!-- Ensure all elements have dark mode variants -->
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white border border-gray-200 dark:border-gray-700">
  Complete dark mode support
</div>
```

## Common Patterns

### Centering Content
```html
<!-- Horizontal center -->
<div class="flex justify-center">Content</div>
<div class="mx-auto w-fit">Content</div>

<!-- Vertical center -->
<div class="flex items-center h-screen">Content</div>

<!-- Center both axes -->
<div class="flex items-center justify-center h-screen">
  Centered content
</div>
```

### Full-Width Container with Max Width
```html
<div class="container mx-auto px-4 max-w-7xl">
  Content with consistent max width
</div>
```

### Aspect Ratio Boxes
```html
<div class="aspect-square">Square</div>
<div class="aspect-video">16:9 video</div>
<div class="aspect-[4/3]">4:3 ratio</div>
```

### Truncate Text
```html
<p class="truncate">Long text that will be truncated with ellipsis...</p>

<p class="line-clamp-3">
  Long text that will be truncated after 3 lines with ellipsis...
</p>
```

### Smooth Scrolling
```html
<html class="scroll-smooth">
  <a href="#section">Smooth scroll to section</a>
</html>
```

## Troubleshooting

### Classes Not Working

1. **Check content configuration:**
```javascript
// tailwind.config.js
content: [
  "./src/**/*.{js,jsx,ts,tsx}",
  // Add all file paths where you use Tailwind
]
```

2. **Dynamic classes won't work:**
```javascript
// ❌ Won't work
const color = 'blue'
<div className={`text-${color}-500`} />

// ✅ Works
<div className={color === 'blue' ? 'text-blue-500' : 'text-red-500'} />
```

3. **Specificity issues:**
```css
/* Use !important sparingly */
<div class="!text-red-500">Overrides other styles</div>
```

### Build Issues

```bash
# Clear cache and rebuild
rm -rf .next node_modules/.cache
npm run dev
```

### IntelliSense Not Working

Install official extension:
- VS Code: "Tailwind CSS IntelliSense"
- Configure in `.vscode/settings.json`:

```json
{
  "tailwindCSS.experimental.classRegex": [
    ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"]
  ]
}
```

## Resources

- Official Documentation: https://tailwindcss.com/docs
- Tailwind UI Components: https://tailwindui.com
- Headless UI (unstyled components): https://headlessui.com
- Tailwind Play (online playground): https://play.tailwindcss.com
- Color Palette Generator: https://uicolors.app
- Community Components: https://tailwindcomponents.com

## Framework Integration Examples

### React
```jsx
export function Card({ title, description }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <h3 className="text-2xl font-bold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}
```

### Vue
```vue
<template>
  <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
    <h3 class="text-2xl font-bold mb-2">{{ title }}</h3>
    <p class="text-gray-600">{{ description }}</p>
  </div>
</template>

<script setup>
defineProps(['title', 'description'])
</script>
```

### Svelte
```svelte
<script>
  export let title
  export let description
</script>

<div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
  <h3 class="text-2xl font-bold mb-2">{title}</h3>
  <p class="text-gray-600">{description}</p>
</div>
```

## Implementation Checklist

When implementing Tailwind CSS:

- [ ] Install `tailwindcss` and framework-specific plugin
- [ ] Configure build tool (Vite/PostCSS/CLI)
- [ ] Set up content paths in configuration
- [ ] Import Tailwind in CSS file
- [ ] Configure custom theme tokens (if needed)
- [ ] Set up dark mode strategy
- [ ] Install VS Code IntelliSense extension
- [ ] Create reusable component patterns
- [ ] Implement responsive breakpoints
- [ ] Add accessibility focus states
- [ ] Test dark mode across all components
- [ ] Optimize for production build
- [ ] Document custom utilities and components
