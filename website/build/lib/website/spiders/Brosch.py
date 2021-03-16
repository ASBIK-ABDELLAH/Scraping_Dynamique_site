import scrapy
import requests
from scrapy import Selector
from ..items import BroschItem

class BroschSpider(scrapy.Spider):
    name = 'Brosch'
    start_urls = ['https://www.wir-machen-druck.de/extrem-guenstig-broschueren-drucken,category,13266.html']


    def parse(self, response):
        items = BroschItem()
        page1 = response.css('.mb-10')

        for res in page1:

            url1 = res.css('.text-center a::attr(href)').get()
            url_1 = "https://www.wir-machen-druck.de/"+str(url1)
            page_2 = str(url_1)
            response_2 = requests.get(page_2)
            response2 = Selector(response_2)
            response_2.close()
            page2 = response2.css('div.col-xs-3.category-box.mb-10')

            for res2 in page2:
                url2 = res2.css(".text-center a::attr(href)").get()
                url_2 = "https://www.wir-machen-druck.de/" + str(url2)
                page_3 = str(url_2)
                response_3 = requests.get(page_3)
                response3 = Selector(response_3)
                response_3.close()
                page3 = response3.css('tr.tbCat_inline.pt-0')

                for res3 in page3:
                    url3 = res3.css(".tbCat_inline2 a::attr(href)").get()
                    url = "https://www.wir-machen-druck.de" + str(url3)
                    items['url_name'] = url
                    page_4 = str(url)

                    response_4 = requests.get(page_4)

                    response4 = Selector(response_4)
                    response_4.close()
                    items['name'] = response4.css(".product-title strong::text").extract()
                    div = response4.css('#sorten > option')

                    for rep10 in div:
                        name = rep10.css('::text').extract()
                        items['Ausfuhrung'] = name
                        sorten = rep10.css('::attr(value)').extract()
                        r = requests.post(url, data={'sorten': sorten[0]})
                        res20 = Selector(r)
                        au = res20.xpath('//select[@id="wmd_shirt_auflage"]/option')

                        for r in au:
                            auf = r.css('::attr(value)').extract()
                            Stuc = r.css('::text').extract()
                            items['Stuck'] = Stuc
                            c = requests.post(url, data={'sorten': sorten[0],
                                                         'auflage': auf[0]})
                            cl = Selector(c)


                            delev = cl.css('.delivery-option-container > label > input[name="deliveryOption"]')
                            for d in delev:
                                auk = d.css('::attr(value)').extract()
                                Life = d.xpath(
                                    '//*[@id="hover_slider_{}"]/div[1]/label/span[2]/span/strong/text()[1]'.format(
                                        auk[0])).get()
                                Life1 = d.xpath(
                                    '//*[@id="hover_slider_{}"]/div[1]/label/span[2]/span/strong/text()[2]'.format(
                                        auk[0])).get()
                                items['Lifertermin'] = Life
                                items['inkl'] = Life1
                                bb = requests.post(url, data={'sorten': sorten[0],
                                                         'auflage': auf[0],
                                                              'deliveryOption': auk[0]})
                                bob = Selector(bb)
                                price = bob.css('#net-price::text').extract()


                                items['Preis'] = str(price).replace(" ", "")[4:-4]
                                yield items





                        


                    






