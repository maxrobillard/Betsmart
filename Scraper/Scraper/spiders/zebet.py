import scrapy
from scrapy import Request
import re
from ..items import NewscrawlerItem

class Zebet(scrapy.Spider):
    name = "zebet"
    allowed_domains = ["zebet.fr"]
    start_urls = ["https://www.zebet.fr/fr/competition/94-premier_league"]

    def parse(self, response):
        #match = response.css("div.item-content.catcomp.item-bloc-type-1").getall()
        #côte = response.css("span.pmq-cote").getall()
        match = response.css( "div.uk-flex.uk-flex-item-1.uk-flex-space-between.uk-flex-middle")

        for cote in match:
            text_match =  cote.css('span.pmq-cote-acteur.uk-text-truncate::text')[0].get()
            text_match1 = cote.css('span.pmq-cote-acteur.uk-text-truncate::text')[4].get()
            text_value =  cote.css('span.pmq-cote::text')[0].get()
            text_value2 =  cote.css('span.pmq-cote::text')[2].get()
            text_value1 = cote.css('span.pmq-cote::text')[4].get()
            yield NewscrawlerItem(
                site = "zebet",
                cote = text_value,
                cote2 = text_value1,
                cote3 = text_value2,
                equipe1 = text_match,
                equipe2 = text_match1
                  )
