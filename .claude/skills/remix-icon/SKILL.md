---
name: remix-icon
description: Guide for implementing RemixIcon - an open-source neutral-style icon library with 3,100+ icons in outlined and filled styles. Use when adding icons to applications, building UI components, or designing interfaces. Supports webfonts, SVG, React, Vue, and direct integration.
---

# RemixIcon Implementation Guide

RemixIcon is a comprehensive icon library with **3,100+ meticulously designed icons** available in both outlined (`-line`) and filled (`-fill`) styles. All icons are built on a 24x24 pixel grid for perfect alignment and consistency.

## When to Use This Skill

Use RemixIcon when:
- Adding icons to web applications, mobile apps, or design systems
- Building UI components that need consistent iconography
- Implementing navigation, buttons, status indicators, or media controls
- Creating presentations, documents, or design mockups
- Need bilingual icon search (English + Chinese)
- Require both outlined and filled icon variants

## Quick Start

### Installation

**NPM (recommended for web projects):**
```bash
npm install remixicon
# or
yarn add remixicon
# or
pnpm install remixicon
```

**CDN (no installation):**
```html
<link
    href="https://cdn.jsdelivr.net/npm/remixicon@4.7.0/fonts/remixicon.css"
    rel="stylesheet"
/>
```

**React:**
```bash
npm install @remixicon/react
```

**Vue 3:**
```bash
npm install @remixicon/vue
```

## Icon Naming Convention

**Pattern:** `ri-{icon-name}-{style}`

Where:
- `icon-name`: Descriptive name in kebab-case (e.g., `arrow-right`, `home`, `user-add`)
- `style`: Either `line` (outlined) or `fill` (filled)

**Examples:**
```
ri-home-line           # Home icon, outlined
ri-home-fill           # Home icon, filled
ri-arrow-right-line    # Right arrow, outlined
ri-search-line         # Search icon, outlined
ri-heart-fill          # Heart icon, filled
```

## Usage Patterns

### 1. Webfont (HTML/CSS)

**Basic usage:**
```html
<i class="ri-admin-line"></i>
<i class="ri-home-fill"></i>
```

**With sizing classes:**
```html
<i class="ri-home-line ri-2x"></i>      <!-- 2em size -->
<i class="ri-search-line ri-lg"></i>    <!-- 1.3333em -->
<i class="ri-heart-fill ri-xl"></i>     <!-- 1.5em -->
```

**Available size classes:**
- `ri-xxs` (0.5em)
- `ri-xs` (0.75em)
- `ri-sm` (0.875em)
- `ri-1x` (1em)
- `ri-lg` (1.3333em)
- `ri-xl` (1.5em)
- `ri-2x` through `ri-10x` (2em - 10em)
- `ri-fw` (fixed width for alignment)

### 2. Direct SVG

**Download and use:**
```html
<img height="32" width="32" src="path/to/admin-fill.svg" />
```

**Inline SVG:**
```html
<svg viewBox="0 0 24 24" fill="currentColor">
  <path d="...icon path data..."/>
</svg>
```

### 3. SVG Sprite

```html
<svg class="remix-icon">
    <use xlink:href="path/to/remixicon.symbol.svg#ri-admin-fill"></use>
</svg>
```

```css
.remix-icon {
    width: 24px;
    height: 24px;
    fill: #333;
}
```

### 4. React Integration

```jsx
import { RiHeartFill, RiHomeLine, RiSearchLine } from "@remixicon/react";

function MyComponent() {
    return (
        <>
            <RiHeartFill
                size={36}              // Custom size
                color="red"            // Fill color
                className="my-icon"    // Custom class
            />
            <RiHomeLine size={24} />
            <RiSearchLine size="1.5em" color="#666" />
        </>
    );
}
```

### 5. Vue 3 Integration

```vue
<script setup lang="ts">
import { RiHeartFill, RiHomeLine } from "@remixicon/vue";
</script>

<template>
    <RiHeartFill size="36px" color="red" className="my-icon" />
    <RiHomeLine size="24px" />
</template>
```

