import scrapy
from scrapy import Request
import re
from ..items import NewscrawlerItem
from datetime import datetime

class Netbet(scrapy.Spider):
    name = "netbet"
    allowed_domains = ["netbet.fr"]
    start_urls = ["https://www.netbet.fr/football/angleterre/premier-league"]

    def parse(self, response):
        #match = response.css("div.item-content.catcomp.item-bloc-type-1").getall()
        #côte = response.css("span.pmq-cote").getall()
        match = response.css( "div.nb-flex-row")

        now = datetime.now()
        date_jour = now.strftime("%m-%d-%Y")

        for cote in match:
            text_match =  cote.css('div.nb-match_actor::text')[0].get()
            text_match1 = cote.css('div.nb-match_actor::text')[1].get()
            text_value =  cote.css("div.nb-odds_amount::text")[0].get()
            text_value2 =  cote.css("div.nb-odds_amount::text")[1].get()
            text_value1 = cote.css("div.nb-odds_amount::text")[2].get()

            date_match = cote.css("div.nb-event_datestart::text").get()
            if (date_match=="Auj"):
                date_match = "06/02"

            yield NewscrawlerItem(
                date_jour = date_jour,
                site = "netbet",
                championnat = "première league",
                cote = text_value,
                cote2 = text_value1,
                cote3 = text_value2,
                equipe1 = text_match,
                equipe2 = text_match1,
                date_match = date_match
                  )
