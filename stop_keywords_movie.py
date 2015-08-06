# coding: utf-8


quality = ['BRRip','BDrip','HD', 'HDDVDRip','DVDRip','R5','DVDScr', 'Workprint', 'TS', 'TC','CAM','WEBRip','SHQ','HQ','HC','WEB','DL','Full','screener','bluray','rip','bd','dd','SHQ','hdrip','hdcam']
quality_format = ['720p','1080p','3D']
codecs  = ['DivX','DivX HD','XviD','MPEG-1','MPEG-2','OGM','H.264','H 264','x264','h264']
exports = ['VCD','SVCD','KVCD']
format_videos_extends = ['MKV','FLV','AVI','MOV','WMV','RMVB','VOB']
format_audio_extends = ['DTS','AC3','MP3','EVO','aac','5.1','7.1']
idiom = ['dublado','legendado','Dual','ÁUDIO','audio','Nacional','br']

character_strip = ['.','-','(',')', '[',']','{','}']

name_posted_by = ['RARBG','yify','LuanHarper','Alan_680','Luan','Harper','AndreTPF','WOLVERDONFILMES','Hive','CM8','ETRG','juggs','juggs','GoPanda','LuanHarper','Alan','680','The Pirate Filmes','totti9','tpf','sam','rav3n','douglasvip','lonewolf666','santi','titan','anoxmous','wolverdon']

other_words = ['EXTENDED','by','FILMES','xbmc_videodb_2015','.com','700mb','baixando']

stop_word_movies = set(quality+quality_format+codecs+exports+format_videos_extends+format_audio_extends+idiom+name_posted_by+other_words)

stop_word_movies = set(word.lower() for word in stop_word_movies)