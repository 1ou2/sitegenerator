# Multilingual Support Implementation Plan

## Overview
This document outlines the implementation plan for adding French (fr) and English (en) multilingual support to the static website generator. Currently, all articles are in French.

## Phase 1: Article Structure & Storage

### 1.1 Reorganize Article Storage
- **Current**: `YYYY/MM/DD/article-name/article-name.md`
- **New**: `YYYY/MM/DD/article-name/fr.md` and `YYYY/MM/DD/article-name/en.md`
- Keep shared resources in same folder: `YYYY/MM/DD/article-name/images/`

### 1.2 Update YAML Frontmatter
Add `language` field to article metadata:
```yaml
---
title: "Article Title"
date: 2024-01-01
tags: "tag1, tag2, tag3"
abstract: "Brief article description"
thumbnail: "image.png"
language: "fr"  # NEW FIELD
---
```

## Phase 2: Code Architecture Changes

### 2.1 Update Article Class (`articles.py`)
- Modify `Article` class to handle language detection
- Add `language` property from YAML frontmatter
- Update file parsing to detect `fr.md`/`en.md` pattern
- Add method to find article translations (same folder, different language)

### 2.2 Update Website Class (`website.py`)
- Modify article discovery to handle new file structure
- Group articles by language for separate processing
- Update URL generation to include language prefix: `/fr/` and `/en/`
- Create language-specific tag pages: `/fr/tags/` and `/en/tags/`
- Generate separate index pages per language

### 2.3 Configuration Updates
Add language settings to `.env`:
```bash
DEFAULT_LANGUAGE="fr"
SUPPORTED_LANGUAGES="fr,en"
SITE_URL="https://example.com"  # for canonical URLs
```

## Phase 3: Template Updates

### 3.1 Add Language Selector
Update all templates (`article.html`, `index.html`, `tag.html`) to include:
```html
<div class="language-selector">
    <a href="/fr/" class="lang-link">FR 🇫🇷</a> | 
    <a href="/en/" class="lang-link">EN 🇬🇧</a>
</div>
```

### 3.2 Add Hreflang Links
Update `<head>` section in templates:
```html
<link rel="alternate" hreflang="fr" href="https://example.com/fr/article-path/" />
<link rel="alternate" hreflang="en" href="https://example.com/en/article-path/" />
<link rel="canonical" href="https://example.com/fr/article-path/" />
```

### 3.3 Localize Navigation
- Create language-specific navigation labels
- Update static page links to include language prefix
- Localize sidebar content (bio section, tags header)

## Phase 4: URL Structure & Generation

### 4.1 New URL Structure
- **Root**: `/` (redirect to default language)
- **French**: `/fr/`, `/fr/tags/`, `/fr/2024/10/21/article/`
- **English**: `/en/`, `/en/tags/`, `/en/2024/10/21/article/`

### 4.2 Cross-Language Linking
- Detect available translations for each article
- Generate appropriate hreflang links
- Handle canonical URL selection (prefer original language)

## Phase 5: Static Pages Translation

### 5.1 Translate Static Pages
Create language versions:
- `static/fr/contact.html` and `static/en/contact.html`
- `static/fr/livres.html` and `static/en/livres.html`

### 5.2 Update Static Page Processing
Modify website generation to:
- Copy static pages to appropriate language directories
- Update internal links to be language-aware

## Phase 6: Mono-Language Article Handling

### 6.1 Detection Logic
- Check if both `fr.md` and `en.md` exist
- If only one language exists, generate only for that language
- Update language selector to show only available languages

### 6.2 Fallback Strategy
- For missing translations, optionally show "Translation not available" message
- Provide link to article in available language

## Phase 7: Migration Strategy

### 7.1 Existing Articles Migration
1. Rename existing `.md` files to `fr.md` (since all current articles are French)
2. Update any hardcoded paths in deployment scripts
3. Test generation with existing content

### 7.2 Backward Compatibility
- Ensure existing URLs still work (redirect or maintain structure)
- Update deployment script to handle new directory structure

## Implementation Priority

1. **High Priority**: Article structure, YAML updates, basic code changes
2. **Medium Priority**: Template updates, URL structure, static pages
3. **Low Priority**: Advanced features like automatic translation detection

## Testing Strategy

1. Test with single-language articles (existing French content)
2. Test with bilingual articles (create sample English translations)
3. Test mono-language scenarios
4. Verify all generated links work correctly
5. Test deployment process

## Future Enhancements

- Automatic language detection from browser preferences
- RSS feeds per language
- Sitemap generation with hreflang annotations
- Translation status tracking
- SEO optimization for multilingual content