# coding: utf-8

import os
import stop_keywords_movie
import api_imdb
import json, string,  unicodedata
import urllib
dir_downloads_complet = '/media/andrei/DOCUMENTOS/FILMES/'





def get_dirs_movies(dir_source):
	list_dirs = []

	list_movies = []

	#get absolut dir 
	dir_source = os.path.abspath(dir_source)

	#get list of all (file and dir) in dir_source
	dir_source_dirs = os.listdir(dir_source)

	#get each element of list
	for dirs in dir_source_dirs:
		dir_path = os.path.join(dir_source, dirs)
		
		#check what is dir!
		if os.path.isdir(dir_path):
			list_dirs.append(dir_path)

			list_movies.append(dirs)
			# print(os.listdir(dir_path))
			# print(dir_path)
			# print(dirs)

	return [list_dirs,list_movies]
	# print(list_dirs)



def contains_legend_in_dir(dir_movie):
	#get list all files and dirs in dir_movie
	dir_of_movie = os.listdir(dir_movie)
	# print(dir_movie)
	for file_or_dir in dir_of_movie:
		if '.srt' in file_or_dir:
			print ('\t '+file_or_dir)

def contains_legend_in_dirs(list_dir_movies):
	for dir_movie in list_dir_movies:
		contains_legend_in_dir(dir_movie)




def get_all_full_name(list_dir_movies):
	list_movie_full_name_and_year = []
	for dir_movie in list_dir_movies:
		list_movie_full_name_and_year.append(get_full_name_movie_and_year(dir_movie))
	return list_movie_full_name_and_year

def get_full_name_movie_and_year(movie_name_in_dir):
	name_movie = movie_name_in_dir.lower()
	# name_movie = remove_latin_accents(name_movie)
	year = ''
	real_name_movie = ''
	print (name_movie)

	tmp_name = ''
	for word in name_movie.split('.'):
		for c in stop_keywords_movie.character_strip:
			if c in word:
				word = word.replace(c,'')
		print (word)
		tmp_name += word+' ' 
		if len(word) == 4:
			try:				
				year = int(word)
				tmp_name = tmp_name.strip(str(word+' '))
				print(tmp_name)
				return {'name_movie':tmp_name,'year':year}
			except Exception:
				pass


	if word in stop_keywords_movie.stop_word_movies:			
			name_movie = name_movie.replace(word,'')
			# print (name_movie)

	for c in stop_keywords_movie.character_strip:
		name_movie = name_movie.replace(c,' ')

	for word in name_movie.split():
		if word in stop_keywords_movie.stop_word_movies:
			name_movie = name_movie.replace(word,'')
	
	
	for word in name_movie.split():
		real_name_movie += word +' '	

		if len(word) == 4:
			try:
				year = int(word)
				real_name_movie = real_name_movie.replace(' '+word+' ','')
			except ValueError:
				pass
				
			pass	

	# print(real_name_movie)
	return {'name_movie':real_name_movie,'year':year}

def contains_json_dir_movie(dir_movie):
	for f in os.listdir(dir_movie):
		if 'json' in f.split('.'):
			return True
	return False

def remove_dir_movie_with_json(list_dir_and_movies):
	list_dir_movie_without_json = []
	# for dir_movie,movie in list_dir_and_movies[0],list_dir_and_movies[1]:
	for i in range(0,len(list_dir_and_movies[0])):
		if not contains_json_dir_movie(list_dir_and_movies[0][i]):
			list_dir_movie_without_json.append([list_dir_and_movies[0][i],list_dir_and_movies[1][i]])
	return list_dir_movie_without_json


def is_named_movie(full_name_movie_and_year,movie):
	# falta o ano :S
	name_movie = full_name_movie_and_year['name_movie']
	year = str(full_name_movie_and_year['year'])
	movie_title = movie['Title'].lower()
	movie_name_pt =movie['name_pt'].lower()

	for c in stop_keywords_movie.character_strip:
		if c in movie_title:
			movie_title = movie_title.replace(c,'')	
		if c in movie_name_pt:
			movie_name_pt = movie_name_pt.replace(c,'')	
	# print("movie:", name_movie,year)			
	# print("search:",movie['Title'],movie['name_pt'], movie['Year'],movie['Release_nobr_date'].split('-')[0])
	# # print( )
	if (year) == movie['Year'] or (year) == movie['Release_nobr_date'].split('-')[0]:
		# print (year,movie['Year'])

		if movie_title in name_movie or movie_name_pt in name_movie: 
			print(name_movie,year,'and',movie['Title'], movie['Year'])					
			return True
	return False

def test_links(list_links_movies,full_name_movie_and_year):
		if list_links_movies:
			count_error = 0			
			for link in list_links_movies:
				
				movie = api_imdb.get_movie(link)
				if is_named_movie(full_name_movie_and_year,movie):
					# print('é')
					return movie
				else:
					count_error+=1
					# print('não é')
					if (count_error == 2):
						return {}
					
		else:
			return 'not found'

def download_image(image_url,name_image,path):
	imgs = image_url.split('.')
	formatt = '.'+imgs[len(imgs)-1]
	# print (imgs[len(imgs)-1])
	print (urllib.urlretrieve(image_url, path+name_image+formatt))


def get_json_all_movies(list_dir_movie_without_json):
	#get name and year of movie
	# list_movie_full_name_and_year = get_all_full_name(list_dir_movie_without_json[1])
	# print(range(len(list_dir_movie_without_json)))
	for i in range(0,len(list_dir_movie_without_json)):
		
		

		name_movie = list_dir_movie_without_json[i][1]
		path = list_dir_movie_without_json[i][0]
		# print (path)
		json_write = path+'/'+name_movie.replace(' ','_')+'.json'
		



		full_name_movie_and_year = get_full_name_movie_and_year(name_movie)
		year = full_name_movie_and_year['year']
		name = full_name_movie_and_year['name_movie']

		list_links_movies = api_imdb.get_list_search(full_name_movie_and_year)


		movie = test_links(list_links_movies,full_name_movie_and_year)
		
		if not movie:
			list_links_movies = api_imdb.get_list_search({'name_movie':name,'year':''})
			movie = test_links(list_links_movies,full_name_movie_and_year)
			# if (movie):
			# 	print (movie)
		else:
			if 'not found' in movie:
				list_links_movies = api_imdb.get_list_search({'name_movie':name,'year':''})
				movie = test_links(list_links_movies,full_name_movie_and_year)
				# print(movie)
		print (movie)
		
		print (json_write)
		f = open(json_write,'w')
		json.dump(movie,f)


def main():
	#get all filme dir name movie of dir 
	list_dir_and_movies = get_dirs_movies(dir_downloads_complet);

	# remove dir movie with json
	list_dir_movie_without_json = remove_dir_movie_with_json(list_dir_and_movies)
	# print(list_dir_movie_without_json)
	# download_image('http://ia.media-imdb.com/images/M/MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@._V1_SX214_AL_.jpg','jhon','./')
	get_json_all_movies(list_dir_movie_without_json)

	# name_movie = list_movie_full_name_and_year[0]

	# list_links_movies = api_imdb.get_list_search(name_movie)

	# link_movie = list_links_movies[0]
	# for link_movie in list_links_movies:
	# api_imdb.verify_link_is_movie(list_links_movies[0],name_movie)
	# api_imdb.get_movie(link_movie)
	# movie = api_imdb.get_movie('/home/andrei/scripts/torrent/imdb/movie.html')
		# movie = api_imdb.get_movie(link_movie)
		# print (movie)

	# contains_legend_in_dirs(list_dir_and_movies[0])

main()