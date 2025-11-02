# Tailwind CSS v4 Configuration

## Setup Summary

This frontend uses **Tailwind CSS v4** with the latest configuration approach.

### Configuration Files

1. **`postcss.config.mjs`** - PostCSS configuration with Tailwind plugin
2. **`app/globals.css`** - Custom theme and utility classes using `@theme inline`
3. **No `tailwind.config.js`** - V4 uses CSS-based configuration

### Key Features Implemented

#### 1. Custom Color Palette
- **Brand Colors**: Primary (blue), Secondary (purple), Accent (cyan)
- **Semantic Colors**: Success, Warning, Error, Info
- **Surface Colors**: Backgrounds, elevated surfaces, borders
- **Text Colors**: Primary, secondary, muted variants

#### 2. Dark Mode Support
- Automatic dark mode detection using `prefers-color-scheme`
- All colors adjusted for optimal dark mode contrast
- Seamless theme switching

#### 3. Design Tokens
- **Spacing Scale**: xs (8px) → 2xl (48px)
- **Border Radius**: sm (6px) → full (rounded)
- **Shadows**: sm, md, lg, xl variants
- **Typography**: System font stacks for sans and mono

#### 4. Custom Utility Classes

##### Chat Interface
- `.chat-container` - Flex container for messages
- `.chat-message` - Base message styling
- `.chat-message-user` - User message bubble
- `.chat-message-assistant` - AI response bubble

##### Buttons
- `.btn` - Base button styles
- `.btn-primary` - Primary action button
- `.btn-secondary` - Secondary action button

##### Components
- `.card` - Card component with shadow and border

#### 5. Accessibility Features
- Focus-visible styles with primary color outline
- Smooth scrolling behavior
- Optimized text selection colors
- Proper contrast ratios for WCAG compliance

#### 6. Performance Optimizations
- CSS variable-based theming (fast switching)
- Minimal CSS output
- Font smoothing for better text rendering
- Overflow control for layout stability

### Using Custom Colors

You can use the custom colors in two ways:

**1. CSS Variables:**
```css
.my-element {
  background: var(--primary);
  color: var(--text-primary);
}
```

**2. Tailwind Classes:**
```jsx
<div className="bg-primary text-white">
  Primary colored element
</div>
```

### Using Custom Utility Classes

```jsx
{/* Chat message from user */}
<div className="chat-message chat-message-user">
  Hello, how can I help?
</div>

{/* Chat message from AI */}
<div className="chat-message chat-message-assistant">
  I'm here to assist you!
</div>

{/* Button components */}
<button className="btn btn-primary">
  Primary Action
</button>

<button className="btn btn-secondary">
  Secondary Action
</button>

{/* Card component */}
<div className="card">
  Card content here
</div>
```

### Standard Tailwind Classes

All standard Tailwind classes work as expected:

```jsx
<div className="flex items-center justify-center p-4 rounded-lg shadow-md">
  <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
    Welcome to Customer Service AI
  </h1>
</div>
```

### Development Workflow

1. **Development Server**: 
   ```bash
   npm run dev
   # or
   pnpm dev
   ```

2. **Build for Production**:
   ```bash
   npm run build
   # or
   pnpm build
   ```

3. **Type Checking**:
   ```bash
   npx tsc --noEmit
   ```

### Verification Checklist

- ✅ Tailwind CSS v4 installed
- ✅ PostCSS configured with @tailwindcss/postcss
- ✅ Custom theme with CSS variables
- ✅ Dark mode support
- ✅ Custom utility classes for chat interface
- ✅ Button variants
- ✅ Card component
- ✅ Accessibility features
- ✅ TypeScript compilation passes
- ✅ Design tokens documented

### Tailwind CSS v4 Differences from v3

If you're familiar with Tailwind v3, note these key changes in v4:

1. **No config file needed** - Use `@theme inline` in CSS
2. **CSS-first configuration** - Define design tokens in CSS
3. **Better performance** - Faster build times
4. **Simplified setup** - Less JavaScript configuration
5. **CSS variables** - More dynamic theming capabilities

### Next Steps

1. Use custom colors and utility classes in components
2. Add more custom components as needed
3. Extend the theme with project-specific design tokens
4. Create reusable component library

---

**Version**: Tailwind CSS v4  
**Last Updated**: November 2, 2025  
**Status**: ✅ Verified and Working

