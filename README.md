# Homebridge on Raspberry Pi 3

Example of Homebridge on RaspberryPi 3

## READ: https://github.com/nfarina/homebridge

This example gives the configuration of 4 accessories/devices; 
- Philips Hue (1st gen)
- Nest thermostat (3rd gen)
- Logitech Harmony Hub
- Raspberry Pi GPIO
- GPS based temperature sensor

Things I used in this setup;
- Raspberry Pi 3 Model B v1.2
- Keyes Relayboard (2 relays)
- Phoenix Contact RPI-BC DIN rail housing
- iPhone/iPad on iOS 11
- PC/Mac (For SSH)
- AppleTV 4 (For remote access)

Useful iOS Apps;
- Home (Expensive but better than default iOS 10 app)
- Prompt (SSH Terminal)
- Eve (For editing Siri commands)

<img src="http://i.imgur.com/QwuybYD.png" width="707" height="387">

<img src="http://i.imgur.com/F0AorQ8.jpg" width="400" height="300"> <img src="http://i.imgur.com/sTtJVN8.jpg" width="400" height="300">

<img src="http://i.imgur.com/c1DaqGE.jpg" width="400" height="300"> <img src="http://i.imgur.com/1XWtP4z.jpg" width="400" height="300"> 

<img src="http://i.imgur.com/G1Lw3vY.jpg" width="177" height="315"> <img src="http://i.imgur.com/rQ3tzQb.jpg" width="177" height="315"> <img src="http://i.imgur.com/aQDJqoO.jpg" width="177" height="315"> <img src="http://i.imgur.com/4sQMA1h.jpg" width="177" height="315">

# Setup Raspberry Pi

First you need to setup the Raspberry Pi, open terminal and enter the following command:

```
sudo raspi-config
```

In the configuration tool enable SSH, VNC, Autologin and change your password.

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

Setup APT, enter the following commands:

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install watchdog
```

Now download the setup files, enter the following command:
  
```
git clone https://github.com/gerarddvb/Homebridge-on-RaspberryPi /home/pi/HomeKit/
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

Enter the following commands to setup webiopi:
```
cd /home/pi/HomeKit/
sudo tar xvzf WebIOPi-0.7.1PATCHED.tar.gz
cd WebIOPi-0.7.1
sudo ./setup.sh										      (Access over internet = no)
sudo webiopi -d -c /etc/webiopi/config  (Test, close after successful connection)
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

# Setup CPU Watchdog

To enable the CPU watchdog enter the following commands, this will reboot the Raspberry Pi after a CPU inactivity of 14 seconds.

```
sudo mv /home/pi/HomeKit/watchdog.conf /etc/
sudo mv /home/pi/HomeKit/watchdog.service /lib/systemd/system/
sudo systemctl enable watchdog
sudo systemctl start watchdog
sudo reboot
```

Test watchdog

To test the watchdog enter the following command, this will freeze your Rapsberry Pi, it should reboot after 14 seconds.

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
* The system will restart after 14 seconds of inactivity
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

