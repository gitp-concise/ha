from argparse import ArgumentParser
from datetime import datetime
from hankyung_scraper import HanKyungScraper


def create_parser() -> ArgumentParser:
    today = datetime.today().strftime("%Y%m%d")

    parser = ArgumentParser()
    parser.add_argument("-s", "--start_date", type=str, required=True, help="example: 20240504")
    parser.add_argument("-e", "--end_date", type=str, default=today, help=f"example: {today}")
    parser.add_argument("-o", "--output", type=str, default="", help="output json file path")
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    # 구현하세요!
    from datetime import date
    import json
    import asyncio
    import selenium.common.exceptions as SE


    def foo(scraper: HanKyungScraper) -> None:
        article_urls: list[str] = scraper.get_article_urls_from_chunk()

        loop = asyncio.get_event_loop()
        future_list = [asyncio.ensure_future(scraper.scrape_article(url, loop)) for url in article_urls]
        result_list: list[dict[str, str]] = loop.run_until_complete(asyncio.gather(*future_list))
        loop.close()
        with open(args.output, 'w', encoding="UTF-8") as out_file:
            json.dump(result_list, out_file, indent=4, ensure_ascii=False)


    start_date: date = datetime.strptime(args.start_date, "%Y%m%d").date()
    end_date: date = datetime.strptime(args.end_date, "%Y%m%d").date()

    scraper: HanKyungScraper = HanKyungScraper(start_date, end_date)
    while not scraper.end_flag:
        try:
            scraper.load_article_chunk()
        except (SE.TimeoutException, SE.NoSuchElementException) as selenium_exception:
            print("selenium exception occur")
            print(selenium_exception)
            foo(scraper)
            exit(-1)

    foo(scraper)