from __future__ import print_function

import time
import uuid

import Adafruit_BluefruitLE

BATTERY_SERVICE_UUID = uuid.UUID('0000180f-0000-1000-8000-00805f9b34fb')
BATTERY_LEVEL_UUID = uuid.UUID('00002a19-0000-1000-8000-00805f9b34fb')

provider = Adafruit_BluefruitLE.get_provider()

def to_str(v):
    return ''.join([chr(c) if isinstance(c, int) else c for c in v])
    
def main():
    provider.clear_cached_data()
    adapter = provider.get_default_adapter()
    if not adapter.is_powered:
        adapter.power_on()
    print('Searching for device...')
    try:
        adapter.start_scan()
        device = provider.find_device(service_uuids=[BATTERY_SERVICE_UUID], name='ITAG')
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
        device.discover([BATTERY_SERVICE_UUID], [BATTERY_LEVEL_UUID])
        service = device.find_service(BATTERY_SERVICE_UUID)
        print('service uuid: {0}'.format(service.uuid))
        battLevel = service.find_characteristic(BATTERY_LEVEL_UUID)
        print('characteristic uuid: {0}'.format(battLevel.uuid))
        print('reading...')
        v = battLevel.read_value()
        v = to_str(v)
        print('battery: {0}'.format(ord(v[0])))
    finally:
        device.disconnect()
        #adapter.power_off()
provider.initialize()
provider.run_mainloop_with(main)
