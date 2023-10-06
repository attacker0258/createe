import feedparser
import os

def fetch_and_create_files(rss_url):
    feed = feedparser.parse(rss_url)

    folder_path = "articles"
    os.makedirs(folder_path, exist_ok=True)

    for entry in feed.entries:
        title = entry.title
        description = entry.summary.replace('\n', ' ')
        file_content = f"title: {title}\ndescription: {description}"

        file_name = f"{folder_path}/{title.lower().replace(' ', '_')}.md"
        with open(file_name, 'w') as file:
            file.write(file_content)

if __name__ == "__main__":
    rss_url = 'YOUR_RSS_FEED_URL'
    fetch_and_create_files(rss_url)
