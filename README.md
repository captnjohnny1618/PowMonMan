# PowMonMan - cross-platform POWer MONitoring and computer MANagement software software

PowMonMan is designed to be a platform independent system for automatic shutdown of UPS-powered computers during a power outage. (Windows support is inbound).  This software is intended to provide system hardware protection by calling a system's shutdown command after an elapsed period of time of a sustained power outage.  The default is 10 minutes.  NO SOFTWARE PROTECTION IS PROVIDED (i.e. files are not saved nor are applications closed beyond what a system does after invoking the shutdown command).

**Please Note Before Going Any Further**: By installing, using, or testing this software you agree that you have read and understood this statement and the developers are not responsible for anything that you may lose (files, data, software, hardware, etc.) during use, misuse, or testing of this software.  The open-source license under which this software is released further guarantees that we are not responsible for anything you may do to your system, however we want to make sure this is extra clear.  Furthermore, do not use this software for system-critical applications or critical computing systems.  I'm just a person developing in his free time.  While I have tested the software extensively on my own systems, I have no idea what it's going to do on yours.  System shutdowns are no joke and PowMonMan can only run if it has root permissions to your system.  Don't mess around with it if you don't know what you're doing.

## The Goals

Many UPSs come with proprietary software that will shutdown systems, however no solution to our knowledge is open-source and cross-platform.  They also require that a USB cable to connected from the UPS to the computer.  Who knows what they hell is going on in there??

Enter PowMonMan (I hate this name, I've got nothing better right now though).  PowMonMan can protect your system hardware in the event of an extended power outage. Hand rolling your own solution isn't too bad, however these typicaly have hard-coded network IPs, port numbers, etc.

With PowMonMan I wanted the installation and use to be relatively simple and straightforward.  In that vein, we've implemented the following

* Entirely implemented with python
* Configuration via human readable YAML config files
* Open source, extensible power outage monitoring (via powmonman_server which runs on a Raspberry Pi)
* Client/Server autodiscovery (no hardcoding IPs and port numbers)
* Detailed logging
* Installable with standard python tools (i.e. pip3)
* Customizable shutdown command (via the configuration file)

## Installation

This software will not do anything for you if your systems are not powered from UPSs (uniterruptible power supplies).  Need some? Here's what I use:

- APC UPS Battery Backup & Surge Protector with AVR, 1500VA, APC Back-UPS Pro (BX1500M) (Powering an iMac and modest Linux/Windows machine)
- APC UPS Battery Backup & Surge Protector with USB Charger, 600VA, APC Back-UPS (BE600M1)  (Powering router, modem, and powmonman RPi server)

### First step: Server (Raspberry Pi installation)

Ensure that your Raspberry Pi is powered from the UPS and running a flavor of Linux (Windows may work, however this is untested).

Connect your power monitor cable's 3.3v output to GPIO pin 4 of your pi, and ground (0v) to pin 5.  Please see below for how to make a power monitoring cable.

Once the Raspberry Pi is up and running and the power monitor cable is connected, clone or download the source code to the Raspberry Pi:
```
git clone https://github.com/captnjohnny1618/PowMonMan.git
```

Navigate into the top-level PowMonMan source directory (the one containing setup.py) and run:
```
sudo pip3 install ./
```

If everything installed correctly, start the server with:
```
sudo powmonman_server
```

The server can take a few seconds to get fully up and running (i.e. UDP broadcast thread and power monitor thread).  In this time period clients won't be able to connect.  It's usually best to wait about thirty seconds or a minute after running the server command before starting the client software.

Thats it! Unless you see errors, the server is running.  

On Linux or Mac, you can print the log using:
```
tail -f /var/log/PowMonMan/server.log
```

### Second step: Clients (Mac, Linux only currently, working on Windows)

(Make sure the server is up and running first!)

On each client you want to run PowMonMan, clone or download the source code to the Raspberry Pi:
```
git clone https://github.com/captnjohnny1618/PowMonMan.git
```

Navigate into the top-level PowMonMan source directory (the one containing setup.py) and run:
```
sudo pip3 install ./
```

If everything installed correctly, start the client with:
```
sudo powmonman_client
```

Check the logs to ensure that the client was able to find and communicate with the server:
```
cat /var/log/PowMonMan/client.log
```

If everything went as it should, you should see something along the lines of (IP address will likely be different):

```
2019-06-29 10:46:58,627 INFO Starting PowMonMan_Client...
2019-06-29 10:46:58,627 INFO Listening for PowMonMan server...
2019-06-29 10:46:59,014 INFO Found! (192.168.3.107)
2019-06-29 10:46:59,018 INFO     Server found at:      192.168.3.107
    Using port:           7444
    Shutdown time (sec):  600
    Current power status: on	    
```

## How it works

(Coming soon!)

## Configuration

(Coming soon!)

## Power Monitoring Setup for Raspberry Pi

** DO NOT ** run 5V into the GPIO pins of a Raspberry Pi.  They are intended for use with a 3.3V signal.  If you want to run PowMonMan using a leftover phone charger or wall wart, run the 5V signal though a simple voltage divider circuit (https://en.wikipedia.org/wiki/Voltage_divider).  Resistor values of 18k (Z1 in wikipedia diagram) and 33k (Z2) produce an output voltage of ~3.23V which works well with PowMonMan.

A more thorough tutorial to make this circuit is coming soon.

## License

This PowMonMan software packages is released under the GNU GPL version 2.0.

Copyright (C) John Hoffman 2019