import pygatt
import time


# Bluetooth stuff
MAC = "02:80:E1:00:00:AA"

adapter = pygatt.GATTToolBackend()

try:
    print("in Try")
    adapter.start()
    device = adapter.connect(MAC)
    device.char_write_handle(0x0011, 0xABCD)
    print("Write ABCD to 0x0011")
    time.sleep(2.0)
    value = device.char_read_handle(0x000e)
    print("Value = " + str(value))
    time.sleep(2.0)
finally:
    adapter.stop()
    print("In finally")


