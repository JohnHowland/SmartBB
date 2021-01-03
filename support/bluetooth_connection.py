import pygatt
import time
import logging

class ble_peripheral():
    def __init__(self, MAC, timeout):
        logging.debug("MAC: " + MAC + "timeout: " + str(timeout))
        self.MAC = MAC
        self.timeout = timeout
        self.adapter = pygatt.GATTToolBackend()

    def initiate_connection(self):
        logging.debug("initiating BLE connction")
        self.adapter.start()
        self.device = self.adapter.connect(self.MAC, self.timeout)

    def disconnect(self):
        logging.debug("Disconnecting BLE connction")
        self.device.disconnect()

    def lock_smartbb(self):
        logging.debug("Lock smartBB command")
        self.device.char_write_handle(0x0011, bytearray([0x55]))

    def unlock_smartbb(self):
        logging.debug("Unlock smartBB command")
        self.device.char_write_handle(0x0011, bytearray([0x4C]))

    def get_characteristics(self):
        logging.debug("Reading characteristics")
        logging.debug(self.device.discover_characteristics())

    def read_characteristic(self, uuid):
        return self.device.char_read(uuid)

