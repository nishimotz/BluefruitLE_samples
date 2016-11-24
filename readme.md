BluefruitLE_samples

2016-09-15 IoTLT Hiroshima Vol.3

Takuya Nishimoto (nishimotz)

* http://ja.nishimotz.com/iotlt_hiroshima

ITAG KeyFinder

* http://amzn.to/2cixREA

Adafruit Python BluefruitLE

* https://github.com/adafruit/Adafruit_Python_BluefruitLE
* https://learn.adafruit.com/bluefruit-le-python-library/usage

Ubuntu Linux + Bluez (5.37 is recommended)

```
$ sudo apt-get update
$ sudo apt-get -y install libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
$ wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.37.tar.gz
$ tar xvfz bluez-5.37.tar.gz
$ cd bluez-5.37
$ ./configure --disable-systemd
$ make
$ sudo make install
$ sudo cp ./src/bluetoothd /usr/local/bin/

$ sudo apt-get install python-dbus

$ cat /etc/rc.local 
#!/bin/sh -e
/usr/local/bin/bluetoothd --experimental &
exit 0

$ sudo chmod 755 /etc/rc.local
```
