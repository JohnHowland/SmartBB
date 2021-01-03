import pygatt
import time
import logging
#import support.lock_control as lock_control
import support.bluetooth_connection as bt_connection

if __name__ == '__main__':
    #LOG_LEVEL = logging.INFO
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = "/home/pi/logs/smartBB.log"
    #LOG_FILE = "/dev/stdout"
    LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
    logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)
    logging.info("Setting up logging")

    # Bluetooth stuff
    MAC = "02:80:E1:00:00:AA"

    ble_device = bt_connection.ble_peripheral(MAC, 10)
   
    while True:
        try:
             ble_device.initiate_connection()
             break
        except:
            logging.debug("Failed to connect. Trying again")
            pass

    ble_device.lock_smartbb()
    ble_device.get_characteristics()
    ble_device.read_characteristic('d973f2e1-b19e-11e2-9e96-0800200c9a66')
    ble_device.unlock_smartbb()
    ble_device.disconnect()


#    adapter = pygatt.GATTToolBackend()

#    while True:
#        try:
#            print("in Try")
#            adapter.start()
#            try:
#                device = adapter.connect(MAC, 10)
#            except:
#                continue
#            device.char_write_handle(0x0011, bytearray([0x55]))
#            print("Write ABCD to 0x0011")
#            time.sleep(2.0)
#            bluetooth_connection.
#            time.sleep(2.0)
#            value = device.char_read('d973f2e1-b19e-11e2-9e96-0800200c9a66')
#            print("Value = " + str(value))
#            time.sleep(2.0)
#        finally:
#            adapter.stop()
#            print("In finally")


