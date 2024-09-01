import scrapy

class GgDealsSpider(scrapy.Spider):
    """
        Base scraper for data scraping from gg.deals that implements Scrapy spiders
    """

    name = "gg.deals"
    start_urls = [
        "https://www.gg.deals/games/"
    ]

    def parse_game(self, response):
        """
            Parses a single game page from gg.deals containing game data we are going to use as our data 
            to be retrieved
        """

        title_selector = response.css("a.active")
        title = title_selector.xpath("./span/text()")

        genres_selector = response.css("div#game-info-genres")
        genres = genres_selector.xpath(".//a//text()")

        tags_selector = response.css("div#game-info-tags")
        tags = tags_selector.xpath(".//a//text()")
        
        description_selector = response.css("div.game-description.description-text")
        description = description_selector.xpath(".//p//text()")

        image_selector = response.css("div.game-info-image-wrapper")
        image = image_selector.xpath(".//div//img//@src")

        if len(description) == 0:
            description = description_selector.xpath(".//text()")

        yield {
                "Title": title.get(),
                "Genres": genres.getall(),
                "Tags": tags.getall(),
                "Description": " ".join(description.getall()).replace("\n", ""),
                "Image": image.get()
            }
    
    def parse_games_page(self, response):
        """
            Parses a multiple games page from gg.deals, and searches for the next page to crawl
        """

        for game_info in response.css("div.game-info-wrapper"):
            game_url = game_info.xpath("./div/div/a/@href").get()
            game_page = response.urljoin(game_url)
            yield scrapy.Request(game_page, callback=self.parse_game)
            
        
        next_page = response.css("li.page.next-page a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_games_page)


    def parse(self, response):
        """
            Scrapy spider entrypoint function to crawl, which redirects to game collection crawling function
        """
        return self.parse_games_page(response)
    