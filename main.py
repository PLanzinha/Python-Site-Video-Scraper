import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import time
from collections import deque


def find_video_urls(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html5lib')

    video_urls = []
    video_tags = soup.find_all('video')
    for video in video_tags:
        if 'src' in video.attrs:
            video_url = video['src']
            if video_url.startswith('/word/') or video_url.startswith('/media/'):
                video_urls.append(video_url)

    return video_urls


def download_video(video_url, download_folder):
    response = requests.get(video_url, stream=True)
    response.raise_for_status()

    file_name = os.path.basename(video_url)
    folder_name = os.path.splitext(file_name)[0]
    folder_path = os.path.join(download_folder, folder_name)

    os.makedirs(folder_path, exist_ok=True)

    save_path = os.path.join(folder_path, file_name)

    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    # print("Downloaded video:", video_url)


def search_and_download_videos(website_url, download_folder, start_number, end_number):
    base_url = 'https://www.handspeak.com/'
    visited_pages = set()
    downloaded_videos = set()

    visited_links_file = os.path.join(download_folder, 'links.txt')

    if os.path.exists(visited_links_file):
        with open(visited_links_file, 'r') as file:
            visited_pages = set(file.read().splitlines())

    queue = deque([website_url])

    while queue:
        page_url = queue.popleft()

        if page_url in visited_pages:
            continue
        visited_pages.add(page_url)

        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html5lib')  # Use html5lib parser

        print(page_url)

        video_urls = find_video_urls(page_url)

        for video_url in video_urls:
            video_url_full = urljoin(base_url, video_url)
            if video_url_full not in downloaded_videos:
                try:
                    download_video(video_url_full, download_folder)
                    downloaded_videos.add(video_url_full)
                except requests.exceptions.HTTPError:
                    print("Failed to download video:", video_url_full)

        page_links = [a['href'] for a in soup.find_all('a', href=True)]

        for link in page_links:
            link_url = urljoin(page_url, link)
            if link_url not in visited_pages:
                link_number = link_url.split('/')[-2]
                if link_number.isdigit() and start_number < int(link_number) <= end_number:
                    queue.append(link_url)
                visited_pages.add(link_url)
                time.sleep(1)

    with open(visited_links_file, 'w') as file:
        file.write('\n'.join(visited_pages))



start_url = 'https://www.handspeak.com/word/8227/'
end_url = 'https://www.handspeak.com/word/10972/'
download_folder = 'D:/videos_data'

start_number = int(start_url.split('/')[-2])
end_number = int(end_url.split('/')[-2])

for number in range(start_number + 1, end_number + 1):
    website_url = f'https://www.handspeak.com/word/{number}/'
    search_and_download_videos(website_url, download_folder, start_number, end_number)
