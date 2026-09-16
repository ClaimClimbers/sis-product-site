# Security in Social public product site

DIY Social Security help and a **medical record review**. Specialists review the file and name what it can and cannot support. Doctor-signed letters about work limits are coming later. **Security in Social brand only.**

This is the public product marketing site for Matt’s demo. It is **not** the partner learning dashboard (Progress / Lessons / Ask).

## Share intent

- **What to share:** this repo, deployed by Pulse to Vercel as a static site. Send the resulting `https://….vercel.app` URL. Do not invent a custom domain.
- **Who it is for:** Matt (partner) walking the product narrative. Claimants, family helpers, and disability-firm operators who need a records review first.
- **Who merges:** Security in Social CEO. **Sam does not merge.** (Internal. Not public footer copy.)
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

Primary nav is six links: Home · For you · For family · How it works · Pricing · Contact. For firms, What you get, Doctor review, and FAQ live in the footer.

## Locks

- Public Home leads with DIY Social Security + medical record review. Primary CTA: **Start a records review**. Secondary: **Join the letter waitlist**.
- Doctor letters (MSS / physical RFC / mental MRFC) are coming later / waitlist. Do not lead Home with letter SKUs.
- Public copy is layman first. Acronyms (MSS, RFC, MRFC) in parentheses or on Pricing / For firms.
- Licensed MD or DO is the sole clinical gate when letters ship. Records specialists assemble packets and draft language from the file. Decline when unsupported.
- Never AI or bots.
- Pricing is **SiS list** at 75% of cited industry upfront: review **$149** first. Mental work-limits letter **$300** and physical work-limits letter **$450** stay listed as coming later / waitlist. Industry cites (SAMPLE) stay named on Pricing: $199 Dr. Kaako, $400 Essential Veteran Services, $600 Dr. Kaako. Clinician sign-off fee is **NEED INPUT** if billed separate.
- No percent of benefits. No outcome guarantees. No invented doctor credentials.
- SAMPLE language only. No live claimant records.
- SSDI only in UI copy. Essential Veteran Services appears only as a Pricing industry cite.
- Claim Climbers appears **once**, on For firms, as first operator customer (ops). Not co-brand. No Claim Climbers logo, colors, or fonts.
- Domain + legal entity remain deferred. Do not buy or invent a domain.
- No em dashes in public copy.

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

Campaign Ink. Newsreader + Source Sans 3. White paper canvas (`#ffffff`). Dark mast (`#07090d`). Gold CTAs (`#c9920f`). Teal accent (`#0f6b5c`). Official tokens in `css/product-site-bold-tokens.css` and the `:root` block in `css/site.css`.

## Contact form

Static stub. Composes a request in the browser. No backend. Public inbox is NEED INPUT. Primary ask is a records review. Secondary is the doctor-letter waitlist.
