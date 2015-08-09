# coding: utf-8
import urllib
from lxml import html
from lxml import etree
from lxml.html import fromstring, tostring
import json

url_base = 'http://www.imdb.com'
url_base_find = url_base+'/find?'

def search_movie(name_movie, year):
	year = str(year)
	list_links_movies = []

	if name_movie:	
		print('search..\tname_movie:['+name_movie+']\tyear:['+ year+']');		
		params_tmp = {'q':name_movie+' '+year, 's':'tt','ttype':'ft','ref_':'fn_ft'}
		
		params = urllib.urlencode(params_tmp)
		# params = "q=%s&ttype=ft&s=tt&ref_=fn_ft" % (name_movie.replace(' ','+')+'+'+year)

		# print (params)
		f = urllib.urlopen(url_base_find,params)
		
		# form  the tree of page of query
		tree = etree.HTML(f.read())  
		
		#append in list_links_movies the links movies of td findList
		for table in tree.xpath("//table"):
			if table.get('class') == 'findList':
				for td in table.xpath("//tr//td"):
					if td.get('class') == 'result_text':
						if not 'development' in tostring(td):
							list_links_movies.append(url_base+td.xpath('a')[0].get('href'))
						# print(url_base+td.xpath('a')[0].get('href'))
		return list_links_movies
	else:
		return []


def get_soundtrack(link):
	print('get soundtrack\t['+link+']')
	page = urllib.urlopen(link)
	tree = etree.HTML(page.read())
	qnt = ''
	soundtrack = []

	for divs in tree.xpath("//div[@id='soundtracks_content']//div[@class='desc']"):		
		qnt = divs.text
		print '\t'+qnt
	if qnt:
		for divs in tree.xpath("//div[@class='list']//div"):	
			class_name = divs.get('class')
			# print(class_name)
			if 'soundTrack' in class_name:
				soundtrack.append(divs.text)
	
	return soundtrack


	
