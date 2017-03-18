# Homebridge on Raspberry Pi 3

Example of Homebridge on RaspberryPi 3

## READ: https://github.com/nfarina/homebridge

This example gives the configuration of 7 accessories/devices; 
- Philips Hue (1st gen Bridge)
- Nest thermostat (3rd gen)
- Logitech Harmony Hub
- Raspberry Pi 3 with GPIO input and output
- GPS based sunset triggers
- GPS based temperature sensor
- Delayed off switches

Things I used in this setup;
- Raspberry Pi 3 Model B v1.2
- Keyes Relayboard (2 relays)
- Phoenix Contact RPI-BC DIN rail housing
- iPhone/iPad on iOS 10
- PC/Mac (For SSH)
- AppleTV 4 (For remote access)
- Home (in iOS AppStore, expensive but better then default iOS 10 app)


<img src="http://i.imgur.com/QwuybYD.png" width="707" height="387">

<img src="http://i.imgur.com/5gXy6WA.jpg" width="168" height="300"> <img src="http://i.imgur.com/f8ldgno.jpg" width="168" height="300"> <img src="http://i.imgur.com/eGamtdA.jpg" width="168" height="300"> <img src="http://i.imgur.com/m8NJ0R9.png" width="168" height="300">

<img src="http://i.imgur.com/91m8Re2.jpg" width="400" height="300"> <img src="http://i.imgur.com/sTtJVN8.jpg" width="400" height="300">

<img src="http://i.imgur.com/s0hQnVC.jpg" width="400" height="300"> <img src="http://i.imgur.com/mbAzrhk.png" width="400" height="300"> 

# Setup Raspberry Pi

First we need to setup the Raspberry Pi, open terminal and enter the following command:

```
sudo raspi-config
```

In the configuration tool enable SSH, VNC, Autologin and change your password.



Now download the setup files, enter the following command:
  
```
git clone https://github.com/gerarddvb/Homebridge-on-RaspberryPi /home/pi/HomeKit/
```

Now it is time to setup APT, enter the following commands:

```
sudo apt-get update
sudo apt-get upgrade
```

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

After these modifications it is time to reboot, enter the following command to reboot:
```
sudo reboot
```

# Install Homebridge

Use these commands to install Homebridge:

```
cd /home/pi/HomeKit/
sudo tar -xvf node-v4.3.2-linux-armv6l.tar.gz 
cd node-v4.3.2-linux-armv6l
sudo cp -R * /usr/local/
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -  
sudo apt-get install -y nodejs
sudo apt-get install libavahi-compat-libdnssd-dev
sudo npm install -g --unsafe-perm homebridge hap-nodejs node-gyp
cd /usr/local/lib/node_modules/homebridge/
sudo npm install --unsafe-perm bignum
cd /usr/local/lib/node_modules/hap-nodejs/node_modules/mdns
sudo node-gyp BUILDTYPE=Release rebuild
```

Use these commands to install the Homebridge plugins.

Initial setup of various plugins is nedeed.
Follow the instructions on the GitHub link to the plugin below.

```
sudo npm install -g homebridge-http
sudo npm install -g homebridge-nest
sudo npm install -g homebridge-philipshue
sudo npm install -g homebridge-harmonyhub
sudo npm install -g homebridge-daylight
sudo npm install -g homebridge-openweathermap-temperature
sudo npm install -g homebridge-delay-switch
```

Test Homebridge

```
homebridge
```

Close after succesful test

Now its time to copy the config.json
```
cd /home/pi/.homebridge/
sudo wget -N <YOUR config.json file>
```

# WebIOPi

To use homebridge-http with GPIO we will need to setup webiopi, skip if you don't wont to use GPIO

Setup GPIO
```
sudo crontab -e
```

Add the following line at the end: 	
```
@reboot sudo python3 /home/pi/HomeKit/gpio.py > /home/pi/HomeKit/webiopilog.txt
```

Enter the following commands to setup webiopi:
```
cd /home/pi/HomeKit/
sudo tar xvzf WebIOPi-0.7.1PATCHED.tar.gz
cd WebIOPi-0.7.1
sudo ./setup.sh										              (Access over internet = no)
sudo webiopi -d -c /etc/webiopi/config 					  	(Test, close after successful connection)
sudo update-rc.d webiopi defaults
sudo /etc/init.d/webiopi start
```

# Setup systemd deamon

After all the accessories/devices are configured and tested, it is time to make it run at boot.

Make sure everything is tested thoroughly, because editing the config.json isn't easy after this point.
Editing will probably break your Raspberry setup, making you start over.

The config.json used by the deamon will be located at /var/homebridge/
```
useradd --system homebridge
sudo mv /home/pi/HomeKit/homebridge /etc/default/
sudo mv /home/pi/HomeKit/homebridge.service /etc/systemd/system/ 
sudo mkdir /var/homebridge
sudo cp -r /home/pi/.homebridge/accessories/ /var/homebridge/
sudo cp -r /home/pi/.homebridge/persist/ /var/homebridge/
sudo cp /home/pi/.homebridge/config.json /var/homebridge/
sudo chown -R homebridge:homebridge /var/homebridge
sudo chmod 777 -R /var/homebridge
sudo systemctl daemon-reload
sudo systemctl enable homebridge
sudo systemctl start homebridge
sudo reboot
```

# Status
After reboot you can check the state of homebridge by entering the following command:

```
sudo systemctl status -l homebridge -n 200
```

This will output the last 200 lines, change that number to get more/less info

# Notes
* The service will restart after 10 seconds if it fails for any reason (or if you kill it for example with kill -s SIGSEGV <pid>)
* Raspberry Pi inputs crashes Homebridge on my setup if you set the config.json to "switchHandling": "realtime”, if you don’t need inputs/state info you should set "switchHandling": “yes”
* Homebridge Harmony crashes often
* Install packages manually with: sudo npm install -g FOLDERNAME
* I am working on the writeup for a CPU watchdog, homebridge-harmony sometimes freezes the system. With watchdog enabled it will auto-reboot after 15 seconds after crash. This is looking quite promising on my setup.

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

