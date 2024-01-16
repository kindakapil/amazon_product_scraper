import scrapy
# from scraper_api import ScraperAPIClient
# client = ScraperAPIClient('your API key here')
import openpyxl



class ProdcrawlerSpider(scrapy.Spider):
    name = "prodcrawler"
    allowed_domains = ["www.amazon.in","www.amazon.com","api.scraperapi.com","proxy.scrapeops.io"]
    start_urls = ['https://www.amazon.com/ACWOWO-Bathroom-Organizer-Diatomaceous-Absorbing/dp/B0BN24SY89/ref=pd_ci_mcx_mh_mcx_ac_nb_0?content-id=amzn1.sym.e1771f4b-c888-4d17-a732-ae66daf85cb2&pd_rd_i=B0BN24SY89']
    list_of_reviews = [] 

    def parse(self, response): 
        global prod_info_list
        prod_info_list = []
        prod_title = response.css('#productTitle::text').get().strip()
        print(f"Product Title: {prod_title}")


        prod_cat = response.css('#nav-subnav a span::text').get().strip()
        print(f"Product Category: {prod_cat}")

        desc_list = response.css('#feature-bullets ul li span::text')
        prod_desc_list = []
        for i in desc_list:
            desc_bullet = i.get() 
            prod_desc_list.append(desc_bullet)
        prod_desc_str = ''
        prod_desc_str = prod_desc_str.join(prod_desc_list)
        print(f"Product Description:\n{prod_desc_str}")

        prod_rating = response.css('#acrPopover span a span::text').get().strip()
        print(f"Product Rating: {prod_rating}")
        
        #Put an if statement here for products that might not even have any reviews
        all_reviews_relative_url = response.css('#reviews-medley-footer div a::attr(href)').get()
        all_reviews_full_url = 'https://www.amazon.com' + all_reviews_relative_url 
        # print(all_reviews_full_url)

        prod_info_list.extend([prod_title,prod_cat,prod_desc_str,prod_rating])
        
        yield response.follow(all_reviews_full_url, callback = self.review_scraper)

    # def list_creation():
        # global list_of_reviews
        # list_of_reviews = []


    def review_scraper(self,response):
        current_page_reviews_list = response.css('span.a-size-base.review-text.review-text-content span::text').extract()
        print(f"The {len(current_page_reviews_list)} reviews on current page are:\n{current_page_reviews_list}") 
        for i in current_page_reviews_list:
            # print(i)
            ProdcrawlerSpider.list_of_reviews.append(i)
        # if 'signin' in next_page_url:
        #     yield response.follow(all_reviews_full_url, callback = self.review_scraper)
        if not len(response.css('li.a-last a::attr(href)').extract()) == 0:
            next_page_url = response.css('li.a-last a::attr(href)').get()
        # if not (next_page_url == None):
        #     if not 'https://www.amazon.in' in next_page_url:
        #         next_page_url = 'https://www.amazon.in' + next_page_url
        #     print(f"Next page URL is:\n {next_page_url}")
        #     # if not next_page_url == None and not 'signin' in next_page_url:    
        #     #     yield response.follow(client.scrapyGet(url = next_page_url), callback = self.review_scraper)
        #     yield response.follow(next_page_url, callback = self.review_scraper)
            yield response.follow(next_page_url, callback = self.review_scraper)

        else:
            print(f"The COMPLETE list of reviews ({len(ProdcrawlerSpider.list_of_reviews)}) is:\n{ProdcrawlerSpider.list_of_reviews} and it has {len(ProdcrawlerSpider.list_of_reviews)} reviews in it")
            string_of_reviews = ''
            string_of_reviews = str(ProdcrawlerSpider.list_of_reviews)
            prod_info_list.append(string_of_reviews)

            prod_info_tuple = tuple(prod_info_list)
            wb = openpyxl.load_workbook('scraped_prods.xlsx')
            ws = wb.active
            ws.append(prod_info_tuple)
            wb.save('scraped_prods.xlsx')

            prod_info_list.clear()
            prod_info_tuple = ()

        

        # if 'signin' in next_page_url:
        # next_page_url = 'https://www.amazon.in' + response.css('li.a-last a::attr(href)').get()
        # if not 'https://www.amazon.in' in next_page_url:
        #     next_page_url = 'https://www.amazon.in' + response.css('li.a-last a::attr(href)').get()
        # scrapy fetch(next_page_url,callback = self.review_scraper)

        # else:
        #     for i in range (20):
        #         yield response.follow



        
        
        





            



        
