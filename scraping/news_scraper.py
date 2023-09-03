from parsel import Selector
import requests


class NewsScraper:
    PLUS_URL = "https://www.prnewswire.com"
    START_URL = "https://www.prnewswire.com/news-releases/news-releases-list/"
    LINK_XPATH = '//div[@class="row newsCards"]/div/a/@href'
    TITLE_V1_XPATH = '//div[@class="col-sm-12 card"]/a/h3/text()'
    TITLE_V2_XPATH = '//div[@class="col-sm-8 col-lg-9 pull-left card"]/h3/text()'
    TEXT_XPATH = '//div[@class="col-lg-10 col-lg-offset-1"]/p/text()'

    def parse_data(self):
        text = requests.get(self.START_URL).text
        tree = Selector(text=text)
        links = tree.xpath(self.LINK_XPATH).extract()
        first_v_title = tree.xpath(self.TITLE_V1_XPATH).extract()
        second_v_title = tree.xpath(self.TITLE_V2_XPATH).extract()
        first_v_title.extend(second_v_title)
        data = []
        for link in links:
            data.append(self.PLUS_URL + link)
            print("self.PLUS_URL: ", self.PLUS_URL + link)
        return links[:5]
        # self.parse_detail(urls=data)

    def parse_detail(self, urls):
        for url in urls:
            text = requests.get(url).text
            tree = Selector(text=text)
            text = tree.xpath(self.TEXT_XPATH).extract()
            print(text)


if __name__ == "__main__":
    scraper = NewsScraper()
    scraper.parse_data()