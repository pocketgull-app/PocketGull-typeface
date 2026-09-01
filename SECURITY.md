# Security Policy

At **PocketGull**, security, mathematical precision, and typography asset integrity are foundational. We take font parsing safety, binary determinism, and supply chain provenance seriously.

## Supported Versions

Only the latest master branch and active production release artifacts receive security and typographic maintenance updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0.0 | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, buffer handling flaw, or malicious font binary risk within PocketGull Typeface, please do **not** disclose it publicly.

Please report vulnerabilities using one of our private channels:

1. **GitHub Private Vulnerability Reporting (Preferred)**:
   [Submit a Private Advisory](https://github.com/pocketgull-app/PocketGull-typeface/security/advisories/new)
2. **Security & Data Protection Officer**:
   Send encrypted details to **dpo@pocketgull.app** or **philgear@gmail.com**.

We acknowledge all vulnerability submissions within **24–48 hours** and commit to releasing patched binaries with cryptographic SHA-256 validation receipts.

---

## Supply Chain & Font Binary Security Standards

1. **Deterministic OpenType Compilation**:
   - All font binaries (.ttf, .woff2) are compiled from sanitized vector sources using deterministic timestamps (1700000000) and verified SHA-256 hashes to prevent binary injection.
2. **Safe OpenType Parsing & Memory Safety**:
   - Compilers and test runners strictly pin dependencies to patched libraries (e.g. onttools >= 4.60.2, pytest >= 9.0.3) to prevent arbitrary file writes and XML injection.
3. **Zero Secret & Zero Telemetry Invariant**:
   - The font binaries and web specimen contain zero tracking pixels, telemetry scripts, or network egress hooks.
