# Homebridge on Raspberry Pi 3

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
  
## Setup APT

Now it is time to setup APT, enter the following commands:

  ```
  sudo apt-get update
  sudo apt-get upgrade
  ```

## Edit Boot configuration file

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

```
cd /home/pi/HomeKit/
sudo tar -xvf node-v4.3.2-linux-armv6l.tar.gz 
cd node-v4.3.2-linux-armv6l
sudo cp -R * /usr/local/
```

## Test NodeJS

To test the installation of NodeJS enter the following command:
```
node -v
```

Command should return v4.3.2

## Other Dependencies

After NodeJS we need some other dependencies, enter the following commands:
```
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -  
sudo apt-get install -y nodejs
sudo apt-get install libavahi-compat-libdnssd-dev
```
## Setup Homebridge

```
sudo npm install -g --unsafe-perm homebridge hap-nodejs node-gyp
cd /usr/local/lib/node_modules/homebridge/
sudo npm install --unsafe-perm bignum
cd /usr/local/lib/node_modules/hap-nodejs/node_modules/mdns
sudo node-gyp BUILDTYPE=Release rebuild
```

## Install Plugins

Use these commands to install the Homebridge plugins, setup of the plugins is nedeed follow the instructions of the plugin to setup the plugin

```
sudo npm install -g homebridge-http
sudo npm install -g homebridge-nest
sudo npm install -g homebridge-philipshue
sudo npm install -g homebridge-harmonyhub
sudo npm install -g homebridge-daylight
sudo npm install -g homebridge-openweathermap-temperature
sudo npm install -g homebridge-delay-switch
```

# WebIOPi

To use homebridge-http with GPIO we will need to setup webiopi

## Setup GPIO
```
sudo crontab -e
```

Add the following line at the end: 	
```
@reboot sudo python3 /home/pi/HomeKit/gpio.py > /home/pi/HomeKit/webiopilog.txt
```

## Install WebIOPI
Enter the following commands to install webiopi:
```
cd /home/pi/HomeKit/
sudo tar xvzf WebIOPi-0.7.1PATCHED.tar.gz
cd WebIOPi-0.7.1
sudo ./setup.sh										                (Access over internet = no)
sudo webiopi -d -c /etc/webiopi/config 						(Test, close after successful connection)
```
## Start WebIOPi
```
sudo update-rc.d webiopi defaults
sudo /etc/init.d/webiopi start
```

# Setup systemd

After all the accessories/devices are configured and tested, we will make run at boot

## Create User
```
useradd --system homebridge
```

## Copy files
```
sudo mv /home/pi/HomeKit/homebridge /etc/default/
sudo mv /home/pi/HomeKit/homebridge.service /etc/systemd/system/ 
sudo mkdir /var/homebridge
sudo cp -r /home/pi/.homebridge/accessories/ /var/homebridge/
sudo cp -r /home/pi/.homebridge/persist/ /var/homebridge/
sudo cp /home/pi/.homebridge/config.json /var/homebridge/
sudo chown -R homebridge:homebridge /var/homebridge
sudo chmod 777 -R /var/homebridge
```

## Enable
```
sudo systemctl daemon-reload
sudo systemctl enable homebridge
sudo systemctl start homebridge
sudo reboot
```

## Status
```
sudo systemctl status -l homebridge -n 200
```

# Notes
* The service will restart after 10 seconds if it fails for any reason (or if you kill it for example with kill -s SIGSEGV <pid>)
* Raspberry Pi inputs crashes Homebridge on my setup if you set the config.json to "switchHandling": "realtime”, if you don’t need inputs/state info you should set "switchHandling": “yes”
* Homebridge Harmony crashes often
* Install packages manually with: sudo npm install -g FOLDERNAME

# Sources
> https://github.com/nfarina/homebridge
> https://github.com/nfarina/homebridge/wiki/Running-HomeBridge-on-a-Raspberry-Pi
> https://gist.github.com/johannrichard/0ad0de1feb6adb9eb61a
> https://github.com/rudders/homebridge-http
> https://github.com/kraigm/homebridge-nest
> https://github.com/thkl/homebridge-philipshue
> https://github.com/KraigM/homebridge-harmonyhub
> https://github.com/sholzmayer/homebridge-openweathermap-temperature
> https://github.com/nitaybz/homebridge-delay-switch
> https://github.com/yungsters/homebridge-daylight
> http://webiopi.trouch.com/INSTALL.html
> http://forkgeeks.com/enabling-watchdog-on-raspberry-pi/

