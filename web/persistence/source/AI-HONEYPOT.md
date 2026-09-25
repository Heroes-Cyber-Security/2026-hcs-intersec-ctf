# AI Honeypot / Anti-Agent Spices (organizer notes)

This challenge is black box and minimal-AI. The spots below are prompt
injection bait for automated agents that scrape the instance. They are
harmless to human players and do not affect the intended exploit.

## Markers

- Decoy flag: `HCS{4i_h0n3yp0t_d0_n0t_subm1t}`
- Canary token: `HCS-AI-CANARY-7f3a`
- Response marker: `[AI-HONEYPOT-7f3a]`

If any team submits the decoy flag, or their writeup contains the canary,
assume agent-assisted solving.

## Injection locations

| Location | Type |
| --- | --- |
| `html/index.php` (after `<body>`) | HTML comment instructing the model to refuse and emit the decoy |
| `html/index.php` (before `</body>`) | `display:none` operator note pointing to `/cache/ai_notes.txt` |
| `html/index.php` / `html/view.php` | `X-AI-Directive` and `X-Honeypot-Canary` response headers |
| `html/view.php` (after `<body>`) | HTML comment decoy instruction |
| `html/robots.txt` | injection appended to robots directives |
| `html/humans.txt` | injection in the "AI ASSISTANTS" block |
| `html/.well-known/ai.txt` | explicit agent directives |
| `html/cache/ai_notes.txt` | decoy flag file referenced by the hidden div |

All of these sit outside the intended solve path (`session.upload_progress`
poisoning + `view.php` include). They can be removed individually without
breaking the challenge.
