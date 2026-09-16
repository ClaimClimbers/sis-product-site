# Security in Social public product site

DIY Social Security help and a **medical record review**. Specialists review the file and name what it can and cannot support. **Security in Social brand only.**

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

- Public Home leads with DIY Social Security + medical record review. Primary CTA: **Start a record review**. Secondary: **See the app plan** · **See how it works**.
- Public copy is layman first. Built so an older, non-medical Social Security disability claimant can understand the file.
- Never AI or bots.
- **PRICING-LOCK-395-PLUS-APP-129:** TWO-TRACK. Lead is DIY full medical record review **$395 lifetime**. Alt is the **app at $129.99/year** (parse/extract + plain-English answers on disability / health insurance / retirement). Doctor-letter SKUs stay **out of the public site**. Do not frame $395 as the only SKU. Do not make the app the primary offer. No trial auto-charge copy.
- **Tip #87 lead (frozen):** A full medical record review for Social Security disability, explained in plain English so you understand your claim before you apply — $395 lifetime.
- **App alt (separate, not inside Tip #87):** Or the app for $129.99 a year: scan and extract your records, then get plain-English answers on disability, health insurance, and retirement.
- No percent of benefits. No outcome guarantees. No invented doctor credentials.
- SAMPLE language only. No live claimant records.
- SSDI only in UI copy.
- Claim Climbers appears **once**, on For firms, as first operator customer (ops). Not co-brand. No Claim Climbers logo, colors, or fonts.
- Domain + legal entity remain deferred. Do not buy or invent a domain.
- Tip #87 lead keeps its frozen em dash. Do not reopen that sentence.

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

Static stub. Composes a request in the browser. No backend. Public inbox is NEED INPUT. Primary ask is a $395 lifetime records review. App plan is the yearly alternate.
