# coding: utf-8

"""
this module constains functions to downloads
need of modules import: urllib 

"""
import os, sys, inspect,json, operator,urllib
import subprocess

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

# print sys.path
from api_open_subtitles import get_legend
from api_youtube import search_soundtrack




def download_file(download_url,download_name,path,formatt):
	"""
	this function download through of 'download_url'
	"""	
	try:
		filename  = os.path.join(path+download_name+formatt)
		if not  os.path.isfile(filename):
			print ('\tdownloading...\t[' + download_url +'] in ['+filename  +']' )
			urllib.urlretrieve(download_url, filename)
	except Exception as e:
		print e
	

def download_info_movie(movie,path_movie, download_legends=True,download_poster=True,download_actor_posters=True,download_trailer=True, download_soundtracks=True):
	path_movie_subtitles = 'subtitles/'
	path_movie_actor_poster = 'actor_posters/'
	path_movie_screenshot = 'screenshots/'
	path_movie_trailers = 'trailers/'
	path_movie_soundtracks = 'soundtracks/'

	path_movie = os.path.join(path_movie,'')
	print (path_movie)	

	#get info of movie 

	Year = movie['Year']			
	Title = movie['Title']			
	imdbID = movie['ImdbID']
	Poster = movie['Poster']
	soundtracks= movie['Soundtrack']
	Cast_actor = movie['Cast_actor']

	# json_data=open('legend.json').read()

	# download_legends = False
	if download_legends:
		try:
			path_movie_subtitles = os.path.join(path_movie,path_movie_subtitles)

			if not os.path.exists(path_movie_subtitles):
				os.mkdir(path_movie_subtitles)

			


			print path_movie_subtitles

			legends  = get_legend(imdbID)
			legends = json.loads(legends)
			fileToJson = open(os.path.join(path_movie_subtitles,Title+'[legend]')+'.json','w')			
			json.dump(legends,fileToJson, indent=4,sort_keys = True)
			fileToJson.close()
			# legends = json.loads(json_data)
			response = legends['response']
			if response:
				if legends['legends']:				
					great  = 0
					list_top_legends = []
					for legend in legends['legends']:						
						downloads =  legend['downloads']
						link_download =  legend['link_download']
						# list_top_legends[link_download] = downloads
						list_top_legends.append([link_download,downloads])
					
					list_top_legends = sorted(list_top_legends)

					n_legends = 5 

					if len(list_top_legends) < n_legends:
						n_legends = len(list_top_legends)

					for i in range(n_legends):
						download_url = list_top_legends[i][0]
						download_name = download_url.split('/')
						download_name = download_name[len(download_name)-1]
						print '\tdownloading legend\t['+download_name+'.zip]' 

						download_file(download_url,download_name,path_movie_subtitles,'.zip')

				else:
					print legends

			
		except OSError, e:
			print e
			# exit()
		
		
	if download_poster:
		print path_movie
		if '@.' in Poster:
			Poster =  Poster.split('@.')[0] +'@.jpg'
			# Poster =  Poster[0] + Poster[len(Poster)-1].split('.')[1]
			# Poster =  Poster[0] + '@.jpg'
			
			print ('\tdownloading Poster..\t[Poster.jpg]')
			download_url = Poster
			download_name = 'Poster'
			download_file(Poster,download_name,path_movie,'.jpg')

	if download_actor_posters:
		try:
			path_movie_actor_poster = os.path.join(path_movie,path_movie_actor_poster)
			if not os.path.exists(path_movie_actor_poster):
				os.mkdir(path_movie_actor_poster)
			print path_movie_actor_poster
			if Cast_actor:
				for actor in Cast_actor:
					
					actor_name = actor['name'] 
					download_url = actor['profile_image']
					if download_url:
						download_url = download_url.replace('._V1_UX32_CR0,0,32,44_AL_','')
						# actor_name = "_".join(c for c in actor_name.split())
						print '\tdownloading picture..\t['+actor_name+']'
						download_url =  download_url.split('@.')[0] +'@.jpg'
						download_file(download_url,actor_name,path_movie_actor_poster,'.jpg')
						# print actor_name,download_url

		except Exception as e:
			print e
	
	if download_soundtracks:
		path_movie_soundtracks = os.path.join(path_movie,path_movie_soundtracks)

		if not os.path.exists(path_movie_soundtracks):
			os.mkdir(path_movie_soundtracks)

		print path_movie_soundtracks


		for soundtrack in soundtracks:
			list_search_soundtrack = search_soundtrack(soundtrack,Title)
			list_search_soundtrack = json.loads(list_search_soundtrack)


			response = list_search_soundtrack['response']
			if response:
				results = list_search_soundtrack['results']
				name_file_soundtrack = path_movie_soundtracks+soundtrack+'['+Title+']'
				if results and not os.path.isfile(name_file_soundtrack+'.*'):					
					link_one = results[0]					
					command = 'youtube-dl '
					args = "--extract-audio --audio-format mp3 -o \""+name_file_soundtrack+ ".%(ext)s\" " + link_one					
					call = command
					call +=args
					return_code = subprocess.check_call(call,shell=True)
				
	if download_trailer:
		path_movie_trailers = os.path.join(path_movie,path_movie_trailers)

		if not os.path.exists(path_movie_trailers):
			os.mkdir(path_movie_trailers)

		print path_movie_trailers


		list_search_trailers = search_soundtrack('Trailer ' + Year ,Title)	
		list_search_trailers = json.loads(list_search_trailers)
		response = list_search_trailers['response']
		if response:
			results = list_search_trailers['results']
			name_file_trailer = path_movie_trailers+Title+" [trailer]"

			if results:					
				link_one = results[0]					
				command = 'youtube-dl '
				args = "-f 22/18/5 -o \""+name_file_trailer+".%(ext)s\" " + link_one					
				call = command
				call +=args
				return_code = subprocess.check_call(call,shell=True)

		name_file_trailer = path_movie_trailers+Title+" [trailer legendado]"

		exists_trailer = False

		list_search_trailers = search_soundtrack('Trailer legendado ' + Year ,Title)	
		list_search_trailers = json.loads(list_search_trailers)
		response = list_search_trailers['response']
		if response:
			results = list_search_trailers['results']
			if results :					
				link_one = results[0]					
				command = 'youtube-dl '
				args = "-f 22/18/5 -o \""+name_file_trailer+ ".%(ext)s\" " + link_one					
				call = command
				call +=args
				return_code = subprocess.check_call(call,shell=True)
		
__author__ = "Andrei Bastos"
__copyright__ = "Copyright"
__version__ = "1.0.1"
__email__ = "andreibastos@outlook.com"
__status__ = "Production"