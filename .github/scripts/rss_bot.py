import feedparser
import os
from datetime import datetime
import time
import yaml

def fetch_and_create_files(rss_urls_file):
    with open(rss_urls_file, 'r', encoding='utf-8') as file:
        rss_urls = [line.strip() for line in file.readlines()]

    folder_path = "_posts"
    os.makedirs(folder_path, exist_ok=True)

    for rss_url in rss_urls:
        print(f"Fetching RSS feed from {rss_url}...")
        feed = feedparser.parse(rss_url)

        for entry in feed.entries:
            title = entry.title
            description_html = entry.summary
            link = entry.link
            date_published = entry.published_parsed if hasattr(entry, 'published_parsed') else None

            if date_published:
                # Convert date to a readable format
                date_str = datetime.utcfromtimestamp(time.mktime(date_published)).strftime('%Y-%m-%d')
            else:
                date_str = "N/A"

            # Create a slug from the title for the file name
            slug = title.lower().replace(' ', '_')
            file_path = f"{folder_path}/{date_str}-{slug}.md"

            # Check if the title includes "bug bytes"
            if "bug bytes" in title.lower():
                # If the title includes "bug_bytes," use tags only without description
                frontmatter_data = {"title": title, "tags": ["bug_bytes"], "link": link, "date": date_str}
            else:
                # If the title does not include "bug_bytes," include description
                description = description_html.replace('\n', ' ').strip()
                frontmatter_data = {"title": title, "description": description, "link": link, "date": date_str}

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("---\n")
                yaml.dump(frontmatter_data, file, default_flow_style=False, allow_unicode=True)
                file.write("---\n")

            print(f"File created: {file_path}")

if __name__ == "__main__":
    rss_urls_file = '../rss_urls.txt'
    fetch_and_create_files(rss_urls_file)
