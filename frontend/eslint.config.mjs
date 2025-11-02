/**
 * ESLint Configuration for Customer Service AI Frontend
 *
 * This configuration extends Next.js recommended settings with:
 * - TypeScript strict rules with sensible defaults
 * - React and React Hooks best practices
 * - Next.js-specific optimizations (Image, Link components)
 * - Code quality rules (no-console, prefer-const, etc.)
 * - Accessibility (jsx-a11y) rules for inclusive design
 *
 * Using ESLint v9 flat config format.
 */

import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
    // Additional ignores for this project:
    "node_modules/**",
    "pnpm-lock.yaml",
    "*.config.ts",
    "*.config.js",
    "*.config.mjs",
    ".env*",
    "tsconfig.json",
    "tsconfig.tsbuildinfo",
  ]),
  {
    rules: {
      // TypeScript-specific rules
      "@typescript-eslint/no-unused-vars": [
        "error",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
          caughtErrorsIgnorePattern: "^_",
        },
      ],
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/explicit-function-return-type": "off",
      "@typescript-eslint/explicit-module-boundary-types": "off",
      "@typescript-eslint/no-non-null-assertion": "warn",

      // React-specific rules
      "react/react-in-jsx-scope": "off", // Not needed in Next.js
      "react/prop-types": "off", // TypeScript handles this
      "react/display-name": "warn",
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",

      // Next.js-specific rules
      "@next/next/no-html-link-for-pages": "error",
      "@next/next/no-img-element": "warn", // Encourage use of next/image

      // Code quality rules
      "no-console": ["warn", { allow: ["warn", "error"] }],
      "no-debugger": "warn",
      "prefer-const": "error",
      "no-var": "error",
      "eqeqeq": ["error", "always"],
      "curly": ["error", "all"],
      "no-throw-literal": "error",

      // Accessibility rules
      "jsx-a11y/alt-text": "warn",
      "jsx-a11y/anchor-is-valid": "warn",
      "jsx-a11y/aria-props": "warn",
      "jsx-a11y/aria-proptypes": "warn",
      "jsx-a11y/aria-unsupported-elements": "warn",
      "jsx-a11y/role-has-required-aria-props": "warn",
      "jsx-a11y/role-supports-aria-props": "warn",
    },
  },
]);

export default eslintConfig;
