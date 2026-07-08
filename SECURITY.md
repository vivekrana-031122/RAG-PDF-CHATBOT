# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, please email **dev.vivekrana@gmail.com** instead of using the public issue tracker.

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will respond within 48 hours and work with you to resolve the issue.

## Security Best Practices

### API Key Management
- **Never commit `.env` files** to version control
- Always use `.env.example` as a template
- Rotate API keys regularly
- Use environment variables for secrets
- Never log API keys or sensitive data

### Input Validation
- Validate all user inputs
- Sanitize file uploads
- Check file types and sizes
- Use Pydantic for API request validation

### Data Protection
- FAISS indexes stored locally are not encrypted by default
- For production, consider encrypted storage
- Implement access controls for uploaded documents
- Log access to sensitive data

### Dependencies
- Keep dependencies updated
- Use `pip-audit` to check for known vulnerabilities
- Review `requirements.txt` regularly

```bash
# Check for vulnerable packages
pip install pip-audit
pip-audit
```

### Deployment Security
- Use HTTPS in production
- Implement rate limiting
- Use environment-specific configurations
- Enable CORS only for trusted origins
- Implement authentication if needed

### Docker Security
- Use specific base image versions (not `latest`)
- Run containers as non-root user
- Scan images for vulnerabilities

```dockerfile
FROM python:3.11-slim
RUN useradd -m appuser
USER appuser
```

## Known Issues

None currently tracked.

## Version Support

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅ Yes   |
| < 0.1   | ❌ No    |

## Security Updates

We will notify users of security updates via:
- GitHub Releases
- GitHub Security Advisories
- Direct email (if contact info available)

Thank you for helping keep this project secure!
