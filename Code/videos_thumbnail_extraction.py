import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
import loggers


class files_download():
    def img_download(self, thumbnail_xpath: str, driver: webdriver, no_videos: int, names):
        self.img_urls = driver.find_elements(By.XPATH, thumbnail_xpath)
        print(f".................{self.img_urls}")
        # if not os.path.exists('./Downloads_file/images'):
        os.makedirs('./Downloads_file/images', exist_ok=True)
        for img_url, name in zip(self.img_urls[:no_videos], names):
            val = img_url.get_attribute('src')
            if val is not None:
                self.response = requests.get(val)
                if self.response.status_code == 200:
                    with open(f'./Downloads_file/images/{name.text[:10]}.jpg', 'wb') as file:
                        file.write(self.response.content)
                        print("image_downloaded")
                else:
                    print(" not 200")
            else:
                print("None")

    def download_video(video_xpath: str, driver: webdriver, file_name: str):
        video_urls = driver.find_elements(By.XPATH, video_xpath)
        for video_url in video_urls:
            val = video_url.get_attribute('href')
            if val is not None:
                response = requests.get(val)
                os.makedirs(f'/Downloads_file/videos')
                if response.status_code == 200:
                    with open(f'{file_name}.mkv', 'wb') as file:
                        file.write(response.content)
                        print("video downloaded")
