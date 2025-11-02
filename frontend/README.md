# Customer Service AI - Frontend

The frontend application for the Advanced Multi-Agent Customer Service AI system. Built with Next.js 16, TypeScript, and Tailwind CSS.

## Overview

This Next.js application provides the user interface for interacting with our multi-agent AI customer service system. It handles technical support, billing inquiries, and compliance questions through specialized AI agents powered by LangChain v1.0+ and LangGraph.

## Tech Stack

- **Framework**: Next.js 16 with App Router
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 4
- **UI Components**: shadcn/ui (to be added)
- **Package Manager**: pnpm
- **Linting**: ESLint 9 (flat config)
- **Fonts**: Geist Sans & Geist Mono (via next/font)

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js**: v20 or higher
- **pnpm**: v9 or higher (recommended) or npm/yarn
  ```bash
  npm install -g pnpm
  ```

## Project Structure

```
frontend/
├── app/                      # Next.js App Router
│   ├── favicon.ico          # Site favicon
│   ├── globals.css          # Global styles and Tailwind directives
│   ├── layout.tsx           # Root layout with metadata
│   └── page.tsx             # Home page component
├── components/              # React components
│   ├── ui/                  # shadcn/ui components (to be added)
│   └── README.md            # Component documentation
├── lib/                     # Utility libraries
│   ├── utils/               # Helper functions
│   │   └── cn.ts           # Tailwind class name utility
│   └── README.md            # Library documentation
├── public/                  # Static assets
│   ├── *.svg               # SVG icons and graphics
│   └── ...
├── .env.example            # Environment variable template
├── eslint.config.mjs       # ESLint configuration (v9 flat config)
├── next.config.ts          # Next.js configuration
├── package.json            # Dependencies and scripts
├── postcss.config.mjs      # PostCSS configuration for Tailwind
├── tailwind.config.js      # Tailwind CSS configuration
└── tsconfig.json           # TypeScript configuration
```

## Getting Started

### 1. Install Dependencies

```bash
cd frontend
pnpm install
```

### 2. Configure Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```bash
cp .env.example .env.local
```

Edit `.env.local` and set the required variables:

```bash
# Backend API URL (default for local development)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start the Development Server

```bash
pnpm dev
```

The application will be available at [http://localhost:3000](http://localhost:3000).

## Available Scripts

| Command | Description |
|---------|-------------|
| `pnpm dev` | Start development server on port 3000 |
| `pnpm build` | Create production build |
| `pnpm start` | Start production server (requires `pnpm build` first) |
| `pnpm lint` | Run ESLint to check code quality |

## Development

### Hot Reloading

The development server supports Fast Refresh. Changes to files will automatically reload in the browser:

- **Pages**: Edit files in `app/` directory
- **Components**: Edit files in `components/` directory
- **Styles**: Edit `app/globals.css` or component-level styles

### Code Quality

#### ESLint

This project uses ESLint v9 with a flat config format. The configuration includes:

- TypeScript-specific rules
- React and React Hooks best practices
- Next.js optimizations (Image, Link components)
- Accessibility (jsx-a11y) rules
- Code quality enforcement

Run linting:

```bash
pnpm lint
```

#### TypeScript

TypeScript is configured with strict mode enabled. Key features:

- Path aliases (`@/*` maps to `./`)
- Strict type checking
- Module resolution: Bundler
- JSX: Preserve (handled by Next.js)

Check types:

```bash
pnpm build
```

### Styling with Tailwind CSS

This project uses Tailwind CSS v4 for styling:

```tsx
// Example: Using Tailwind classes
export default function MyComponent() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <h1 className="text-4xl font-bold text-blue-600">Hello World</h1>
    </div>
  );
}
```

The `cn()` utility from `lib/utils/cn.ts` helps with conditional class names:

```tsx
import { cn } from "@/lib/utils/cn";

<div className={cn(
  "base-classes",
  isActive && "active-classes",
  "more-classes"
)} />
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000` |

**Note**: Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.

## Building for Production

### Create Production Build

```bash
pnpm build
```

This command:
1. Type-checks the entire codebase
2. Lints all files
3. Creates optimized production bundles
4. Generates static pages where possible

### Start Production Server

```bash
pnpm start
```

The production server will start on port 3000.

## Key Features

### Current Implementation

- ✅ **Next.js 16 App Router**: Modern file-based routing
- ✅ **TypeScript**: Full type safety
- ✅ **Tailwind CSS**: Utility-first styling
- ✅ **Responsive Design**: Mobile-first approach
- ✅ **Dark Mode Support**: System preference detection
- ✅ **SEO Optimized**: Meta tags, Open Graph, Twitter cards
- ✅ **Accessibility**: ARIA attributes and semantic HTML

### Coming Soon (Per Phase Development)

- 🔄 **Chat Interface**: Real-time conversation UI
- 🔄 **Agent Indicators**: Visual feedback for active agents
- 🔄 **Streaming Responses**: Token-by-token display
- 🔄 **Session Management**: Conversation history
- 🔄 **Error Handling**: User-friendly error messages

## Troubleshooting

### Port Already in Use

If port 3000 is already in use:

```bash
# Use a different port
pnpm dev -- -p 3001
```

### Module Not Found Errors

Clear Next.js cache and reinstall dependencies:

```bash
rm -rf .next node_modules
pnpm install
pnpm dev
```

### TypeScript Errors

Regenerate TypeScript definitions:

```bash
rm -rf .next
pnpm dev
```

### Styling Not Working

Ensure Tailwind is properly configured and rebuild:

```bash
pnpm build
```

## Learn More

### Next.js Resources

- [Next.js Documentation](https://nextjs.org/docs) - Learn about Next.js features and API
- [Next.js App Router](https://nextjs.org/docs/app) - Deep dive into App Router
- [Learn Next.js](https://nextjs.org/learn) - Interactive Next.js tutorial

### TypeScript Resources

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [TypeScript with Next.js](https://nextjs.org/docs/app/building-your-application/configuring/typescript)

### Tailwind CSS Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Tailwind CSS with Next.js](https://tailwindcss.com/docs/guides/nextjs)

## Contributing

See the root [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

## License

This project is part of the ASU VibeCoding curriculum.

---

**Built with ❤️ by the ASU VibeCoding Team**
