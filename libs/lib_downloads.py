# coding: utf-8

"""
this module constains functions to downloads
need of modules import: urllib 

"""


def download_file(download_url,download_name,path,formatt):
	"""
	this function download through of 'download_url'
	"""	
	if '.' in download_url:
		tmp_split_link = download_url.split('.')
		formatt = '.'+tmp_split_link[len(tmp_split_link)-1]	
	try:
		urllib.urlretrieve(download_url, path+download_name+formatt)
	except Exception as e:
		print e
	


__author__ = "Andrei Bastos"
__copyright__ = "Copyright"
__version__ = "1.0.1"
__email__ = "andreibastos@outlook.com"
__status__ = "Production"