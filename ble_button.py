from __future__ import print_function

import time
import uuid

import Adafruit_BluefruitLE

BUTTON_SERVICE_UUID = uuid.UUID('0000ffe0-0000-1000-8000-00805f9b34fb')
BUTTON_VALUE_UUID = uuid.UUID('0000ffe1-0000-1000-8000-00805f9b34fb')

provider = Adafruit_BluefruitLE.get_provider()

def received(data):
    print('Received: {0}'.format(ord(data[0])))

def main():
    provider.clear_cached_data()
    adapter = provider.get_default_adapter()
    if not adapter.is_powered:
        adapter.power_on()
    print('Searching for device...')
    try:
        adapter.start_scan()
        device = provider.find_device(service_uuids=[BUTTON_SERVICE_UUID], name='ITAG')
        if device is None:
            raise RuntimeError('Failed to find device!')
        else:
            print('device: {0}'.format(device.name))
            print('id: {0}'.format(device.id))
    finally:
        adapter.stop_scan()
    print('Connecting to device...')
    device.connect()
    try:
        print('Discovering services...')
        device.discover([BUTTON_SERVICE_UUID], [BUTTON_VALUE_UUID])
        service = device.find_service(BUTTON_SERVICE_UUID)
        print('service uuid: {0}'.format(service.uuid))
        buttonValue = service.find_characteristic(BUTTON_VALUE_UUID)
        print('characteristic uuid: {0}'.format(buttonValue.uuid))
        print('subscribing...')
        buttonValue.start_notify(received)
        print('Waiting 60 seconds...')
        time.sleep(60)
    finally:
        device.disconnect()
        
provider.initialize()
provider.run_mainloop_with(main)
