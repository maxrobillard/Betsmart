import scrapy
from scrapy import Request
import re
from ..items import NewscrawlerItem
from datetime import datetime

class Zebet(scrapy.Spider):
    name = "zebet"
    allowed_domains = ["zebet.fr"]
    start_urls = ["https://www.zebet.fr/fr/competition/94-premier_league"]

    def parse(self, response):
        #match = response.css("div.item-content.catcomp.item-bloc-type-1").getall()
        #côte = response.css("span.pmq-cote").getall()
        #match = response.css( "div.uk-flex.uk-flex-item-1.uk-flex-space-between.uk-flex-middle")
        match = response.css( "div.item-content.catcomp.item-bloc-type-1")

        now = datetime.now()
        date_jour = now.strftime("%m-%d-%Y")

        for cote in match:
            text_match =  cote.css('span.pmq-cote-acteur.uk-text-truncate::text')[0].get()
            text_match1 = cote.css('span.pmq-cote-acteur.uk-text-truncate::text')[4].get()
            text_value =  cote.css('span.pmq-cote::text')[0].get()
            text_value2 =  cote.css('span.pmq-cote::text')[2].get()
            text_value1 = cote.css('span.pmq-cote::text')[4].get()

            date_match = cote.css("div.bet-time::text").get()

            if (date_match=="Auj"):
                date_match =date_jour

            yield NewscrawlerItem(
                date_jour = date_jour,
                site = "zebet",
                championnat = "première league",
                cote = text_value,
                cote2 = text_value1,
                cote3 = text_value2,
                equipe1 = text_match,
                equipe2 = text_match1,
                date_match = date_match
                  )