## Icon Categories

Icons are organized into **20 semantic categories**:

| Category | Examples | Use Cases |
|----------|----------|-----------|
| **Arrows** | arrow-left, arrow-up, corner-up-left | Navigation, directions, flows |
| **Buildings** | home, bank, hospital, store | Locations, facilities |
| **Business** | briefcase, archive, pie-chart | Commerce, analytics |
| **Communication** | chat, phone, mail, message | Messaging, contact |
| **Design** | brush, palette, magic, crop | Creative tools |
| **Development** | code, terminal, bug, git-branch | Developer tools |
| **Device** | phone, laptop, tablet, printer | Hardware, electronics |
| **Document** | file, folder, article, draft | Files, content |
| **Editor** | bold, italic, link, list | Text formatting |
| **Finance** | money, wallet, bank-card, coin | Payments, transactions |
| **Food** | restaurant, cake, cup, knife | Dining, beverages |
| **Health & Medical** | health, heart-pulse, capsule | Healthcare, wellness |
| **Logos** | github, twitter, facebook | Brand icons |
| **Map** | map, pin, compass, navigation | Location, directions |
| **Media** | play, pause, volume, camera | Multimedia controls |
| **System** | settings, download, delete, add | UI controls, actions |
| **User & Faces** | user, account, team, contacts | Profiles, people |
| **Weather** | sun, cloud, rain, moon | Climate, forecast |
| **Others** | miscellaneous icons | General purpose |

## Finding Icons

### 1. Browse by Category
Visit https://remixicon.com and navigate categories to visually browse icons.

### 2. Search with Keywords
Use English or Chinese keywords. Icons have comprehensive tags for discoverability.

**Example searches:**
- "home" → home, home-2, home-3, home-gear, home-wifi
- "arrow" → arrow-left, arrow-right, arrow-up, arrow-down
- "user" → user, user-add, user-follow, account-circle

### 3. Consider Icon Variants
Many icons have numbered variants (home, home-2, home-3) offering stylistic alternatives.

## Best Practices

### Choosing Styles

**Line (Outlined) Style:**
- Use for: Clean, minimal interfaces
- Best with: Light backgrounds, high contrast needs
- Examples: Navigation menus, toolbars, forms

**Fill (Filled) Style:**
- Use for: Emphasis, active states, primary actions
- Best with: Buttons, selected items, important indicators
- Examples: Active nav items, primary CTAs, notifications

### Accessibility

**Always provide aria-labels for icon-only elements:**
```html
<button aria-label="Search">
    <i class="ri-search-line"></i>
</button>
```

**For decorative icons, use aria-hidden:**
```html
<span aria-hidden="true">
    <i class="ri-star-fill"></i>
</span>
```

### Performance

**For web applications:**
- Use webfonts (WOFF2: 179KB) for multiple icons
- Use individual SVGs for 1-5 icons only
- Use SVG sprites for 5-20 icons
- Prefer CDN for faster global delivery

**Font formats by size (smallest to largest):**
1. WOFF2: 179KB (recommended)
2. WOFF: 245KB
3. TTF: 579KB
4. EOT: 579KB (legacy IE support)

### Color and Sizing

**Use currentColor for flexibility:**
```css
.icon {
    color: #333;  /* Icon inherits this color */
}
```

**Maintain 24x24 grid alignment:**
```css
/* Good - maintains grid */
.icon { font-size: 24px; }
.icon { font-size: 48px; }  /* 24 * 2 */

/* Avoid - breaks grid alignment */
.icon { font-size: 20px; }
.icon { font-size: 30px; }
```

### Framework Integration

**Next.js:**
```jsx
import '@/styles/remixicon.css';  // In _app.js or layout
import { RiHomeLine } from "@remixicon/react";
```

**Tailwind CSS:**
```html
<i class="ri-home-line text-2xl text-blue-500"></i>
```

