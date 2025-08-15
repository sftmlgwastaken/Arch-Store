#!/bin/bash
cls

PYTHON_PATH=$(which python3) # Path assoluto di python3

echo "Welcome to the Arch-Store installation program!"
echo "What do you want to do?"
echo "1) Install Arch-Store"
echo "2) Uninstall Arch-Store"
read -p "Select an option [1/2]: " action

if [[ "$action" == "1" ]]; then
    echo "Downloading dependencies..."
    sudo pacman -Sy
    sudo pacman -S tk git python3 python-pip --noconfirm

    # Librerie Python globali (se necessarie)
    sudo pip install --break-system-packages webbrowser

    read -p "Install it for all users? (y/n): " choice

    if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
        echo "Installing Arch-Store for all users..."

        # Creazione cartella /opt/Arch-Store con permessi totali
        sudo mkdir -p /opt/Arch-Store
        sudo chmod 777 /opt/Arch-Store

        # Cambio proprietà temporanea a utente corrente per clonare senza sudo
        sudo chown "$USER":"$USER" /opt/Arch-Store
        git clone https://github.com/Samuobe/Arch-Store.git /opt/Arch-Store

        # Ripristino permessi totali a tutti
        sudo chmod -R 777 /opt/Arch-Store

        SCRIPT_PATH="/opt/Arch-Store/main.py"
        ICON_PATH="/opt/Arch-Store/icon.png"
        DESKTOP_FILE="/usr/share/applications/arch-store.desktop"

        # Creazione file .desktop con permessi totali
        sudo bash -c "cat <<EOF > \"$DESKTOP_FILE\"
[Desktop Entry]
Type=Application
Name=Arch Store
Exec=$PYTHON_PATH \"$SCRIPT_PATH\"
Icon=$ICON_PATH
Categories=System;
Terminal=false
EOF"

        sudo chmod 777 "$DESKTOP_FILE"

        echo "Arch-Store installed for all users."
        echo "Desktop file created at: $DESKTOP_FILE"

    else
        echo "Installing Arch-Store for current user..."

        mkdir -p "$HOME/.programs"
        cd "$HOME/.programs" || exit
        git clone https://github.com/Samuobe/Arch-Store.git
        chmod -R 777 "$HOME/.programs/Arch-Store"

        SCRIPT_PATH="$HOME/.programs/Arch-Store/main.py"
        ICON_PATH="$HOME/.programs/Arch-Store/icon.png"
        DESKTOP_FILE="$HOME/.local/share/applications/arch-store.desktop"

        mkdir -p "$HOME/.local/share/applications"

        cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Type=Application
Name=Arch Store
Exec=$PYTHON_PATH "$SCRIPT_PATH"
Icon=$ICON_PATH
Categories=System;
Terminal=false
EOF

        chmod 777 "$DESKTOP_FILE"

        echo "Arch-Store installed for current user."
        echo "Desktop file created at: $DESKTOP_FILE"
    fi

elif [[ "$action" == "2" ]]; then
    echo "Uninstalling Arch-Store..."

    if [[ -d "/opt/Arch-Store" ]]; then
        echo "Removing system-wide installation..."
        sudo rm -rf /opt/Arch-Store
        sudo rm -f /usr/share/applications/arch-store.desktop
        echo "System-wide Arch-Store removed."
    elif [[ -d "$HOME/.programs/Arch-Store" ]]; then
        echo "Removing user installation..."
        rm -rf "$HOME/.programs/Arch-Store"
        rm -f "$HOME/.local/share/applications/arch-store.desktop"
        echo "User Arch-Store removed."
    else
        echo "Arch-Store not found in common installation paths."
    fi

else
    echo "Invalid choice. Exiting."
fi
