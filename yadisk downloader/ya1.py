import yadisk
import shutil
import time
import zipfile
import argparse

def upload(path):
	zipfilename=path.rsplit('/', 1)[1] + '.zip'

	with zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), path))

    new_name = zipfilename.rsplit('.', 1)[1] + '.abc'
	shutil.copyfile(zipfilename, new_name)
    # Загружает "file_to_upload.txt" в "/destination.txt"
	client.upload("tomato1.abc", f"/Agro Filtered/{new_name}")
	print(f'Шард загружен. Время выполнения: {round(time.time()-start)} сек.')


def download(path):
	client.download(f"/Agro Filtered/{path}", f"{path}.abc")
	shutil.copyfile(f"{path}.abc", f"{path}.zip")

	with zipfile.ZipFile(f"{path}.zip", 'r') as zip_ref:
    	zip_ref.extractall(f"{path}")

	print(f'Шард скачан и разархивирован. Время выполнения: {round(time.time()-start)} сек.')


def main(file_path, operation):
	with open('yandex token.txt', 'r') as file:
    	token = file.read().strip()
		client = yadisk.Client(token=token)

	if client.check_token()==False:
		print("Ошибка токена.")
        exit()

    if operation == "upload":
        upload(file_path)

    if operation == "download":
        download(file_path)

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
