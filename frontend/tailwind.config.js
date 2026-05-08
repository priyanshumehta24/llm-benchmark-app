/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: "var(--color-bg-val)",
        surface: "var(--color-surface-val)",
        "surface-2": "var(--color-surface-2-val)",
        "surface-offset": "var(--color-surface-offset-val)",
        divider: "var(--color-divider-val)",
        border: "var(--color-border-val)",
        text: "var(--color-text-val)",
        "text-muted": "var(--color-text-muted-val)",
        "text-faint": "var(--color-text-faint-val)",
        primary: "var(--color-primary-val)",
        "primary-hover": "var(--color-primary-hover-val)",
        "primary-active": "var(--color-primary-active-val)",
        "primary-highlight": "var(--color-primary-highlight-val)",
        amber: "var(--color-amber-val)",
        "amber-hover": "var(--color-amber-hover-val)",
        "amber-highlight": "var(--color-amber-highlight-val)",
        violet: "var(--color-violet-val)",
        "violet-hover": "var(--color-violet-hover-val)",
        "violet-highlight": "var(--color-violet-highlight-val)",
        success: "var(--color-success-val)",
        "success-highlight": "var(--color-success-highlight-val)",
        error: "var(--color-error-val)",
        "error-highlight": "var(--color-error-highlight-val)",
      },
      fontFamily: {
        display: ['"Space Grotesk"', '"Inter"', "sans-serif"],
        body: ['"Inter"', '"DM Sans"', "sans-serif"],
        mono: ['"JetBrains Mono"', '"Fira Code"', "monospace"],
      },
      borderRadius: {
        sm: "var(--radius-sm-val)",
        md: "var(--radius-md-val)",
        lg: "var(--radius-lg-val)",
        xl: "var(--radius-xl-val)",
        full: "var(--radius-full-val)",
      }
    },
  },
  plugins: [],
}
