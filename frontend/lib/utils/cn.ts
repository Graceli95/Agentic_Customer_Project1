/**
 * Utility for conditionally joining classNames together
 * Useful for combining Tailwind CSS classes with conditional logic
 * 
 * @example
 * ```tsx
 * <div className={cn('base-class', isActive && 'active-class', 'another-class')}>
 *   Content
 * </div>
 * ```
 */

type ClassValue = string | number | boolean | undefined | null;
type ClassArray = ClassValue[];
type ClassDictionary = Record<string, boolean>;
type ClassInput = ClassValue | ClassArray | ClassDictionary;

/**
 * Combines multiple class names into a single string
 * Filters out falsy values automatically
 */
export function cn(...inputs: ClassInput[]): string {
  const classes: string[] = [];

  for (const input of inputs) {
    if (!input) {
      continue;
    }

    if (typeof input === 'string' || typeof input === 'number') {
      classes.push(String(input));
    } else if (Array.isArray(input)) {
      const result = cn(...input);
      if (result) {
        classes.push(result);
      }
    } else if (typeof input === 'object') {
      for (const key in input) {
        if (input[key]) {
          classes.push(key);
        }
      }
    }
  }

  return classes.join(' ');
}

/**
 * Alternative: If you want to use the popular `clsx` or `classnames` library:
 * 
 * 1. Install: `pnpm add clsx`
 * 2. Import and export: `export { clsx as cn } from 'clsx';`
 * 
 * Or with tailwind-merge for better Tailwind class handling:
 * 
 * 1. Install: `pnpm add clsx tailwind-merge`
 * 2. Create this utility:
 * ```ts
 * import { clsx, type ClassValue } from 'clsx';
 * import { twMerge } from 'tailwind-merge';
 * 
 * export function cn(...inputs: ClassValue[]) {
 *   return twMerge(clsx(inputs));
 * }
 * ```
 */

