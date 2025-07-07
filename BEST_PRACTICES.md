# Best Practices Guide

This project consolidates guidelines from multiple documents to keep development consistent and secure.

## Code Style

- **JavaScript/TypeScript**: Use ESLint with the Airbnb config and run Prettier before committing.
- **Python**: Format code with Black (line length 88) and check with flake8.
- **Ruby**: Follow the default RuboCop rules.
- Prefer descriptive names and document functions clearly.

## Testing

- Run `vitest run` for Node code, `pytest tests/` for Python, and `bundle exec rspec` for Ruby.
- Aim for 90% or higher coverage and mock external services.

## Pull Requests

- Title PRs using `[Feature|Fix|Chore] Short description`.
- Provide a concise summary and a **Testing Done** section.
- Run `eslint . && prettier --write .`, `black . && flake8`, or `rubocop -a` beforehand.

## Docker

- Use multi-stage builds and leverage layer caching.
- Run containers with minimal privileges and restrict exposed ports.
- Keep images updated and rely on named volumes for persistent data.
- Monitor CPU and memory usage.

## Administration

- Perform daily diagnostics, weekly cleanup, and monthly benchmarks.
- Review logs for issues and monitor performance metrics.
- Update dependencies regularly and test changes before deployment.
- Document configuration changes and maintain backups.

## Security

- Work inside a virtual environment and verify dependency hashes.
- Restrict directory permissions and apply secure defaults.
- Validate file types and sizes, scan for threats, and process documents in isolated environments.
- Maintain a security checklist throughout processing.

## Implementation Tips

- Preserve original documents and implement robust error handling.
- Keep code optimized for readability and document behavior.
- Ensure automated tests cover critical functionality.

## Enhancement Workflow

- Back up the project and close open files before running enhancement scripts.
- Wait for the script to finish, then review all generated changes.
