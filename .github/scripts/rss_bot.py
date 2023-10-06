import feedparser
import os
from datetime import datetime
import time

def fetch_and_create_files(rss_urls_file):
    with open(rss_urls_file, 'r') as file:
        rss_urls = [line.strip() for line in file.readlines()]

    folder_path = "articles"
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
                date_str = datetime.utcfromtimestamp(time.mktime(date_published)).strftime('%Y-%m-%d %H:%M:%S UTC')
            else:
                date_str = "N/A"

            # Check if the title includes "bug_bytes"
            is_bug_bytes = "bug_bytes" in title.lower()

            # Generate file content
            file_content = f"title: {title}\nlink: {link}\ndate: {date_str}"
            if not is_bug_bytes:
                # If the title does not include "bug_bytes," include description
                description = description_html.replace('\n', ' ').strip()
                file_content += f"\ndescription: {description}"

            # Ensure the file name is unique
            clean_title = title.lower().replace(' ', '_')
            file_name = f"{folder_path}/{clean_title}_{int(time.time())}.md"

            with open(file_name, 'w') as file:
                file.write(file_content)
            print(f"File created: {file_name}")

if __name__ == "__main__":
    rss_urls_file = '../rss_urls.txt'
    fetch_and_create_files(rss_urls_file)
