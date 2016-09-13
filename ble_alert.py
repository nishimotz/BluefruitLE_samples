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
    adapter.power_on(timeout_sec=60)
    print('Searching for device...')
    try:
        adapter.start_scan(timeout_sec=60)
        device = provider.find_device(service_uuids=[IMMEDIATE_ALERT_UUID], name='ITAG', timeout_sec=60)
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
        device.discover([IMMEDIATE_ALERT_UUID], [ALERT_LEVEL_UUID], timeout_sec=60)
        service = device.find_service(IMMEDIATE_ALERT_UUID)
        print('service uuid: {0}'.format(service.uuid))
        alertLevel = service.find_characteristic(ALERT_LEVEL_UUID)
        print('characteristic uuid: {0}'.format(alertLevel.uuid))
        print('Waiting 3 seconds...')
        time.sleep(3)
        print('writing level 2...')
        alertLevel.write_value(chr(2))
        print('Waiting 3 seconds...')
        time.sleep(3)
        print('writing level 0...')
        alertLevel.write_value(chr(0))
        print('Waiting 3 seconds...')
        time.sleep(3)
    finally:
        device.disconnect(timeout_sec=60)
        
provider.initialize()
provider.run_mainloop_with(main)
