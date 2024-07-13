from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os
import re
import requests

review = [
    'https://www.google.com/search?q=miss+korea+bbq&oq=miss+KOREA+BBQ&gs_lcrp=EgZjaHJvbWUqDAgAECMYJxiABBiKBTIMCAAQIxgnGIAEGIoFMhIIARAuGBQYrwEYxwEYhwIYgAQyDAgCEAAYFBiHAhiABDIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIGCAcQRRg90gEHMzI2ajBqOagCALACAA&sourceid=chrome&ie=UTF-8#lrd=0x89c259a8f0e6dff7:0xf690d3dfef37dcf,1,,,,',
    'https://www.google.com/search?q=hae+jang+chon+korean+bbq+restaurant&oq=Hae+Jang+Chon+Korean+BBQ+Restaurant&gs_lcrp=EgZjaHJvbWUqDAgAECMYJxiABBiKBTIMCAAQIxgnGIAEGIoFMg0IARAuGK8BGMcBGIAEMgwIAhAAGBQYhwIYgAQyBwgDEAAYgAQyBwgEEAAYgAQyBwgFEAAYgAQyBwgGEAAYgAQyBggHEEUYPdIBBzMyMmowajmoAgCwAgA&sourceid=chrome&ie=UTF-8#lrd=0x80c2b89b437ecda9:0xc6e1364fd48e3303,1,,,,',
    'https://www.google.com/search?q=seoul+k-b.b.q.%26+hotpot&oq=Seoul+K-B.B.Q.%26+HotPot&gs_lcrp=EgZjaHJvbWUqDAgAECMYJxiABBiKBTIMCAAQIxgnGIAEGIoFMg0IARAuGK8BGMcBGIAEMgcIAhAAGIAEMgcIAxAAGIAEMgcIBBAAGIAEMggIBRAAGBYYHjINCAYQABiGAxiABBiKBTIGCAcQRRg90gEHMjkxajBqOagCALACAA&sourceid=chrome&ie=UTF-8#lrd=0x876c7d5dd351069f:0x9892088474a76e99,1,,,,',
    'https://www.google.com/search?q=quarters+korean+bbq&oq=Quarters+Korean+BBQ&gs_lcrp=EgZjaHJvbWUqDAgAECMYJxiABBiKBTIMCAAQIxgnGIAEGIoFMhIIARAuGBQYrwEYxwEYhwIYgAQyDAgCEAAYFBiHAhiABDIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIGCAcQRRg90gEHMjY2ajBqOagCALACAA&sourceid=chrome&ie=UTF-8#lrd=0x80c2c77d3cd03da3:0x34cb953bda09e5f9,1,,,,',
    'https://www.google.com/search?q=Surisan&sca_esv=458fc5d25ecd7a59&sca_upv=1&gl=us&hl=en&pws=0&sxsrf=ADLYWIJut-Ke4EQvlbrrQYodSEs6bYdugQ%3A1720827019556&source=hp&ei=i7yRZrqrIPi6vr0P_ZiV6AY&iflsig=AL9hbdgAAAAAZpHKmwVjEmqjhLox7wKxxZhoi8jFg_uS&ved=0ahUKEwj6nOCZ1KKHAxV4na8BHX1MBW0Q4dUDCBc&uact=5&oq=Surisan&gs_lp=Egdnd3Mtd2l6IgdTdXJpc2FuMgoQIxiABBgnGIoFMgUQLhiABDIFEAAYgAQyCxAuGIAEGMcBGK8BMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIHEAAYgAQYCjIFEAAYgARIogNQ2AFY2AFwAXgAkAEAmAHBAaABwQGqAQMwLjG4AQPIAQD4AQL4AQGYAgKgAs0BqAIKwgIHECMYJxjqApgDBpIHAzEuMaAHkwo&sclient=gws-wiz#lrd=0x808580e3ef0f755d:0xcff30a7ad296edbf,1,,,,',
    'https://www.google.com/search?q=Quarters+Korean+BBQ&sca_esv=458fc5d25ecd7a59&sca_upv=1&gl=us&hl=en&pws=0&sxsrf=ADLYWIJozPQdsvTOCjlYbGQSwJh8JdDzDw%3A1720823157148&source=hp&ei=da2RZq2cB4fl2roP2M-O2Ac&iflsig=AL9hbdgAAAAAZpG7hWHuSu65QsS0XqE4ScZSFVfhw0FA&ved=0ahUKEwjtqoHoxaKHAxWHslYBHdinA3sQ4dUDCBc&uact=5&oq=Quarters+Korean+BBQ&gs_lp=Egdnd3Mtd2l6IhNRdWFydGVycyBLb3JlYW4gQkJRMgoQIxiABBgnGIoFMhEQLhiABBiRAhjHARiKBRivATIKEAAYgAQYFBiHAjIFEAAYgAQyBRAAGIAEMgsQABiABBiRAhiKBTILEAAYgAQYkQIYigUyBRAAGIAEMgUQABiABDIFEAAYgARI7wZQiQRYiQRwAXgAkAEAmAHHAaABxwGqAQMwLjG4AQPIAQD4AQL4AQGYAgOgAhSYAwCIBgGQBhS6BgYIARABGAiSBwEzoAcA&sclient=gws-wiz-serp#lrd=0x80c2c77d3cd03da3:0x34cb953bda09e5f9,1,,,,',
    'https://www.google.com/search?q=Surisan&sca_esv=458fc5d25ecd7a59&sca_upv=1&gl=us&hl=en&pws=0&sxsrf=ADLYWIKACEyr7xz49s5xhEYYyOiyggCEhw%3A1720823161054&ei=ea2RZon9AqLh2roPjfKwoAs&ved=0ahUKEwjJnfHpxaKHAxWisFYBHQ05DLQQ4dUDCA8&uact=5&oq=Surisan&gs_lp=Egxnd3Mtd2l6LXNlcnAiB1N1cmlzYW4yChAAGLADGNYEGEcyChAAGLADGNYEGEcyChAAGLADGNYEGEcyChAAGLADGNYEGEcyChAAGLADGNYEGEcyChAAGLADGNYEGEcyChAAGLADGNYEGEcyChAAGLADGNYEGEcyEBAAGIAEGLADGEMYyQMYigUyDhAAGIAEGLADGJIDGIoFMg4QABiABBiwAxiSAxiKBTINEAAYgAQYsAMYQxiKBTIZEC4YgAQYsAMYQxjHARjIAxiKBRivAdgBATITEC4YgAQYsAMYQxjIAxiKBdgBATIZEC4YgAQYsAMY0QMYQxjHARjIAxiKBdgBATIZEC4YgAQYsAMYQxjHARjIAxiKBRivAdgBATIZEC4YgAQYsAMYQxjHARjIAxiKBRivAdgBATIZEC4YgAQYsAMYQxjHARjIAxiKBRivAdgBATIZEC4YgAQYsAMYQxjHARjIAxiKBRivAdgBATIZEC4YgAQYsAMYQxjHARjIAxiKBRivAdgBAUi3B1CWBliWBnADeAGQAQCYAQCgAQCqAQC4AQPIAQD4AQL4AQGYAgOgAhSYAwCIBgGQBhS6BgYIARABGAiSBwEzoAcA&sclient=gws-wiz-serp#lrd=0x808580e3ef0f755d:0xcff30a7ad296edbf,1,,,,',
    'https://g.co/kgs/315U52Z'
]
review_lst = ['https://www.google.com/search?gl=us&hl=en&pws=0&sca_esv=458fc5d25ecd7a59&sca_upv=1&cs=1&output=search&q=Bap+Bowl+Korean+Food&ludocid=7606258533037607132&lsig=AB86z5VMwG5EWduPWnfJP-ZWE8za&kgs=42cd3ab734e9d3a2&shndl=-1&shem=lsde,lsp&source=sh/x/loc/act/m1/1#lrd=0x88e5b5011155ebcb:0x698edbd60b7d88dc,1,,,,']
options = Options()
options.add_argument("--lang=en")
options.add_argument('--start-maximized')  # 창을 최대화
options.add_argument('--disable-notifications')  # 알림 비활성화
options.add_argument('--disable-gpu')
options.add_argument('--headless')

