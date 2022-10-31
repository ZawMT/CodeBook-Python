from zipfile import ZipFile

if __name__ == '__main__':
	input_files = ['01-TestFiles/file1.txt', '01-TestFiles/file2.txt']
	with ZipFile('01-TestFiles/files.zip', mode='w') as zf:
		for f in input_files:
			zf.write(f)