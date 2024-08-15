from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
# 구현하세요!
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from typing import List, Dict
import json
import time
from datetime import datetime
from tqdm import tqdm


class HanKyungScraper:
    # 구현하세요!
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    

    def get_article_urls(self, start_date: datetime, end_date: datetime) -> List[str]:
        article_urls = []
        n = 1

        self.driver.get("https://www.hankyung.com/all-news")
        time.sleep(2)

        # 경제 카테고리 진입 및 필요한 태그들 로딩될 때까지 대기
        self.driver.find_element(By.CSS_SELECTOR, '#inner > header > div > div.section__gnb__wrap > nav > ul > li:nth-child(3) > a').click()
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.box-module-inner.economyDiv.slick-slide.slick-current.slick-active')))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.daily-news')))

        while True:
            
            # 각 day-wrap으로부터 경제 카테고리의 기사 URL 수집
            try:
                day_wrap_selector = f'#container > div.all-news-wrap.layout-inner > div.contents > div.module-group.box-module.slick-initialized.slick-slider > div > div > div.box-module-inner.economyDiv.slick-slide.slick-current.slick-active > div.daily-news > div:nth-child({n})'
                day_wrap = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, day_wrap_selector)))
                
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                economy_div = soup.select_one(day_wrap_selector)

                if not economy_div:
                    print("경제 카테고리 내 기사 모음 태그(day-wrap)를 찾지 못했습니다.")
                    break

                # 주어진 날짜 범위에 해당하는 기사 URL 수집
                date_elements = economy_div.find_all('strong', class_='txt-date')

                for date_elem in date_elements:
                    date_text = date_elem.get_text(strip=True)
                    try:
                        current_date = datetime.strptime(date_text, '%Y.%m.%d')
                    except ValueError:
                        print("날짜 형식이 올바르지 않습니다.")
                        continue

                    if start_date <= current_date <= end_date:
                        news_items = date_elem.find_next('ul').find_all('li', {'data-aid': True})
                        for item in news_items:
                            link_tag = item.find('a', {'data-pm': 'N'})
                            if link_tag:
                                href = link_tag['href']
                                article_urls.append(href)
                    
                    # 주어진 날짜 범위에 해당하는 기사 URL 수집을 마치면 URL 리스트 반환하고 함수 끝
                    elif current_date < start_date:
                        return article_urls

                # 다음 day-wrap으로
                n += 1
        
            except Exception:

                # 더보기 눌러
                try:
                    more_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '#container > div.all-news-wrap.layout-inner > div.contents > div.module-group.box-module.slick-initialized.slick-slider > div > div > div.box-module-inner.economyDiv.slick-slide.slick-current.slick-active > div.btn-more-wrap > button'))
                    )
                    more_button.click()
                    time.sleep(2)
                except Exception:
                    print("더보기 버튼을 찾지 못했습니다.")
                    break

        # 일단 저장
        now = datetime.now().strftime('%m%d%H%M')
        txt_dir = f"url_{now}.txt"
        with open(txt_dir, 'w', encoding='utf-8') as f:
            f.write('\n'.join(article_urls))

        return article_urls


    def url_to_data(self, url_list: List[str], output_path: str) -> None:
        data = []

        for article in tqdm(url_list):
            self.driver.get(article)
            time.sleep(2)
            try:
                article_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                # 제목
                title = article_soup.find('h1', class_='headline')
                title_text = title.get_text(strip=True) if title else 'No Title'

                # 입력날짜, 수정날짜
                date_elements = article_soup.find_all('span', class_='item')
                input_date = None
                modified_date = None

                for element in date_elements:
                    date_span = element.find('span', class_='txt-date')
                    if date_span:
                        date_text = date_span.get_text(strip=True)
                        if '입력' in element.get_text():
                            input_date = date_text
                        elif '수정' in element.get_text():
                            modified_date = date_text

                # 본문
                article_body = article_soup.find('div', id='articletxt')
                article_body_text = article_body.get_text(strip=True) if article_body else 'No Article Body'

                article_data = {
                    'date': input_date,
                    'date_edit': modified_date,
                    'href': article,
                    'title': title_text,
                    'article': article_body_text
                }
                data.append(article_data)

            except Exception:
                print(f'{article} 기사의 내용을 크롤링하지 못했습니다.')
                continue
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def close(self):
        self.driver.quit()