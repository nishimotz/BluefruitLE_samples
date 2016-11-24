from __future__ import print_function

import time
import uuid

import Adafruit_BluefruitLE

IMMEDIATE_ALERT_UUID = uuid.UUID('00001802-0000-1000-8000-00805F9B34FB')
ALERT_LEVEL_UUID = uuid.UUID('00002A06-0000-1000-8000-00805F9B34FB')

provider = Adafruit_BluefruitLE.get_provider()

def main():
    provider.clear_cached_data()
    adapter = provider.get_default_adapter()
    if not adapter.is_powered:
        adapter.power_on()
    print('Searching for device...')
    try:
        adapter.start_scan()
        device = provider.find_device(service_uuids=[IMMEDIATE_ALERT_UUID], name='ITAG')
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
        device.discover([IMMEDIATE_ALERT_UUID], [ALERT_LEVEL_UUID])
        service = device.find_service(IMMEDIATE_ALERT_UUID)
        print('service uuid: {0}'.format(service.uuid))
        alertLevel = service.find_characteristic(ALERT_LEVEL_UUID)
        print('characteristic uuid: {0}'.format(alertLevel.uuid))
        print('Waiting 3 seconds...')
        time.sleep(3)
        print('writing level 2...')
        alertLevel.write_value(chr(2))
        print('Waiting 30 seconds...')
        time.sleep(30)
        print('writing level 0...')
        alertLevel.write_value(chr(0))
        print('Waiting 3 seconds...')
        time.sleep(3)
    finally:
        device.disconnect()
        
provider.initialize()
provider.run_mainloop_with(main)
