#!/bin/bash


echo "Welcome to the Arch-Store installation program!"
echo "What do you want to do?"
echo "1) Install/Update Arch-Store"
echo "2) Uninstall Arch-Store"
read -p "Select an option [1/2/5]: " action

if [[ "$action" == "1" ]]; then
    mkdir arch-store-install
    cd arch-store-install

    PYTHON_PATH=$(which python3)
    echo 
    echo
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

    sudo touch /usr/share/arch-store/script 

    cd ..
    rm -rf arch-store-install

elif [[ "$action" == "2" ]]; then
    echo
    echo
    echo "Uninstalling Arch-Store..."
    sudo pacman -Rns arch-store
    sudo pacman -Rns arch-store-git
    echo "FINISHED!"
elif [[ "$actions" == "5" ]]; then
    echo "Installing Arch-Store DEV branch..."
    wget https://raw.githubusercontent.com/samuobe/Arch-Store/main/PKGBUILD/PKGBUILD-dev
    mv PKGBUILD-dev PKGBUILD
    makepkg -si
    rm PKGBUILD
    echo "FINISHED!" 

    cd ..
    rm -rf arch-store-install
fi


rm -- "$0"

