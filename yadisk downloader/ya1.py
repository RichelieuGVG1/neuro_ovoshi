import yadisk
import shutil
import time
import zipfile
import argparse
import os

global client

def upload(path, client):
	#print(client)
	if '/' in path:
		zipfilename=path.rsplit('/', 1)[1] + '.zip'
	else:
		zipfilename=path+ '.zip'

	with zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED) as zipf:
		for root, dirs, files in os.walk(path):
			for file in files:
				zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), path))

	new_name = zipfilename.rsplit('.', 1)[0] + '.abc'
	shutil.copyfile(zipfilename, new_name)
    # Загружает "file_to_upload.txt" в "/destination.txt"
	#print(new_name, zipfilename)
	client.upload(new_name, f"/Agro Filtered/{new_name}")
	os.remove(zipfilename)
	os.remove(new_name)
	print(f'Шард загружен. Время выполнения: {round(time.time()-start)} сек.')


def download(path, client):
	if path.isdigit():
		client.download(f"/Agro Filtered/{path}", f"{path}.abc")
	else:
		client.download(f"/Agro Filtered/{path}.abc", f"{path}.abc")
	shutil.copyfile(f"{path}.abc", f"{path}.zip")

	with zipfile.ZipFile(f"{path}.zip", 'r') as zip_ref:
		zip_ref.extractall(f"{path}")

	os.remove(f"{path}.abc")
	os.remove(f"{path}.zip")
	print(f'Шард скачан и разархивирован. Время выполнения: {round(time.time()-start)} сек.')


def main(file_path, operation):
	with open('yandex token.txt', 'r') as file:
		token = file.read().strip()
		client = yadisk.Client(token=token)

	#print(list(client.listdir("disk:/Agro Filtered")))

	if client.check_token()==False:
		print("Ошибка токена.")
		exit()

	elif operation == "upload":
		upload(file_path, client)

	elif operation == "download":
		download(file_path, client)

	else:
		print("Неверно указана операция. Используйте -u для загрузки или -d для скачивания.")
		exit()


import time
start=time.time()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Пример работы с аргументами командной строки")
    parser.add_argument("file_path", help="Путь к файлу")
    parser.add_argument("-u", "--upload", action="store_const", const="upload", dest="operation",
                        help="Выполнить загрузку шарда")
    parser.add_argument("-d", "--download", action="store_const", const="download", dest="operation",
                        help="Выполнить скачивание шарда")
    args = parser.parse_args()
    main(args.file_path, args.operation)
