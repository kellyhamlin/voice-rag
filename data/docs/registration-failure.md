markdown
---
title: Endpoint Registration Failure
type: synthetic-runbook
---
# Endpoint Registration Failure

When an endpoint fails to REGISTER, isolate auth vs. reachability vs. timing.

## Common causes
- 401/407 then giving up: wrong credentials or realm mismatch.
- 403 Forbidden: account disabled or wrong source IP.
- No response: signaling never reaches the registrar (routing/firewall).
- Expired contact: registration interval shorter than NAT binding timeout.

## Steps
1. Capture the REGISTER and the response code.
2. For 401/403, verify credentials, realm, and account status.
3. For no response, trace signaling reachability to the registrar.
4. Tune the re-registration interval below the NAT binding timeout.
