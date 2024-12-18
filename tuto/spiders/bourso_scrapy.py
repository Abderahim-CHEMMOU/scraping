# import scrapy

# class LinksSpider(scrapy.Spider):
#     name = 'bourso'
#     allowed_domains = ['boursorama.com']
#     start_urls = ['https://www.boursorama.com/']

#     def parse(self, response):
#         # Récupérer tous les liens avec un sélecteur CSS
#         links = response.css("a.c-headlines::attr(href)").getall()

#         for link in links:
#             full_link = response.urljoin(link)
#             yield {"link": full_link}


import scrapy

class LinksSpider(scrapy.Spider):
    name = 'bourso'
    allowed_domains = ['boursorama.com']
    start_urls = ['https://www.boursorama.com/']

    def parse(self, response):
        # Étape 1 : Récupérer tous les liens avec un sélecteur CSS
        links = response.css("a.c-headlines::attr(href)").getall()

        for link in links:
            # Construire l'URL complète
            full_link = response.urljoin(link)
            # Suivre chaque lien et extraire le titre dans parse_article
            yield scrapy.Request(url=full_link, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css("h1.c-title-big.c-title--color-dark span::text").get()
        if not title:
            title = response.xpath("//h1[contains(@class, 'c-title-big')]/text()").get()

        date_heure = response.css("div.c-source.c-news-detail__source span.c-source__time::text").get()

        
        source = response.css("strong.c-source__name.c-source__name--news::text").get()
        # source video
        if not source:
            source = response.css("strong.c-source__name.c-source--video-program::text").get()

        paragraphs = response.css("article.c-news-detail__content p:not([class])::text").getall()

        # Nettoyer et joindre le texte des paragraphes
        contenu = " ".join([p.strip() for p in paragraphs if p.strip()])


        # print("contenu==", contenu)
        # Retourner l'URL et le titre de l'article
        yield {
            "url": response.url,
            "title": title.strip() if title else "Titre non trouvé",
            "date_heure": date_heure if date_heure else "Date non trouvé",
            "source": source if source else "Source non trouvé",
            "contenu": contenu if contenu else "Contenu non trouvé"
        }
