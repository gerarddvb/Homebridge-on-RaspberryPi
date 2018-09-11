# Homebridge on Raspberry Pi 3

Example of Homebridge on RaspberryPi 3

## READ: https://github.com/nfarina/homebridge

This example gives the configuration of these accessories/devices; 
- Nest thermostat (3rd gen)
- Logitech Harmony Hub
- Camera
- Fan
- Smoke Detector
- Motion Detector
- GPS Temperature & humidity sensor

Things I used in this setup;
- Raspberry Pi 3 Model B+
- Raspbian Stretch with Desktop
- Raspberry Pi Camera Module V2
- Keyes Relayboard (2 relays)
- Makeblock MQ2 Gas Sensor
- HC-SR501 PIR Motion Sensor
- Phoenix Contact RPI-BC DIN rail housing
- iPhone/iPad on iOS 11.3
- PC/Mac (For SSH)
- AppleTV 4 (For remote access)

Useful iOS Apps;
- Home (Expensive but better than default iOS app)
- Prompt
- iTeleport
- Eve (Edit Siri commands)

Useful Mac Apps;

- Etcher
- Apple Screen Sharing
- Termius
- Transmit

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
After reboot test SSH and VNC connection, when succesful, disconnect display, mouse and keyboard.

# Install Homebridge

Setup APT, enter the following commands:

```
sudo apt-get update
sudo apt-get upgrade
```

Use these commands to install Homebridge:

```
sudo apt-get install libavahi-compat-libdnssd-dev
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g --unsafe-perm homebridge
```

Use these commands to install the Homebridge plugins.

Initial setup of various plugins is nedeed.
Follow the instructions on the GitHub link to the plugin below.

```
sudo npm install -g homebridge-http
sudo npm install -g homebridge-ws
sudo npm install -g homebridge-nest

sudo npm install -g npm@4
sudo npm install -g homebridge-harmonyhub@0.3.0-alpha.2
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

Enter the following commands to enable homebridge to run at boot and restart after 10 seconds of inactivity.

The config.json used by the deamon will be located at /var/homebridge/
```
sudo useradd --system homebridge
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

To enable the CPU watchdog enter the following commands, this will reboot the Raspberry Pi after a CPU inactivity of 15 seconds.

```
sudo nano /boot/config.txt
```

Add the following lines:

```
# Watchdog enable
dtparam=watchdog=on

# VNC resolution enable
hdmi_group=2
hdmi_force_hotplug=1

# VNC resolution
# 2=640x400
# 27=1280x800
# 46=1440x900
# 76=2560x1600
# 82=1080p
# 85=720p
hdmi_mode=46
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

# Setup Raspberry Pi Camera Module

Use these commands to install the Raspberry Pi Camera Module.

```
raspi-config 				 Enable Camera
sudo nano /etc/modules		Add: bcm2835-v4l2
sudo reboot 
raspistill -o cam.jpg
sudo apt install ffmpeg
cd /opt
sudo mkdir homebridge-camera-rpi
sudo chown pi homebridge-camera-rpi
git clone https://github.com/moritzmhmk/homebridge-camera-rpi
cd homebridge-camera-rpi
npm install
node standalone.js
sudo mv /home/pi/HomeKit/homebridge-camera-rpi.conf.json /etc/
sudo mv /home/pi/HomeKit/hap-camera-rpi.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable hap-camera-rpi
sudo systemctl start hap-camera-rpi
sudo reboot
```

# Status

You can check the state of homebridge by entering the following command:

```
sudo systemctl status -l homebridge -n 200
sudo systemctl status -l hap-camera-rpi -n 200
```

This will output the last 200 lines, change that number to get more/less info

You can check the status of WebIOPi by entering the following address in your browser:

```
http://RASPBERRYIPADDRESS:8000/
```

# Notes
* The service will restart after 10 seconds if it fails for any reason (or if you kill it for example with 'sudo systemctl stop homebridge')
* The system will restart after 15 seconds of inactivity
* Install packages manually with: sudo npm install -g FOLDERNAME

# Sources
> https://github.com/nfarina/homebridge

> https://github.com/nfarina/homebridge/wiki/Running-HomeBridge-on-a-Raspberry-Pi

> https://nodejs.org/en/download/package-manager/

> https://github.com/rudders/homebridge-http

> https://github.com/gerarddvb/homebridge-http

> https://github.com/kraigm/homebridge-nest

> https://github.com/KraigM/homebridge-harmonyhub

> https://github.com/ebaauw/homebridge-ws

> https://github.com/moritzmhmk/homebridge-camera-rpi

> http://webiopi.trouch.com/INSTALL.html

> http://forkgeeks.com/enabling-watchdog-on-raspberry-pi/

> https://gist.github.com/johannrichard/0ad0de1feb6adb9eb61a

> https://elinux.org/RPiconfig#Video_mode_options

> https://github.com/KhaosT/HAP-NodeJS/blob/master/lib/gen/HomeKitTypes.js

# DIN 81346 Electrical Drawing

<img src="http://i.imgur.com/MJpKMJF.jpg" width="400" height="300"> <img src="http://i.imgur.com/qjb6moe.jpg" width="400" height="300">

<img src="http://i.imgur.com/2p3Mwdm.jpg" width="400" height="300"> <img src="http://i.imgur.com/vX08V4T.jpg" width="400" height="300">
