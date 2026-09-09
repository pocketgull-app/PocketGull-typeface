# Fontsource Upstream Onboarding Specification for PocketGull

## Package Target: `@fontsource/pocketgull` & `@fontsource/pocketgull-mono`

This directory provides the automated packaging and onboarding assets for publishing PocketGull to [Fontsource](https://fontsource.org), the modern open-source npm font delivery platform.

### How to Submit to Fontsource
1. Fork [fontsource/fontsource](https://github.com/fontsource/fontsource).
2. Create package directory: `packages/pocketgull` and `packages/pocketgull-mono`.
3. Copy `distribution/fontsource/metadata.json` to `packages/pocketgull/metadata.json`.
4. Run `fontsource` packager CLI to generate standard CSS files and subsets.
5. Open PR: `feat: add pocketgull clinical superfamily`.

### Target Developer Usage
Once published, React, Next.js, and web developers can consume PocketGull without CDN tracking:

```bash
npm install @fontsource/pocketgull @fontsource/pocketgull-mono
```

```javascript
// In main.js / _app.js:
import "@fontsource/pocketgull/400.css"; // Fineliner
import "@fontsource/pocketgull/700.css"; // Bold Display
import "@fontsource/pocketgull-mono/400.css"; // ICU Telemetry
```