def get_movie(link):
	# link = '/home/andrei/scripts/torrent/imdb/movie.html'	
	print ('Downloading..\t['+link+']')
	movie = {}
	movie['Response'] = False
	movie['Poster'] = 'N/A'
	movie['Year'] = "N/A"
	movie['Rated'] = "N/A"
	movie['Release_nobr'] = "N/A"
	movie['Release_nobr_date'] = "N/A"
	movie['Runtime'] =  "N/A"
	movie['Genre'] = "N/A"
	movie['Director'] = "N/A"
	movie['Writer'] = "N/A"
	movie['Description'] = "N/A"
	movie['ImdbRating'] = "N/A"
	movie['Metascore'] = "N/A"
	movie['ImdbVotes'] = "N/A"
	movie['ImdbID'] = "N/A"
	movie['Type'] = "N/A"

	try:
		page = urllib.urlopen(link)
		tree = etree.HTML(page.read())

		list_id_import = set(['title-overview-widget','content-2-wide','article title-overview','maindetails_center_top','maindetails_center_bottom','titleRecs','titleCast','titleStoryLine','titleDetails'])
		for divs in tree.xpath("//div[@id='pagecontent']//div"):
			id_tmp = divs.get('id')
			if (id_tmp in list_id_import):
				# print(id_tmp)
				if 'title-overview-widget' in id_tmp:
					temp_poster = divs.xpath("//table//tbody//tr//td//div[@class='image']//img")
					if temp_poster:
						movie['Poster'] = temp_poster[0].get('src')

					tmp_title = divs.xpath("//table//tbody//tr//td[@id='overview-top']//h1//span")

					for class_name in tmp_title:
						if class_name.get('class'):
							if 'itemprop' in class_name.get('class'):
								movie['name_pt'] = class_name.text.replace("\n",'')					
							if 'title-extra' in class_name.get('class'):
								movie['Title'] = class_name.text.split('"')[1::2][0]
							else:
								movie['Title'] = movie['name_pt'] 

					if divs.xpath("//table//tbody//tr//td[@id='overview-top']//h1//span//a"):
						movie['Year'] = divs.xpath("//table//tbody//tr//td[@id='overview-top']//h1//span//a")[0].text	
					if divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='infobar']//meta"):			
						movie['Rated'] = divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='infobar']//meta")[0].get('content')
					if divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='infobar']//span[@class='nobr']//a"):
						movie['Release_nobr'] = " ".join((c for c in divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='infobar']//span[@class='nobr']//a")[0].text.split()))
					if divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='infobar']//span[@class='nobr']//a//meta"):
						movie['Release_nobr_date'] = divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='infobar']//span[@class='nobr']//a//meta")[0].get('content')			
					if divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='infobar']//time"):
						movie['Runtime'] =  " ".join((c for c in divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='infobar']//time")[0].text.split()[0:2]))
					if divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='infobar']//a//span"):
						movie['Genre'] =  ", ".join((c.text for c in divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='infobar']//a//span")))
					if divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@itemprop='director']//a//span"):
						movie['Director'] = ", ".join((c.text  for c in divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@itemprop='director']//a//span")))
					if divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@itemprop='creator']//a//span"):
						movie['Writer'] = ", ".join((c.text  for c in divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@itemprop='creator']//a//span")))
					if ((divs.xpath("//table//tbody//tr//td[@id='overview-top']//p"))):
						movie['Description'] = ((divs.xpath("//table//tbody//tr//td[@id='overview-top']//p")))[1].text
					if ((divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='star-box giga-star']//div[@class='titlePageSprite star-box-giga-star']"))):
						movie['ImdbRating'] = ((divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='star-box giga-star']//div[@class='titlePageSprite star-box-giga-star']")))[0].text.strip(' ').replace(',','.')
					if ((divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='star-box giga-star']//div[@class='star-box-details']//a"))):
						for tmp in ((divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='star-box giga-star']//div[@class='star-box-details']//a"))):
							if '/' in tmp.text:
								movie['Metascore'] = tmp.text.split('/')[0].strip(' ')
					if ((divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='star-box giga-star']//div[@class='star-box-details']//span"))):
						movie['ImdbVotes'] = ((divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='star-box giga-star']//div[@class='star-box-details']//span")))[3].text
					if divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='infobar']//span[@class='nobr']//a"):
						movie['ImdbID'] = "".join(c for  c in [x if x.startswith('tt') else '' for x in divs.xpath("//table//tbody//tr//td[@id='overview-top']//div[@class='infobar']//span[@class='nobr']//a")[0].get('href').split('/') ])				
					movie['Type'] = 'movie'

				if 'maindetails_center_bottom' in id_tmp:
					
					# temp div
					tmp_div =divs.xpath("//div[@id='titleAwardsRanks']")
					awards = 'N/A'
					if (tmp_div):
						awards = divs.xpath("//div[@id='titleAwardsRanks']/span/b")[0].text
						if(awards):
							awards += ' ' + divs.xpath("//div[@id='titleAwardsRanks']/span")[1].text
						else:
							awards = divs.xpath("//div[@id='titleAwardsRanks']/span")[1].text
					movie['Awards'] = awards
					# print('degub')
					# cast  = divs.xpath("//div[@id='titleCast']//table//tbody//tr//td[@class='primary_photo']//img")
					cast  = divs.xpath("//div[@id='titleCast']//table//tr//td[@class='primary_photo']//img")
					# for tmp_cast in cast:
					# 	print ((tmp_cast.get('loadlate')))
					movie['Actors'] = ", ".join(c.get('title') for c in cast)
					cast_actor=[]

					for tr in cast:					
						profile_image_actor = tr.get('loadlate')
						name_actor = tr.get('title')					
						tmp_actor = {'name':name_actor,'profile_image':profile_image_actor}
						cast_actor.append(tmp_actor)
					movie['Cast_actor'] = cast_actor
					if divs.xpath("//div[@id='titleStoryLine']//div//p"):
						movie['Plot'] = divs.xpath("//div[@id='titleStoryLine']//div//p")[0].text
					if divs.xpath("//div[@id='titleDetails']//div"):
						movie['Country'] = "".join(c.text for c in divs.xpath("//div[@id='titleDetails']//div")[1]).strip('\n').split(':')[1].replace('|', ', ')				
						movie['Language'] = "".join(c.text for c in divs.xpath("//div[@id='titleDetails']//div")[2]).strip('\n').split(':')[1].replace('|', ', ')

					link_sound_track = link.split('/')
					link_sound_track = link_sound_track[0:(len(link_sound_track)-1)]
					link_sound_track = "/".join(c for c in link_sound_track)+'/soundtrack'
					movie['Soundtrack'] = get_soundtrack(link_sound_track)

		movie['Response'] = True
	except Exception as e:
		print e

	
	return json.dumps(movie,indent=4,sort_keys=True)


