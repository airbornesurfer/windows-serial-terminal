## About

Since switching to Windows 11, I have fallen in love with Windows Terminal--the built-from-the-ground-up terminal emulator for Windows that combines everything that I loved about Linux and MacOS with the functionality of tabbed windows and a serious dose of customization. However, because much of my command line work falls into communicating with an external device over serial, I wanted to be able to keep that workflow within Windows Terminal like I'm used to doing already. In other words, I didn't want to have to resort to using a separate GUI like PuTTY when a command-line tool like Screen or Minicom would do just fine. The problem is that, since the removal of HyperTerminal in Windows Vista, Windows has not included a CLI solution for serial communication (which is kinda weird because Telnet is still buried in Windows 11; if the reasoning was because obsolescence, you'd think that Telnet would also get the axe).

Now, since I have Ubuntu installed, I could just install Screen or Minicom and call it a day, but WSL 2 does not support serial communication. If I wanted to use those tools, I would either need to change the WSL version every time I wanted to use the serial port or install another instance of Linux under WSL 1. I mean, it works, but I really just felt it inefficient to have to fire up Debian (the install is smaller than Ubuntu) just so I could use Minicom.

After a little more digging, I found Makerdiary's Terminal-S. It's a simple serial terminal written in Python that can be compiled as a self-contained exe. This little gem was exactly what I was looking for in terms of functionality! It automatically connects to the COM port (or drops a list of available ports) and connects using some default settings for baud rate, stopbit, and parity. I can fire up Windows Terminal, invoke the command in PowerShell, and I'm good to go!

But this is Windows Terminal, and I have this lovely menu of drop-down presets that will automatically spawn the environment of my choice with some lovely aesthetic theming. So, I want to be able to just click on a new tab and get that full retro terminal feel without needing to pretend I'm even in Windows! What I need to do is alter the program just a smidge so that instead of looking for flags in the command-line structure (ie -b for setting baud rate), the program will just ask me what settings I want to use (including some defaults for simplicity). To do this, I simply altered the @click.command section to only look for serial ports and moved the connection settings to a series of prompts in the main function.

Of course, it took me a little bit to deconstruct the program (as well as re-learn Python, which I hadn't really used in any significant capacity for half a decade at least), but now I have it working exactly how I want it to work, and it feels right! Of course, I had never used Python on Windows before, either, so wrapping my head around PowerShell has been enlightening as well (Yes, I'm late to the PowerShell party, so I'm making up for it). Once I figured out how to use Pyinstaller (after remembering how to set a PATH variable in Windows), then I just have to drop the portable EXE file into a nice, out of the way place in Windows (might as well put it in a folder in C:) and make sure that folder is added to the PATH variable.

![](https://user-images.githubusercontent.com/948283/82290238-050e5600-99d9-11ea-9b36-50fb12471e95.png)
Screenshot of terminal-s, I'll upload a new screenshot after I dig my RC2014 back out.


## Features

+ auto-detect serial port
+ list available ports to choose

## Install
```
pip install terminal-s
```

## Run
```
terminal-s
```

On windows, you can also type <kbd>Win</kbd> + <kbd>r</kbd> and enter `terminal-s` to launch it.

## Package
```
pip install pyinstaller
pyinstaller terminal-s.spec
```
