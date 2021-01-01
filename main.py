import pygatt


# Bluetooth stuff
MAC = "02:80:E1:00:00:AA"

adapter = pygatt.BGAPIBackend()

try:
    print("in Try")
    adapter.start()
    device = adapter.connect(MAC)
    value = device.char_read("a1e8f5b1-696b-4e4c-87c6-69dfe0b0093b")
    print("Value = " + str(value))
finally:
    adapter.stop()
    print("In finally")


