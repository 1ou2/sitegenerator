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
        self.config = {
            "md_dir": self.md_dir,
            "html_dir": self.html_dir,
            "top_tags": self.top_tags,
            "nb_articles_per_page": self.nb_articles_per_page,
            "show_full_content": self.show_full_content
        }

    def get(self, key):
        return self.config[key]
    
class Website:
    def __init__(self,conf):
        self.config = conf
        self.articles = []
        self.articles_by_tag = {}

    # get list of all markdown files
    def get_markdown_files(self):
        md_files = []
        for root, dirs, files in os.walk(self.config.md_dir):
            for file in files:
                if file.endswith(".md"):
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

        # sort by date
        self.articles = self.get_articles_by_date()
        
        # add path to this article
        for article in self.articles:
            article.path = article.md_file_path.replace(self.config.md_dir, self.config.html_dir).replace(".md", ".html")

        # add links to previous and next articles
        for i, article in enumerate(self.articles):
            if i > 0:
                article.prev_path = os.path.relpath(self.articles[i-1].path,os.path.dirname(article.path)) 
            if i < len(self.articles) - 1:
                article.next_path = os.path.relpath(self.articles[i+1].path,os.path.dirname(article.path))

        tag_count = {}
        for article in self.articles:
            for tag in article.tags:
                if tag not in tag_count:
                    tag_count[tag] = 0
                tag_count[tag] += 1
        # array of tags in count order from max to min
        self.sorted_tags =  [k for k,v in sorted(tag_count.items(), key=lambda x:x[1],reverse=True)]

    # html article has been created
    def add(self,article):
        self.articles.append(article)

        for tag in article.tags:
            if tag not in self.articles_by_tag:
                self.articles_by_tag[tag] = []
            self.articles_by_tag[tag].append(article)


    def get_top_tags(self,top):
        """ Return the top most used tags """
        return self.sorted_tags[:top]

    def get_template(self,filename):
        template_dir = "templates"
        filename = os.path.join(template_dir, filename)
        with open(filename, 'r') as file:
            return file.read()
    
    def get_articles_by_tag(self, tag):
        return self.articles_by_tag.get(tag, [])
    
    def get_articles_by_date(self):
        # sort articles by date
        return sorted(self.articles, key=lambda x: x.date, reverse=True)
    
    # create html file, in html_dir, by transforming the markdown into html
    def generate_html_article(self,article):
        # md files were copied in the html directory, we currently have 
        # html_dir/YYYY/MM/DD/article_dir/article.md
        # we will create html_dir/YYYY/MM/DD/article_dir/article.html
        html_file_path = article.md_file_path.replace(self.config.md_dir, self.config.html_dir).replace(".md", ".html")
        # css file path
        # html article is in html_dir/YYYY/MM/DD/article_dir/article.html
        # css file is in html_dir/assets/style.css
        css_path = os.path.join(self.config.html_dir,"assets", self.config.css_file)
        # variables used in the template
        css_rel_path = os.path.relpath(css_path, os.path.dirname(html_file_path))
        title = article.title
  
        top_tags = self.get_top_tags(self.config.top_tags)
        html_top_tags = "".join([f'<a href="../../../../tags/{tag}.html"><span class="meta-box tag-{i+1}">{tag}</span></a>' for i, tag in enumerate(top_tags)])

        html_template = self.get_template("article.html")
        rendered_html = eval(f"f'''{html_template}'''")
        
        

        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(rendered_html)

    def update_image_paths(content, article_path):
        # Get the directory of the article
        article_dir = os.path.dirname(article_path)
        
        # Define the regex pattern to match the <a href> tags with specific suffixes
        href_pattern = r'(<a href="([^"]+\.(?:png|jpg|jpeg|svg))">)'
        
        # Define the regex pattern to match the <img src> tags with specific suffixes
        src_pattern = r'(<img[^>]*\s+src="([^"]+\.(?:png|jpg|jpeg|svg))"[^>]*>)'
        
        def replace_path(match, pattern_type):
            if pattern_type == 'href':
                full_tag, href = match.groups()
                full_path = os.path.join(article_dir, href)
                return full_tag.replace(f'href="{href}"', f'href="{full_path}"')
            elif pattern_type == 'src':
                full_tag, src = match.groups()
                full_path = os.path.join(article_dir, src)
                return full_tag.replace(f'src="{src}"', f'src="{full_path}"')
        
        # Use re.sub with a replacement function, ignoring case
        updated_content = re.sub(href_pattern, lambda m: replace_path(m, 'href'), content, flags=re.IGNORECASE)
        updated_content = re.sub(src_pattern, lambda m: replace_path(m, 'src'), updated_content, flags=re.IGNORECASE)
        
        return updated_content

    # generate the main page for the site
    def generate_tag_pages(self):
        # Create tags directory
        tags_dir = os.path.join(self.config.html_dir, "tags")
        os.makedirs(tags_dir, exist_ok=True)
        
        for tag in self.articles_by_tag:
            articles = self.articles_by_tag[tag]
            tag_articles = ""
            
            for article in articles:
                article_link = os.path.relpath(article.path, tags_dir)
                tag_articles += f'<p><a href="{article_link}">{article.title}</a> - {article.date}</p>'
            
            top_tags = self.get_top_tags(self.config.top_tags)
            html_top_tags = "".join([f'<a href="{t}.html"><span class="meta-box tag-{i+1}">{t}</span></a>' for i, t in enumerate(top_tags)])
            
            html_template = self.get_template("tag.html")
            tag_name = tag
            rendered_html = eval(f"f'''{html_template}'''")
            
            tag_file_path = os.path.join(tags_dir, f"{tag}.html")
            with open(tag_file_path, 'w', encoding='utf-8') as f:
                f.write(rendered_html)

    def generate_index(self):
        total_pages = math.ceil(len(self.articles) / self.config.nb_articles_per_page)
        for page in range(total_pages):
            start = page * self.config.nb_articles_per_page
            end = start + self.config.nb_articles_per_page
            articles = self.articles[start:end]
            
            
            page_title = f"Page {page+1} of {total_pages}"
            html_top_tags = "hello"
            html_articles = ""
            template_name = "embedded_article.html" if self.config.get("show_full_content") else "embedded_article_summary.html"
            html_template = self.get_template(template_name)
            css_path = os.path.join("assets", self.config.css_file)
            for article in articles:
                subpath = os.path.relpath(article.path, self.config.html_dir)
                content = eval(f"f'''{html_template}'''")
                
                if self.config.get("show_full_content"):
                    content = Website.update_image_paths(content, subpath)
                html_articles += content
            link_prev = ""
            link_next = ""
            if page == 1:
                link_prev = "index.html"
            if page > 1:
                link_prev = f'index-{page-1}.html'
            if page < total_pages - 1:
                link_next = f'index-{page+1}.html'


            print(f"for page {page} {link_prev=} {link_next=}")
            top_tags = self.get_top_tags(self.config.top_tags)
            html_top_tags = "".join([f'<a href="tags/{tag}.html"><span class="meta-box tag-{i+1}">{tag}</span></a>' for i, tag in enumerate(top_tags)])

            html_template = self.get_template("index.html")
            rendered_html = eval(f"f'''{html_template}'''")
            
            if page == 0:
                html_file_path = os.path.join(self.config.html_dir, "index.html")
            else:
                html_file_path = os.path.join(self.config.html_dir, f"index-{page}.html")
            
            with open(html_file_path, 'w', encoding='utf-8') as f:
                f.write(rendered_html)

    

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
            
