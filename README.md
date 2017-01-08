# Homebridge on RaspberryPi

Example of Homebridge on RaspberryPi 3 (This should also work on Pi 2 and model B+, models that don’t have 40-pin GPIO should not install the webiopi patch)

This is a work-in-progress, in this setup we will use the Pixel image and desktop. This will change soon, I am working on a CLI only version off this setup

## READ: https://github.com/nfarina/homebridge

This example gives the config of 4 accessories/devices; 
- Philips Hue (1st gen Bridge)
- Nest thermostat (3rd gen)
- Logitech Harmony Hub
- Raspberry Pi 3 with GPIO input and output
- GPS based sunset trigger(s) with offset

# Setup Raspberry

APT
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install netatalk

Edit Boot configuration file (Pixel/RealVNC Only)
sudo nano /boot/config.txt
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=30

# Install Homebridge

https://github.com/nfarina/homebridge/wiki/Running-HomeBridge-on-a-Raspberry-Pi

NodeJS
wget https://nodejs.org/dist/v4.3.2/node-v4.3.2-linux-armv6l.tar.gz 
tar -xvf node-v4.3.2-linux-armv6l.tar.gz 
cd node-v4.3.2-linux-armv6l
sudo cp -R * /usr/local/

node -v

Other Dependencies
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -     (NOT on ARMv6)
sudo apt-get install -y nodejs
sudo apt-get install libavahi-compat-libdnssd-dev

Install Homebridge
sudo npm install -g --unsafe-perm homebridge hap-nodejs node-gyp
cd /usr/local/lib/node_modules/homebridge/
sudo npm install --unsafe-perm bignum
cd /usr/local/lib/node_modules/hap-nodejs/node_modules/mdns
sudo node-gyp BUILDTYPE=Release rebuild

Install Plugins
sudo npm install -g homebridge-http			https://github.com/rudders/homebridge-http
sudo npm install -g homebridge-nest			https://github.com/kraigm/homebridge-nest
sudo npm install -g homebridge-philipshue		https://github.com/thkl/homebridge-philipshue
sudo npm install -g homebridge-harmonyhub	https://github.com/KraigM/homebridge-harmonyhub
sudo npm Install -g homebridge-daylight		https://github.com/yungsters/homebridge-daylight

# WebIOPi Setup

Installation

——————————
HEADLESS/ARMv6 ONLY
sudo apt-get install rpi.gpio <MAYBE sudo apt-get install python-rpi.gpio>
——————————

wget http://sourceforge.net/projects/webiopi/files/WebIOPi-0.7.1.tar.gz
tar xvzf WebIOPi-0.7.1.tar.gz
cd WebIOPi-0.7.1
wget https://raw.githubusercontent.com/doublebind/raspi/master/webiopi-pi2bplus.patch
patch -p1 -i webiopi-pi2bplus.patch
sudo ./setup.sh
sudo webiopi -d -c /etc/webiopi/config (Test, close after successful connection)
sudo /etc/init.d/webiopi start
sudo update-rc.d webiopi defaults

Copy files
copy gpio1.py to /home/pi/  
cd /home/pi
wget <*GitHub/Dropbox link to gpio.py>

Setup GPIO
sudo crontab -e
Add: @reboot sudo python3 /home/pi/gpio1.py > /home/pi/webiopilog.txt


# Setup systemctl

Place homebridge under /etc/default/
sudo mv /home/pi/Desktop/homebridge /etc/default/

Place homebridge.service under /etc/systemd/system/
sudo mv /home/pi/Desktop/homebridge.service /etc/systemd/system/ 

Create User
useradd --system homebridge

Copy files
sudo mkdir /var/homebridge
sudo cp -r /home/pi/.homebridge/accessoiries/ /var/homebridge/
sudo cp -r /home/pi/.homebridge/persist/ /var/homebridge/
sudo cp /home/pi/.homebridge/config.json /var/homebridge/
sudo chown -R homebridge:homebridge /var/homebridge
sudo chmod 777 -R /var/homebridge

Enable
sudo systemctl daemon-reload
sudo systemctl enable homebridge
sudo systemctl start homebridge

Status
sudo systemctl status -l homebridge -n 200

# Notes
* The service will restart after 10 seconds if it fails for any reason (or if you kill it for example with kill -s SIGSEGV <pid>)
* Raspberry Pi inputs crashes Homebridge on my setup if you set the config.json to "switchHandling": "realtime”, if you don’t need inputs/state info you should set "switchHandling": “yes”
* Homebridge Harmony crashes often
* Install packages manually with: sudo npm install -g <FOLDERNAME>

