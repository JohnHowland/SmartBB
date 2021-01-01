import pygatt
import time


# Bluetooth stuff
MAC = "02:80:E1:00:00:AA"

adapter = pygatt.GATTToolBackend()

try:
    print("in Try")
    adapter.start()
    device = adapter.connect(MAC, 10)
    device.char_write_handle(0x0011, bytearray([0x55]))
    print("Write ABCD to 0x0011")
    time.sleep(2.0)
    print("Reading characteristics")
    print(device.discover_characteristics())
    time.sleep(2.0)
    value = device.char_read('d973f2e1-b19e-11e2-9e96-0800200c9a66')
    print("Value = " + str(value))
    time.sleep(2.0)
finally:
    adapter.stop()
    print("In finally")