**CSS Modules:**
```jsx
import styles from './component.module.css';
import 'remixicon/fonts/remixicon.css';

<i className={`ri-home-line ${styles.icon}`}></i>
```

## Advanced Usage

### Custom Icon Sizing with CSS

```css
.custom-icon {
    font-size: 32px;
    line-height: 1;
    vertical-align: middle;
}

/* Responsive sizing */
@media (max-width: 768px) {
    .custom-icon {
        font-size: 24px;
    }
}
```

### Icon Animations

```css
.spinning-icon {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
```

### Dynamic Icons in React

```jsx
function IconButton({ iconName, filled = false }) {
    const iconClass = `ri-${iconName}-${filled ? 'fill' : 'line'}`;
    return <i className={iconClass} />;
}

// Usage
<IconButton iconName="home" />
<IconButton iconName="heart" filled />
```

## Design Tool Integration

### Figma Plugin
Install the official RemixIcon plugin for Figma:
- **Plugin:** RemixIcon
- **URL:** https://www.figma.com/community/plugin/1089569154784319246/remixicon
- **Feature:** Direct icon access within Figma workspace

### Copy to Design Tools
Icons can be directly copied from https://remixicon.com to:
- Sketch
- Figma (without plugin)
- Adobe XD
- Adobe Illustrator

### PowerPoint & Keynote
Use RemixIcon-Slides for direct integration:
- **Repository:** https://github.com/Remix-Design/RemixIcon-Slides
- **Feature:** Edit icon styles directly in presentations

## Common Patterns

### Navigation Menu
```html
<nav>
    <a href="/home">
        <i class="ri-home-line"></i>
        <span>Home</span>
    </a>
    <a href="/search">
        <i class="ri-search-line"></i>
        <span>Search</span>
    </a>
    <a href="/profile">
        <i class="ri-user-line"></i>
        <span>Profile</span>
    </a>
</nav>
```

### Button with Icon
```html
<button class="btn-primary">
    <i class="ri-download-line"></i>
    Download
</button>
```

### Status Indicators
```jsx
// React example
function StatusIcon({ status }) {
    const icons = {
        success: <RiCheckboxCircleFill color="green" />,
        error: <RiErrorWarningFill color="red" />,
        warning: <RiAlertFill color="orange" />,
        info: <RiInformationFill color="blue" />
    };
    return icons[status];
}
```

### Input with Icon
```html
<div class="input-group">
    <i class="ri-search-line"></i>
    <input type="text" placeholder="Search..." />
</div>
```

## Troubleshooting

### Icons not displaying

**Check:**
1. CSS file is loaded: `<link href="remixicon.css" rel="stylesheet" />`
2. Class name syntax: `ri-{name}-{style}` (e.g., `ri-home-line`)
3. Font files are accessible (check browser Network tab)
4. No font-family override conflicting with `.ri-*` classes

### Wrong icon size

**Solutions:**
- Use size classes: `ri-lg`, `ri-2x`, etc.
- Set parent `font-size` property
- Ensure `line-height: 1` for proper alignment
- Use `vertical-align: middle` if needed

### Icons look blurry

**Causes:**
- Non-integer font sizes breaking pixel grid
- Browser zoom levels
- Transform properties causing subpixel rendering

**Fix:** Use multiples of 24px (24, 48, 72, 96) for crisp rendering

## Resources

- **Website:** https://remixicon.com
- **GitHub:** https://github.com/Remix-Design/RemixIcon
- **NPM:** https://www.npmjs.com/package/remixicon
- **React Package:** @remixicon/react
- **Vue Package:** @remixicon/vue
- **License:** Apache 2.0 (free for personal and commercial use)
- **Total Icons:** 3,100+
- **Current Version:** 4.7.0

## Support

- **Issues:** https://github.com/Remix-Design/RemixIcon/issues
- **Email:** jimmy@remixdesign.cn
- **Twitter/X:** @RemixDesignHQ

## Version History

- **v4.7.0** (Latest): 3,100+ icons with React and Vue packages
- Full changelog available on GitHub releases
