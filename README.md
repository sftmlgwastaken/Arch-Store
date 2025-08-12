
# Arch Store

Arch store is an intuitive store for Arch Linux software written in Python!




## Features

- You can search with: pacman, AUR, flatpak
- Allows you to select a series of programs to install or remove before launching the actions you have chosen.
- It allows you to update everything automatically with just one click!
- Multilingual
- Allows you to easily choose which repositories to use



## Installation

### Dependencies:
#### Arch:
- Tkinter (Install with ```sudo pacman -S tk```)
#### Python library:
- os (pre-installed)
- tkinter (Installed with the previous command)
- subprocess (pre-installed)
- threading (pre-installed)
- lpak (included in the program download)
- webborwser
### Installation
To begin, download the ZIP file for the latest release.
Once downloaded, extract EVERYTHING INTO THE SAME FOLDER AS IS, launch main.py, and everything should start up!

### Trick: Change language
To change the language, start the program, go to settings and select the language from the list, then press confirm. The interface will restart with the new language. Be careful to select the language from the list and not write it by hand. If it is written by hand and there is an error, the configuration file will be restored to prevent errors during startup.



    
## How to use
It is easy to use, with three main screens.
### Search page
<img width="1993" height="1000" alt="serach" src="https://github.com/user-attachments/assets/9c7412ce-3f2b-4dea-85d4-f8902940d07b" />

On this page there is a search bar. Just type in what you want and press enter, and the results will appear. If you like, you can even try searching for nothing! On this screen, you will see the install or remove buttons, depending on what you want to do. Every action you select is reversible. In other words, if you first select to install Reaper but then decide you don't need it, you can remove it from the list by searching for it and clicking on “Don't install.” Once you have made your selection, you can click on “Start actions,” which will open the second installation screen (explanation below). On the search screen, there is also an “update” button, which is used to update everything and also opens the same installation screen. There is also a settings button that will open a settings screen (thank goodness).
### Install page
<img width="1242" height="957" alt="update" src="https://github.com/user-attachments/assets/e6844b4f-caeb-435d-bab5-1e033b637b8d" />

The installation or update page has a button and a screen. When you press the start button, the screen displays the output as if you were using it from the terminal. 

NB: Sudo permissions will be required for updates and installations.

### Settings page
<img width="1995" height="1041" alt="settings" src="https://github.com/user-attachments/assets/271aac81-9cf8-46cb-ba06-c29a89a9174f" />
The settings page is fairly intuitive. It allows you to enable or disable various sources, such as flatpak, aur, or pacman. It should be noted that at least one must be enabled, otherwise the program will not work. There is also a language option with a drop-down menu and a confirmation button that will reload the interface.
## How does it work?
This section attempts to explain how it works. If you just want to use it, feel free to skip it, but if you want to tinker with it, modify it, or just understand it out of curiosity, read on! I'll try to explain it clearly.

### Data extrapolation
To extract names, repositories, and descriptions, there is a system mainly based on replace(). For pacman and AUR, the process is similar and easier, while for flatpak it is a little less so. The outputs of the respective search commands for each program are taken, divided, and printed on the screen. The buttons then use lambda to send the data of the programs I want to modify as parameters.
### Config file
The configuration file is a simple file that allows you to save the configuration. It can also be edited manually, but to prevent errors at startup, it is restored in case of errors. There is also a reset configuration button in case the problem is not detected. It is always recommended to edit using the GUI.
## Used By

This project is actively used by:

- Me :-)


