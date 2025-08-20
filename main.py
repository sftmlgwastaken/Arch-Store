#!/usr/bin/env python3
import os
import subprocess
import threading
import library.lpak as lpak
import webbrowser
import getpass
import PyQt6.QtWidgets as pq
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from PyQt6.QtGui import QIcon
import sys

#fast access variables
avaible_languages = ["Italiano", "English", "Español"]

#Base variables
install_pacman_packages=[]
remove_pacman_packages=[]
install_aur_packages=[]
remove_aur_packages=[]
install_flatpak_packages=[]
remove_flatpak_packages=[]

search_status = False
install_status = False
last_search = ""

#Other impportant varibiles
pacman_programs = []
flatpak_programs = ['No matches found']
aur_programs = []


#colours varibiles
install_color = "#008000"
remove_color = "red"
modified_color = "lightblue"
base_action_button_style="color: white; font: bold 12pt 'Arial'; padding: 4px 8px; border-radius: 5px;"

#Auto-set variables
base_dir = os.path.dirname(os.path.realpath(__file__))
working_dir="/var/lib/arch-store"
os.chdir(base_dir)
user_name = getpass.getuser()

#add anything global to global scope before using it global, also put defaults
setting_repo_pacman="enable"
setting_repo_aur="enable"
setting_repo_flatpak="enable"
aur_method="yay"
language="English"
AppImagesDir=f"{working_dir}/AppImages"

#Config data
def load_config_data():    
    def write_new_config_file():
        with open(f"{working_dir}/settings.conf", "w") as f:
            f.write("pacman=enable\n")
            f.write("aur=enable\n")
            f.write("flatpak=enable\n")
            f.write("aur_method=yay\n")
            f.write("language=English\n")
            f.write(f"AppImmageDir={working_dir}/AppImages")
    def read_config_data():
        global setting_repo_pacman, setting_repo_aur, setting_repo_flatpak, aur_method, language, AppImagesDir
        with open(f"{working_dir}/settings.conf", "r") as f:
            file_configuration_data = [line.rstrip('\n') for line in f.readlines()]
        setting_repo_pacman=file_configuration_data[0].split("=")[1]
        setting_repo_aur=file_configuration_data[1].split("=")[1]
        setting_repo_flatpak=file_configuration_data[2].split("=")[1]
        aur_method=file_configuration_data[3].split("=")[1]
        language=file_configuration_data[4].split("=")[1]
        AppImagesDir=file_configuration_data[5].split("=")[1]
    if not os.path.isfile(f"{working_dir}/settings.conf"):
        write_new_config_file()    
    try:        
        read_config_data()        
    except:
        write_new_config_file()
        read_config_data()
    if not language in avaible_languages:
        write_new_config_file()
        read_config_data()
load_config_data()
no_repo_error_text_default=lpak.get("no installation method", language)
os.makedirs(AppImagesDir, exist_ok=True)

#ALLERT
def show_allert(title, message):
    msg = pq.QMessageBox()
    msg.setIcon(pq.QMessageBox.Icon.Information)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.setStandardButtons(pq.QMessageBox.StandardButton.Ok | pq.QMessageBox.StandardButton.Cancel)
    retval = msg.exec()
#END ALLERT

###############
#SETTINGS DATA#

