from pyicloud import PyiCloudService

# Login
appleID = raw_input('Enter your Apple ID: ')
applePass = raw_input('Enter your password: ')

appleData = PyiCloudService(appleID, applePass)

# Choose first device
device = appleData.devices[0]
device.play_sound()