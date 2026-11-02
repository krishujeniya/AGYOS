# Phase 5A: Deployment Guide

> Guide the user through deploying their ScrollHeart site to GitHub Pages.
> Keep instructions simple — the user may not be a developer.
> Explain every step in human terms.

---

## Pre-Deployment Checklist

Before deploying, verify:

- [ ] All 3 files exist: `index.html`, `css/style.css`, `js/main.js`
- [ ] `.nojekyll` file exists in the root
- [ ] `<meta name="robots" content="noindex, nofollow">` is in the HTML head
- [ ] No analytics scripts, tracking pixels, or cookies
- [ ] No social media meta tags (`og:title`, `twitter:card`, etc.)
- [ ] Audio requires user gesture to play (test by opening index.html locally)
- [ ] Site renders correctly on mobile (test at 375px width)
- [ ] `prefers-reduced-motion` fallback works

---

## Option A: GitHub Pages (Recommended)

### Step 1: Create a New Repository

Tell the user:
> "First, let's create a new repository on GitHub. Give it an innocent name — not something like 'for-sarah' or 'love-letter'. Try something like 'scroll-test-84' or 'quiet-pages'. This keeps it private and hard to find."

**Repository naming rules:**
- ✅ `scroll-test-84`, `quiet-pages`, `frontend-experiment`, `night-sky-demo`
- ❌ `for-sarah`, `love-letter`, `my-crush`, `her-gift`, `scrollheart-for-emily`

**Settings:**
- Set to **Private** if the user has GitHub Pro (recommended)
- Set to **Public** if free tier (acceptable — the obfuscated name protects it)
- Do NOT add a README (keep it clean)

### Step 2: Upload Files

Tell the user:
> "Now upload the files I created. You can drag and drop them directly into GitHub, or use Git if you're comfortable with it."

**Drag-and-drop method (for non-technical users):**
1. Go to the repository page on GitHub
2. Click "Add file" → "Upload files"
3. Drag the entire folder contents (index.html, css/, js/, .nojekyll)
4. Click "Commit changes"

**Git method (for technical users):**
```bash
cd scrollheart-story
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/{username}/{repo-name}.git
git branch -M main
git push -u origin main
```

### Step 3: Enable GitHub Pages

Tell the user:
> "Now let's turn on GitHub Pages so she can view it in a browser."

1. Go to repository **Settings**
2. Click **Pages** in the left sidebar
3. Under "Source", select **Deploy from a branch**
4. Select **main** branch, **/ (root)** folder
5. Click **Save**
6. Wait 1–2 minutes for deployment
7. The URL will appear at the top: `https://{username}.github.io/{repo-name}/`

### Step 4: Verify Deployment

Tell the user:
> "Open the link in your phone's browser. Make sure everything looks good before you send it to her."

**Check on mobile:**
- Does the overlay appear first?
- Does clicking "Begin" start the audio?
- Do the scenes scroll smoothly?
- Is the text readable?
- Does the replay button work?

---

## Option B: Custom Domain (Advanced, Optional)

If the user wants a more romantic URL (e.g., `quiet-stories.com`):

Tell the user:
> "If you want a custom URL instead of the GitHub one, you can buy a cheap domain (around $10/year) and connect it. This hides your GitHub username and looks more polished."

**Steps:**
1. Buy a domain from Namecheap, Google Domains, or similar
2. In GitHub repo Settings → Pages → Custom domain, enter the domain
3. Add DNS records (A records pointing to GitHub IPs, or CNAME)
4. Wait for DNS propagation (up to 24 hours)
5. Enable "Enforce HTTPS"

**Domain naming suggestions:**
- `quiet-stories.com`, `night-sky-pages.com`, `starlight-memories.com`
- Avoid anything with "love", "heart", "crush", or her name

---

## Option C: Local Preview Only

If the user isn't ready to deploy yet:

Tell the user:
> "You can preview it locally first. Just open the `index.html` file in your browser. Note: audio might not work locally on some browsers due to security restrictions, but everything else should look right."

**Local preview limitations:**
- Audio may not load from `file://` protocol in some browsers
- Use a simple local server if needed: `python3 -m http.server 8000`

---

## Privacy Measures

### Already Built Into the Site:
- `<meta name="robots" content="noindex, nofollow">` — prevents search engine indexing
- No analytics, tracking pixels, or cookies
- No social media preview cards
- Generic page title ("A Story for You")

### Additional Recommendations:

**Repository privacy:**
> "If you have GitHub Pro, set the repository to Private. If you're on the free plan, the public repo is fine — the name is obscure enough that no one will find it."

**Password protection (optional):**
> "If you want true privacy, GitHub Pages doesn't support password protection on free accounts. Instead, I can help you deploy this to **Netlify** or **Vercel** where we can set up secure edge-function password protection so only she can access it."

If the user wants this, DO NOT provide a Javascript `prompt()` based password — this is insecure and easily bypassed by disabling JS or viewing the source code. Instead, guide them to create a free Netlify account and deploy the folder there, utilizing Netlify's access control features or edge functions for actual security.

---

## Post-Deployment Message to User

After successful deployment:

> "Your story is live! 🎉 Here's the link: `{url}`
>
> Before you send it to her, a few things:
> 1. Open it on your phone first to make sure it looks right
> 2. Try it in both portrait and landscape
> 3. Test the audio — make sure it plays when you tap 'Begin'
> 4. If anything looks off, let me know and I'll fix it
>
> When you're ready to send it, I've got some tips on the best way to do that too."

Then proceed to **Phase 5B: Post-Build Guidance** by loading `references/07-post-build-guide.md`.