def open_setting(window):
    #Edit repo
    def settings_change_pacman_status():
        with open(f"{working_dir}/settings.conf", "r") as f:
            file_configuration_data = [line.rstrip('\n') for line in f.readlines()]
        if setting_repo_pacman == "enable":
            new_status = "disable"
            button_repo_pacman.setText(lpak.get("enable", language))
        else:
            new_status = "enable"
            button_repo_pacman.setText(lpak.get("disable", language))
        with open(f"{working_dir}/settings.conf", "w") as f:
            f.write("pacman="+new_status+"\n")
            for line in file_configuration_data:
                if not "pacman=" in line:
                    f.write(line+"\n")   
        load_config_data()
    def settings_change_aur_status():
        with open(f"{working_dir}/settings.conf", "r") as f:
            file_configuration_data = [line.rstrip('\n') for line in f.readlines()]
        if setting_repo_aur == "enable":
            new_status = "disable"
            button_repo_aur.setText(lpak.get("enable", language))
        else:
            new_status = "enable"
            button_repo_aur.setText(lpak.get("disable", language))
        with open(f"{working_dir}/settings.conf", "w") as f:
            f.write(file_configuration_data[0]+"\n")
            f.write("aur="+new_status+"\n")
            for line in file_configuration_data:
                if not "aur=" in line and not "pacman=" in line:
                    f.write(line+"\n")   
        load_config_data()

    def settings_change_flatpak_status():
        with open(f"{working_dir}/settings.conf", "r") as f:
            file_configuration_data = [line.rstrip('\n') for line in f.readlines()]
        if setting_repo_flatpak == "enable":
            new_status = "disable"
            button_repo_flatpak.setText(lpak.get("enable", language))
        else:
            new_status = "enable"
            button_repo_flatpak.setText(lpak.get("disable", language))
        with open(f"{working_dir}/settings.conf", "w") as f:            
            for line in file_configuration_data:
                for line in file_configuration_data:
                    if not "flatpak=" in line:
                        f.write(line+"\n")
                    else:
                        f.write("flatpak="+new_status+"\n")
        load_config_data()
    def settings_change_language(settings_page):
        with open(f"{working_dir}/settings.conf", "r") as f:
            file_configuration_data = [line.rstrip('\n') for line in f.readlines()]
        language = menu_select_language.currentText()
        with open(f"{working_dir}/settings.conf", "w") as f:
            for line in file_configuration_data:
                if not "language=" in line:
                    f.write(line+"\n")
                else:
                    f.write("language="+language+"\n")
        show_allert(lpak.get("restart required", language), lpak.get("please restart to apply the changes", language))               

    def change_aur_method(button, label):
        if aur_method == "paru":
            new_method = "yay"
        else:
            new_method = "paru"
        with open(f"{working_dir}/settings.conf", "r") as f:
            file_configuration_data = [line.rstrip('\n') for line in f.readlines()]        
        with open(f"{working_dir}/settings.conf", "w") as f:
            for line in file_configuration_data:
                if not "aur_method=" in line:
                    f.write(line+"\n")
                else:
                    f.write("aur_method="+new_method+"\n")
        load_config_data()
        label.setText(lpak.get("aur method", language)+": "+aur_method)
        button.setText(lpak.get("changed", language))        
        
    def setting_change_appimagedir(button):
        new_dir = pq.QFileDialog.getExistingDirectory(settings_page, lpak.get("select a folder", language))
        response = pq.QMessageBox.question(settings_page,
            lpak.get("confirm change", language),
            lpak.get("attenction this action will clear existing appimages dataset", language),
            pq.QMessageBox.StandardButton.Yes | pq.QMessageBox.StandardButton.No,
            pq.QMessageBox.StandardButton.No
        )
        if response == pq.QMessageBox.StandardButton.Yes:    
            with open(f"{working_dir}/settings.conf", "w") as f:
                f.write("")
            with open(f"{working_dir}/settings.conf", "r") as f:
                file_configuration_data = [line.rstrip('\n') for line in f.readlines()]
            with open(f"{working_dir}/settings.conf", "w") as f:
                for line in file_configuration_data:
                    if not "AppImmageDir=" in line:
                        f.write(line+"\n")
                    else:
                        f.write("AppImmageDir="+new_dir+"\n")
            button.setText(lpak.get("changed", language))
            load_config_data()
        else:
            return
    #Other
    def settings_reset_settings(window):
        os.remove(f"{working_dir}/settings.conf")        
        load_config_data()
        show_allert(lpak.get("restart required", language), lpak.get("please restart to apply the changes", language))  

    settings_page = pq.QWidget()
    settings_page.setWindowTitle(lpak.get("arch store settings", language))
    settings_page.setGeometry(0, 0, 900, 600)   
    layout = pq.QGridLayout(settings_page)    
    settings_page.setWindowIcon(QIcon(f"{working_dir}/icon.png"))

    settings_label_title = pq.QLabel(lpak.get("settings", language))
    settings_label_repo = pq.QLabel(lpak.get("enable disable repo", language))
    settings_label_title.setStyleSheet("color: black; font: bold 12pt 'Arial';")
    settings_label_repo.setStyleSheet("font-weight: bold; font-style: italic;")

    #pacman repo
    label_repo_pacman=pq.QLabel("Pacman")
    if setting_repo_pacman == "enable":
        text_setting_repo_pacman = lpak.get("disable", language)
    else:
        text_setting_repo_pacman = lpak.get("enable", language)
    button_repo_pacman = pq.QPushButton(text_setting_repo_pacman)
    button_repo_pacman.pressed.connect(settings_change_pacman_status)
    #aur repo
    label_repo_aur=pq.QLabel("Aur")
    if setting_repo_aur == "enable":
        text_setting_repo_aur = lpak.get("disable", language)
    else:
        text_setting_repo_aur = lpak.get("enable", language)
    button_repo_aur = pq.QPushButton(text_setting_repo_aur)
    button_repo_aur.pressed.connect(settings_change_aur_status)
    #flatpak repo
    label_repo_flatpak=pq.QLabel("Flatpak")
    if setting_repo_flatpak == "enable":
        text_setting_repo_flatpak = lpak.get("disable", language)
    else:
        text_setting_repo_flatpak = lpak.get("enable", language)
    button_repo_flatpak = pq.QPushButton(text_setting_repo_flatpak)
    button_repo_flatpak.pressed.connect(settings_change_flatpak_status)
    #
    button_reset_settings= pq.QPushButton(lpak.get("reset settings", language))
    button_reset_settings.pressed.connect(lambda window=window: settings_reset_settings(window))
    #change AUR method
    label_aur_method = pq.QLabel(lpak.get("aur method", language)+": "+aur_method)
    button_change_aur_method = pq.QPushButton(lpak.get("change", language))
    button_change_aur_method.pressed.connect(lambda button=button_change_aur_method, label=label_aur_method: change_aur_method(button, label))
    #other label
    label_other_settings = pq.QLabel(text=lpak.get("other", language))
    label_other_settings.setStyleSheet("font-weight: bold; font-style: italic;")
    #language      
    menu_select_language = pq.QComboBox()
    menu_select_language.addItems(avaible_languages)
    menu_select_language.setCurrentText(language)
    label_language=pq.QLabel(lpak.get("language", language))
    button_language_confirm=pq.QPushButton(lpak.get("confirm change language", language))    
    button_language_confirm.pressed.connect(lambda settings_page=settings_page: settings_change_language(settings_page))
    #appimagedir
    appimagesdir_label = pq.QLabel(lpak.get("appimages installation path", language))
    appimagesdir_button = pq.QPushButton(lpak.get("change appimage path", language))
    appimagesdir_button.pressed.connect(lambda button =appimagesdir_button: setting_change_appimagedir(button))
    #crediti
    def github_button():
        webbrowser.open("https://github.com/IlNonoP/Arch-Store")
    author_label = pq.QLabel(lpak.get("made whit heart by Samuobe", language))
    project_link = pq.QPushButton(lpak.get("github project", language))
    project_link.pressed.connect(github_button)
    #LINE
    line_separazione = pq.QFrame()
    line_separazione.setFrameShape(pq.QFrame.Shape.HLine)   
    line_separazione.setFrameShadow(pq.QFrame.Shadow.Sunken) 
    #
    empty_label = pq.QLabel(" ")
    #
    layout.addWidget(settings_label_title)
    layout.addWidget(settings_label_title, 0, 0, 1, 2)  
    layout.addWidget(button_reset_settings, 0, 3)
    layout.addWidget(settings_label_repo, 1, 0)
    layout.addWidget(label_repo_pacman, 2, 0)
    layout.addWidget(button_repo_pacman, 2, 1)
    layout.addWidget(label_repo_flatpak, 3, 0)
    layout.addWidget(button_repo_flatpak, 3, 1)
    layout.addWidget(label_repo_aur, 4, 0)
    layout.addWidget(button_repo_aur, 4, 1)
    layout.addWidget(label_aur_method, 5, 0)
    layout.addWidget(button_change_aur_method, 5, 1)
    layout.addWidget(empty_label, 6, 0)
    layout.addWidget(label_other_settings, 7, 0)
    #setLayout(layout)
    #
    layout.addWidget(label_language, 8, 0)
    layout.addWidget(menu_select_language, 8, 1)
    layout.addWidget(button_language_confirm, 9, 0, 1, 1)

    layout.addWidget(appimagesdir_label, 10, 0)
    layout.addWidget(appimagesdir_button, 10, 1)

    layout.addWidget(line_separazione, 12, 0, 1, 3)  # row=12, colspan=3
    layout.addWidget(author_label, 13, 0)
    layout.addWidget(project_link, 13, 1)

    layout.setRowStretch(layout.rowCount(), 1)

    settings_page.show()