# 위치 권한 차단
prefs = {
    "profile.default_content_setting_values.geolocation": 2  # 위치 요청 차단
}
options.add_experimental_option("prefs", prefs)

driver_path = '/opt/homebrew/bin/chromedriver'  # chromedriver 경로
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

def extract_url_from_style(style):
    """Extract URL from the background-image style attribute."""
    url_pattern = re.compile(r'url\((.*?)\)')
    match = url_pattern.search(style)
    if match:
        return match.group(1).strip('"')
    return None

def scroll_and_collect_reviews(driver, max_reviews=30, scroll_pause_time=2):
    popup = driver.find_element(By.CLASS_NAME, 'review-dialog-list')
    last_height = driver.execute_script("return arguments[0].scrollHeight", popup)

    collected_reviews = []
    review_count = 0

    while True:
        scroll_pause_time =+ 1
        # "more" 버튼 클릭
        more_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "review-more-link")))
        if not more_buttons:
            break  # "more" 버튼이 더 이상 없으면 반복 종료
        for button in more_buttons:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", button)  # 버튼이 보일 때까지 스크롤
                time.sleep(1)
                button.click()
                time.sleep(3)  # 새 리뷰가 로드될 때까지 충분한 시간 대기
            except Exception as e:
                print(f'Error clicking "more" button: {str(e)}')

        # 스크롤
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", popup)
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return arguments[0].scrollHeight", popup)
        if new_height == last_height:
            break
        last_height = new_height

        # "display:none" 속성을 가진 요소들을 보이게 만들기
        elements_to_show = driver.find_elements(By.XPATH, '//*[@style="display:none"]')
        for elem in elements_to_show:
            driver.execute_script("arguments[0].setAttribute('style', 'display:block;');", elem)

    # 리뷰 데이터 수집
    reviews = driver.find_elements(By.CLASS_NAME, 'WMbnJf')
    for review in reviews:
        try:
            review_text = review.find_element(By.CLASS_NAME, 'review-full-text').text
            review_id = review.find_element(By.CLASS_NAME, 'TSUbDb').text

            # 사진 URL 수집 및 저장
            photo_urls = []
            photos = review.find_elements(By.CLASS_NAME, 'JrO5Xe')
            for photo_idx, photo in enumerate(photos):
                style = photo.get_attribute('style')
                photo_url = extract_url_from_style(style)
                if photo_url:
                    photo_urls.append(photo_url)

                # 사진 저장 (각 가게별 폴더 생성)
                store_name = driver.title.split(' - ')[0].strip()
                folder_name = f'/Users/shinseohyunn/Desktop/bigsis/reviews/{store_name}'
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                photo_filename = f'{folder_name}/{review_id}_photo_{photo_idx+1}.jpg'
                with open(photo_filename, 'wb') as f:
                    f.write(requests.get(photo_url).content)

            # 리뷰 데이터 저장
            collected_reviews.append({
                'Store Name': store_name,
                'Review ID': review_id,
                'Review Text': review_text,
                'Photo URLs': photo_urls
            })

            review_count += 1
            print(f'Review {review_count} collected.')

            # 리뷰 개수가 max_reviews에 도달하면 종료
            if review_count >= max_reviews:
                return collected_reviews

        except Exception as e:
            print(f'Error processing review: {str(e)}')

    return collected_reviews


for store_url in review_lst:
    try:
        driver.get(store_url)
        time.sleep(10)  # 페이지가 로드될 때까지 대기

        # 스크롤 및 리뷰 수집
        review_data = scroll_and_collect_reviews(driver, max_reviews=500)

        # 데이터 프레임 생성 및 CSV 저장
        df = pd.DataFrame(review_data)
        store_name = driver.title.split(' - ')[0].strip()
        csv_filename = f'/Users/shinseohyunn/Desktop/bigsis/reviews/{store_name}.csv'
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f'Reviews saved to {csv_filename}')
        
        # 수집된 리뷰 데이터 개수 출력
        print(f'Number of reviews collected: {len(review_data)}')

    except Exception as e:
        # 에러 발생 시 스크린샷 저장
        error_screenshot_path = f'/Users/shinseohyunn/Desktop/bigsis/reviews/error_{store_url.replace("https://www.google.com/search?", "").replace("/", "_")}.png'
        driver.save_screenshot(error_screenshot_path)
        print(f'Error processing {store_url}: {str(e)}')
        print(f'Screenshot saved: {error_screenshot_path}')

driver.quit()
