from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
# 구현하세요!
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import date, datetime
from bs4 import Tag
# selenium이 urllib3와 certifi 패키지를 의존성으로 가집니다. 써도 되는 거겠죠?
# 개별 뉴스 페이지(정적인 페이지)의 정보들을 스크레핑하는 데 selenium 쓰니 느립니다.ㅠㅠ
from urllib3 import PoolManager, BaseHTTPResponse
import certifi
from asyncio import AbstractEventLoop

# selenium 성능 향상 옵션들
# 크롬창 띄우지 않는 게 설정 과 이미지 로딩 막는 옵션
chrome_options: Options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

URL: str = "https://www.hankyung.com/all-news"
TIMEOUT: int = 15

http: PoolManager = PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where()
)


class HanKyungScraper:
    # 구현하세요!

    def __init__(self, start_date: date, end_date: date):
        self.driver: WebDriver = webdriver.Chrome(options=chrome_options)
        self.start_date: date = start_date
        self.end_date: date = end_date
        self.end_flag = False
        self.driver.get(URL)
        print("loaded page")

        # click econ button from main page
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, MainPageSelector.econ_button))
        ).click()

    @staticmethod
    def select_one(tag: Tag, css_selector: str) -> Tag:
        selected_tag: Tag | None = tag.select_one(css_selector)
        if selected_tag is None:
            raise Exception(f"element not found\ncss_selector:{css_selector}\ntag:{tag}")
        return selected_tag

    @staticmethod
    def date_predicate(t: Tag, start_date: date, end_date: date) -> bool:
        written_date_str: str = HanKyungScraper.select_one(t, ".txt-date").text
        written_date: date = datetime.strptime(written_date_str, "%Y.%m.%d").date()

        if start_date <= written_date <= end_date:
            return True
        else:
            return False

    def load_article_chunk(self) -> None:
        if self.end_flag:
            return None

        WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, MainPageSelector.moreover_button))
        ).click()

        oldest_date_tag: WebElement = WebDriverWait(self.driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, MainPageSelector.oldest_date))
        )

        last_data: date = datetime.strptime(oldest_date_tag.text, "%Y.%m.%d").date()
        if last_data < self.start_date:
            self.end_flag = True

        print(f"date: {last_data}")

    def get_article_urls_from_chunk(self) -> list[str]:
        soup: BeautifulSoup = BeautifulSoup(self.driver.page_source, 'html.parser')
        valid_chunks: list[Tag] = list(
            filter(
                lambda t: HanKyungScraper.date_predicate(t, self.start_date, self.end_date),
                soup.select(MainPageSelector.article_chunk)
            )
        )

        links: list[str] = []
        for chunk in valid_chunks:
            links.extend([t.attrs['href'] for t in chunk.select(MainPageSelector.article_link_from_article_chunk)])
        return links

    async def scrape_article(self, article_link: str, loop: AbstractEventLoop) -> dict[str, str]:
        print(f"request to {article_link}")
        # request
        res: BaseHTTPResponse = await loop.run_in_executor(None, http.request, 'GET', article_link)

        html_doc: str = res.data.decode('utf-8')
        soup = BeautifulSoup(html_doc, 'html.parser')

        # extract data
        written_date: str = HanKyungScraper.select_one(soup, ArticlePageSelector.written_date).text.strip()
        update_date: str = HanKyungScraper.select_one(soup, ArticlePageSelector.updated_date).text.strip()
        title: str = HanKyungScraper.select_one(soup, ArticlePageSelector.title).text.strip()
        article: str = HanKyungScraper.select_one(soup, "#articletxt").get_text(strip=True)

        return {"date": written_date, "date_edit": update_date, "href": article_link, "title": title,
                "article": article}


class MainPageSelector:
    moreover_button: str = "div.box-module-inner.economyDiv > div.btn-more-wrap > button.btn-more"
    chunk_date: str = ".all-news-wrap .economyDiv .daily-news > .day-wrap > strong.txt-date"
    article_chunk: str = ".all-news-wrap .economyDiv .daily-news > .day-wrap "
    article_link_from_article_chunk: str = "ul.news-list > li .news-tit > a"
    oldest_date: str = ".all-news-wrap .economyDiv .daily-news > .day-wrap:last-child > strong.txt-date"
    econ_button: str = "#inner > header > div > div.section__gnb__wrap > nav > ul > li:nth-child(3) > a"


class ArticlePageSelector:
    written_date: str = "#container > div > div > article > div > div > div.article-timestamp > div.datetime > span:nth-child(1) > span"
    updated_date: str = "#container > div > div > article > div > div > div.article-timestamp > div.datetime > span:nth-child(2) > span"
    title: str = ".article-contents > h1.headline"
