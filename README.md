# sitegenerator
Static website generator for blogs with markdown articles, tag system, light/dark theme support, and **multilingual content**.

## Features
- Markdown articles with YAML frontmatter
- **Multilingual support (French/English)**
- **Language-specific URL structure (/fr/, /en/)**
- **SEO-optimized hreflang links**
- Tag system with dedicated tag pages
- Light/dark theme toggle
- Responsive design
- Pagination support
- Thumbnail support for articles
- Static page support

## Install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration
Create a `.env` file:
```bash
MARKDOWN_DIR="articles"
HTML_DIR="html"
CSS_FILE="style.css"
TOP_TAGS=5
NB_ARTICLES_PER_PAGE=2
SHOW_FULL_CONTENT=false
SERVER="your_server_ip"
SITE_DIR="/var/www/your_site"

# Multilingual configuration
DEFAULT_LANGUAGE="fr"
SUPPORTED_LANGUAGES="fr,en"
SITE_URL="https://1ou2.com"
```

- `MARKDOWN_DIR`: Source articles directory
- `HTML_DIR`: Generated HTML output directory
- `CSS_FILE`: CSS stylesheet (must be in assets folder)
- `TOP_TAGS`: Number of top tags to display in sidebar
- `NB_ARTICLES_PER_PAGE`: Articles per index page
- `SHOW_FULL_CONTENT`: Show full articles (true) or abstracts only (false) on index
- `SERVER`: Remote server IP for deployment
- `SITE_DIR`: Remote directory path for deployment
- `DEFAULT_LANGUAGE`: Default language for the site (fr or en)
- `SUPPORTED_LANGUAGES`: Comma-separated list of supported languages
- `SITE_URL`: Full website URL for generating canonical links

## Article Format
Articles use markdown with YAML frontmatter:
```yaml
---
title: "Article Title"
date: 2024-01-01
tags: "tag1, tag2, tag3"
abstract: "Brief article description"
thumbnail: "image.png"  # optional
language: "fr"          # fr or en
---

Your markdown content here...
```

### Multilingual Articles
Articles are organized by language using the following structure:
```
articles/YYYY/MM/DD/article-name/
├── fr.md                    # French version
├── en.md                    # English version (optional)
├── images/                  # Shared resources
└── other-assets/
```

**URL Structure:**
- French: `https://yoursite.com/fr/2024/01/01/article-name/`
- English: `https://yoursite.com/en/2024/01/01/article-name/`

## Project Structure
- `articles/`: Markdown source files organized by date (YYYY/MM/DD/article-name/)
  - `fr.md`: French version of the article
  - `en.md`: English version of the article (optional)
  - Shared assets (images, diagrams, etc.)
- `assets/`: CSS, images, JavaScript files
- `static/`: Static HTML pages (contact, about, etc.)
- `templates/`: HTML templates for generation
- `html/`: Generated website output with language-specific directories

## Generate Website
```bash
python3 website.py
```

This generates:
- Language-specific index pages (`/fr/`, `/en/`)
- Individual article pages with multilingual support
- Language-specific tag pages (`/fr/tags/`, `/en/tags/`)
- Automatic hreflang links for SEO
- Language selector on each page
- Copies assets and static files

**Generated Structure:**
```
html/
├── fr/
│   ├── 2024/01/01/article-name/index.html
│   └── tags/tag-name.html
├── en/
│   ├── 2024/01/01/article-name/index.html
│   └── tags/tag-name.html
├── assets/
└── static-pages/
```

## Deploy
```bash
python3 deploy.py
```

Deployment:
1. Creates timestamped backup of remote HTML directory
2. Copies local `html/` folder to remote server via SCP
3. Requires SSH key authentication to remote server

### Nginx Configuration for Multilingual Support
The new multilingual structure requires updated Nginx configuration. See `nginx-multilingual.conf` for a complete example.

**Key points:**
- Root `/` redirects to default language `/fr/`
- Each language has its own URL space: `/fr/` and `/en/`
- Static assets remain shared across languages
- Proper language headers and caching

**Simple Nginx setup:**
```nginx
server {
    server_name 1ou2.com;
    root /var/www/your_site;
    
    # Redirect root to default language
    location = / {
        return 302 /fr/;
    }
    
    # Language-specific routes
    location /fr/ {
        try_files $uri $uri/ /fr/index.html;
    }
    
    location /en/ {
        try_files $uri $uri/ /en/index.html;
    }
}
```

## Files
- `website.py`: Main generator script
- `articles.py`: Article parsing and processing
- `deploy.py`: Remote deployment script
- `templates/`: HTML templates for different page types
- `assets/style.css`: Main stylesheet with light/dark theme support
- `assets/theme-toggle.js`: Theme switching functionality

## Multilingual Features

### SEO Optimization
- **Hreflang tags**: Automatic generation of `<link rel="alternate" hreflang="lang" />` 
- **Canonical URLs**: Proper canonical link generation
- **Language-specific sitemaps**: Each language gets its own URL structure
- **Clean URLs**: `/fr/2024/01/01/article-name/` format

### Language Management
- **Language detection**: Automatic detection from YAML frontmatter
- **Translation discovery**: Articles can find their translations automatically
- **Fallback handling**: Graceful handling of mono-language articles
- **Language selector**: Visual selector with flags (🇫🇷 🇬🇧)

### Content Organization
- **Shared assets**: Images and resources shared between language versions
- **Language-specific tags**: Tag pages generated per language
- **Independent navigation**: Each language maintains its own article flow

# TODO ~~Multilang support~~
[✅] ~~Translate articles~~

[✅] ~~Store both versions in same folder~~
```
YYYY/MM/DD/article-name/
  fr.md
  en.md
  images/
```

[✅] ~~Modify yaml to add language tag~~

[✅] ~~Add crosslink between languages~~
```html
<link rel="alternate" hreflang="fr" href="https://example.com/fr/floating-point/" />
<link rel="alternate" hreflang="en" href="https://example.com/en/floating-point/" />
<link rel="canonical" href="https://example.com/fr/floating-point/" />
```

[✅] ~~Add language selector in template~~
```html
🇫🇷 FR | 🇬🇧 EN
```

[✅] ~~Handle mono language case~~
Some articles will be written in only one language

[ ] Static pages
Translate also static pages (livres and contact)

[ ] Create two separates pages for tags
create a /fr/tags/ and a /en/tags/
use a separate template for fr-tag.html en-tag.html 