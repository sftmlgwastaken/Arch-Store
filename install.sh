#!/bin/bash
echo "Welcome to the Arch-Store installation program!"
echo "What do you want to do?"
echo "1) Install/Update Arch-Store"
echo "2) Uninstall Arch-Store"
read -p "Select an option [1/2]: " action

if [[ "$action" == "1" ]]; then
    # install_dependencies   # <--- togli se non hai questa funzione

    PYTHON_PATH=$(which python3)
    clear
    read -p "Install the stable version? (y/n): " choice

    if [[ "$choice" =~ ^[Yy]$ ]]; then
        echo "Installing Arch-Store stable..."
        wget https://raw.githubusercontent.com/samuobe/Arch-Store/main/PKGBUILD/PKGBUILD
        makepkg -si
        rm PKGBUILD
        echo "FINISHED!"       
    else
        echo "Installing Arch-Store from main branch..."        
        wget https://raw.githubusercontent.com/samuobe/Arch-Store/main/PKGBUILD/PKGBUILD-git
        mv PKGBUILD-git PKGBUILD
        makepkg -si
        rm PKGBUILD
        echo "FINISHED!"        
    fi

elif [[ "$action" == "2" ]]; then
    echo "Uninstalling Arch-Store..."
    sudo pacman -Rns arch-store
    sudo pacman -Rns arch-store-git
    echo "FINISHED!"
fi