#END SETTINGS##
###############

###########
###OTHER###
def open_appimages_settings(window):
        global appimages_window
        def update_appimage_window(name, program_user_base):
            appimage_path, _ = pq.QFileDialog.getOpenFileName(
                 
                caption=lpak.get("select an appimage", language),
                filter=("AppImage (*.AppImage)")
            )
            if appimage_path:  
                button.setText(str(appimage_path))
            os.remove(AppImagesDir+f"/{name}-{program_user_base}.AppImage")
            os.system(f"mv '{appimage_path}' '{AppImagesDir}/{name}-{program_user_base}.AppImage'")
            show_allert(lpak.get("update completed", language), lpak.get("update completed", language))            

        def remove_appimage(name, program_user_base):            
            os.remove(AppImagesDir+f"/{name}-{program_user_base}.AppImage")
            os.remove(AppImagesDir+f"/{name}-{program_user_base}.png")
            if program_user_base == "-":
                cmd = f"rm '/usr/share/applications/{name}-archstore.desktop'"
                subprocess.run(["pkexec", "bash", "-c", cmd])                
            else:
                desktop_path = os.path.expanduser(f"~/.local/share/applications/{name}-archstore.desktop")
                os.remove(desktop_path)
            with open(f"{working_dir}/appimages.data.conf", "r") as f:
                appimage_data = f.readlines()
            with open(f"{working_dir}/appimages.data", "w") as f:
                for line in appimage_data:
                    if line != f"{name}|{program_user_base}":
                        f.write(line)
            show_allert(lpak.get("remove completed", language), lpak.get("remove completed", language))
            

        def start_add_appimage():
            def select_file_appimage(button, parent_window):
                appimage_path, _ = pq.QFileDialog.getOpenFileName(
                    parent=parent_window,  
                    caption=lpak.get("select an appimage", language),
                    filter=("AppImage (*.AppImage)")
                )
                if appimage_path:  
                    button.setText(str(appimage_path))
            def select_file_icon(button, parent_window):
                icon_path, _ = pq.QFileDialog.getOpenFileName(
                    parent=add_appimage_window,
                    caption=lpak.get("select an icon", language),
                    filter= "PNG (*.png)"
                )
                if icon_path:
                    button.setText(str(icon_path))
            
            def confirm_appimage_install(name_text, path_but, icon_but, category_selection):
                name = name_text.text()
                path = path_but.text()
                icon = icon_but.text()
                category = category_selection.currentText()
                if "|" in name or name == None or name == "":
                    show_allert(lpak.get("illegal caracter", language), lpak.get("you can't use the following caracther", language)+": |")
                    return
                if not os.path.isfile(path):
                    show_allert(lpak.get("invalid appimage location", language), lpak.get("the appimage you selected was not found", language))
                    return
                if not os.path.isfile(icon):
                    show_allert(lpak.get("invalid icon location", language), lpak.get("the icon you selected was not found", language))
                    return    

                response = pq.QMessageBox.question(add_appimage_window,
                    lpak.get("confirm installation", language),
                    lpak.get("do you want to install it for all users", language),
                    pq.QMessageBox.StandardButton.Yes | pq.QMessageBox.StandardButton.No,
                    pq.QMessageBox.StandardButton.No
                ) 
                
                if response == pq.QMessageBox.StandardButton.Yes:
                    program_user = "-"
                else:
                    program_user = user_name
                os.system(f"mv '{icon}' '{AppImagesDir}/{name}-{program_user}.png'")
                os.system(f"mv '{path}' '{AppImagesDir}/{name}-{program_user}.AppImage'")
                desktop_entry_data = f"[Desktop Entry]\nType=Application\nName={name}\nExec='{AppImagesDir}/{name}-{program_user}.AppImage'\nIcon={AppImagesDir}/{name}-{program_user}.png\nCategories={category};"
                if program_user == "-":
                    with open("desktop_temp", "w") as f:
                        f.write(desktop_entry_data)
                    subprocess.run([
                            "pkexec", "cp", f"{working_dir}/desktop_temp", f"/usr/share/applications/{name}-archstore.desktop"
                        ])
                    os.remove("desktop_temp")
                else:
                    desktop_path = os.path.expanduser(f"~/.local/share/applications/{name}-archstore.desktop")
                    with open(desktop_path, "w") as f:
                        f.write(desktop_entry_data)
                with open(f"{working_dir}/appimages.data", "r") as f:
                    appimage_file_data = f.readlines()
                with open (f"{working_dir}/appimages.data", "w") as f:
                    for line in appimage_file_data:
                        f.write(line)                        
                    f.write(f"\n{name}|{program_user}")
                show_allert(lpak.get("installation completed", language), lpak.get("installation completed", language))
            
            add_appimage_window = pq.QWidget()
            add_appimage_window.setGeometry(0, 0, 900, 500)
            add_appimage_window.setWindowIcon(QIcon(f"{working_dir}/icon.png"))
            add_appimage_window.setWindowTitle(lpak.get("add appimage", language))
            appimage_name_label = pq.QLabel(lpak.get("name", language))
            appimage_name_textbox = pq.QLineEdit("")
            appimage_path_label = pq.QLabel(lpak.get("path", language))
            appimage_path_button = pq.QPushButton(lpak.get("select an appimage", language))
            appimage_path_button.pressed.connect(lambda path_button=appimage_path_button, back_top=add_appimage_window: select_file_appimage(path_button, back_top))
            appimage_ico_label = pq.QLabel(lpak.get("icon", language))
            appimage_ico_button = pq.QPushButton(lpak.get("select an icon", language))
            appimage_ico_button.pressed.connect(lambda ico_button = appimage_ico_button, back_top=add_appimage_window: select_file_icon(ico_button, back_top))      
            avaible_appimage_types = ["Utility", "Game", "Graphics", "Network", "AudioVideo", "Development", "Office", "Presentation"]
            menu_select_type = pq.QComboBox()
            menu_select_type.addItems(avaible_appimage_types)
            label_type=pq.QLabel(lpak.get("app type", language))
            appimage_confirm_button = pq.QPushButton(lpak.get("install appimage",language))
            appimage_confirm_button.pressed.connect(lambda name=appimage_name_textbox, path=appimage_path_button, icon=appimage_ico_button, tipe=menu_select_type: confirm_appimage_install(name, path, icon, tipe))
            
            #
            layout = pq.QGridLayout(add_appimage_window)

            layout.addWidget(appimage_name_label, 0, 0)
            layout.addWidget(appimage_name_textbox, 0, 1)
            layout.addWidget(appimage_path_label, 1,0)
            layout.addWidget(appimage_path_button,1,1)
            layout.addWidget(appimage_ico_label, 2, 0)
            layout.addWidget(appimage_ico_button, 2, 1)
            layout.addWidget(label_type, 3, 0)
            layout.addWidget(menu_select_type, 3, 1)
            layout.addWidget(appimage_confirm_button, 4, 2)
            add_appimage_window.show()       

        appimages_window = pq.QWidget()
        appimages_window.setWindowTitle(lpak.get("manage appimages", language))
        appimages_window.setWindowIcon(QIcon(f"{working_dir}/icon.png"))       
        appimages_window.setGeometry(0, 0, 600, 500)    
        layout = pq.QVBoxLayout(appimages_window)
        # Scroll Area
        scroll = pq.QScrollArea()
        scroll.setWidgetResizable(True)

        container = pq.QWidget()
        container_layout = pq.QGridLayout(container)
        container.setLayout(container_layout)

        if not os.path.isfile(f"{working_dir}/appimages.data"):
            with open(f"{working_dir}/appimages.data", "w") as f:
                pass

        with open(f"{working_dir}/appimages.data", "r") as f:
            appimages_data = f.readlines()

        
        row = 0
        if appimages_data == []:
            no_appimage_apps_label = pq.QLabel(lpak.get("no appimages app", language))
            container_layout.addWidget(no_appimage_apps_label)
        else:            
            actions_label_title= pq.QLabel(lpak.get("actions", language))
            name_label_title=pq.QLabel(lpak.get("name",language))
            user_label_title=pq.QLabel(lpak.get("user", language))

            container_layout.addWidget(actions_label_title, 0, 0)
            container_layout.addWidget(name_label_title, 0, 2)
            container_layout.addWidget(user_label_title, 0, 3)
            


            line = pq.QFrame()
            line.setFrameShape(pq.QFrame.Shape.HLine)
            container_layout.addWidget(line, 1, 0, 1, 4)

            row = 2
            for app in appimages_data:
                try:
                    name, user = app.strip().split("|")
                    if user == "-" or user == user_name:                       

                        remove_button = pq.QPushButton(lpak.get("remove", language))
                        remove_button.clicked.connect(lambda _, n=name, u=user: remove_appimage(n, u))

                        update_button = pq.QPushButton(lpak.get("update", language))
                        update_button.clicked.connect(lambda _, n=name, u=user: update_appimage_window(n, u))

                        container_layout.addWidget(remove_button, row, 0)
                        container_layout.addWidget(update_button, row, 1)                       
                        container_layout.addWidget(pq.QLabel(name), row, 2)                      
                        container_layout.addWidget(pq.QLabel(user), row, 3)
                    
                        line = pq.QFrame()
                        line.setFrameShape(pq.QFrame.Shape.HLine)
                        container_layout.addWidget(line, row + 1, 0, 1, 4)
                        row = row +2
                except Exception as e:
                    print("Errore caricando appimages:", e)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        add_appimage_button = pq.QPushButton(lpak.get("add appimage", language))
        add_appimage_button.clicked.connect(start_add_appimage)
        layout.addWidget(add_appimage_button)
        container_layout.setRowStretch(container_layout.rowCount(), 1)

        appimages_window.show()


