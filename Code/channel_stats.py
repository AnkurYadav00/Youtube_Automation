import time
from bs4 import BeautifulSoup as bs
import requests
from selenium.webdriver import Keys
import pandas as pd
# from code_porperties import API_KEY
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from Code import videos_thumbnail_extraction

thumbnails = "//a[@id='thumbnail']//img"
video_links = "//a[@id='thumbnail' and @class='yt-simple-endpoint inline-block style-scope ytd-thumbnail']"
titles = "//a[@id = 'video-title-link']"
views_total = "//a[@id = 'video-title-link']/../..//div[@id='metadata-line']/span[1]"
comments_count = "//h2[@id='count']//span[1]"
likes_total = "//div[@id='actions']//ytd-segmented-like-dislike-button-renderer//span"
each_comment = '//div[@id="content"]//yt-formatted-string[@id="content-text"]'


url = "https://www.youtube.com/watch?v=5W9QiJo95Ws"


# extracts Channel link
def channel_url(video_url) -> str:
    try:
        channel_video_url = requests.get(video_url)
        channel_video_url.encoding = "utf-8"
        video_page = bs(channel_video_url.text, 'html.parser')
        channel_video_url_01 = video_page.find_all('div')
        channel_link = channel_video_url_01[0].find_all_next('link')[1].get('href')
        return channel_link
    except Exception as e:
        raise e


# channel_id = channel_url(url)[28:]
channel_id = channel_url(url)

video_stats = {
    'titles': [],
    'videos_url': [],
    'views': [],
    'likes': [],
    'comments': []
}


def channel_stats(chnl_id: str, no_of_videos: int):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    videos_page_url = chnl_id + '/videos'
    driver.get(videos_page_url)
    time.sleep(3)

    def scroll_page():
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(3)

    views_element = []
    download_file = videos_thumbnail_extraction.files_download()
    try:
        while len(views_element) < 5:
            scroll_page()
            videos_elements = driver.find_elements(By.XPATH, "//a[@id = 'video-title-link']")
            views_element = driver.find_elements(By.XPATH,
                                                 "//a[@id = 'video-title-link']/../..//div[@id='metadata-line']/span[1]")
            # print(len(views_element))
            download_file.img_download(thumbnails, driver, no_of_videos, videos_elements)
        for i, j in zip(videos_elements, views_element):
            try:
                video_stats['videos_url'].append(i.get_attribute('href'))
                video_stats['titles'].append(i.text)
                video_stats['views'].append(j.text)
                # print(i.get_attribute('href'), " ", i.text, " ", j.text)
            except Exception as e:
                raise e
    except Exception as e:
        raise e
    for i in video_stats['videos_url'][0:no_of_videos]:
        videos_required_files_data(i, driver)


def videos_required_files_data(url, driver):
    driver.get(url)

    def scroll_page():
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

    try:
        scroll_page()
        scroll_page()
        total_comments = driver.find_element(By.XPATH, "//h2[@id='count']//span[1]").text
        likes = driver.find_element(By.XPATH,
                                    "//div[@id='actions']//ytd-segmented-like-dislike-button-renderer//span").text
    except Exception as e:
        raise 'ERROR : page not loaded'

    comments_elements, counter, comments_list = [], 0, []

    while int(total_comments.replace(",", "")) != len(comments_elements):
        print(int(total_comments), len(comments_elements))
        old_length = len(comments_elements)
        scroll_page()
        comments_elements = driver.find_elements(By.XPATH,
                                                 '//div[@id="content"]//yt-formatted-string[@id="content-text"]')
        if old_length == len(comments_elements):
            counter += 1
            # print(counter)
        if counter >= 4:
            for j in comments_elements:
                comments_list.append(j.text)
                print("Comments:   ->   ",j.text)
            break
    else:
        for j in comments_elements:
            comments_list.append(j.text)

    video_stats['comments'].extend(comments_list)
    video_stats['likes'].append(likes)


# title_list(channel_url(url))

def dict_to_excel(channel_name, data):
    df = pd.DataFrame(data)
    df.to_excel(f'{channel_name}.xlsx', sheet_name='Sheet1', startcol=0, startrow=0, index=False)


def fun_calls(channel_name: str, videos_total: int):
    channel_stats(channel_name, videos_total)
    # for i, j in video_stats.items():
    #     print(i, "----->", j)
    #     print(len(j))
    required_stats = {
        'titles': video_stats['titles'][:len(video_stats['likes'])],
        'videos_url': video_stats['videos_url'][:len(video_stats['likes'])],
        'views': video_stats['views'][:len(video_stats['likes'])],
        'likes': video_stats['likes'][:len(video_stats['likes'])],
        'comments': video_stats['comments'][:len(video_stats['likes'])]
    }
    print(required_stats)
    # dict_to_excel(channel_name, required_stats)
    return required_stats

fun_calls(channel_id,3)
