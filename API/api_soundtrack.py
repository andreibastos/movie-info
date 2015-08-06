# coding: utf-8

import urllib
from lxml import html
from lxml import etree
from lxml.html import fromstring, tostring


url_base = 'https://www.youtube.com'
url_base_find = url_base+'/find?'




def search_soundtrack(soundtrack_name,soundtrack_autor):
	print ("search:\t"+soundtrack_name + " in " + url_base )



soundtrack_name = "Taya's Theme"
soundtrack_autor = ''
search_soundtrack(soundtrack_name,soundtrack_autor)
