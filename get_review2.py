from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os
import requests
import re  # Regular expression module to parse URLs

options = Options()
options.add_argument("--lang=en")
options.add_argument('--start-maximized')
options.add_argument('--disable-notifications')

prefs = {
    "profile.default_content_setting_values.geolocation": 2
}
options.add_experimental_option("prefs", prefs)

driver_path = 'C:/Users/piano/.wdm/drivers/chromedriver/win64/126.0.6478.126/chromedriver-win32/chromedriver.exe'
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

def extract_url_from_style(style):
    """Extract URL from the background-image style attribute."""
    url_pattern = re.compile(r'url\((.*?)\)')
    match = url_pattern.search(style)
    if match:
        return match.group(1).strip('"')
    return None

def scroll_and_collect_reviews(driver, max_reviews=50, scroll_pause_time=2):
    popup = driver.find_element(By.CLASS_NAME, 'review-dialog-list')
    last_height = driver.execute_script("return arguments[0].scrollHeight", popup)

    collected_reviews = []
    review_count = 0

    while True:
        # "more" 버튼 클릭
        more_buttons = driver.find_elements(By.CLASS_NAME, "review-more-link")
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
        reviews = driver.find_elements(By.CLASS_NAME, 'WMbnJf')
        for review in reviews:
            try:
                review_text = review.find_element(By.CLASS_NAME, 'review-full-text').text
                review_id = review.get_attribute('data-review-id')

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
                        folder_name = f'C:/해커톤/reviews/{store_name}'
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
                # 에러 발생 시 스크린샷 저장
                error_screenshot_path = f'C:/해커톤/reviews/error_{driver.current_url.replace("https://www.google.com/search?", "").replace("/", "_")}.png'
                driver.save_screenshot(error_screenshot_path)
                print(f'Error processing review: {str(e)}')
                print(f'Screenshot saved: {error_screenshot_path}')

    return collected_reviews

review_lst = ['https://www.google.com/search?q=Jun+Won+Dak&sca_esv=458fc5d25ecd7a59&sca_upv=1&gl=us&hl=en&pws=0&source=hp&ei=cKCRZreWAezg2roPsqaCmAw&iflsig=AL9hbdgAAAAAZpGugJcEm7ZXmDm5_jLRPs4O92xn8PH0&ved=0ahUKEwi3jtWyuaKHAxVssFYBHTKTAMMQ4dUDCBc&uact=5&oq=Jun+Won+Dak&gs_lp=Egdnd3Mtd2l6IgtKdW4gV29uIERhazILEC4YgAQYxwEYrwEyBRAAGIAEMgUQABiABDIGEAAYFhgeMgsQABiABBiGAxiKBTILEAAYgAQYhgMYigUyCBAAGIAEGKIESLsDUABYAHAAeACQAQCYAYkBoAGJAaoBAzAuMbgBA8gBAPgBAvgBAZgCAaACjgGYAwCSBwMwLjGgB7AG&sclient=gws-wiz#lrd=0x80c2b942b6d08167:0x31833e2529443c12,1,,,,']

for store_url in review_lst:
    try:
        driver.get(store_url)
        time.sleep(10)  # 페이지가 로드될 때까지 대기

        # 스크롤 및 리뷰 수집
        review_data = scroll_and_collect_reviews(driver, max_reviews=100)

        # 데이터 프레임 생성 및 CSV 저장
        if review_data:
            df = pd.DataFrame(review_data)
            store_name = review_data[0]['Store Name']
            csv_filename = f'C:/해커톤/reviews/{store_name}_reviews.csv'
            df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
            print(f'Reviews saved to {csv_filename}')
            
            # 수집된 리뷰 데이터 개수 출력
            print(f'Number of reviews collected: {len(review_data)}')
        else:
            print(f'No reviews collected for {store_url}')

    except Exception as e:
        # 에러 발생 시 스크린샷 저장
        error_screenshot_path = f'C:/해커톤/reviews/error_{store_url.replace("https://www.google.com/search?", "").replace("/", "_")}.png'
        driver.save_screenshot(error_screenshot_path)
        print(f'Error processing {store_url}: {str(e)}')
        print(f'Screenshot saved: {error_screenshot_path}')

driver.quit()
