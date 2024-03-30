from taxonomy_preprocess import main as mainn
from taxonomy_preprocess import taxonomy_data_loader as loader

def main():
	loader()
	input_name = input('Enter certain name of species> ')
	return mainn(input_name)
	    
if __name__ == '__main__':
	main()
	import os
	os.system('pause')
