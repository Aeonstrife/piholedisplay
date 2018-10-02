# Pihole Display

## Hardware
  - Raspberry Pi zero with pihole
  - Waveshare 2.13 inch ePaper display (I got mine from [here](https://www.aliexpress.com/item/250x122-2-13inch-E-Ink-display-HAT-for-Raspberry-Pi-supports-partial-refresh/32812115703.html))
## Installation
### Waveshare display drivers
  - Install the libraries mentioned [here](https://www.waveshare.com/wiki/Pioneer600#Libraries_Installation_for_RPi).
  - Enable spi, i2c and edit the modules config file as given [here](https://www.waveshare.com/wiki/Pioneer600#Configuring_the_interfaces)
  - [Optional] Download demo code from [here](https://www.waveshare.com/wiki/File:2.13inch_e-Paper_HAT-code.7z) and run it to make sure everything is working
### Font Installation
  - to install the font on your Pi, run
    ~~~~
    cd ~
    wget http://kottke.org/plus/type/silkscreen/download/silkscreen.zip
    unzip silkscreen.zip
    ~~~~
  - also install the requests library (needs pip to be installed)
    ~~~~
    sudo pip install requests
    ~~~~
### Final steps
  - If you downloaded the demo code, just place the stats.py inside the 2.13inch_e-Paper_HAT-code/raspberrypi/python folder
  - If you didnot download the demo code, copy the python folder from this repo into your pi folder.
  - run the stats.py script using 
    ~~~~
    sudo python stats.py
    ~~~~
### Running on startup
  - Lastly we just want to make this run at boot. We'll do that the easy way by editing /etc/rc.local with sudo nano /etc/rc.local and adding sudo python ~pi/stats.py & before exit 0
  - Then save and you can reboot to test it out