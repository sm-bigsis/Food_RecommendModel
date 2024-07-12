from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os
import requests

options = Options()
options.add_argument("--lang=en")
options.add_argument('--start-maximized')  # 창을 최대화
options.add_argument('--disable-notifications')  # 알림 비활성화

# 위치 권한 차단
prefs = {
    "profile.default_content_setting_values.geolocation": 2  # 위치 요청 차단
}
options.add_experimental_option("prefs", prefs)

driver_path = '/opt/homebrew/bin/chromedriver'  # chromedriver 경로
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

def scroll_and_collect_reviews(driver, scroll_pause_time=2):
    popup = driver.find_element(By.CLASS_NAME, 'review-dialog-list')
    last_height = driver.execute_script("return arguments[0].scrollHeight", popup)

    while True:
        # "more" 버튼 클릭
        more_buttons = driver.find_elements(By.CLASS_NAME, "review-more-link")
        if not more_buttons:
            break  # "more" 버튼이 더 이상 없으면 반복 종료

        for button in more_buttons:
            try:
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
    review_data = []
    reviews = driver.find_elements(By.CLASS_NAME, 'WMbnJf')
    for idx, review in enumerate(reviews[:50], start=1):
        try:
            review_text = review.find_element(By.CLASS_NAME, 'review-full-text').text
            review_id = review.find_element(By.CLASS_NAME, 'TSUbDb').text

            # 사진 URL 수집 및 저장
            photo_urls = []
            photos = review.find_elements(By.CLASS_NAME, 'JrO5Xe')
            for photo_idx, photo in enumerate(photos):
                photo_url = photo.get_attribute('src')
                photo_urls.append(photo_url)

                # 사진 저장
                response = requests.get(photo_url)
                if response.status_code == 200:
                    folder_name = '/Users/shinseohyunn/Desktop/bigsis/reviews'
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)

                    photo_filename = f'{folder_name}/{review_id}_photo_{photo_idx+1}.jpg'
                    with open(photo_filename, 'wb') as f:
                        f.write(response.content)

            # 리뷰 데이터 저장
            review_data.append({
                'Review ID': review_id,
                'Review Text': review_text,
                'Photo URLs': photo_urls
            })

            # 수집된 리뷰 데이터 로그 출력
            print(f'Review {idx} collected.')

        except Exception as e:
            # 에러 발생 시 스크린샷 저장
            error_screenshot_path = f'/Users/shinseohyunn/Desktop/bigsis/reviews/error_{driver.current_url.replace("https://www.google.com/search?", "").replace("/", "_")}.png'
            driver.save_screenshot(error_screenshot_path)
            print(f'Error processing review {idx}: {str(e)}')
            print(f'Screenshot saved: {error_screenshot_path}')

    return review_data


review_lst = [
    'https://www.google.com/search?q=Jun+Won+Dak&oq=Jun+Won+Dak&gs_lcrp=EgZjaHJvbWUyDAgAEEUYORjjAhiABDINCAEQLhivARjHARiABDIHCAIQABiABDIHCAMQABiABDIICAQQABgWGB4yDQgFEAAYhgMYgAQYigUyDQgGEAAYhgMYgAQYigUyDQgHEAAYhgMYgAQYigUyCggIEAAYgAQYogQyCggJEAAYgAQYogTSAQcxODFqMGo5qAIAsAIB&sourceid=chrome&ie=UTF-8#lrd=0x80c2b942b6d08167:0x31833e2529443c12,1,,,,'
]

for store_url in review_lst:
    try:
        driver.get(store_url)
        time.sleep(10)  # 페이지가 로드될 때까지 대기

        # 스크롤 및 리뷰 수집
        review_data = scroll_and_collect_reviews(driver)

        # 데이터 프레임 생성 및 CSV 저장
        df = pd.DataFrame(review_data)
        csv_filename = '/Users/shinseohyunn/Desktop/bigsis/reviews/reviews.csv'
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
