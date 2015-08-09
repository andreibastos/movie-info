# coding: utf-8

import urllib
from lxml import html
from lxml import etree
from lxml.html import fromstring, tostring
import json

url_base = 'https://www.youtube.com'
url_base_find = url_base+'/results?'


words_by_search = ['','soundtrack']

def search_soundtrack(soundtrack_name,soundtrack_movie_name):
	words_by_search[0] = soundtrack_movie_name
	
	response = False

	results = []

	for words_search in words_by_search:
		print ("search:\t"+soundtrack_name + " "+ words_search + " in " + url_base )

		search_query = soundtrack_name + " "+ words_search

		params_tmp = {'search_query':search_query}	
		
		params = urllib.urlencode(params_tmp)

		link =url_base_find+params 

		# to test download the page 
		# link = 'youtube.html' 

		print (link)


		f = urllib.urlopen(link)
		

		tree = etree.HTML(f.read())  

		num =  tree.xpath("//p[@class='num-results first-focus']/strong")
		num_results = 0

		
		error = 'not errors'

		try:
			num_results = float(num[0].text)
			if num_results > 0:
				
				tmp_h3 = tree.xpath("//div/h3/a")
				if tmp_h3:				
					for a in tmp_h3:
						tmp_link = url_base + a.get('href')					
						results.append(tmp_link)
			response = True	
			break
		except Exception as e:
			error = e 
			response = False
	
	return json.dumps({'response':response,'results':results, 'meta':{'mensage':str(error)}},indent = 4, sort_keys=True) 

		


# soundtrack_name = "Taya's Theme"
# soundtrack_movie_name = 'American Sniper'

# print search_soundtrack(soundtrack_name,soundtrack_movie_name)
