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
    adapter.power_on(timeout_sec=60)
    print('Searching for device...')
    try:
        adapter.start_scan(timeout_sec=60)
        device = provider.find_device(service_uuids=[BUTTON_SERVICE_UUID], name=None, timeout_sec=60)
        if device is None:
            raise RuntimeError('Failed to find device!')
        else:
            print('device: {0}'.format(device.name))
            print('id: {0}'.format(device.id))
    finally:
        adapter.stop_scan(timeout_sec=60)
    print('Connecting to device...')
    device.connect(timeout_sec=60)
    try:
        print('Discovering services...')
        device.discover([BUTTON_SERVICE_UUID], [BUTTON_VALUE_UUID], timeout_sec=60)
        service = device.find_service(BUTTON_SERVICE_UUID)
        print('service uuid: {0}'.format(service.uuid))
        buttonValue = service.find_characteristic(BUTTON_VALUE_UUID)
        print('characteristic uuid: {0}'.format(buttonValue.uuid))
        print('subscribing...')
        buttonValue.start_notify(received)
        print('Waiting 60 seconds...')
        time.sleep(60)
    finally:
        device.disconnect(timeout_sec=60)
        
provider.initialize()
provider.run_mainloop_with(main)
