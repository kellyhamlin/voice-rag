---
title: One-Way Audio
type: synthetic-runbook
---
# One-Way Audio Troubleshooting

One-way audio (caller hears callee but not vice versa, or neither hears the
other after connect) is almost always an RTP media-path problem, not signaling.

## Common causes
- NAT traversal: RTP is sent to a private IP because no SBC/ALG is rewriting SDP.
- Asymmetric routing: media takes a path with a firewall dropping inbound RTP.
- Codec mismatch: SDP offer/answer negotiated a codec one side won't send.
- Half-open firewall pinhole: signaling allowed, media UDP ports blocked.

## Steps
1. Confirm the call connects (200 OK / ACK) — if so, signaling is fine.
2. Capture on both legs; check whether RTP flows in each direction.
3. Inspect the SDP c= and m= lines for private addresses or one-sided codecs.
4. Verify firewall/SBC is pinholing the negotiated RTP port range.
