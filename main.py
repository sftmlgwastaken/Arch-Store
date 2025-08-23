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
from PyQt6.QtCore import QProcess
import sys

#PY files
import appimages as archstoreAppimages
import settings as archstoreSettings
from show_allert import show_allert
from show_installed_programs import show as show_installed_programs

#fast access variables
avaible_languages = ["Italiano", "English", "Español", "Română", "Polski", "Norsk"]

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

#END ALLERT

def open_setting():
    respose = archstoreSettings.open_setting(language, working_dir, avaible_languages)
    if respose == True:
        load_config_data()
    

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

    def close_updates():
        update_window.close()

    def start_update():
        global install_status        
        install_status = True
        button.setDisabled(True)
        label.setText(lpak.get("update in progress", language))
        progress_bar.setRange(0, 0) 
        update_window.repaint()  

        proc = QProcess(update_window)       
        def on_finished(exitCode, exitStatus):
            global install_status
            install_status = False
            progress_bar.setRange(0, 1)
            button.setText(lpak.get("finished", language))
            label.setText(lpak.get("finished", language))
            try:
                button.pressed.disconnect()
            except TypeError:
                pass
            button.setDisabled(False)
            button.clicked.connect(close_updates)
            update_window.update()

        def on_error(err):
            global install_status
            install_status = False
            progress_bar.setRange(0, 1)
            label.setText(f"{lpak.get('error', language)}: {err}")
            button.setDisabled(False)
            operations_window.update()
         
        proc.finished.connect(on_finished)
        proc.errorOccurred.connect(on_error)

        proc.start("pkexec", ["bash", os.path.join(working_dir, "actions.sh")])

    update_window = pq.QWidget()
    update_window.setGeometry(100, 100, 400, 200)
    update_window.setWindowIcon(QIcon(f"icon.png"))
    update_window.setWindowTitle(lpak.get("update", language))
    layout = pq.QVBoxLayout(update_window)
    label = pq.QLabel(lpak.get("click to start update", language))
    layout.addWidget(label)
    progress_bar = pq.QProgressBar()      
    layout.addWidget(progress_bar)  
    button = pq.QPushButton(lpak.get("start update", language))    
    layout.addWidget(button)
    button.pressed.connect(start_update)

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
        global install_status, proc
        if install_status == True:
            show_allert(lpak.get("an install instance is alredy in progress", language), lpak.get("an install instance is alredy in progress", language))
            return

        install_status = True

        # Aggiorna subito la UI (thread principale)
        button.setDisabled(True)
        label.setText(lpak.get("install in progress", language))
        progress_bar.setRange(0, 0)
        operations_window.repaint()
    
        proc = QProcess(operations_window) 


        def on_finished(exitCode, exitStatus):
            global install_status
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

        def on_error(err):
            global install_status
            install_status = False
            progress_bar.setRange(0, 1)
            label.setText(f"{lpak.get('error', language)}: {err}")
            button.setDisabled(False)
            operations_window.update()

        proc.finished.connect(on_finished)
        proc.errorOccurred.connect(on_error)

        proc.start("pkexec", ["bash", os.path.join(working_dir, "actions.sh")])


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
    program_search = program_search.strip()

    if not program_search:
        error_label_textbox_empty = pq.QLabel(lpak.get("so you're looking for nothing", language))
        error_label_textbox_empty.setStyleSheet("color: red; font: bold 14pt 'Arial'")
        scrollable_layout.addWidget(error_label_textbox_empty, 0, 0, 1, 4)
        search_status = False
        return

    search_label.setText(f"{lpak.get('i\'m looking for', language)} {program_search}...")
    root.repaint()
    
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
    #Clean widget
    for i in reversed(range(scrollable_layout.count())):
        widget_to_remove = scrollable_layout.itemAt(i).widget()
        if widget_to_remove:
            widget_to_remove.deleteLater()

    # Header tabella    
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
                program_button_download.pressed.connect(lambda name=program_id, repository="flatpak", button=program_button_download, stat=status: download_program(name, repository, button, stat))
                
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


#small functions
def open_github():
    webbrowser.open("https://github.com/Samuobe/Arch-Store")
# Inizializzazione GUI
app = pq.QApplication(sys.argv)
root = pq.QMainWindow()
root.setWindowTitle(lpak.get("arch store", language))
root.setGeometry(400, 100, 1000, 800)
root.setWindowIcon(QIcon("icon.png"))

central_widget = pq.QWidget()
root.setCentralWidget(central_widget)
main_layout = pq.QVBoxLayout(central_widget)

##MENU
menu_bar = root.menuBar()
appimage_menu = menu_bar.addMenu("AppImages")
update_appimages_action = appimage_menu.addAction(lpak.get("update", language)+"/"+lpak.get("remove", language))
install_appimage_action = appimage_menu.addAction(lpak.get("install", language))
update_appimages_action.triggered.connect(lambda: archstoreAppimages.open_appimages_settings(language, working_dir))
install_appimage_action.triggered.connect(lambda: archstoreAppimages.start_add_appimage(language, working_dir))
#
settings_menu = menu_bar.addMenu(lpak.get("settings", language))
open_setting_action = settings_menu.addAction(lpak.get("settings", language))
open_setting_action.triggered.connect(open_setting)
#
other_menu = menu_bar.addMenu(lpak.get("other", language))
open_currently_installed_packages = other_menu.addAction(lpak.get("installed packages", language))
open_github_action = other_menu.addAction("GitHub")
exit_action = other_menu.addAction(lpak.get("exit", language))

exit_action.triggered.connect(app.quit)
open_github_action.triggered.connect(open_github)
open_currently_installed_packages.triggered.connect(lambda: show_installed_programs(language, working_dir, aur_method, setting_repo_pacman, setting_repo_aur, setting_repo_flatpak))

##END MENU

# TOP bar
top_layout = pq.QHBoxLayout()
search_label = pq.QLabel(lpak.get("search", language))
search_label.setStyleSheet("font: bold 14pt 'Arial'")
search_bar = pq.QLineEdit("")
search_bar.setFixedWidth(500)
search_button = pq.QPushButton(lpak.get("search", language))
update_button = pq.QPushButton(lpak.get("update", language))

search_button.pressed.connect(lambda: search_program(" "))
update_button.pressed.connect(update_all_apps)

for w in [search_label, search_bar, search_button, update_button]:
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
