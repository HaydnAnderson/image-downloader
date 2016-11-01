import urllib, json, sys, os.path, argparse
import hashlib
import time
import re



# //==== EDIT THIS ====\\

log_file = open('log.txt', 'r+')
username = 'dronenerds'
sleep_time = 120
download_img = False
console_log = True
download_img1 = True
path_name = 'images/'

# //==== EDIT THIS ====\\

def find_new_images(images, existing):
	ids = [i['id'] for i in existing]
	return [i for i in images if i['id'] not in ids]

def get_img(username):
	url = 'http://www.instagram.com/{}/media'.format(username)
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return data['items']

def download_image(url):
	filename = url.split('/')[-1]
	fullfilename = os.path.join(path_name, filename)
	urllib.urlretrieve(url, fullfilename)

def get_url(geturl):
	instaurl = geturl['images']['standard_resolution']['url']
	path = re.sub(r'\w\d{3}x\d{3}\/', '', instaurl)
	path = path.split('?')[0]
	return path

def get_args():
    parser = argparse.ArgumentParser(description='Download images from Instagram')
    parser.add_argument('-u', '--username', type=str, help='Instagram username')
    parser.add_argument('-s', '--sleep', type=int, default=120, help='How long to sleep inbetween checks')
    parser.add_argument('-d', '--dry-run', action='store_false', help='Don\'t actually download old images, but download new ones')
    parser.add_argument('-i', '--i-path', type= str, default='images/', help='Image download folder')
    args = parser.parse_args()
    return args.username, args.sleep, args.dry_run, args.i_path

def main():
	if console_log:
		username, sleep_time, download_img1, path_name = get_args()
	else:
		pass
	print "Getting twenty photos from {}".format(username)
	images = get_img(username)
	if not os.path.exists(path_name):
		os.makedirs(path_name)
	if download_img:
		print "Downloading..."
		for i in images:
			download_image(get_url(i))
	last = images
	while True:
		time.sleep(sleep_time)
		images = get_img(username)
		new_images = find_new_images(images, last)
		last = images
		if new_images:
			print "{} new post(s)".format(len(new_images))
			if download_img1:
				for image in new_images:
					download_image(get_url(image))

if __name__ == "__main__":
	sys.exit(main())