def open_other():
    other_option_window = pq.QWidget()
    other_option_window.setWindowTitle(lpak.get("other options", language))
    other_option_window.setWindowIcon(QIcon(f"{working_dir}/icon.png"))
    other_option_window.setGeometry(0, 0, 400, 400)
    layout=pq.QVBoxLayout(other_option_window)    
    setting_button = pq.QPushButton(lpak.get("settings", language))
    setting_button.pressed.connect(lambda window=other_option_window: open_setting(window))
    appimage_button = pq.QPushButton(lpak.get("manage appimages", language))
    appimage_button.pressed.connect(lambda window=other_option_window: open_appimages_settings(window))
    
    layout.addWidget(appimage_button)
    layout.addWidget(setting_button)

    other_option_window.show()
    
#END OTHER#
###########


def update_all_apps():
    global install_status
    if setting_repo_pacman == "disable" and setting_repo_aur == "disable" and setting_repo_flatpak == "disable":
        show_allert(lpak.get("attenction", language), lpak.get("no installation method", language))
        return
    if install_status:
        show_allert(lpak.get("attenction", language), lpak.get("an install instance is alredy in progress", language))
        return

    # Scrive script
    with open(f"{working_dir}/actions.sh", "w") as f:
        f.write("#!/bin/bash")
        if setting_repo_pacman == "enable":
            f.write("\nsudo pacman -Syu --noconfirm")
        if setting_repo_aur == "enable":
            f.write(f"\n{aur_method} -Syu --noconfirm")
        if setting_repo_flatpak == "enable":
            f.write("\nflatpak upgrade --assumeyes")


    def close_settings():
        update_window.close()

    def start_update():
        global install_status        
        install_status = True
        update_button.setDisabled(True)
        text_area.setText(lpak.get("update in progress", language))
        progress_bar.setRange(0, 0) 
        update_window.repaint()           
        proc = subprocess.run(["pkexec", "bash", os.path.join(working_dir, "actions.sh")])
        os.remove(f"{working_dir}/actions.sh")   
        install_status = False
        progress_bar.setRange(0, 1)  
        update_button.setText(lpak.get("finished", language))
        text_area.setText(lpak.get("finished", language))        
        try:
            update_button.pressed.disconnect()
        except TypeError:
            pass      
        update_button.setDisabled(False)
        update_button.clicked.connect(close_settings)
        update_window.update()

    update_window = pq.QWidget()
    update_window.setGeometry(100, 100, 400, 200)
    update_window.setWindowIcon(QIcon(f"icon.png"))
    update_window.setWindowTitle(lpak.get("update", language))
    layout = pq.QVBoxLayout(update_window)
    text_area = pq.QLabel(lpak.get("click to start update", language))
    layout.addWidget(text_area)
    progress_bar = pq.QProgressBar()      
    layout.addWidget(progress_bar)  
    update_button = pq.QPushButton(lpak.get("start update", language))    
    layout.addWidget(update_button)
    update_button.pressed.connect(start_update)

    update_window.show()   
    
