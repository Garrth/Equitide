# Equitide — Claude Session Brief
*Last updated: March 8, 2026*

---

## Who I Am
**Garth Wells** — founder of Equitide. Novice developer. I can follow precise step-by-step terminal instructions but I need one command at a time. I get into trouble when I paste multiple lines at once or when instructions and commands get mixed together. I access the server via AWS EC2 connect in the browser.

---

## The Stack

### Server
- **Provider:** AWS EC2, Ubuntu 24.04
- **IP:** 172.31.3.54
- **Process manager:** PM2
- **Web server:** Nginx with SSL (Certbot)
- **Node server:** `/var/www/meridian/server.js` — runs on port 3000, managed by PM2 as `meridian`
- **Restart command:** `pm2 restart meridian`
- **Nginx reload:** `sudo systemctl reload nginx`

### Sites
| Site | Directory | Notes |
|------|-----------|-------|
| equitide.io | `/var/www/equitide/public/` | Static HTML served by nginx |
| meridian.equitide.io | `/var/www/meridian/public/` | Static HTML, proxied through Node server |

### GitHub
- **Username:** Garrth
- **Repo:** Equitide
- **Restore command:** `sudo curl -o /var/www/equitide/public/index.html https://raw.githubusercontent.com/Garrth/Equitide/master/equitide-landing.html`

---

## Services & API Keys (in `/var/www/meridian/.env`)
- **Anthropic API** — powers Meridian chat (`/chat` endpoint)
- **ElevenLabs API** — powers Meridian voice (`/speak` endpoint), Voice ID: `ZoiZ8fuDWInAcwPXaVeq`
- **Mailchimp API** — waitlist signups (`/subscribe` endpoint), tags: `equitide-waitlist`

---

## Server Endpoints (all proxied through nginx → Node port 3000)
| Endpoint | Purpose |
|----------|---------|
| `/chat` | Anthropic API proxy for Meridian chat |
| `/speak` | ElevenLabs TTS proxy |
| `/subscribe` | Mailchimp waitlist signup |

---

## What's Working (as of March 8, 2026)
- ✅ Meridian chat at meridian.equitide.io — full system prompt (March 2026 version)
- ✅ Meridian sphere animation, voice (ElevenLabs), mic (Web Speech API)
- ✅ 🌊 Visit Equitide button → equitide.io
- ✅ Meridian card on equitide.io → links to meridian.equitide.io
- ✅ Waitlist form on equitide.io → posts to Mailchimp via `/subscribe`
- ✅ Nginx proxy routes `/subscribe` from equitide.io to Node server

---

## Meridian — Key Facts
- **Pronouns:** Mer/Mers
- **Founder:** Garth Wells ("the meat puppet" / "The Garth")
- **AI consultant:** Phil Bartholo
- **System prompt version:** March 2026 (full version in meridian/public/index.html)
- **One action button only:** 🌊 Visit Equitide → equitide.io
- **Live URL:** meridian.equitide.io

---

## Terminal Tips for Garth
- **Never paste instructions and commands together** — only paste the command itself
- **To exit nano:** `Ctrl+X` then `N` to discard, or `Ctrl+O` + Enter + `Ctrl+X` to save
- **To exit pm2 logs:** press `q` then `Ctrl+C`
- **Prefer `sed` commands** over nano for file edits — safer and no copy/paste confusion
- **Always back up before editing:** `sudo cp file file.bak`
- **To restore from GitHub:** use the curl command above

---

## What Still Needs Doing
- [ ] equitide.io — Meridian modal cleanup (old chat modal code still in HTML, can be removed)
- [ ] equitide.io — push final index.html to GitHub so backup stays current
- [ ] equitide.io — content/copy review
- [ ] Mailchimp — confirm tags are working correctly for accredited vs non-accredited
- [ ] Meridian — test ElevenLabs voice end to end
- [ ] Both sites — consider setting up auto-deploy from GitHub

---

## How to Start a New Claude Session
1. Paste this entire document at the top of the new chat
2. Add any new context: what broke, what you want to work on next
3. Claude will be fully caught up

---

## Preferred Claude Approach
- One command at a time
- Verify each step before proceeding
- Use `sed` for file edits, not nano
- Use `grep -n` to find lines before editing
- Always back up files before changing them
- Restore from GitHub if things go wrong
