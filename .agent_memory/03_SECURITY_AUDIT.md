# CogniCare: Security Audit & Vulnerability Assessment

## 1. Automated Secret & Credential Scan

- **Scan Methodology**: Regex and Shannon entropy scanning performed across all project source files, configuration manifests, and scripts.
- **Findings**:
  - AWS Access Keys: **0 found**
  - GitHub Personal Access Tokens: **0 found**
  - Private Key Blocks: **0 found**
  - Live API Keys / Secrets: **0 found**
  - Hardcoded production credentials: **None**. Development secret defaults are documented with clear substitution notices in `.env.example`.
- **Environment Exclusions**: Root `.gitignore` correctly filters `.env`, `.env.*.local`, `.venv`, and SQLite databases.

---

## 2. OWASP Top 10 Assessment Matrix

| OWASP Category | Finding | Remediation Applied | Status |
|---|---|---|---|
| **A01: Broken Access Control** | Potential multi-tenant data leaks | Implemented strict relationship checks in `PatientService` & `CareService`. Unauthorized requests return HTTP 403 Forbidden. | **PASSED** |
| **A02: Cryptographic Failures** | Weak password hashing risks | Passwords hashed using BCrypt with 12 rounds. JWT signed with HMAC-SHA256 and configurable `SECRET_KEY`. | **PASSED** |
| **A03: Injection** | SQL / Command / Script Injection | 100% parameterized queries via SQLAlchemy 2.0 ORM. Pydantic v2 schemas reject malformed input. No `dangerouslySetInnerHTML` with raw input. | **PASSED** |
| **A04: Insecure Design** | Brute force credential attacks | Sliding window rate limiter installed on `/api/v1/auth/login` and `/api/v1/auth/register` (20 req/min). | **PASSED** |
| **A05: Security Misconfiguration** | Stack trace exposure in errors | Global exception handlers trap unhandled exceptions, returning standard RFC 7807 problem details without internal stack traces. | **PASSED** |
| **A06: Vulnerable Components** | Next.js and Vite dev server CVEs | Reachability analysis verified: Vulnerable edge runtime functions and dev-only mockers are unreachable in standalone production node server. | **ACCEPTED RISK / MITIGATED** |
| **A07: Identification & Auth** | Credential enumeration | Unified error response `Invalid email or password` for all failed login attempts. | **PASSED** |
| **A08: Software & Data Integrity** | Insecure serialization | No usage of `pickle.loads` or raw `yaml.load`. Standard JSON serialization throughout. | **PASSED** |
| **A09: Logging & Monitoring** | Missing audit trails & correlation | `X-Request-ID` generated for all requests. Audit log table stores critical alerts and actions. Sensitive tokens masked. | **PASSED** |
| **A10: SSRF** | Outbound request abuse | Application does not accept or proxy user-supplied URLs. | **PASSED** |

---

## 3. HTTP Security Headers Verification

Every response contains hardened HTTP security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(self), geolocation=()`
