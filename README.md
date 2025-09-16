# Auto-RSS Jekyll Blog (GitHub Pages)

This repository auto-creates Jekyll posts from an RSS feed using a GitHub Action.

## Features
- Uses Jekyll for static site generation (host on GitHub Pages)
- GitHub Actions pulls an RSS feed and generates `_posts/YYYY-MM-DD-slug.md` files
- Runs on schedule and on manual trigger

## Setup steps
1. Create a new repository named `yourusername.github.io` (or any name if you prefer to set Pages from branch).
2. Add these files and push to `main` branch.
3. In GitHub repo Settings → Secrets and variables → Actions:
   - Add a repository secret (or variable) named `RSS_URL` with the RSS feed URL you want to import.
     - Example: `https://example.com/feed.xml`
   - (Optional) Add `POSTS_DIR` with the value `_posts` if you want a custom posts path.
4. Enable GitHub Pages:
   - Settings → Pages → Branch: `main` / folder: `/ (root)` (or the branch you use)
   - Wait a minute — your site will be available at `https://yourusername.github.io/` (if repo named `yourusername.github.io`) or the URL shown by GitHub.
5. To test manually:
   - Go to Actions → the workflow `autopost` → Run workflow → choose `main` and click Run.
6. The workflow will fetch the RSS feed, create new markdown files in `_posts/`, commit and push them. GitHub Pages will build your site using Jekyll.

## Customize
- Edit `_config.yml` to change site title, author, theme.
- Change cron schedule in `.github/workflows/autopost.yml` if you want a different frequency.
