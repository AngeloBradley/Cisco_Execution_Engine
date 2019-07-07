import json

def loadDeviceList(*args):
	#Because the main.py file that calls this method is located in the root directory,
	#the relative path of the file needs to behave as though this method is also at the 
	#root of the directory. In this file's internal test, a single integer is passed to the function
	#to give the args list a length of size 1 which allows the function to behave as though the method resides 
	#where it actually resides. 
	foldername = ''    
	if len(args) == 1:
		foldername = '../__device_repository/devices.json'
	else:
		foldername = '__device_repository/devices.json'
	###########################################################################################################
	
	with open(foldername) as json_data:
		data = json.load(json_data)

	deviceList = []
	#Unpacking and restructuring json info for response object
	for deviceType, devices in data.items():
		for infoCapsule in devices:
			for genericLabel, device in infoCapsule.items():
				deviceList.append(device)

	return deviceList

if __name__ == '__main__':
	print(loadDeviceList(1))
