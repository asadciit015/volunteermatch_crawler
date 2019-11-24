# -*- coding: utf-8 -*-
import scrapy, math
from urllib.parse import parse_qsl, urlsplit, urlencode


class OrganizationCrawlerSpider(scrapy.Spider):
	name = 'organization_crawler'
	allowed_domains = ['volunteermatch.org']

	def get_url_query_dict(self, url):
		return dict(parse_qsl(urlsplit(url).query)) if url not in ( "", None,) else {}


	def gen_url_with_query_dict(self, url, **qs):
		uri = urlsplit(url)
		parsed_url = '{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=uri)
		parsed_url_qs = self.get_url_query_dict(url)
		parsed_url_qs.update(**qs)
		parsed_url_qstr = urlencode(parsed_url_qs)
		return f"{parsed_url}?{parsed_url_qstr}"


	def start_requests(self):
		start_urls = ['https://www.volunteermatch.org/search/orgs.jsp?l=Ohio&k=&submitsearch=Search']
		for url in start_urls:
			yield scrapy.Request(url=url, callback=self.visit_search_links)


	def visit_search_links(self, response):
		total_pages = 1
		total_results = 10
		page_descripter = response.css("p.descriptor::text").extract()
		# 'Displaying 1 - 10 of 4195\n
		if len(page_descripter)>=3:
			total_results = int(page_descripter[2].split()[-1])
			total_pages = int(math.ceil(total_results/10))
			self.logger.info(f'total_results > {total_results} total_pages >>> {total_pages}')

		search_links = [ self.gen_url_with_query_dict(
								url=response.url,
								s=x*10+1)
						for x in range(0, total_pages)]

		for i, search_link in enumerate(search_links):
			self.logger.info(f'\n{">"*50}\n[search_link] {i+1}/{total_pages}:{search_link}\n{"<"*50}\n')
			yield scrapy.Request(
							url=search_link, callback=self.visit_org_links,
							meta={"page_number": i+1, "total_results":total_results, "search_link":search_link},
						)


	def visit_org_links(self, response):
		org_links = response.css("h3 > a[href^='/search/org']::attr('href')").extract()
		total_org_links = len(org_links)
		for i, org_link in enumerate(org_links):
			self.logger.info(f'\n{">"*50}\n[org_link] {i+1}/{total_org_links}:{org_link}\n{"<"*50}\n')
			yield scrapy.Request(
					url=response.urljoin(org_link), callback=self.parse_org_links,
					meta={"page_number": response.meta.get("page_number"),
						  "total_results":response.meta.get("total_results"),
						  "search_link": response.meta.get("search_link")}
					)
	

	def parse_org_links(self, response):
		short_mission = response.css("#short_mission::text").extract_first()
		# 'The mission of NAMI Lorain County is to improve the quality of life for consumers living with disabling brain disorders/mental illness through providing their families and friends with educational opportunities, support groups, and advocacy in the pu...'
		website = response.css("a[target='new']::attr('href')").extract_first() or ""
		# 'http://www.nami-lc.org'
		name = response.css(".rwd_display::text").extract_first()
		# 'NAMI OF LORAIN COUNTY'
		return {
				"Organization Name" : name,
				"Mission Statement": short_mission,
				"Website Link": website if "/reviews/orgreview.jsp?" not in website else None,
				"Organization Link": response.url,
				"Search Link" : response.meta.get("search_link"),
				"Current Page": response.meta.get("page_number"),
				"Total Results" : response.meta.get("total_results")
			}



