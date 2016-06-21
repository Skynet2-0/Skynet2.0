from SharkserversBuyer import SharkserversBuyer


# The code here will actually buy a VPS from Zappiehost
zhb = SharkserversBuyer('ReFmFHFad@bBY.co.uk', 'eSGNdcjNdJMnCVTNrXSgzUVMYZDGqoLl!')
result = zhb.getSSHInfo()

if result == True:
    print("VPS BOUGHT! Details:")
    print("Sharkservers email: " + zhb.getEmail())
    print("Sharkservers password: " + zhb.getPassword())
    print("SSH IP: " + zhb.getIP())
    print("SSH Username: " + zhb.getSSHUsername())
    print("SSH Password: " + zhb.getSSHPassword())
else:
    print("Failed to buy VPS from Sharkservers...")
