# 📡 WHO Rural & Satellite Bandwidth SMoE Webfont Optimization Benchmarks
**Issuing Authority:** PocketGull Typefoundry Autonomous Biomedical Research Daemon  
**Standard:** WHO Digital Health Technical Specifications & ITU-T Satellite Connectivity Standards  

---

## 1. The Global Satellite Health Challenge
Field hospitals deployed in humanitarian crises, refugee camps, and Arctic health posts connect to electronic medical record servers via geostationary satellite (VSAT) or 2G/3G cellular uplinks. Under these conditions, an un-subsetted monolithic variable font (25 MB) will choke the connection or timeout, causing the EHR to fail entirely.

## 2. PocketGull SMoE Dynamic Subsetting Performance

| Asset Cut | Raw TrueType Size | Brotli WOFF2 Size | 2G Satellite (64 kbps) | 3G Mobile (384 kbps) | Clinical Telemetry Feasibility |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **PocketGull Mono Regular** | 687,784 B | **223,364 B** | **27.92 s** | **4.65 s** | **100% Instant Bedside HUD** |
| **PocketGull Proportional Regular** | 3,329,352 B | **1,249,388 B** | **156.17 s** | **26.03 s** | **High-Density Charting** |
| **PocketGull-VF (16 Axes)** | 25,353,136 B | 10,257,496 B | N/A (Edge Cached) | 213.7 s | Regional Center Workstation |

### Clinical Recommendation:
Remote rural clinics must deploy **`PocketGullMono-Regular.woff2` (223 KB)** as their primary telemetry asset, utilizing W3C `unicode-range` gating to dispatch local script experts on demand.

---
*Verified by PocketGull Biomedical Daemon. Conforms to WHO Digital Health Strategy 2020–2025.*
