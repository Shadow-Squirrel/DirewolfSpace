# Direwolf Space Systems — website

Source for **direwolfspace.com**, the public website of Direwolf Space Systems, LLC.

The site is a plain static site (HTML, CSS and a little JavaScript) with no build step, so it can be edited in any text editor and hosted for free on GitHub Pages.

## Layout

```
index.html            Home
capabilities.html     The four capability areas
intelligence.html     Intelligence products and recurring reporting
training.html         Courses and tabletop exercises
technology.html       Advanced Systems roadmap (future tense by design)
insights.html         Public analysis (launch page until the first pieces publish)
about.html            Mission, company facts, doing business with Direwolf
contact.html          Email-based inquiry form (no backend required)
404.html              Not-found page
assets/css/style.css  All styling (design tokens at the top of the file)
assets/js/main.js     Mobile nav, scroll reveal, star field, contact form
assets/img/           Logo lockups, mark, favicons, social share image, hero backdrops
assets/fonts/         Self-hosted web fonts
robots.txt, sitemap.xml
.github/workflows/pages.yml   GitHub Pages deployment
```

The hero backdrop is the supplied Earth-from-orbit image, saved as `assets/img/hero-space.webp` (extended upward with a faded band of its own sky so the full panorama fits the tall home hero) and `assets/img/hero-space-portrait.webp` (a crop for phones). Replace both files to change the backdrop; keep the same names and the pages need no edits.

Motion on the site (twinkling stars, the orbit track, scroll reveals, the typewriter block and hover effects) is disabled automatically for visitors who set "reduce motion" in their operating system.

All links between pages are **relative** (`about.html`, `assets/css/style.css`). Keep them that way. GitHub project sites are served under a sub-path, and root-relative links (`/about.html`) would break there.

## Publishing on GitHub Pages

1. Merge this branch into `main` (or push it as `main`).
2. In the repository, open **Settings → Pages**.
3. Under **Build and deployment → Source**, choose **GitHub Actions**.
4. Push to `main` (or run the "Deploy site to GitHub Pages" workflow from the **Actions** tab). The site will be live at `https://<your-github-username>.github.io/DirewolfSpace/` within a minute or two.

If you would rather not use Actions, choose **Deploy from a branch** instead, select `main` and `/ (root)`, and delete `.github/workflows/pages.yml`. Either option works because the site needs no build.

## Pointing direwolfspace.com at the site

1. At your DNS provider, add these records:
   - `A` records for the apex domain (`direwolfspace.com`) pointing to `185.199.108.153`, `185.199.109.153`, `185.199.110.153` and `185.199.111.153`.
   - A `CNAME` record for `www` pointing to `<your-github-username>.github.io`.
2. In **Settings → Pages → Custom domain**, enter `direwolfspace.com` and save. GitHub will add a `CNAME` file to the repository automatically. Commit it if it appears on a branch.
3. Once the DNS check passes, tick **Enforce HTTPS**.

The pages already declare `https://direwolfspace.com/...` as their canonical URL, and `sitemap.xml` and `robots.txt` use that domain, so nothing else needs to change when the domain goes live.

## Editing content

- Every page carries the same header, nav and footer. When you change one, change all of them (search for the same markup across the `.html` files).
- Design tokens (colours, fonts, spacing) live in the `:root` block at the top of `assets/css/style.css`.
- The contact form posts to [FormSubmit](https://formsubmit.co), a free form-relay service that forwards every submission to `contact@direwolfspace.com` (no account needed). **One-time activation:** the first time the form is submitted, FormSubmit emails an activation link to `contact@direwolfspace.com`; click it and every later submission is delivered. Until then the form reports that it could not be sent. After activation, FormSubmit's confirmation page offers a random alias endpoint (for example `https://formsubmit.co/1a2b3c...`); swapping it into the form's `action` and `data-endpoint` attributes in `contact.html` keeps the address out of the page source. To change the destination address, edit those two attributes and the `mailto:` links in the footers.
- Fonts (Michroma, Space Grotesk, Inter) are self-hosted in `assets/fonts/` under the SIL Open Font License, so the site makes no third-party requests. The `@font-face` rules are at the top of the stylesheet.

## Content rules the site follows

The copy presents Direwolf as fully capable now, in the present tense, with a few honesty rules kept:

- No pricing, customer names, contract awards, past performance, testimonials, team bios or headcount.
- SDVOSB certification and SAM.gov registration are described as **in progress**, not held. Update `about.html` and `index.html` when they are complete.
- No facility clearance is implied. Work is described as unclassified and CUI handled in protected environments.
- No roadmap, milestones or "building toward" language anywhere. The analysis platform, RF/PNT technology and space cybersecurity technology are described as capabilities Direwolf builds and operates.
- No actual intelligence findings are published. The Iran Foreign Space Capability Assessment is listed as a featured assessment available on request; make sure it is ready to send before promoting the page.

## Things to add when available

- UEI, CAGE code and NAICS codes on `about.html` (candidates to verify with your accountant or a PTAC/APEX Accelerator: 541990, 541690, 541511, 541715, 611430).
- A one-page capability statement PDF, linked from `about.html`.
- A LinkedIn company page link in the footer.
- Real posts on `insights.html`, starting with the first public analysis piece.
- A privacy notice if you add analytics or a third-party form service.

## Local preview

Any static file server works:

```
python3 -m http.server 8000
```

Then open `http://localhost:8000/`.
