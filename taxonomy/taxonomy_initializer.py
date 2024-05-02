from taxonomy_preprocess import main as mainn

def main(file_path):
	with open(file_path, "r") as file:
		for line in file:
			mainn(line)
	#return mainn(input_name)
	    
if __name__ == '__main__':
	main('name.txt')
