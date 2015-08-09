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

def main():

	#input path movie , example: test/tt1132620/
	path_movie = '/media/andrei/DOCUMENTOS/FILMES/Hot Pursuit (2015) [1080p]'

	path_movie = os.path.abspath(path_movie)

	#get name and year of movie
	#make function to get name movie through of path_movie
	name_movie = "Hot Pursuit"
	year = '2015'

	#get list link in imdb
	list_links_movies = search_movie(name_movie,year)
	# list_links_movies = ['ok']

	if list_links_movies:
		# get first movie of list 

		movie = get_movie(list_links_movies[0])
		f = open(os.path.join(path_movie,name_movie)+'.json','w')
		# f = open('test.json','w')
		json.dump(json.loads(movie),f,indent=4)
		# json_data=open('test.json').read()
		# json.dump(movie_json,f)
		# movie = json.loads(json_data)
		movie = json.loads(movie)

		# print movie 
		#if Response is True the movie is ok 
		Response = movie['Response']
		if Response:
			download_info_movie(movie,path_movie)


	




	


main()