def start_selectionated_operations(program_name):
    global start_operation_button, operation_list_label, install_pacman_packages, remove_pacman_packages, install_aur_packages, remove_aur_packages, install_flatpak_packages, remove_flatpak_packages, install_status
    
    #pacman
    if install_pacman_packages != []:
        install_pacman_command = "sudo pacman -S --noconfirm "
        for package in install_pacman_packages:
            install_pacman_command=install_pacman_command+package+" "
    else:
        install_pacman_command = "echo "+lpak.get("no pacman install actions", language)
    if remove_pacman_packages != []:
        remove_pacman_command = "sudo pacman -Rn --noconfirm "
        for package in remove_pacman_packages:
            remove_pacman_command = remove_pacman_command+package+" "
    else:
        remove_pacman_command = "echo "+lpak.get("no pacman remove actions", language)
    #aur
    if install_aur_packages != []:
        install_aur_command = f"{aur_method} -S --noconfirm "
        for package in install_aur_packages:
            install_aur_command = install_aur_command+package+" "
    else:
        install_aur_command = "echo "+lpak.get("no install aur actions", language)
    if remove_aur_packages != []:
        remove_aur_command = f"{aur_method} -Rn --noconfirm "
        for package in remove_aur_packages:
            remove_aur_command = remove_aur_command + package+" "
    else:
        remove_aur_command = "echo "+lpak.get("no remove aur actions", language)
    #flatpak
    if install_flatpak_packages != []:
        install_flatpak_command = "flatpak install --assumeyes "
        for package in install_flatpak_packages:
            install_flatpak_command = install_flatpak_command+package
    else:
        install_flatpak_command = "echo "+lpak.get("no install flatpak actions", language)
    if remove_flatpak_packages != []:
        remove_flatpak_command = "flatpak remove --assumeyes "
        for package in remove_flatpak_packages:
            remove_flatpak_command = remove_flatpak_command + package
    else:
        remove_flatpak_command = "echo "+lpak.get("no remove flatpak actions", language)
    with open(f"{working_dir}/actions.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("\n"+install_pacman_command)
        f.write("\n"+remove_pacman_command)
        f.write("\n"+install_aur_command)
        f.write("\n"+remove_aur_command)
        f.write("\n"+install_flatpak_command)
        f.write("\n"+remove_flatpak_command)    

    def close_operations():
        operations_window.close()        
    
    def after_operations():
        global install_pacman_packages, remove_pacman_packages
        global modified_list
        update_button.setText(lpak.get("update", language))
        try:
            update_button.pressed.disconnect()
        except TypeError:
            pass      
        content_layout.removeWidget(modified_list)
        modified_list.deleteLater()
        modified_list = None
        update_button.pressed.connect(update_all_apps)
        install_pacman_packages.clear()
        remove_pacman_packages.clear()
        install_aur_packages.clear()
        remove_aur_packages.clear()        
        search_program(last_search)
    
    def start_thread_operations(label, button):
        global install_status
        if install_status == True:
            messagebox.showinfo(lpak.get("an install instance is alredy in progress", language), lpak.get("an install instance is alredy in progress", language), parent=operations_window) 
            return
        os.chdir(working_dir)
        install_status = True
        button.setDisabled(True)
        label.setText(lpak.get("install in progress", language))
        progress_bar.setRange(0, 0) 
        operations_window.repaint()
        install_status = True
        proc = subprocess.run(["pkexec", "bash", os.path.join(working_dir, "actions.sh")])
        os.remove(f"{working_dir}/actions.sh")       
        install_status = False
        progress_bar.setRange(0, 1)  
        button.setText(lpak.get("finished", language))
        label.setText(lpak.get("finished", language))        
        try:
            button.pressed.disconnect()
        except TypeError:
            pass
        after_operations()      
        button.setDisabled(False)
        button.clicked.connect(close_operations)
        operations_window.update()

    operations_window = pq.QWidget()
    operations_window.setWindowTitle(lpak.get("star actions", language))    
    operations_window.setWindowIcon(QIcon("icon.png"))
    layout = pq.QVBoxLayout(operations_window)
    install_label = pq.QLabel(lpak.get("click to start operations", language))
    start_button = pq.QPushButton(lpak.get("start actions", language))
    start_button.pressed.connect(lambda: start_thread_operations(install_label, start_button))
    progress_bar = pq.QProgressBar()     

     

    layout.addWidget(install_label)
    layout.addWidget(progress_bar) 
    layout.addWidget(start_button)

    operations_window.show()

def download_program(program_name, repository, button, status):
    global start_operation_button, program_button_download, operation_list_label, modified_list
    global modified_list
    program_name=program_name.split(" ")[0]
    
    if repository == "aur":
        if status[0] == "Remove" or status[0] == "Do not install":
            if status[0] == "Remove":
                button.setText(lpak.get("do not remove", language))
                button.setStyleSheet(f"background-color: {modified_color}; {base_action_button_style}")
                status[0] = "Do not remove" 
                remove_aur_packages.append(program_name)                
            else:
                button.setText(lpak.get("install", language)) 
                status[0] = "Install"    
                button.setStyleSheet(f"background-color: {install_color}; {base_action_button_style}")
                install_aur_packages.remove(program_name) 
        elif status[0] == "Install" or status[0] == "Do not remove":
            if status[0] == "Install":
                button.setText(lpak.get("do not install", language))
                button.setStyleSheet(f"background-color: {modified_color}; {base_action_button_style}")
                status[0] = "Do not install" 
                install_aur_packages.append(program_name)
            else:
                button.setText(lpak.get("remove", language))
                status[0] = "Remove" 
                button.setStyleSheet(f"background-color: {remove_color}; {base_action_button_style}")
                remove_aur_packages.remove(program_name)         
    elif repository == "flatpak":
        if status[0] == "Remove" or status[0] == "Do not install":
            if status[0] == "Remove":
                button.setText(lpak.get("do not remove", language)) #lpak
                button.setStyleSheet(f"background-color: {modified_color}; {base_action_button_style}")
                status[0] = "Do not remove"
                remove_flatpak_packages.append(program_name)
            else:
                button.setText(lpak.get("install", language))
                button.setStyleSheet(f"background-color: {install_color}; {base_action_button_style}")
                status[0] = "Install" 
                install_flatpak_packages.remove(program_name)
        elif status[0] == "Install" or status[0] == "Do not remove":
            if status[0] == "Install":
                status[0] = "Do not install" 
                button.setText(lpak.get("do not install", language))
                button.setStyleSheet(f"background-color: {modified_color}; {base_action_button_style}")
                install_flatpak_packages.append(program_name)
            else:
                button.setText(lpak.get("remove", language))
                status[0] = "Remove" 
                button.setStyleSheet(f"background-color: {remove_color}; {base_action_button_style}")
                remove_flatpak_packages.remove(program_name)
    else:
        
        if status[0] == "Remove" or status[0] == "Do not install":
            if status[0] == "Remove":
                button.setText(lpak.get("do not remove", language))
                status[0] = "Do not remove"
                button.setStyleSheet(f"background-color: {modified_color}; {base_action_button_style}")
                remove_pacman_packages.append(program_name)
            else:
                button.setText(lpak.get("install", language)) 
                button.setStyleSheet(f"background-color: {install_color}; {base_action_button_style}")
                status[0] = "Install" 
                install_pacman_packages.remove(program_name)
                
        elif status[0] == "Install" or status[0] == "Do not remove":
            if status[0] == "Install":
                button.setText(lpak.get("do not install", language))
                status[0] = "Do not install"
                button.setStyleSheet(f"background-color: {modified_color}; {base_action_button_style}")
                install_pacman_packages.append(program_name)
            else:
                button.setText(lpak.get("remove", language))
                button.setStyleSheet(f"background-color: {remove_color}; {base_action_button_style}")
                status[0] = "Remove"
                remove_pacman_packages.remove(program_name)
        else:
            print("ERROR, Invalid status!\nin: download_program()")
            exit()
    if install_pacman_packages!=[] or remove_pacman_packages!=[] or install_aur_packages !=[] or remove_aur_packages!=[] or install_flatpak_packages != [] or remove_flatpak_packages!=[]:
        actions_text=""
        update_button.setText(lpak.get("start actions", language))

        try:
            update_button.pressed.disconnect()
        except TypeError:
            pass
      
        update_button.pressed.connect(lambda program_name=program_name:start_selectionated_operations(program_name))
       
        if install_pacman_packages != []:
            actions_text=actions_text+lpak.get("pacman install", language)+":\n"
            for package in install_pacman_packages:
                actions_text = actions_text + package+"\n"
            actions_text = actions_text+"\n"

        if remove_pacman_packages != []:
            actions_text=actions_text+lpak.get("pacman remove", language)+":\n"
            for package in remove_pacman_packages:
                actions_text = actions_text + package+"\n"
            actions_text = actions_text+"\n"

        #aur
        if install_aur_packages != []:
            actions_text=actions_text+"\n"+lpak.get("aur install", language)+":\n"
            for package in install_aur_packages:
                actions_text = actions_text + package+"\n"
            actions_text = actions_text+"\n"

        if remove_aur_packages != []:
            actions_text=actions_text+"\n"+lpak.get("aur remove", language)+":\n"
            for package in remove_aur_packages:
                actions_text = actions_text + package+"\n"

        #flatpak
        if install_flatpak_packages != []:
            actions_text=actions_text+"\n"+lpak.get("flatpak install", language)+":\n"
            for package in install_flatpak_packages:
                actions_text = actions_text + package+"\n"
            actions_text = actions_text+"\n"

        if remove_flatpak_packages != []:
            actions_text=actions_text+"\n"+lpak.get("pacman remove", language)+":\n"
            for package in remove_flatpak_packages:
                actions_text = actions_text + package+"\n"

        try:
            content_layout.removeWidget(modified_list)
            modified_list.deleteLater()
            modified_list = None
        except: 
            pass
        
        modified_list = pq.QLabel(actions_text)
        modified_list.setWordWrap(True)
        modified_list.setStyleSheet("font: 12pt 'Arial'; margin: 10px;")
        content_layout.addWidget(modified_list, 0) 

        
    else:
        update_button.setText(lpak.get("update", language))
        try:
            update_button.pressed.disconnect()
        except TypeError:
            pass      
        content_layout.removeWidget(modified_list)
        modified_list.deleteLater()
        modified_list = None

        update_button.pressed.connect(update_all_apps)
  

# Funzione principale di ricerca
def search_program(name):
    global program_button_download, search_status, last_search, no_program_found_label
    global pacman_programs, aur_programs, flatpak_programs, scrollable_layout

    # Pulizia etichette di errore
    for label in ['no_program_found_label', 'error_label_textbox_empty']:
        try:
            eval(label).deleteLater()
        except:
            pass

    # Controllo se nessun repo è abilitato
    if setting_repo_pacman == "disable" and setting_repo_aur == "disable" and setting_repo_flatpak == "disable":
        show_allert(lpak.get("attenction", language), no_repo_error_text_default)
        return

    if search_status:
        return
    search_status = True

    # Pulizia widget esistenti
    for widget in scrollable_frame.findChildren(pq.QWidget):
        widget.deleteLater()

    # Imposta la stringa di ricerca
    program_search = search_bar.text() if name == " " else name
    #search_bar.clear()
    program_search = program_search.strip()

    if not program_search:
        error_label_textbox_empty = pq.QLabel(lpak.get("so you're looking for nothing", language))
        error_label_textbox_empty.setStyleSheet("color: red; font: bold 14pt 'Arial'")
        scrollable_layout.addWidget(error_label_textbox_empty, 0, 0, 1, 4)
        search_status = False
        return

    search_label.setText(f"{lpak.get('i\'m looking for', language)} {program_search}...")
    root.repaint()

    def parse_pacman_output(output):
        lines = [l for l in output.split("\n") if l]
        programs = []
        for i in range(len(lines)-1, 0, -2):
            programs.append(lines[i-1] + "|" + lines[i])
        return programs

    def parse_aur_output(output):
        lines = [l for l in output.split("\n") if l]
        programs = []
        for i in range(len(lines)-1, 0, -2):
            programs.append(lines[i-1] + "|" + lines[i])
        return programs

    #pacman
    if setting_repo_pacman == "enable":
        programs_pacman = os.popen("pacman -Ss "+program_search).read()   
        programs_commodo = programs_pacman.split("\n")
        programs_commodo = programs_commodo[:300]
        try:
            programs_commodo.remove("")    
        except:
            pass
        x = len(programs_commodo)
        pacman_programs=[]
        x = x-1    
        while x >= 0:        
            pacman_programs.append(programs_commodo[x-1]+"|"+programs_commodo[x])
            x = x-2  
    else:
        pacman_programs = []
    #AUR
    if setting_repo_aur == "enable":
        programs_commodo.clear()
        if name == " ":
            pass
        else:
            program_search = name
        command = f"{aur_method} -Ssa "+program_search
        programs_yay = os.popen(command).read()    
        programs_commodo = programs_yay.split("\n")
        programs_commodo.remove("")
        x = len(programs_commodo)
        x = x-1    
        aur_programs =[]
        while x >= 0:        
            aur_programs.append(programs_commodo[x-1]+"|"+programs_commodo[x])
            x = x-2 
    else:
        aur_programs = []        
    #flatpak
    if setting_repo_flatpak == "enable":
        if name == " ":
            pass
        else:
            program_search = name
        command = "flatpak search "+program_search
        flatpak_programs = os.popen(command).read()
        flatpak_programs = flatpak_programs.replace("\t", "    ")
        flatpak_programs = flatpak_programs.split("\n")
        last = flatpak_programs.pop()
        if last != "":
            flatpak_programs.append(last)
        command = "flatpak list"
        flatpak_installed_programs = os.popen(command).read()
        flatpak_installed_programs = flatpak_installed_programs.split("\n")
    else:
        flatpak_programs = []
    #Generate interface
    # Pulizia layout prima di generare interfaccia
    for i in reversed(range(scrollable_layout.count())):
        widget_to_remove = scrollable_layout.itemAt(i).widget()
        if widget_to_remove:
            widget_to_remove.deleteLater()

    # Header tabella
   # Header tabella
    #headers = ["actions", "programs",  "repository", "description"]
    actions_label = pq.QLabel(lpak.get("actions", language))
    programs_label = pq.QLabel(lpak.get("programs", language))
    repository_label = pq.QLabel(lpak.get("repository", language))
    description_label = pq.QLabel(lpak.get("description", language))

    actions_label.setStyleSheet("font: bold 14pt 'Arial'; color: #004080")
    programs_label.setStyleSheet("font: bold 14pt 'Arial'; color: #004080")
    repository_label.setStyleSheet("font: bold 14pt 'Arial'; color: #004080")
    description_label.setStyleSheet("font: bold 14pt 'Arial'; color: #004080")




    scrollable_layout.addWidget(actions_label, 0, 0)
    scrollable_layout.addWidget(programs_label, 0, 2)
    scrollable_layout.addWidget(repository_label, 0, 4)
    scrollable_layout.addWidget(description_label, 0, 6)
    """
    for idx, key in enumerate(headers):
    
        header_label = pq.QLabel(lpak.get(key, language))
        header_label.setStyleSheet("font: bold 14pt 'Arial'; color: #004080")
        scrollable_layout.addWidget(header_label, 0, idx*2)
    """

    row = 1
    #Generate download data

    if setting_repo_pacman == "enable":
        for program in pacman_programs:
            program_repository = program.split("/")[0]
            program_commodo = program.split("/")[1]
            program_name = program_commodo.split("|")[0]
            program_description = program_commodo.split("|")[1]
            if program_name.split(" ")[0] in install_pacman_packages or program_name.split(" ")[0] in install_aur_packages:
                button_download_text=lpak.get("do not install", language)
                status = ["Do not install"]
            elif program_name.split(" ")[0] in remove_aur_packages or program_name.split(" ")[0] in install_pacman_packages:
                button_download_text=lpak.get("do not remove", language)
                status = ["Do not remove"]
            else:
                if "[" in program_name:
                    button_download_text = lpak.get("remove", language)
                    status = ["Remove"]
                else:
                    button_download_text = lpak.get("install", language)
                    status = ["Install"]



            program_button_download = pq.QPushButton(parent=scrollable_frame, text=button_download_text)
            if status[0] == "Install":
                button_action_color = install_color
            elif status[0] == "Remove":
                button_action_color = remove_color
            else:
                button_action_color = modified_color
            program_button_download.setStyleSheet(f"background-color: {button_action_color}; {base_action_button_style}")
            program_button_download.pressed.connect(lambda name=program_name, repository=program_repository, button=program_button_download, stat=status: download_program(name, repository, button, stat))
            #
            
            scrollable_layout.addWidget(pq.QLabel(program_name), row, 2)
            scrollable_layout.addWidget(pq.QLabel(program_description), row, 6)
            scrollable_layout.addWidget(pq.QLabel(program_repository), row, 4)
            scrollable_layout.addWidget(program_button_download, row, 0)
            #
            line = pq.QFrame()
            line.setFrameShape(pq.QFrame.Shape.HLine)
            line.setFrameShadow(pq.QFrame.Shadow.Sunken)
            scrollable_layout.addWidget(line, row + 1, 0, 1, 7)

            row = row + 2  
    if setting_repo_flatpak == "enable":
        for program in flatpak_programs:
            #program name
            program_name_pure = ""
            last_char=""
            for char in program:
                if char == " " and last_char == " ":
                    break
                else:
                    program_name_pure = program_name_pure+char
                    last_char = char
            program = program.replace(program_name_pure, "", 1)
            program = program.lstrip(" ") #rimozione spazi fino al carattere
            #program description
            program_description = ""
            last_char=""
            for char in program:
                if char == " " and last_char == " ":
                    break
                else:
                    program_description = program_description+char
                    last_char = char
            program = program.replace(program_description, "")
            program = program.lstrip(" ")# rimozione spazi fino al carattere
            #program id
            program_id = ""
            last_char=""
            for char in program:
                if char == " " and last_char == " ":
                    break
                else:
                    program_id = program_id+char
                    last_char = char
            program = program.replace(program_id, "")
            program = program.lstrip(" ")# rimozione spazi fino al carattere
            #program verion number
            program_version = ""
            last_char=""
            for char in program:
                if char == " " and last_char == " ":
                    break
                else:
                    program_version = program_version+char
                    last_char = char
            program = program.replace(program_version, "")
            program = program.lstrip(" ")# rimozione spazi fino al carattere
            #progrema status version
            program_version_status = ""
            last_char=""
            for char in program:
                if char == " " and last_char == " ":
                    break
                else:
                    program_version_status = program_version_status+char
                    last_char = char
            program = program.replace(program_version_status, "")
            program = program.lstrip(" ")# rimozione spazi fino al carattere
            #progrema status version
            program_repository = program
            if program_name_pure.endswith(" "):
                program_name_pure = program_name_pure[:-1]
            if program_description.endswith(" "):
                program_description = program_description[:-1]
            if program_id.endswith(" "):
                program_id = program_id[:-1]
            if program_version.endswith(" "):
                program_version = program_version[:-1]
            if program_version_status.endswith(" "):
                program_version_status = program_version_status[:-1]
            if program_repository.endswith(" "):
                program_repository = program_repository[:-1]

            program_name = program_name_pure + " ("+program_version+" "+program_version_status+") ("+program_id+")"
            status = ["Do not install"]
            if program_name_pure in install_flatpak_packages:
                button_download_text=lpak.get("do not install", language)
                status = ["Do not install"]
            elif program_name_pure in remove_flatpak_packages:
                button_download_text=lpak("do not remove", language)
                status = ["Do not remove"]
            else:
                for program in flatpak_installed_programs:
                    if program_name_pure.lower() in program.lower():
                        button_download_text = lpak.get("remove", language)
                        status = ["Remove"]
                        break
                    else:
                        button_download_text = lpak.get("install", language)
                        status = ["Install"]
            if status[0] == "Install":
                button_action_color = install_color
            elif status[0] == "Remove":
                button_action_color = remove_color
            else:
                button_action_color = modified_color
            if not "No matches found ( )" in program_name:                

                program_button_download = pq.QPushButton(parent=scrollable_frame, text=button_download_text)
                program_button_download.setStyleSheet(f"background-color: {button_action_color}; {base_action_button_style}")
                program_button_download.pressed.connect(lambda name=program_name, repository=program_repository, button=program_button_download, stat=status: download_program(name, repository, button, stat))
                
                scrollable_layout.addWidget(pq.QLabel(program_name), row, 2)
                scrollable_layout.addWidget(pq.QLabel(program_description), row, 6)
                scrollable_layout.addWidget(pq.QLabel(program_repository), row, 4)
                scrollable_layout.addWidget(program_button_download, row, 0)
                #
                line = pq.QFrame()
                line.setFrameShape(pq.QFrame.Shape.HLine)
                line.setFrameShadow(pq.QFrame.Shadow.Sunken)
                scrollable_layout.addWidget(line, row + 1, 0, 1, 7)

                row = row + 2  
    if setting_repo_aur == "enable":
        for program in aur_programs:
            program_repository = program.split("/")[0]
            program_commodo = program.split("/")[1]
            program_name = program_commodo.split("|")[0]
            program_description = program_commodo.split("|")[1]
           
            test = program_name.split("(")
            try:
                test = test[2]
                button_download_text=lpak.get("remove", language)
                status = ["Remove"]
            except:
                button_download_text=lpak.get("install", language)
                status = ["Install"]

            program_button_download = pq.QPushButton(parent=scrollable_frame, text=button_download_text)
            if status[0] == "Install":
                button_action_color = install_color
            elif status[0] == "Remove":
                button_action_color = remove_color
            else:
                button_action_color = modified_color
            program_button_download.setStyleSheet(f"background-color: {button_action_color}; {base_action_button_style}")
            program_button_download.pressed.connect(lambda name=program_name, repository=program_repository, button=program_button_download, stat=status: download_program(name, repository, button, stat))
            #            
            scrollable_layout.addWidget(pq.QLabel(program_name), row, 2)
            scrollable_layout.addWidget(pq.QLabel(program_description), row, 6)
            scrollable_layout.addWidget(pq.QLabel(program_repository), row, 4)
            scrollable_layout.addWidget(program_button_download, row, 0)
            #
            line = pq.QFrame()
            line.setFrameShape(pq.QFrame.Shape.HLine)
            line.setFrameShadow(pq.QFrame.Shadow.Sunken)
            scrollable_layout.addWidget(line, row + 1, 0, 1, 7)

            row = row + 2  
    #END RESEARCH
    search_label.setText(lpak.get("search", language))
    search_status = False
   
    scrollable_layout.setRowStretch(scrollable_layout.rowCount(), 1)


    #
    if flatpak_programs == ['No matches found']:
        flatpak_programs = []
    if pacman_programs == [] and flatpak_programs == [] and aur_programs == []:
        no_program_found_label = pq.QLabel(lpak.get("no program found", language))
        no_program_found_label.setStyleSheet("color: red; font: bold 14pt 'Arial'")
        scrollable_layout.addWidget(no_program_found_label, row, 0, 1, 6)
    last_search = program_search


# Inizializzazione GUI
app = pq.QApplication(sys.argv)
root = pq.QMainWindow()
root.setWindowTitle(lpak.get("arch store", language))
root.setGeometry(400, 100, 1000, 800)
root.setWindowIcon(QIcon("icon.png"))

central_widget = pq.QWidget()
root.setCentralWidget(central_widget)
main_layout = pq.QVBoxLayout(central_widget)

# Barra superiore
top_layout = pq.QHBoxLayout()
search_label = pq.QLabel(lpak.get("search", language))
search_label.setStyleSheet("font: bold 14pt 'Arial'")
search_bar = pq.QLineEdit("")
search_bar.setFixedWidth(500)
search_button = pq.QPushButton(lpak.get("search", language))
update_button = pq.QPushButton(lpak.get("update", language))
other_button = pq.QPushButton(lpak.get("other", language))

search_button.pressed.connect(lambda: search_program(" "))
update_button.pressed.connect(update_all_apps)
other_button.pressed.connect(open_other)

for w in [search_label, search_bar, search_button, update_button, other_button]:
    top_layout.addWidget(w)
    top_layout.setSpacing(15)

main_layout.addLayout(top_layout)

# Layout centrale
content_layout = pq.QHBoxLayout()
main_layout.addLayout(content_layout)

# Scroll area a sinistra
scroll_area = pq.QScrollArea()
scroll_area.setWidgetResizable(True)
scrollable_frame = pq.QWidget()
scrollable_layout = pq.QGridLayout(scrollable_frame)
scroll_area.setWidget(scrollable_frame)
content_layout.addWidget(scroll_area, 1)

root.show()
sys.exit(app.exec())
    

       

