import argparse
import os,shutil
from dotenv import load_dotenv
from articles import Article
import math,re

class Configuration:
    def __init__(self):
        load_dotenv()
        self.md_dir = os.getenv("MARKDOWN_DIR")
        self.html_dir = os.getenv("HTML_DIR")
        self.css_file = os.getenv("CSS_FILE", "style.css")
        self.top_tags = int(os.getenv("TOP_TAGS", 10))
        self.nb_articles_per_page = int(os.getenv("NB_ARTICLES_PER_PAGE", 5))
        self.show_full_content = os.getenv("SHOW_FULL_CONTENT", "true").lower() == "true"
        
        # Multilingual configuration
        self.default_language = os.getenv("DEFAULT_LANGUAGE", "fr")
        self.supported_languages = os.getenv("SUPPORTED_LANGUAGES", "fr,en").split(",")
        self.site_url = os.getenv("SITE_URL", "https://example.com")
        
        self.config = {
            "md_dir": self.md_dir,
            "html_dir": self.html_dir,
            "top_tags": self.top_tags,
            "nb_articles_per_page": self.nb_articles_per_page,
            "show_full_content": self.show_full_content,
            "default_language": self.default_language,
            "supported_languages": self.supported_languages,
            "site_url": self.site_url
        }

    def get(self, key):
        return self.config[key]
    
