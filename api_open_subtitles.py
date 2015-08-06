# coding: utf-8
import urllib
from lxml import html
import lxml.html as html
from lxml import etree
from lxml.html import fromstring, tostring
import json

url_base = 'http://www.opensubtitles.org'
url_search = 'http://www.opensubtitles.org/pb/search/sublanguageid-pob/imdbid-'


def get_legend(imdbID):
	legend = {}
	

	imdbID = imdbID.strip('tt')
	print (imdbID)
	link = url_search + imdbID
	print (link)
	
	link = '/home/andrei/scripts/torrent/imdb/legend.html'
	link = 'http://www.opensubtitles.org/pb/search/sublanguageid-all/subtrusted-on/hearingimpaired-on/hd-on/autotranslation-on'
	page = None
	tree = None

	response = False

	try:
		page = urllib.urlopen(link)
		tree = etree.HTML(page.read())
	except Exception as inst:
		# print str(inst)
		return json.dumps({'error':{'code':1,'mensage':str(inst)},'response':response})
		

	try:
		for div in tree.xpath("//div[@style='text-align:center']"):
			for a in div.xpath('h1/a'):
				legend['link_download'] = a.get('href')
				legend['name_movie'] = a.xpath('span')[0].text
		

		for span in div.xpath("//div[@itemtype='http://schema.org/Movie']/h2"):
				legend['name_movie_file'] = span.text
		response = True
		return json.dumps({'response':response,'legend':legend})


	except Exception as msg:
		print msg
		legends = []
		try:

			for tr in tree.xpath("//table[@id='search_results']//tr"):
				# for columns of tr 
				index_column = 0

				# to legend 
				name_movie = None
				quality_legend = []
				name_movie_file = None
				language = None
				cd = None
				date = None
				fps = 0.0
				downloads = None
				link_download = None
				legend_type = None
				punctuation = None
				comments = 0
				imdbVote = 0
				autor_name = None
				autor_rank = None

				len_columns = len(tr)
				legend = None
				
				tmp_class = tr.get('class')
				
				if len_columns == 9 and not 'head' in tmp_class:								
					legend = {}
					
					for td in tr.xpath('td'):
						# print ('\t'+str(index_column))
						if index_column == 0:
							for a in td.xpath('strong/a'):
								name_movie =  ((a.text.replace('\n','').replace('\t','')))
								
							for img in td.xpath('img'):
								# print (tostring(img))
								src = img.get('src')
								if src:						
									if '/' in src:
										tmp_src = src.split('/')
										src = tmp_src[len(tmp_src)-1]
										if '.' in src:
											src = src.split('.')[0]	
											# print src
										quality_legend.append(src)

							for br in td.xpath("//br"):						
								if br.tail:
									name_movie_file = br.tail
									
							for span in td.xpath('span'):							
								name_movie_file = span.get('title')
							
							
							# print (name_movie)
							# print (quality_legend)
							# print (name_movie_file)

						if index_column == 1:
							a = td.xpath('a')
							if a:
								language = a[0].get('title')						
							# print (language)
							# print (tostring(td))
						if index_column == 2:
							# print (tostring(td))
							cd = td.text.replace('\n','').replace('\t','')					
							# print (cd)

						if index_column == 3:
							for time in td.xpath('time'):
								date = time.text
							
							for span in td.xpath('span'):
								fps = float(span.text)

							# print (date)
							# print (fps)

						if index_column == 4:
							for a in td.xpath('a'):
								link_download = url_base + a.get('href')
								downloads = int (a.text.replace('x','').replace('\n',''))

							for span in td.xpath('span'):
								legend_type = span.text

							# print link_download	
							# print (downloads)
							# print (legend_type)
						if index_column  == 5:
							punctuation = td.text							
							for img in td.xpath('img'):
								punctuation = (img.get('src').split('/')[len(img)-1])

							# print (punctuation) 

						if index_column == 6:
							comments = td.text
							# print comments

						if index_column == 7:
							imdbVote = td.xpath('a')[0].text
							# print(imdbVote)

						if index_column == 8:
							if len(td.xpath('a'))>0:
								autor_name = td.xpath('a')[0].text
							if len(td.xpath('a/img'))>0:						
								autor_rank = td.xpath('a/img')[0].get('alt')

							# print (autor_name)
							# print (autor_rank)

						index_column +=1;

					legend['name_movie'] = name_movie
					legend['name_movie_file'] = name_movie_file
					legend['quality_legend'] = quality_legend
					legend['language'] = language
					legend['cd'] = cd 
					legend['date'] = date
					legend['fps'] = fps
					legend['downloads'] = downloads
					legend['link_download'] = link_download 
					legend['punctuation'] = punctuation
					legend['comments'] = comments
					legend['imdbVote'] = imdbVote
					legend['autor_name'] = autor_name
					legend['autor_rank'] = autor_rank
					legends.append(legend)
					# print(legend)
					# print ('\n')
					response = True

			return json.dumps({'response':response,'legends':legends})
		
		except Exception as inst:
			print 'error 2 '
			return json.dumps({'error':{'code':2,'mensage':str(inst)},'response':response})

f = open('legendas.json','w')

legenda = get_legend('70219')

print (legenda)

f.write(legenda)
f.close
