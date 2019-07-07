from os import walk

def loadTestCaseNames(*args):
    #Because the main.py file that calls this method is located in the root directory,
	#the relative path of the file needs to behave as though this method is also at the 
	#root of the directory. In this file's internal test, a single integer is passed to the function
	#to give the args list a length of size 1 which allows the function to behave as though the method resides 
	#where it actually resides. 
	foldername = ''    
	if len(args) == 1:
		foldername = '../__test_case_repository'
	else:
		foldername = '__test_case_repository'
	###########################################################################################################
	
	availableFiles = []

	for root, dirs, files in walk(foldername, topdown=False):
		for name in files:
			if '.py' == name[-3:] and name != 'loadTestCaseNames.py':
				availableFiles.append(name)

	return availableFiles


if __name__ == '__main__':
	print(loadTestCaseNames(1))