class Website:
    def __init__(self,conf):
        self.config = conf
        self.articles = []
        self.articles_by_tag = {}
        self.articles_by_language = {}  # New: articles grouped by language

    # get list of all markdown files
    def get_markdown_files(self):
        md_files = []
        for root, dirs, files in os.walk(self.config.md_dir):
            for file in files:
                # Only include supported language files
                if file in ['fr.md', 'en.md']:
                    md_files.append(os.path.join(root, file))
        return md_files

    # clean html dir
    def clean_html_dir(self):
        # delete html dir
        shutil.rmtree(self.config.html_dir,ignore_errors=True)
        os.makedirs(self.config.html_dir)

    def init_html(self):
        self.clean_html_dir()
        # copy md_dir to html_dir  # cp -r md_dir/* html_dir
        shutil.copytree(self.config.md_dir, self.config.html_dir, dirs_exist_ok=True)
        # copy assets to html_dir/assets
        assets_dir = os.path.join(self.config.html_dir, "assets")
        os.makedirs(assets_dir, exist_ok=True)
        shutil.copytree("assets", assets_dir, dirs_exist_ok=True)
        # copy static files to html_dir
        static_dir = os.path.join(self.config.html_dir)
        os.makedirs(static_dir, exist_ok=True)
        shutil.copytree("static", static_dir, dirs_exist_ok=True)

    def init_articles(self):
        md_files = self.get_markdown_files()
        # create one article object per markdown file
        for md_file in md_files:
            article = Article(md_file)
            self.add(article)

        # Group articles by language and sort by date
        for lang in self.config.get('supported_languages') or ['fr', 'en']:
            if lang in self.articles_by_language:
                self.articles_by_language[lang] = self.get_articles_by_date(lang)

        # sort all articles by date for backward compatibility
        self.articles = self.get_articles_by_date()
        
        # add path to this article with language prefix
        for article in self.articles:
            # New URL structure: /lang/2025/11/10/article-name/
            rel_path = article.md_file_path.replace(self.config.md_dir + "/", "")
            # Remove language file name and add language prefix
            path_parts = rel_path.split("/")
            if len(path_parts) >= 4:  # year/month/day/article/lang.md
                article_path = "/".join(path_parts[:-1])  # remove lang.md
                article.path = os.path.join(self.config.html_dir, article.language, article_path, "index.html")
            else:
                article.path = article.md_file_path.replace(self.config.md_dir, self.config.html_dir).replace(".md", ".html")

        # add links to previous and next articles within same language
        for lang in self.config.get('supported_languages') or ['fr', 'en']:
            if lang in self.articles_by_language:
                lang_articles = self.articles_by_language[lang]
                for i, article in enumerate(lang_articles):
                    if i > 0:
                        article.prev_path = os.path.relpath(lang_articles[i-1].path, os.path.dirname(article.path)) 
                    if i < len(lang_articles) - 1:
                        article.next_path = os.path.relpath(lang_articles[i+1].path, os.path.dirname(article.path))

        # Count tags by language
        self.sorted_tags_by_language = {}
        for lang in self.config.get('supported_languages') or ['fr', 'en']:
            tag_count = {}
            if lang in self.articles_by_language:
                for article in self.articles_by_language[lang]:
                    for tag in article.tags:
                        if tag not in tag_count:
                            tag_count[tag] = 0
                        tag_count[tag] += 1
                self.sorted_tags_by_language[lang] = [k for k,v in sorted(tag_count.items(), key=lambda x:x[1], reverse=True)]
        
        # Keep global sorted tags for backward compatibility 
        tag_count = {}
        for article in self.articles:
            for tag in article.tags:
                if tag not in tag_count:
                    tag_count[tag] = 0
                tag_count[tag] += 1
        self.sorted_tags = [k for k,v in sorted(tag_count.items(), key=lambda x:x[1], reverse=True)]

    # html article has been created
    def add(self, article):
        self.articles.append(article)

        # Group articles by language
        if article.language not in self.articles_by_language:
            self.articles_by_language[article.language] = []
        self.articles_by_language[article.language].append(article)

        # Group articles by tag (global)
        for tag in article.tags:
            if tag not in self.articles_by_tag:
                self.articles_by_tag[tag] = []
            self.articles_by_tag[tag].append(article)


    def get_top_tags(self,top):
        """ Return the top most used tags """
        return self.sorted_tags[:top]

    def get_top_tags_by_language(self, language, top):
        """ Return the top most used tags for a specific language """
        if language in self.sorted_tags_by_language:
            return self.sorted_tags_by_language[language][:top]
        return []

    def get_template(self,filename):
        template_dir = "templates"
        filename = os.path.join(template_dir, filename)
        with open(filename, 'r') as file:
            return file.read()
    
    def get_articles_by_tag(self, tag):
        return self.articles_by_tag.get(tag, [])
    
    def get_articles_by_date(self, language=None):
        """Sort articles by date, optionally filtered by language"""
        if language:
            articles = self.articles_by_language.get(language, [])
        else:
            articles = self.articles
        return sorted(articles, key=lambda x: x.date, reverse=True)
    
    # create html file, in html_dir, by transforming the markdown into html
    def generate_html_article(self, article):
        # New structure: html_dir/lang/YYYY/MM/DD/article_dir/index.html
        html_file_path = article.path
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(html_file_path), exist_ok=True)
        
        # Calculate relative CSS path from new location
        css_path = os.path.join(self.config.html_dir, "assets", self.config.css_file)
        css_rel_path = os.path.relpath(css_path, os.path.dirname(html_file_path))
        title = article.title
        
        # Get top tags for this language
        lang_top_tags = self.sorted_tags_by_language.get(article.language, [])[:self.config.top_tags]
        
        # Calculate relative path to tags from article location
        tags_path = f"../../../../../{article.language}/tags/"
        html_top_tags = "".join([f'<a href="{tags_path}{tag}.html"><span class="meta-box tag-{i+1}">{tag}</span></a>' for i, tag in enumerate(lang_top_tags)])

        # Get translations for hreflang
        translations = article.find_translations()
        hreflang_links = self.generate_hreflang_links(article, translations)
        
        # Language selector
        language_selector = self.generate_language_selector(article, translations)

        html_template = self.get_template("article.html")
        if article.language == "fr":
            html_template = self.get_template("article.html")
        elif article.language == "en":
            html_template = self.get_template("en-article.html")
        else:
            raise ValueError(f"language not supported : {article.language}")
        rendered_html = eval(f"f'''{html_template}'''")
        
        # Update image paths to point to shared location
        article_rel_path = os.path.relpath(article.path, self.config.html_dir)
        rendered_html = Website.update_image_paths(rendered_html, article_rel_path)

        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(rendered_html)

    def update_image_paths(content, article_path):
        # Get the directory of the article
        article_dir = os.path.dirname(article_path)
        
        # For multilingual articles, images are in the shared location
        # Convert from fr/2025/11/10/floating-point to 2025/11/10/floating-point  
        shared_path = article_dir
        if article_dir.startswith('fr/') or article_dir.startswith('en/'):
            shared_path = article_dir.split('/', 1)[1]  # Remove language prefix
        
        # Define the regex pattern to match the <a href> tags with specific suffixes
        href_pattern = r'(<a href="([^"]+\.(?:png|jpg|jpeg|svg|excalidraw|txt))">)'
        
        # Define the regex pattern to match the <img src> tags with specific suffixes
        src_pattern = r'(<img[^>]*\s+src="([^"]+\.(?:png|jpg|jpeg|svg))"[^>]*>)'
        
        def replace_path(match, pattern_type):
            if pattern_type == 'href':
                full_tag, href = match.groups()
                # Create relative path to shared image location
                full_path = f"../../../../../{shared_path}/{href}"
                return full_tag.replace(f'href="{href}"', f'href="{full_path}"')
            elif pattern_type == 'src':
                full_tag, src = match.groups()
                # Create relative path to shared image location  
                full_path = f"../../../../../{shared_path}/{src}"
                return full_tag.replace(f'src="{src}"', f'src="{full_path}"')
        
        # Use re.sub with a replacement function, ignoring case
        updated_content = re.sub(href_pattern, lambda m: replace_path(m, 'href'), content, flags=re.IGNORECASE)
        updated_content = re.sub(src_pattern, lambda m: replace_path(m, 'src'), updated_content, flags=re.IGNORECASE)
        
        return updated_content

    # generate the main page for the site
    def generate_tag_pages(self):
        """Generate tag pages for each language"""
        # Get all languages from the articles
        languages = set(article.language for article in self.articles)
        
        for language in languages:
            # Create tags directory for this language
            tags_dir = os.path.join(self.config.html_dir, language, "tags")
            os.makedirs(tags_dir, exist_ok=True)
            
            # Group articles by tag for this specific language
            articles_by_tag_lang = {}
            if language in self.articles_by_language:
                for article in self.articles_by_language[language]:
                    for tag in article.tags:
                        if tag not in articles_by_tag_lang:
                            articles_by_tag_lang[tag] = []
                        articles_by_tag_lang[tag].append(article)
            
            # Generate a page for each tag in this language
            for tag in articles_by_tag_lang:
                articles = articles_by_tag_lang[tag]
                tag_articles = ""
                
                # Build the list of articles for this tag
                for article in articles:
                    article_link = os.path.relpath(article.path, tags_dir)
                    tag_articles += f'<p><a href="{article_link}">{article.title}</a> - {article.date}</p>'
                
                # Get top tags for this language
                top_tags = self.sorted_tags_by_language.get(language, [])[:self.config.top_tags]
                html_top_tags = "".join([f'<a href="{t}.html"><span class="meta-box tag-{i+1}">{t}</span></a>' for i, t in enumerate(top_tags)])
                
                # Use language-specific template
                template_name = f"{language}-tag.html" if language != self.config.default_language else "tag.html"
                try:
                    html_template = self.get_template(template_name)
                except FileNotFoundError:
                    # Fallback to default template if language-specific template doesn't exist
                    html_template = self.get_template("tag.html")
                
                tag_name = tag
                rendered_html = eval(f"f'''{html_template}'''")
                
                # Write the tag page file
                tag_file_path = os.path.join(tags_dir, f"{tag}.html")
                with open(tag_file_path, 'w', encoding='utf-8') as f:
                    f.write(rendered_html)

    def generate_index(self):
        """Generate language-specific index pages"""
        # Generate index for each supported language
        for lang in self.config.get('supported_languages') or ['fr', 'en']:
            self.generate_language_index(lang)
        
        # Generate a root index that redirects to default language
        self.generate_root_index()
    
    def generate_language_index(self, language):
        """Generate index pages for a specific language"""
        if language not in self.articles_by_language:
            return
        
        lang_articles = self.articles_by_language[language]
        if not lang_articles:
            return
            
        # Create language directory
        lang_dir = os.path.join(self.config.html_dir, language)
        os.makedirs(lang_dir, exist_ok=True)
        
        total_pages = math.ceil(len(lang_articles) / self.config.nb_articles_per_page)
        
        for page in range(total_pages):
            start = page * self.config.nb_articles_per_page
            end = start + self.config.nb_articles_per_page
            articles = lang_articles[start:end]
            
            page_title = f"Page {page+1} of {total_pages}" if total_pages > 1 else ""
            html_articles = ""
            template_name = "embedded_article.html" if self.config.get("show_full_content") else "embedded_article_summary.html"
            html_template = self.get_template(template_name)
            
            # Language-specific CSS path
            css_path = os.path.join("../assets", self.config.css_file)
            
            for article in articles:
                # Calculate relative path from language index to article
                subpath = os.path.relpath(article.path, lang_dir)
                content = eval(f"f'''{html_template}'''")
                
                if self.config.get("show_full_content"):
                    content = Website.update_image_paths(content, subpath)
                html_articles += content
                
            # Language-specific navigation
            link_prev = ""
            link_next = ""
            if page == 1:
                link_prev = "index.html"
            elif page > 1:
                link_prev = f'index-{page-1}.html'
            if page < total_pages - 1:
                link_next = f'index-{page+1}.html'

            print(f"Generating {language} index page {page} {link_prev=} {link_next=}")
            
            # Language-specific top tags
            lang_top_tags = self.sorted_tags_by_language.get(language, [])[:self.config.top_tags]

            html_top_tags = "".join([f'<a href="tags/{tag}.html"><span class="meta-box tag-{i+1}">{tag}</span></a>' for i, tag in enumerate(lang_top_tags)])

            # Generate language selector for index
            language_selector = self.generate_index_language_selector(language)
            
            if language == "fr":
                html_template = self.get_template("index.html")
            elif language == "en":
                html_template = self.get_template("en-index.html")
            else:
                raise ValueError(f"language not supported : {language}")
            
            rendered_html = eval(f"f'''{html_template}'''")
            
            # Save in language directory
            if page == 0:
                html_file_path = os.path.join(lang_dir, "index.html")
            else:
                html_file_path = os.path.join(lang_dir, f"index-{page}.html")
            
            with open(html_file_path, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
    
    def generate_root_index(self):
        """Generate root index that redirects to default language"""
        default_lang = self.config.get('default_language') or 'fr'
        
        # Simple redirect page
        redirect_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=/{default_lang}/">
    <title>Redirecting...</title>
</head>
<body>
    <p>Redirecting to <a href="/{default_lang}/">main site</a>...</p>
</body>
</html>'''
        
        root_index_path = os.path.join(self.config.html_dir, "index.html")
        with open(root_index_path, 'w', encoding='utf-8') as f:
            f.write(redirect_html)
    
    def generate_index_language_selector(self, current_language):
        """Generate language selector for index pages"""
        language_flags = {"fr": "🇫🇷", "en": "🇬🇧"}
        selector_links = []
        
        for lang in self.config.get('supported_languages') or ['fr', 'en']:
            if lang in self.articles_by_language and self.articles_by_language[lang]:
                flag = language_flags.get(lang, lang.upper())
                is_current = lang == current_language
                css_class = 'lang-current' if is_current else 'lang-link'
                selector_links.append(f"""<a href="../{lang}" onclick="document.cookie='lang={lang}; path=/; max-age='+(60*60*24*365)" class="{css_class}">{flag} {lang.upper()}</a>""")
        
        return " | ".join(selector_links)

    def generate_hreflang_links(self, article, translations):
        """Generate hreflang links for multilingual SEO"""
        hreflang_links = []
        site_url = self.config.get('site_url')
        
        for lang, translation_path in translations.items():
            # Generate URL: https://example.com/fr/2025/11/10/floating-point/
            rel_path = translation_path.replace(self.config.md_dir + "/", "")
            path_parts = rel_path.split("/")
            if len(path_parts) >= 4:  # year/month/day/article/lang.md
                article_path = "/".join(path_parts[:-1])  # remove lang.md
                url = f"{site_url}/{lang}/{article_path}/"
                hreflang_links.append(f'<link rel="alternate" hreflang="{lang}" href="{url}" />')
        
        # Add canonical link (prefer original language or default)
        canonical_lang = article.language
        if canonical_lang in translations:
            rel_path = translations[canonical_lang].replace(self.config.md_dir + "/", "")
            path_parts = rel_path.split("/")
            if len(path_parts) >= 4:
                article_path = "/".join(path_parts[:-1])
                canonical_url = f"{site_url}/{canonical_lang}/{article_path}/"
                hreflang_links.append(f'<link rel="canonical" href="{canonical_url}" />')
        
        return "\n".join(hreflang_links)
    
    def generate_language_selector(self, article, translations):
        """Generate language selector HTML"""
        language_flags = {"fr": "🇫🇷", "en": "🇬🇧"}
        selector_links = []
        
        for lang in self.config.get('supported_languages') or ['fr', 'en']:
            if lang in translations:
                # Calculate relative URL to other language version  
                # From /lang/2025/11/10/article/ to /lang/2025/11/10/article/
                rel_path = translations[lang].replace(self.config.md_dir + "/", "")
                path_parts = rel_path.split("/")
                if len(path_parts) >= 4:
                    article_path = "/".join(path_parts[:-1])  # remove lang.md
                    lang_url = f"../../../../../{lang}/{article_path}/"
                    flag = language_flags.get(lang, lang.upper())
                    is_current = lang == article.language
                    css_class = 'lang-current' if is_current else 'lang-link'
                    selector_links.append(f"""<a href="{lang_url}" onclick="document.cookie='lang={lang}; path=/; max-age='+(60*60*24*365)" class="{css_class}">{flag} {lang.upper()}</a>""")
        
        return " | ".join(selector_links)

    

if __name__ == "__main__":
    conf = Configuration()
    www = Website(conf)
    www.init_html()
    www.init_articles()

    www.generate_index()

    www.generate_tag_pages()

    for article in www.articles:
        print(f"Generating html for article {article.title}")
        www.generate_html_article(article)
            
