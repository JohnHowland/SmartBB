import bluetooth

# Bluetooth stuff
bd_addr = "20:13:05:30:01:14"
port = 1
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

# 0x1X for straight forward and 0x11 for very slow to 0x1F for fastest
sock.send('\x1A')

sock.close()
