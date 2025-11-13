import markdown,yaml
from markdown.extensions import fenced_code, codehilite
import os,shutil,re
from dotenv import load_dotenv

class Article:
    def __init__(self,md_file_path=""):
        self.meta_data = {}
        self.md_content = ""
        self.md_file_path = md_file_path
        self.prev_path = ""
        self.next_path = ""
        self.path = ""
        self.rel_path = ""
        
        if md_file_path:
            self.parse_markdown_article()

        

    def __repr__(self):
        return f"Article: {self.meta_data}"
    
    def check_metadata(self):
        """Check if required metadata fields are present"""
        required_fields = ["title", "date", "tags"]
        for field in required_fields:
            if field not in self.meta_data:
                return False
            
        # create html_tags field with language-specific links
        language = getattr(self, 'language', 'fr')
        self.html_tags = "".join([f'<a href="../../../../../{language}/tags/{tag}.html"><span class="meta-box tag-{i+1}">{tag}</span></a>' for i, tag in enumerate(self.tags)])
        return True
    

    def get_md_content(self):
        return self.md_content

    def parse_metadata(self):
        self.title = self.meta_data.get("title", "")
        date_str = self.meta_data.get("date", "")
        # Convert date string to consistent format for sorting
        if isinstance(date_str, str):
            self.date = date_str
        else:
            self.date = str(date_str) if date_str else ""
        # tags are separated by commas, split the tags string and strip spaces
        self.tags = [t.strip() for t in self.meta_data.get("tags", "").split(",")]
        self.abstract = self.meta_data.get("abstract", "")
        self.thumbnail = self.meta_data.get("thumbnail", "")
        # Add language support
        self.language = self.meta_data.get("language", "fr")  # Default to French
        
        # Extract article slug from path for translations
        self.article_slug = self.extract_article_slug()
        
        if not self.check_metadata():
            print(f"Error: Invalid metadata")
    
    def extract_article_slug(self):
        """Extract article slug from file path for multilingual support"""
        if not self.md_file_path:
            return ""
        
        # Extract the article directory name from path like:
        # articles/2025/11/10/floating-point/fr.md -> floating-point
        path_parts = self.md_file_path.split(os.sep)
        
        # Find the article directory (the one before language file)
        for i, part in enumerate(path_parts):
            if part in ['fr.md', 'en.md']:
                if i > 0:
                    return path_parts[i-1]
                break
        
        return ""
    
    def get_translations_dir(self):
        """Get the directory containing all translations of this article"""
        if not self.md_file_path:
            return ""
        
        return os.path.dirname(self.md_file_path)
    
    def find_translations(self):
        """Find all available translations of this article"""
        translations = {}
        translations_dir = self.get_translations_dir()
        
        if not translations_dir or not os.path.exists(translations_dir):
            return translations
        
        # Look for language files in the same directory
        for filename in os.listdir(translations_dir):
            if filename.endswith('.md'):
                lang_code = filename.replace('.md', '')
                if lang_code in ['fr', 'en']:  # Supported languages
                    translations[lang_code] = os.path.join(translations_dir, filename)
        
        return translations
        if not self.check_metadata():
            print(f"Error: Invalid metadata")

    def parse_markdown_article(self):
        """Parse markdown file, extract meta data and content"""
        self.html = ""
        with open(self.md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

            # Use regex to extract the YAML front matter
            yaml_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
            match = yaml_pattern.match(content)

            if match:
                yaml_content = match.group(1)
                md_content = content[match.end():]
                self.html = markdown.markdown(
                    md_content,
                    extensions=[
                        'fenced_code',
                        'codehilite',
                        'tables',
                        'markdown.extensions.nl2br'
                    ]
                )
                self.snippet = markdown.markdown(md_content)[:200]
                # Parse YAML content
                try:
                    meta_data = yaml.safe_load(yaml_content)
                except yaml.YAMLError as e:
                    # If YAML parsing fails, try a custom approach
                    # some data contains ':' so we split on the first ':' encountered
                    #print(f"Error parsing YAML in {self.md_file_path}")
                    meta_data = {}
                    lines = yaml_content.split('\n')
                    current_key = None
                    current_value = []
                    
                    for line in lines:
                        if ':' in line and not line.startswith(' ') and not line.startswith('\t'):
                            if current_key:
                                meta_data[current_key] = ' '.join(current_value).strip()
                            key, value = line.split(':', 1)
                            current_key = key.strip()
                            current_value = [value.strip()] if value.strip() else []
                        elif current_key and line.strip():
                            current_value.append(line.strip())
                    
                    if current_key:
                        meta_data[current_key] = ' '.join(current_value).strip()

            else:
                meta_data = {}
                md_content = content

            self.meta_data = meta_data
            self.md_content = md_content
            self.parse_metadata()

if __name__ == "__main__":
    pass
        