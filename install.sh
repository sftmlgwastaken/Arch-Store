#!/bin/bash
clear

echo "Welcome to the Arch-Store installation program!"
echo "What do you want to do?"
echo "1) Install Arch-Store"
echo "2) Uninstall Arch-Store"
echo "3) Update Arch-Store"
read -p "Select an option [1/2/3]: " action

# Funzione per installare le dipendenze
install_dependencies() {
    echo "📦 Downloading dependencies..."
    sudo pacman -Sy
    sudo pacman -S git python3 python-pip --noconfirm --needed
    pip install PyQt6 --break-system-packages
}

if [[ "$action" == "1" ]]; then
    install_dependencies

    PYTHON_PATH=$(which python3)
    clear
    read -p "Install it for all users? (y/n): " choice

    if [[ "$choice" =~ ^[Yy]$ ]]; then
        echo "Installing Arch-Store for all users..."

        if ! getent group archstore >/dev/null; then
            echo "Creating group 'archstore'..."
            sudo groupadd archstore
        fi

        echo "Adding user $USER to group 'archstore'..."
        sudo usermod -aG archstore "$USER"

        sudo mkdir -p /opt/Arch-Store

        if [[ -d "/opt/Arch-Store/.git" ]]; then
            echo "Arch-Store already exists, updating..."
            cd /opt/Arch-Store || exit
            sudo git reset --hard HEAD
            sudo git pull origin main
        else
            sudo git clone https://github.com/Samuobe/Arch-Store.git /opt/Arch-Store
        fi

        sudo chown -R root:archstore /opt/Arch-Store
        sudo chmod -R 770 /opt/Arch-Store

        SCRIPT_PATH="/opt/Arch-Store/main.py"
        ICON_PATH="/opt/Arch-Store/icon.png"
        DESKTOP_FILE="/usr/share/applications/arch-store.desktop"

        sudo bash -c "cat <<EOF > \"$DESKTOP_FILE\"
[Desktop Entry]
Type=Application
Name=Arch Store
Exec=$PYTHON_PATH \"$SCRIPT_PATH\"
Icon=$ICON_PATH
Categories=System;
Terminal=false
EOF"

        sudo chmod 644 "$DESKTOP_FILE"

        echo "✅ Arch-Store installed/updated for all users."
        echo "📌 Desktop file created at: $DESKTOP_FILE"
        echo "👥 User $USER added to group 'archstore'."
        echo ""
        echo "⚠️  To apply group changes immediately, log out and log in"
    else
        echo "Installing Arch-Store for current user..."

        mkdir -p "$HOME/.programs"
        if [[ -d "$HOME/.programs/Arch-Store/.git" ]]; then
            echo "Arch-Store already exists, updating..."
            cd "$HOME/.programs/Arch-Store" || exit
            git reset --hard HEAD
            git pull origin main
        else
            git clone https://github.com/Samuobe/Arch-Store.git "$HOME/.programs/Arch-Store"
        fi
        chmod -R 700 "$HOME/.programs/Arch-Store"

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

        chmod 700 "$DESKTOP_FILE"

        echo "✅ Arch-Store installed/updated for current user."
        echo "📌 Desktop file created at: $DESKTOP_FILE"
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

elif [[ "$action" == "3" ]]; then
    install_dependencies

    echo "Updating Arch-Store..."
    if [[ -d "/opt/Arch-Store/.git" ]]; then
        echo "Updating system-wide installation..."
        cd /opt/Arch-Store || exit
        sudo git reset --hard HEAD
        sudo git pull origin main
        echo "System-wide Arch-Store updated."
    elif [[ -d "$HOME/.programs/Arch-Store/.git" ]]; then
        echo "Updating user installation..."
        cd "$HOME/.programs/Arch-Store" || exit
        git reset --hard HEAD
        git pull origin main
        echo "User Arch-Store updated."
    else
        echo "Arch-Store is not installed, please install it first."
    fi

else
    echo "Invalid choice. Exiting."
fi
