# Security Policy

At **PocketGull**, security, cryptographic determinism, and typography asset integrity are foundational. We adhere to **OpenSSF (Open Source Security Foundation)** standards and treat font binary compilation, glyph parsing safety, and supply chain provenance as safety-critical engineering disciplines.

## Supported Versions (Semantic Versioning 2.0.0)

We follow strict Semantic Versioning (`MAJOR.MINOR.PATCH`). Active production releases receive full security and typographic maintenance updates.

| Version | Supported          | Status |
| :--- | :---: | :--- |
| **2.0.x** | :white_check_mark: | **Active Production Superfamily Release (Google Fonts Standard)** |
| 1.0.x | :white_check_mark: | Critical security patches only |
| < 1.0.0 | :x: | Deprecated / End-of-Life |

---

## Reporting a Vulnerability

If you discover a security vulnerability, memory corruption risk, buffer handling flaw, or malicious font binary condition within PocketGull Typeface, please do **not** disclose it publicly.

Please report vulnerabilities through our coordinated private disclosure channels:

1. **GitHub Private Vulnerability Reporting (Preferred)**:
   [Submit a Private Advisory via GitHub Security](https://github.com/pocketgull-app/PocketGull-typeface/security/advisories/new)
2. **Security & Data Protection Officer**:
   Send details to **dpo@pocketgull.app** or **philgear@gmail.com**.

### Response Timeline
* **Initial Acknowledgement**: Within **24–48 hours**.
* **Triage & Reproduction**: Within **3 business days**.
* **Remediation & Patch Release**: Within **7 business days**, accompanied by a cryptographically signed GitHub Release with SHA-256 binary manifests.

---

## OpenSSF Supply Chain & Font Binary Security Standards

1. **W3C OpenType Sanitizer (OTS) Pre-Flight Hardening**:
   All font binaries (`.ttf`, `.woff2`) MUST achieve 100% pass rates across W3C OTS validation prior to release, ensuring zero buffer overruns or malformed table boundaries in client browsers.
2. **Strict 2-Byte Word-Boundary Alignment**:
   All TrueType `.glyf` records are padded to strict 2-byte word boundaries (`loca[i] % 2 == 0`) and table checksum adjustments are cryptographically recomputed (`0xB1B0AFBA - fontChecksum`).
3. **Zero Executable Code Injection (Names & Postscript Tables)**:
   Font name tables (`nameID 0–25`) and PostScript strings are sanitized of non-printable control characters, zero-width Unicode vectors, and script execution triggers.
4. **Deterministic OpenType Compilation**:
   Binaries are compiled with deterministic timestamps (`SOURCE_DATE_EPOCH=1700000000`) to guarantee reproducible builds and verifiable artifact digests.
5. **Zero Secret & Zero Telemetry Invariant**:
   Font binaries and the interactive web specimen contain zero analytics scripts, zero tracking pixels, and zero outbound network egress.
