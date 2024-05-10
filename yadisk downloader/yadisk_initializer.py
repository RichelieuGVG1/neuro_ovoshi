import yadisk
import shutil
import time
import zipfile
import argparse
import os

from ya1 import upload, download

global client
global flag
global path

flag = 1
path = 'sharden'

def main():
	with open('yandex token.txt', 'r') as file:
		token = file.read().strip()
		client = yadisk.Client(token=token)

	if flag:
		for entry in os.scandir(path):
			if entry.is_dir():
				#print(entry.name)
				upload(path+'/'+entry.name, client)
	else:
		download(path, client)

if __name__ == '__main__':
	main()