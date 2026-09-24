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
tools/render_hero_background.py   Regenerates the Earth-from-orbit hero backdrops
robots.txt, sitemap.xml
.github/workflows/pages.yml   GitHub Pages deployment
```

The hero backdrop (night-side Earth limb, city lights, star field, nebula, sun glare) is rendered procedurally rather than taken from a stock photo, so it is royalty-free and can be re-rendered with different parameters:

```
pip install numpy pillow
python3 tools/render_hero_background.py
```

Motion on the site (twinkling stars, the orbit track, the ticker, scroll reveals, the typewriter block and hover effects) is disabled automatically for visitors who set "reduce motion" in their operating system.

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
- The contact form composes an email in the visitor's mail client. Change the destination by editing the `data-to` attribute on the `<form>` in `contact.html` and the `mailto:` links in the footers. To collect submissions without email, wire the form to a service such as Formspree or Basin by replacing the form's `action` and removing the JavaScript handler in `assets/js/main.js`.
- Fonts (Michroma, Space Grotesk, Inter) are self-hosted in `assets/fonts/` under the SIL Open Font License, so the site makes no third-party requests. The `@font-face` rules are at the top of the stylesheet.

## Content rules the site follows

The copy was written to stay credible while the company is new:

- No pricing, customer names, contract awards, past performance, testimonials, team bios or headcount.
- SDVOSB certification and SAM.gov registration are described as **being pursued**, not held. Update `about.html` when they are complete.
- No facility clearance is implied. Work is described as unclassified, with CUI handling when required.
- Advanced Systems, the analysis platform, RF/PNT technology and space cybersecurity products are described in the **future tense**.
- No actual intelligence findings are published. `insights.html` is a launch page until real pieces exist.

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
