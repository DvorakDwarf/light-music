# light-music
This is the finished version of my music-reacting LEDs project. It does what it says on the tin. Works on .wav files, could most definitely be adapted to work on other audio formats. You need a few things to run this. 

First, you need to make sure you know how you will connect some audio output to your raspberry pi. Now, you need to follow this guide to setup so that you can even control the LEDs in the first place: https://dordnung.de/raspberrypi-ledstrip/.
Now you need to install pigpio(http://abyz.me.uk/rpi/pigpio/) and other libraries used in the script. The script will look for a folder called "Songs" in the same directory and then open a .wav file inside. It will crash if it doesn't find one. If the script crashes when you run it, it's likely because you did not turn on pigpio(sudo pigpiod in console)

At this point you should be able to use it. Type "help" when the script is running to see all commands. Have fun !
