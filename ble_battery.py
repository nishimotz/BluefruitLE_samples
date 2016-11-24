from __future__ import print_function

import time
import uuid

import Adafruit_BluefruitLE

BATTERY_SERVICE_UUID = uuid.UUID('0000180F-0000-1000-8000-00805f9b34fb')
BATTERY_LEVEL_UUID = uuid.UUID('00002a19-0000-1000-8000-00805f9b34fb')

provider = Adafruit_BluefruitLE.get_provider()

def main():
    provider.clear_cached_data()
    adapter = provider.get_default_adapter()
    adapter.power_on()
    print('Searching for device...')
    try:
        adapter.start_scan()
        device = provider.find_device(service_uuids=[BATTERY_SERVICE_UUID], name=None, timeout_sec=60)
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
        device.discover([BATTERY_SERVICE_UUID], [BATTERY_LEVEL_UUID], timeout_sec=60)
        service = device.find_service(BATTERY_SERVICE_UUID)
        print('service uuid: {0}'.format(service.uuid))
        battLevel = service.find_characteristic(BATTERY_LEVEL_UUID)
        print('characteristic uuid: {0}'.format(battLevel.uuid))
        print('reading...')
        v = battLevel.read_value()
        print('battery: {0}'.format(ord(v[0])))
    finally:
        device.disconnect()
        
provider.initialize()
provider.run_mainloop_with(main)
