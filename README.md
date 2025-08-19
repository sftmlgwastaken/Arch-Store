
# Arch Store

Arch store is an intuitive store for Arch Linux software written in Python!




## Features

- You can search with: pacman, AUR, flatpak
- Allows you to select a series of programs to install or remove before launching the actions you have chosen.
- It allows you to update everything automatically with just one click!
- AppImage support for single user or for all
- Multilingual (Italiano, English, Espanol)
- Allows you to easily choose which repositories to use



## Installation/Update/Remove
### Automatic script
<img width="676" height="270" alt="install script" src="https://github.com/user-attachments/assets/c35c3f94-80b2-4770-99da-6ee2201497f3" />

There is an automatic script that allows you to install, remove and update everything at once, and allows you to choose between installation for the current user only or for everyone on the system.

Just run: ```curl -LO https://raw.githubusercontent.com/Samuobe/Arch-Store/main/install.sh && bash install.sh```

Follow the two instructions and... Done! Easy, right?
### Manual
#### Dependencies:
##### Arch:
- QT (Pre-installed in most cases)
#### Python library:
- os (pre-installed)
- PyQT (```pip install PyQt6 --break-system-packages```)
- subprocess (pre-installed)
- threading (pre-installed)
- lpak (included in the program download)
- webborwser (pre-installed)

To begin, download the ZIP file for the latest release.
Once downloaded, extract EVERYTHING INTO THE SAME FOLDER AS IS, launch main.py, and everything should start up!

### Trick: Change language
To change the language, start the program, go to settings and select the language from the list, then press confirm. The interface will restart with the new language. Be careful to select the language from the list and not write it by hand. If it is written by hand and there is an error, the configuration file will be restored to prevent errors during startup.



    
## How to use
It is easy to use, with three main screens.
### Search page
<img width="2196" height="1477" alt="Ricerca" src="https://github.com/user-attachments/assets/57151d20-4da4-4eb0-bd72-30185f37696b" />

On this page there is a search bar. Just type in what you want and press enter, and the results will appear. If you like, you can even try searching for nothing! On this screen, you will see the install or remove buttons, depending on what you want to do. Every action you select is reversible. In other words, if you first select to install Reaper but then decide you don't need it, you can remove it from the list by searching for it and clicking on “Don't install.” Once you have made your selection, you can click on “Start actions,” which will open the second installation screen (explanation below). On the search screen, there is also an “update” button, which is used to update everything and also opens the same installation screen. There is also a settings button that will open a settings screen (thank goodness).
### Install page
<img width="1352" height="939" alt="install" src="https://github.com/user-attachments/assets/6f33e35c-e403-4739-ab20-a2d08f1fb02b" />

The installation or update page has a button and a screen. When you press the start button, the screen displays the output as if you were using it from the terminal. 

NB: Sudo permissions will be required for updates and installations.

### Settings page
<img width="1352" height="939" alt="impostazioni" src="https://github.com/user-attachments/assets/194dcf35-0028-411d-aab1-cf981e55ee42" />


The settings page is fairly intuitive. It allows you to enable or disable various sources, such as flatpak, aur, or pacman. It should be noted that at least one must be enabled, otherwise the program will not work. There is also a language option with a drop-down menu and a confirmation button that will reload the interface.

### AppImage support
<img width="2200" height="1476" alt="appimages" src="https://github.com/user-attachments/assets/f2619b7b-2ee9-42ce-87ba-7c0e5e8d17e8" />

One feature requested by a Reddit user was support for AppImages, and here it is! It should be fairly straightforward: go to Other > Manage AppImages and you will find a list of those installed. You can update them by selecting a more recent AppImage, which will replace the old one, or remove the program. When you install one, you will need to enter the name, an icon, the AppImage file, and choose the category. After that, you can choose whether to install it only for yourself or for everyone on the system. Other users will not see what you have installed only for yourself, but everyone will see those installed at the system level, which will require the root password to be installed or removed. You can choose where to store the appimages and icons, but I recommend leaving the default setting, which is the subfolder "./ AppImages" subfolder in the program directory because when the folder is changed in the settings, the configuration file is reset, but the AppImages and desktop files are not automatically updated. Therefore, first uninstall everything and then reinstall it if you really need to change it.
## How does it work?
This section attempts to explain how it works. If you just want to use it, feel free to skip it, but if you want to tinker with it, modify it, or just understand it out of curiosity, read on! I'll try to explain it clearly.

### Data extrapolation
To extract names, repositories, and descriptions, there is a system mainly based on replace(). For pacman and AUR, the process is similar and easier, while for flatpak it is a little less so. The outputs of the respective search commands for each program are taken, divided, and printed on the screen. The buttons then use lambda to send the data of the programs I want to modify as parameters.
### Config file
The configuration file is a simple file that allows you to save the configuration. It can also be edited manually, but to prevent errors at startup, it is restored in case of errors. There is also a reset configuration button in case the problem is not detected. It is always recommended to edit using the GUI.
## Used By

This project is actively used by:

- Me :-)


