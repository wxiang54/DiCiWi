import requests
from pyicloud import PyiCloudService

# Login
api = PyiCloudService('jappleseed@apple.com', 'password')

# Choose first device
    # Optional: add fxnality for multiple devices (be able to choose)
device = api.devices[0]

print device.location