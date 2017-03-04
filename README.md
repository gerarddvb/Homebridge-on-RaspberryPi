# Homebridge on Raspberry Pi 3


# NOT USEABLE!!!!


Example of Homebridge on RaspberryPi 3

## READ: https://github.com/nfarina/homebridge

This example gives the config of 7 accessories/devices; 
- Philips Hue (1st gen Bridge)
- Nest thermostat (3rd gen)
- Logitech Harmony Hub
- Raspberry Pi 3 with GPIO input and output
- GPS based sunset triggers
- GPS based temperature sensor
- Delayed off switches


# Setup Raspberry Pi

## System setup

First we need to setup the Raspberry Pi, open terminal and enter the following command:

  ```
  sudo raspi-cofig
  ```

In the config tool enable SSH, VNC and Autologin

After that open a new terminal window and enter the following command:

  ```
  sudo reboot
  ```

## Download setup files

Download the setup files, enter the following command:
  
  ```
  git clone https://github.com/gerarddvb/Homebridge-on-RaspberryPi /home/pi/HomeKit/
  ```
  
# Setup APT

Now it is time to setup APT, enter the following commands:

  ```
  sudo apt-get update

  sudo apt-get upgrade
  ```

# Edit Boot configuration file

Pixel uses RealVNC, if you want to use VNC you should enter the following command:

  ```
  sudo nano /boot/config.txt
  ```
  
Uncheck (-#) the following lines:

```
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=30
```

Add the following line:

```
dtparam=watchdog=on
```

# Install Homebridge

## NodeJS

NodeJS is needed to run Homebridge on Raspberry Pi, run the following commands to install NodeJS:

> wget https://nodejs.org/dist/v4.3.2/node-v4.3.2-linux-armv6l.tar.gz 

> tar -xvf node-v4.3.2-linux-armv6l.tar.gz 

> cd node-v4.3.2-linux-armv6l

> sudo cp -R * /usr/local/

## Test NodeJS

To test the installation of NodeJS enter the following command:

> node -v

Command should return (4.3.2)

## Other Dependencies

After NodeJS we need some other dependencies, enter the following commands:

> curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -

> sudo apt-get install -y nodejs

> sudo apt-get install libavahi-compat-libdnssd-dev

# Install Homebridge

Now install Homebridge with the following commands:

> sudo npm install -g --unsafe-perm homebridge hap-nodejs node-gyp

> cd /usr/local/lib/node_modules/homebridge/

> sudo npm install --unsafe-perm bignum

> cd /usr/local/lib/node_modules/hap-nodejs/node_modules/mdns

> sudo node-gyp BUILDTYPE=Release rebuild

# Install Plugins

Use these commands to install the Homebridge plugins, setup of the plugins is nedeed follow the instructions of the plugin to setup the plugin

> sudo npm install -g homebridge-http			https://github.com/rudders/homebridge-http

> sudo npm install -g homebridge-nest			https://github.com/kraigm/homebridge-nest

> sudo npm install -g homebridge-philipshue		https://github.com/thkl/homebridge-philipshue

> sudo npm install -g homebridge-harmonyhub	https://github.com/KraigM/homebridge-harmonyhub

> sudo npm Install -g homebridge-daylight		https://github.com/yungsters/homebridge-daylight

# WebIOPi Setup

To use homebridge-http we will need to setup webiopi

——————————
HEADLESS/ARMv6 ONLY
sudo apt-get install rpi.gpio <MAYBE sudo apt-get install python-rpi.gpio>
——————————

Enter the following commands to setup webiopi:

> wget http://sourceforge.net/projects/webiopi/files/WebIOPi-0.7.1.tar.gz

> tar xvzf WebIOPi-0.7.1.tar.gz

> cd WebIOPi-0.7.1

> wget https://raw.githubusercontent.com/doublebind/raspi/master/webiopi-pi2bplus.patch

> patch -p1 -i webiopi-pi2bplus.patch

> sudo ./setup.sh

> sudo webiopi -d -c /etc/webiopi/config (Test, close after successful connection)

> sudo /etc/init.d/webiopi start

> sudo update-rc.d webiopi defaults

## Setup GPIO

Enter the following commands to setup the GPIO for homebridge-http

> cd /home/pi

> wget <*GitHub/Dropbox link to gpio.py>

> sudo crontab -e

> Add: @reboot sudo python3 /home/pi/gpio1.py > /home/pi/webiopilog.txt

# Setup systemctl

> Place homebridge under /etc/default/
> sudo mv /home/pi/Desktop/homebridge /etc/default/

> Place homebridge.service under /etc/systemd/system/

> sudo mv /home/pi/Desktop/homebridge.service /etc/systemd/system/ 

> useradd --system homebridge

> sudo mkdir /var/homebridge

> sudo cp -r /home/pi/.homebridge/accessoiries/ /var/homebridge/

> sudo cp -r /home/pi/.homebridge/persist/ /var/homebridge/

> sudo cp /home/pi/.homebridge/config.json /var/homebridge/

> sudo chown -R homebridge:homebridge /var/homebridge

> sudo chmod 777 -R /var/homebridge

## Enable

> sudo systemctl daemon-reload

> sudo systemctl enable homebridge

> sudo systemctl start homebridge

## Status
> sudo systemctl status -l homebridge -n 200

# Notes
* The service will restart after 10 seconds if it fails for any reason (or if you kill it for example with kill -s SIGSEGV <pid>)
* Raspberry Pi inputs crashes Homebridge on my setup if you set the config.json to "switchHandling": "realtime”, if you don’t need inputs/state info you should set "switchHandling": “yes”
* Homebridge Harmony crashes often
* Install packages manually with: sudo npm install -g <FOLDERNAME>

