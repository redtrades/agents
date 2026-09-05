# Security & Compliance Analysis: Govcon-Factory Swarm
**Persona:** Security/Compliance  
**Model:** ox-alpha  
**Date:** 2026-08-25  

## 1. Diagnosis

### 1.1 Secrets Management
*   **Current State:** Secrets (govconapi.env, SAM keys) live in `credentials/`, which is correctly `.gitignore`'d. However, there is no formal mechanism for **rotation** (e.g., SAM.gov/DSBS keys) or **encryption at rest** for these local files.
*   **Risk:** Exposure via accidental `git add -f` (though hooks exist) or local system compromise.
*   **Gap:** No automated secrets scanning in the CI pipeline (`.github/workflows/ci.yml`) beyond a custom `scripts/hooks/pre-commit` script.

### 1.2 Data Handling & PII
*   **PII Leakage:** `runs/` directories contain `trace.json` and envelope files which store UEIs, firm names, and—critically—contact person names/emails/phones from S4 (DSBS).
*   **GDPR/CCPA:** While firms are entities, the `PrimaryContactFullname`, `Email`, and `Phone` fields in `operations/data/sbs/` (14,979 records) constitute PII. Currently, no data retention policy or automated cleanup exists for stale `runs/`.
*   **Snapshot Hygiene:** The `govcon-factory` skill warns against committing `email`/`phone`/`contact_person`, but the `factory/` code (e.g., `ingest_sbs.py`) does not explicitly strip these before persisting to `runs/`.

### 1.3 Audit Trail & SOP Adherence
*   **Audit Strength:** The `factory/factory.db` (SQLite) and `trace.json` provide excellent traceability for stage-to-stage transforms.
*   **Gate Enforcement:** `factory/gates/registry.py` implements the `SOP-DELIVERABLES.md` G1 (Compliance) and G4 (Format) gates, but G3 (Eligibility) is currently missing a robust automated implementation for "SBA Small Business Search (SBS/DSBS) outage resilience" (SOP §2.4 G3d).
*   **SOP-DELIVERABLES.md Gate Enforcement:** The `value` gate in `factory/gates/registry.py` is a strong start, but it relies on string matching which can be bypassed by "slop" that mimics the required structure without providing real intelligence.

### 1.4 Supply Chain & Supplier Risk
*   **Dependencies:** The stack (requests, pyyaml, pypdf) is standard but lacks an automated vulnerability scanner (e.g., `safety` or `pip-audit`).
*   **Upstream Risk:** High reliance on `govconapi` and undocumented `DSBS` internal endpoints. If these schemas change or go down, the "fail-closed" rule 2 stops production.

---

## 2. Proposals

### 2.1 Secrets & CI Hardening
*   **Secret Rotation Script:** Implement `scripts/rotate-keys.sh` to automate SAM.gov and govconapi key rotation and update `credentials/*.env`.
*   **CI Scanning:** Add `trufflehog` or `gitleaks` to `.github/workflows/ci.yml` to prevent credential leakage in `research/` or `proposals/`.
*   **Repo Path:** `.github/workflows/ci.yml`, `scripts/rotate-keys.sh`

### 2.2 PII Redaction & Data Retention
*   **Envelope Sanitizer:** Modify `factory/envelope.py` to include a `redact()` method that strips PII fields (Email, Phone) before writing to `runs/` for demo/research purposes.
*   **Retention Policy:** Add `scripts/cleanup-runs.sh` to purge `runs/` older than 30 days (excluding those marked as `golden-set`).
*   **Repo Path:** `factory/envelope.py`, `scripts/cleanup-runs.sh`, `factory/runner.py`

### 2.3 Automated Eligibility (G3) & Compliance
*   **Eligibility Gate:** Implement the full G3 eligibility check in `factory/gates/registry.py`, including the "SBS degradation rule" (SOP §2.4 G3d) to check `data/sbs_manual_*.png` if the API fails.
*   **Audit Logging:** Enhance `factory/runner.py` to log the `agent_id` and `prompt_version` for all stages where `produced_by.kind == "agent"`.
*   **Repo Path:** `factory/gates/registry.py`, `factory/runner.py`

### 2.4 Supplier/Dependency Audit
*   **Vulnerability Scanning:** Add `pip-audit` to the CI workflow to monitor the supply chain (pypdf, requests, etc.).
*   **Repo Path:** `.github/workflows/ci.yml`, `pytest.ini`

---

## 3. Prioritization

| Priority | Task | Impact | Effort |
| :--- | :--- | :--- | :--- |
| **P0** | Automated G3 Eligibility Gate (Fail-Closed) | High (Legal/Compliance) | Medium |
| **P0** | CI Secrets Scanning (Gitleaks/Trufflehog) | High (Security) | Low |
| **P1** | PII Redaction in Envelopes/Traces | High (Privacy) | Medium |
| **P1** | Data Retention Policy (30-day purge) | Medium (Compliance) | Low |
| **P2** | Secret Rotation Script | Medium (Security) | Medium |
| **P2** | Dependency Vulnerability Scanning | Low (Security) | Low |

---

## 4. Risks & Dependencies
*   **Dependency:** Implementation of G3 depends on the `SBS/DSBS` profile API stability (`recipes/sbs-search.md`).
*   **Risk:** PII redaction might break the `provenance` gate if the gate expects verbatim matches that have been stripped. The sanitizer must run *after* gate verification but *before* final disk write for non-local storage.
*   **Risk:** Automated rotation for SAM.gov keys is limited by the upstream API's own rotation interface (usually manual web UI).
