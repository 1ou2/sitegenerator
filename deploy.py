# Deploy to remote server
import subprocess
import os
from dotenv import load_dotenv

def deploy():
    load_dotenv()
    
    server = os.getenv("SERVER")
    site_dir = os.getenv("SITE_DIR")
    html_dir = os.getenv("HTML_DIR", "html")
    
    if not server or not site_dir:
        print("Error: SERVER and SITE_DIR must be set in .env file")
        return
    
    # Backup remote html directory
    backup_cmd = f"ssh ubuntu@{server} 'cd {site_dir} && mv html html_backup_$(date +%Y%m%d_%H%M%S)'"
    subprocess.run(backup_cmd, shell=True)
    
    # Copy local html to remote
    copy_cmd = f"scp -r {html_dir} ubuntu@{server}:{site_dir}/"
    subprocess.run(copy_cmd, shell=True)

    # check deployment - use curl to fetch the homepage
    # site_dir should be like /var/www/mysite
    # check if we get a 200 OK response
    domain = site_dir.split('/')[-1]
    check_cmd = f"curl -o /dev/null -s -w '%{{http_code}}' https://{domain}"
    result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
    if result.stdout.strip() != "200":
        print("Deployment failed: Unable to reach the site or non-200 response")
        return
    
    print(f"Deployment completed to {server}:{site_dir}")

if __name__ == "__main__":
    deploy()
    