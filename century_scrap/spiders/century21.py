import scrapy
import csv


class Century21Spider(scrapy.Spider):
    name = 'century21'
    allowed_domains = ['century21.com.ve']
    start_urls = ['https://www.century21.com.ve/v/resultados/en-pais_venezuela/en-estado_anzoategui/en-municipio_lecheria']

    def parse(self, response):
    # Obtener la ruta XPath del contenedor de los listados de propiedades.
        listings_container_xpath = '//div[contains(@class, "listing-results")]'
        # Extraer los datos de los listados de propiedades.
        for listing in response.xpath(listings_container_xpath):
            # Obtener el título de la propiedad.
            title = listing.xpath('.//a[contains(@class, "listing-title")]/text()').get()
            
            # Obtener la dirección de la propiedad.
            address = listing.xpath('.//address/text()').get()
            
            # Obtener el precio de la propiedad.
            price = listing.xpath('.//a[contains(@class, "price")]/text()').get()
            
            yield {
                'Title': title,
                'Address': address,
                'Price': price
            }

    # Obtener la URL de la página siguiente y hacer scraping de los datos.
        next_page_url = response.xpath('//a[contains(@class, "next-page")]/@href').get()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    # Guardar los datos en un archivo CSV.
        with open('century21.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([title, address, price])
