# Homebridge on Raspberry Pi 3

Example of Homebridge on RaspberryPi 3

## READ: https://github.com/nfarina/homebridge

This example gives the configuration of 4 accessories/devices; 
- Nest thermostat (3rd gen)
- Logitech Harmony Hub
- Raspberry Pi GPIO
- GPS based temperature sensor

Things I used in this setup;
- Raspberry Pi 3 Model B v1.2
- Raspbian Stretch 4.9 with Desktop
- Keyes Relayboard (2 relays)
- Phoenix Contact RPI-BC DIN rail housing
- iPhone/iPad on iOS 11.2
- PC/Mac (For SSH)
- AppleTV 4 (For remote access)

Useful iOS Apps;
- Home (Expensive but better than default iOS app)
- Prompt
- iTeleport
- Eve (Edit Siri commands)

Useful Mac Apps;

- ApplePi-Baker
- Apple Screen Sharing
- Terminal
- Transmit


<img src="http://i.imgur.com/CnYg1Oa.png" width="811" height="359">

<img src="http://i.imgur.com/F0AorQ8.jpg" width="400" height="300"> <img src="http://i.imgur.com/sTtJVN8.jpg" width="400" height="300">

<img src="http://i.imgur.com/c1DaqGE.jpg" width="400" height="300"> <img src="http://i.imgur.com/1XWtP4z.jpg" width="400" height="300"> 

<img src="http://i.imgur.com/G1Lw3vY.jpg" width="177" height="315"> <img src="http://i.imgur.com/rQ3tzQb.jpg" width="177" height="315"> <img src="http://i.imgur.com/aQDJqoO.jpg" width="177" height="315"> <img src="http://i.imgur.com/4sQMA1h.jpg" width="177" height="315">

# Setup Raspberry Pi

Connect a display, mouse and keyboard to the Raspberry Pi, open terminal and enter the following command:

```
sudo raspi-config
```

In the configuration tool enable SSH, VNC, Autologin, Wifi and change your password.

Open VNC Server settings from the system tray.

Options > Security

```
Encryption = Prefer On
Authentication = VNC Password
```

Download the setup files, enter the following command:
  
```
git clone https://github.com/gerarddvb/Homebridge-on-RaspberryPi /home/pi/HomeKit/
sudo reboot
```
After reboot test SSH and VNC connection, when succesful disconnect display, mouse and keyboard.

# Install Homebridge

Setup APT, enter the following commands:

```
sudo apt-get update
sudo apt-get upgrade
```

Use these commands to install Homebridge:

```
sudo apt-get install libavahi-compat-libdnssd-dev
sudo apt-get install nodejs
sudo apt-get install npm
sudo npm install -g --unsafe-perm homebridge
```

Use these commands to install the Homebridge plugins.

Initial setup of various plugins is nedeed.
Follow the instructions on the GitHub link to the plugin below.

```
sudo npm install -g homebridge-http
sudo npm install -g homebridge-nest
sudo npm install -g homebridge-harmonyhub
sudo npm install -g homebridge-openweathermap-temperature
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

To use homebridge-http with GPIO you will need to setup webiopi, skip if you don't want to use GPIO

Setup GPIO
```
sudo crontab -e
```

Add the following line at the end: 	
```
@reboot sudo python3 /home/pi/HomeKit/gpio.py > /home/pi/HomeKit/webiopilog.txt
```
Save changes with CTRL-X

Enter the following commands to setup webiopi:
```
cd /home/pi/HomeKit
sudo wget http://sourceforge.net/projects/webiopi/files/WebIOPi-0.7.1.tar.gz
sudo tar xvzf WebIOPi-0.7.1.tar.gz
cd WebIOPi-0.7.1
sudo wget https://raw.githubusercontent.com/doublebind/raspi/master/webiopi-pi2bplus.patch
patch -p1 -i webiopi-pi2bplus.patch
sudo ./setup.sh
sudo webiopi -d -c /etc/webiopi/config 		(Test, close after successful connection)
sudo update-rc.d webiopi defaults
sudo /etc/init.d/webiopi start
```

# Setup systemd deamon

After all the accessories/devices are configured and tested, it is time to make it run at boot.

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

# Setup CPU Watchdog

To enable the CPU watchdog enter the following commands, this will reboot the Raspberry Pi after a CPU inactivity of 14 seconds.

```
sudo nano /boot/config.txt
```

Add the following line:

```
dtparam=watchdog=on
```
Save changes with CTRL-X


Enter the following commands

```
sudo apt-get install watchdog
sudo mv /home/pi/HomeKit/watchdog.conf /etc/
sudo mv /home/pi/HomeKit/watchdog.service /lib/systemd/system/
sudo systemctl enable watchdog
sudo systemctl start watchdog
sudo reboot
```

Test watchdog

To test the watchdog enter the following command, this will freeze your Rapsberry Pi, it should reboot after 15 seconds.

```
:(){ :|:& };:
```

# Status

You can check the state of homebridge by entering the following command:

```
sudo systemctl status -l homebridge -n 200
```

This will output the last 200 lines, change that number to get more/less info

You can check the status of WebIOPi by entering the following address in your browser:

```
http://RASPBERRYIPADDRESS:8000/
```

# Notes
* The service will restart after 10 seconds if it fails for any reason (or if you kill it for example with kill -s SIGSEGV <pid>)
* The system will restart after 15 seconds of inactivity
* Raspberry Pi inputs crashes Homebridge on my setup if you set the config.json to "switchHandling": "realtime”, if you don’t need inputs/state info you should set "switchHandling": “yes”
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

> http://webiopi.trouch.com/INSTALL.html

> http://forkgeeks.com/enabling-watchdog-on-raspberry-pi/

# DIN 81346 Electrical Drawing

<img src="http://i.imgur.com/MJpKMJF.jpg" width="400" height="300"> <img src="http://i.imgur.com/qjb6moe.jpg" width="400" height="300">

<img src="http://i.imgur.com/2p3Mwdm.jpg" width="400" height="300"> <img src="http://i.imgur.com/vX08V4T.jpg" width="400" height="300">
