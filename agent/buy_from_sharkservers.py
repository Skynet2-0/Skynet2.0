from SharkserversBuyer import SharkserversBuyer


# The code here will actually buy a VPS from Zappiehost
zhb = SharkserversBuyer('MbnXeB@EmhCbrLi.eu', 'XzaChKQqtTkoxhsVTRJbUbcaRPxJWFMa!')
result = zhb.getSSHInfo()

if result == True:
    print("VPS BOUGHT! Details:")
    print("Zappiehost email: " + zhb.getEmail())
    print("Zappiehost password: " + zhb.getPassword())
    print("SSH IP: " + zhb.getIP())
    print("SSH Username: " + zhb.getSSHUsername())
    print("SSH Password: " + zhb.getSSHPassword())
else:
    print("Failed to buy VPS from Zappiehost...")
