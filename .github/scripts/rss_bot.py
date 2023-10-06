import feedparser
import os

def fetch_and_create_files(rss_url):
    print("Fetching RSS feed...")
    feed = feedparser.parse(rss_url)

    folder_path = "articles"
    os.makedirs(folder_path, exist_ok=True)

    for entry in feed.entries:
        title = entry.title
        description = entry.description
        file_content = f"title: {title}\ndescription: {description}"

        file_name = f"{folder_path}/{title.lower().replace(' ', '_')}.md"
        with open(file_name, 'w') as file:
            file.write(file_content)
        print(f"File created: {file_name}")

if __name__ == "__main__":
    rss_url = 'https://blog.intigriti.com/category/bugbytes/feed/'
    fetch_and_create_files(rss_url)
