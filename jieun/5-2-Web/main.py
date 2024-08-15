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
    start_date = datetime.strptime(args.start_date, '%Y%m%d')
    end_date = datetime.strptime(args.end_date, '%Y%m%d')
    output_path = args.output if args.output else f"results_{datetime.now().strftime('%Y%m%d%H%M')}.json"

    scraper = HanKyungScraper()
    article_urls = scraper.get_article_urls(start_date, end_date)
    scraper.url_to_data(article_urls, output_path)
    scraper.close()