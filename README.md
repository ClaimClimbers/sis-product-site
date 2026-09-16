# Security in Social public product site

Hearing-ready SSD **Medical Source Statements (MSS)**, **physical RFC**, and **mental MRFC**. Transparency pattern (clear steps, flat list pricing at 75% of cited industry, stand-by integrity). **Security in Social brand only.**

This is the public product marketing site for Matt’s demo. It is **not** the partner learning dashboard (Progress / Lessons / Ask).

## Share intent

- **What to share:** this repo, deployed by Pulse to Vercel as a static site. Send the resulting `https://….vercel.app` URL. Do not invent a custom domain.
- **Who it is for:** Matt (partner) walking the product narrative. Claimants, family helpers, and disability-firm operators who need an MSS / RFC / MRFC packet.
- **Who merges:** Security in Social CEO. **Sam does not merge.**
- **What not to share as this product:** `sis-partner-git-1730` (partner learning). This site has no progress bars and no lesson library.

## Pages

| Page | File |
| --- | --- |
| Home | `index.html` |
| For you | `for-you.html` |
| For family | `for-family.html` |
| For firms | `for-firms.html` |
| How it works | `how-it-works.html` |
| What you get | `what-you-get.html` |
| Pricing | `pricing.html` |
| Clinical gate | `clinical-gate.html` |
| FAQ | `faq.html` |
| Contact | `contact.html` |

Nav and footer are duplicated on every page so the demo works without a build step.

## Locks

- Lead with hearing-ready SSD MSS / physical RFC / mental MRFC. Do not lead with “IMO”.
- MD/DO is the sole clinical gate. Records specialists assemble packets and draft language from the exhibits. Licensed MD/DO attests or declines. Decline when unsupported.
- Pricing is **SiS list** at 75% of cited industry upfront: screen **$149**, mental MRFC **$300**, physical RFC **$450**. Industry cites: $199 Dr. Kaako, $400 Essential Veteran Services, $600 Dr. Kaako. Clinician attestation fee is **NEED INPUT** if billed separate.
- No percent of benefits. No outcome guarantees. No invented doctor credentials.
- SAMPLE PHI language only. No live claimant records.
- Claim Climbers appears **once**, on For firms, as first operator customer (ops). Not co-brand. No Claim Climbers logo, colors, fonts, or VA nexus copy.
- Domain + legal entity remain deferred. Do not buy or invent a domain.

## Local

```bash
python3 -m http.server 3000
```

Open `http://localhost:3000/`.

## Deploy (Pulse / Vercel)

No build step. Framework preset **Other**. Root of this repo is the upload.

1. Connect `ClaimClimbers/sis-product-site`.
2. Deploy. Send Matt the `vercel.app` URL.
3. Do not point a custom domain until Sam says go.

`vercel.json` enables `cleanUrls` so `/pricing` and `/pricing.html` both work after deploy. Local Python serving still uses the `.html` hrefs in the nav.

## Visual

Direction A campaign: Newsreader + Source Sans 3, ink mast and footer, hard gold CTAs, SiS lockup, radius 16. Distinct from Claim Climbers.com. No Claim Climbers colors or fonts.

## Contact form

Static stub. Composes a request in the browser. No backend. Public inbox is NEED INPUT.
