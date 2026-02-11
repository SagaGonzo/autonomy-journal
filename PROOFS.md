# Proofs & Receipts

## Repository Verification
- **URL:** https://github.com/SagaGonzo/autonomy-journal
- **Visibility:** Public
- **Access Check:** 200 OK (Verified via curl -I)

### curl -I https://github.com/SagaGonzo/autonomy-journal
```
HTTP/1.1 200 OK
Accept-Ranges: bytes
Cache-Control: max-age=0, private, must-revalidate
Connection: close
Content-Type: text/html; charset=utf-8
Date: Wed, 11 Feb 2026 04:04:06 GMT
Etag: W/"7dcd4023b639191d1e72784ea19c9557"
Referrer-Policy: no-referrer-when-downgrade
Server: github.com
Strict-Transport-Security: max-age=31536000; includeSubdomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: deny
X-Github-Request-Id: 4420:19BAAC:998CF35:CBCAFAB:698BFFB1
X-Xss-Protection: 0
```

## Release Pack
- **Version:** v1.2.3
- **Status:** Pushed to main branch

## Local Validation Receipts
```text
# tools/make_proofs.sh output
Running PII scan...
PII_SCAN_PASS
Validating schemas...
SCHEMA_OK schemas/reality_state.v1.schema.json
SCHEMA_OK schemas/autonomy_journal.v1.autonomy.schema.json
Generating test JSONL data...
Generating checksums...
b42f1816512ae61ff9f6165833fad3a6cae2a981528fc311fb41c3b83b15e141  proofs/run1.jsonl
b42f1816512ae61ff9f6165833fad3a6cae2a981528fc311fb41c3b83b15e141  proofs/run2.jsonl
Validating JSONL structure...
JSONL_VALIDATE_PASS

Proof generation complete!
```

## CI/CD
- **Status:** Pending configuration
