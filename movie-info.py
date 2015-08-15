# coding: utf-8

import os, sys, inspect

 # realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)

 # use this if you want to include modules from a subfolder
cmd_subfolder  = []
cmd_subfolder.append(os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"API"))))
cmd_subfolder.append(os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"libs"))))
cmd_subfolder.append(os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"test"))))

for tmp_cmd_subfolder in cmd_subfolder:
	if tmp_cmd_subfolder not in sys.path:
	 	sys.path.insert(0, tmp_cmd_subfolder)



import stop_keywords_movie, lib_downloads, api_open_subtitles, json, string,  unicodedata, urllib

from api_imdb import search_movie,get_movie
from lib_downloads import download_info_movie
import errno

def extract_name_movie(path_movie):
	name_movie = ''	
	year = ''
	path, dir_movie = os.path.split(path_movie)

	for c in stop_keywords_movie.character_strip:
		dir_movie = dir_movie.replace(c,' ')
	
	for word in dir_movie.split():
		# print word
		name_movie += word + ' '

		if len(word) == 4:
			try:
				year = int(word)
				name_movie = name_movie.replace(word+' ','')
				break
			except Exception as e:
				
				pass

	# print name_movie,year
	# print dir_movie
	if year:
		return {'name_movie':name_movie,'year':year}
	else:
		return {}


def main():

	path_movies = "/media/andrei/DOCUMENTOS/FILMES/"

	path_movie  = "/media/andrei/DOCUMENTOS/FILMES/O.Franco.Atirador.2015.720p.Dual-WOLVERDONFILMES.COM/"
	for path_movie in os.listdir(path_movies):
		get_info_movie(os.path.join(path_movies,path_movie))
		print ('\n')
	# get_info_movie(path_movie)


def is_named_movie(name_movie,year,movie):

	name_movie = name_movie.lower().replace(',',' ')
	movie_title = movie['Title'].lower().replace(',',' ')
	movie_name_pt =movie['name_pt'].lower().replace(',',' ')

	name_movie = name_movie.replace(',',' ')
	year = str(year).replace(',',' ')

	for c in stop_keywords_movie.character_strip:
		if c in movie_title:
			movie_title = movie_title.replace(c,' ')	
		if c in movie_name_pt:
			movie_name_pt = movie_name_pt.replace(c,' ')	


	#test ingles
	name_movie_split = name_movie.split()
	movie_title_split = movie_title.split()
	movie_name_pt_split = movie_name_pt.split()

	name_movie_size = len(name_movie_split)
	movie_title_size = len(movie_title_split)
	movie_name_pt_size = len(movie_name_pt_split)

	count_word = 0

	for word in name_movie_split:
		if word in movie_title_split:
			count_word +=1
			pass
		if word in movie_name_pt_split:
			count_word +=1
			pass 

	

	# if count_word/movie_name_pt_size > 0.8 or count_word/movie_title_size > 0.8 :

	# 	print count_word
	# 	print name_movie_split, name_movie_size, year
	# 	print movie_title_split,movie_title_size, movie['Year']
	# 	print movie_name_pt_split, movie_name_pt_size, movie['Release_nobr_date'].split('-')[0]



	if (year) == movie['Year'] or (year) == movie['Release_nobr_date'].split('-')[0]:
		if count_word/movie_name_pt_size > 0.8 or count_word/movie_title_size > 0.8 :
			print(name_movie,year,'and',movie['Title'], movie['Year'])					
			return True
	return False
	


def get_info_movie(path_movie):
	#input path movie , example: test/tt1132620/
	# path_movie = '/media/andrei/DOCUMENTOS/FILMES/Hot Pursuit (2015) [1080p]'

	# path_movie = os.path.abspath(path_movie)
	
	name_movie = ''
	year = ''

	movie_name = extract_name_movie(path_movie)

	if movie_name:
		name_movie = movie_name['name_movie']
		year = movie_name['year'] 

	if name_movie:

	#get name and year of movie
	#make function to get name movie through of path_movie
		print name_movie,'\t',year

	# #get list link in imdb
	list_links_movies = search_movie(name_movie,year)
	
	# # list_links_movies = ['ok']

	if list_links_movies:
		print list_links_movies[0]
	# 	# get first movie of list 

		movie_json = get_movie(list_links_movies[0])
		movie = json.loads(movie_json)

		if movie['Response']:

			if is_named_movie(name_movie,year,movie):
				print name_movie
			else:
				list_links_movies = search_movie(name_movie,'')
				if list_links_movies:
					movie_json = get_movie(list_links_movies[0])
					movie = json.loads(movie_json)
					if movie['Response']:
						if is_named_movie(name_movie,'',movie):
							print name_movie
					else:
						pass

			f = open(os.path.join(path_movie,name_movie.replace(' ','_'))+'.json','w')	
			json.dump(movie,f,indent=4, sort_keys=True)
			f.close()

			download_info_movie(movie,path_movie)

	# 	# json_data=open('test.json').read()
	# 	# json.dump(movie_json,f)
	# 	# movie = json.loads(json_data)
	# 	movie = json.loads(movie)

	# 	# print movie 
	# 	#if Response is True the movie is ok 
	# 	Response = movie['Response']
	# 	if Response:
			

	


main()