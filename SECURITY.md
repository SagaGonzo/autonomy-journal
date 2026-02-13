# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.2.3   | :white_check_mark: |
| < 1.2.3 | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within Autonomy Journal, please send an email to security@autonomy-journal.example. All security vulnerabilities will be promptly addressed.

Please include the following information:
- Description of the vulnerability
- Steps to reproduce
- Possible impact
- Suggested fix (if available)

We appreciate your efforts to responsibly disclose your findings.

## Security Measures

- Unicode security scanning via `tools/unicode_guard.py` detects hidden/bidirectional Unicode characters
- PII scanning is performed on all outputs via `tools/pii_scan.py`
- Schema validation ensures data integrity
- All operations are deterministic and auditable via JSONL logs
