import uuid
mac_address = uuid.getnode()
mac_address_hex = ':'.join(['{:02x}'.format((mac_address >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])
print(mac_address_hex)