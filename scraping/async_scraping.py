from parsel import Selector
import asyncio
import httpx


class AsyncNewsScraper:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    START_URL = "https://www.prnewswire.com/news-releases/news-releases-list/?page={}&pagesize=100"
    PLUS_URL = "https://www.prnewswire.com"
    LINK_XPATH = '//div[@class="row newsCards"]/div/a/@href'
    TITLE_DETAIL_XPATH = '//div[@class="col-sm-12 col-xs-12 "]/h1/text()'
    TITLE_V2_DETAIL_XPATH = '//div[@class="col-sm-8 col-vcenter col-xs-12 "]/h1/text()'
    IMAGE_URL_XPATH = '//a[@class="tablogofocus"]/img/@data-getimg'

    # START_URL = "https://www.prnewswire.com/news-releases/news-releases-list/"

    async def async_generator(self):
        for page in range(1, 3):
            yield page

    async def async_generator_detail(self, links):
        for page in links:
            yield page

    async def get_url(self, client, url):
        response = await client.get(url)
        await self.parse_links(content=response.text, client=client)
        return response

    async def parse_links(self, content, client):
        tree = Selector(text=content)
        links = tree.xpath(self.LINK_XPATH).extract()
        print(links)
        async for detail in self.async_generator_detail(links):
            await self.parse_detail(url_detail=detail, client=client)

    async def parse_data(self):
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            async for page in self.async_generator():
                print(f"URL: {self.START_URL.format(page)}")
                await self.get_url(client=client, url=self.START_URL.format(page))
            # task = asyncio.create_task(self.get_url(client=client,
            #                                         url=self.START_URL))
            # news_gather = await asyncio.gather(*task)
            # await task
        await client.aclose()
    async def parse_detail(self, url_detail, client):
        response = await client.get(self.PLUS_URL + url_detail)
        tree = Selector(text=response.text)
        title = tree.xpath(self.TITLE_DETAIL_XPATH).extract()
        img_url = tree.xpath(self.IMAGE_URL_XPATH)
        if not title:
            title_v2 = tree.xpath(self.TITLE_V2_DETAIL_XPATH).extract()
            print(self.PLUS_URL + url_detail)
            print(f"Title: {title_v2}")
            print(f"IMG_URL: {img_url}")
        else:
            print(self.PLUS_URL + url_detail)
            print(f"Title: {title}")
            print(f"IMG_URL: {img_url}")
if __name__ == "__main__":
    scraper = AsyncNewsScraper()
    asyncio.run(scraper.parse_data())