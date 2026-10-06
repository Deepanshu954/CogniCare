# Progress Decisions Log

Refer to [`.ai/design/decisions.md`](file:///Users/deepanshu954/GitHub/Capstone/.ai/design/decisions.md) for full architectural justifications.

### Key Active Decisions:
1. **Monorepo Structure**: `backend/` (FastAPI) and `frontend/` (Next.js).
2. **Database**: PostgreSQL 16 schema with SQLite/PostgreSQL support in testing/local dev.
3. **Ports**: Backend 8000, Frontend 3000.
4. **Mock AI Provider**: Active by default if `OPENAI_API_KEY` is not provided, allowing 100% autonomous local testing and grading.
5. **Deterministic Escalation**: SOS and missed reminders trigger alerts immediately via server service.
