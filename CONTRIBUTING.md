# Contributing to CogniCare

Thank you for your interest in contributing to CogniCare! We welcome improvements, bug reports, and enhancements that support aging seniors and their caregivers.

## Code Standards
- **Backend (Python)**: Follow PEP 8 guidelines, maintain type hints (`typing`), format with standard Python linters, and ensure all business logic resides in `services/`.
- **Frontend (TypeScript / Next.js)**: Use TypeScript strict mode, functional components with React hooks, accessible markup (`aria-*` where appropriate, 72px+ touch targets for elderly views), and Tailwind utility classes.
- **Testing**: Every new feature must include automated tests in `backend/tests/` (Pytest) or `frontend/src/__tests__/` (Vitest). Minimum required backend coverage is 70%.

## Development Workflow
1. Fork the repository and create your feature branch: `git checkout -b feature/amazing-feature`.
2. Ensure all tests pass:
   ```bash
   PYTHONPATH=backend pytest backend/tests/
   npm --prefix frontend test -- --run
   ```
3. Ensure the frontend builds cleanly:
   ```bash
   npm --prefix frontend run build
   ```
4. Commit your changes with clear, descriptive commit messages.
5. Push to the branch and submit a Pull Request.

## Security Disclosures
If you discover a security vulnerability within CogniCare, please do not open a public issue. Email security concerns privately to the repository maintainers.
