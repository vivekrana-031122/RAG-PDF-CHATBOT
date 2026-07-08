# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- [ ] PostgreSQL integration for scalable multi-tenant data
- [ ] Redis caching layer for high-frequency session lookups
- [ ] JWT-based authentication and user authorization
- [ ] API rate limiting & request throttling
- [ ] LangSmith / Phoenix tracing for LLM observability
- [ ] Kubernetes deployment guide with Helm chart
- [ ] Support for additional file formats (Excel, Markdown)
- [ ] Multi-language document support

---

## [1.0.0] — 2026-07-07

### 🔒 Security
- Added UUID format validation on all session-scoped disk paths to prevent directory traversal attacks.
- Replaced crash-on-import `ValueError` with a graceful warning when `OPENAI_API_KEY` is absent, enabling safe test and container builds.
- Added Bandit security scan to GitHub Actions CI pipeline.
- Added CodeQL static analysis workflow scheduled weekly.
- Added Dependabot for automated dependency vulnerability alerts.

### ✨ Added
- **Disk Persistence:** `SessionManager` now serializes FAISS index files and conversation history JSON metadata to local disk, restoring sessions automatically across server restarts.
- **Dual Interface:** Streamlit UI (`app.py`) and FastAPI REST API (`api.py`) fully operational.
- **Source Tracking:** Every query response includes the source document name, page number, and text preview.
- **Docker Compose:** Multi-container orchestration for one-command deployment.
- **CI Pipeline:** GitHub Actions workflow running tests, Ruff linting, and Bandit security scans on every push and PR.
- **Community Files:** Added `CODE_OF_CONDUCT.md`, structured Issue Templates (bug, feature), and PR Template.
- **Render + HuggingFace Deploy:** `render.yaml` for Render.com deployment.

### 📖 Documentation
- System architecture Mermaid diagram in README.
- Full REST API endpoint reference with request/response JSON examples.
- Local setup guide, docker deployment guide, and testing guide.

---

## [0.1.0] — 2026-03-22

### Added
- Initial project scaffolding with FastAPI, Streamlit, LangChain, FAISS.
- Basic `/upload` and `/ask/{session_id}` endpoints.
- In-memory session management.
- `requirements.txt`, `Dockerfile.api`, `Dockerfile.ui`.
