import PyQt6.QtWidgets as pq
import library.lpak as lpak
from PyQt6.QtGui import QIcon
import os
from show_allert import show_allert
import webbrowser
from PyQt6.QtCore import QProcess
def load_config_data(working_dir, avaible_languages, language):
    def write_new_config_file():
        with open(f"{working_dir}/settings.conf", "w") as f:
            f.write("pacman=enable\n")
            f.write("aur=enable\n")
            f.write("flatpak=enable\n")
            f.write("aur_method=yay\n")
            f.write("language=English\n")
            f.write(f"AppImmageDir={working_dir}/AppImages")
    def read_config_data():
        global pacman_status, aur_status, flatpak_status, aur_method, new_language, app_image_dir, old_language
        with open(f"{working_dir}/settings.conf", "r") as f:
            file_configuration_data = [line.rstrip('\n') for line in f.readlines()]
        pacman_status=file_configuration_data[0].split("=")[1]
        aur_status=file_configuration_data[1].split("=")[1]
        flatpak_status=file_configuration_data[2].split("=")[1]
        aur_method=file_configuration_data[3].split("=")[1]
        old_language=file_configuration_data[4].split("=")[1]
        app_image_dir=file_configuration_data[5].split("=")[1]
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


def open_setting(language, working_dir, avaible_languages, version):
    global pacman_status, aur_status, flatpak_status, aur_method, new_language, app_image_dir
    load_config_data(working_dir, avaible_languages, language)

    if not os.path.isfile(working_dir+"/script"):
        script_installation_status = False
    else:
        script_installation_status = True
    #Edit repo
    def confirm_changes():
        global pacman_status, aur_status, flatpak_status, aur_method, new_language, app_image_dir, old_language
        new_language = menu_select_language.currentText()
        
        
        with open(f"{working_dir}/settings.conf", "w") as f:
            f.write("pacman="+pacman_status+"\n")
            f.write("aur="+aur_status+"\n")
            f.write("flatpak="+flatpak_status+"\n")
            f.write("aur_method="+aur_method+"\n")
            f.write("language="+new_language+"\n")            
            f.write("AppImmageDir="+app_image_dir)
        language = new_language
        if old_language != new_language:
            show_allert(lpak.get("restart required", language), lpak.get("please restart to apply the changes", language))   
        else:   
            show_allert(lpak.get("finished", language), lpak.get("updated settings", language))
        return True
        
    def settings_change_pacman_status(language, working_dir):    
        global pacman_status    
        if pacman_status == "enable":
            pacman_status = "disable"
            button_repo_pacman.setText(lpak.get("enable", language))
        else:
            pacman_status = "enable"
            button_repo_pacman.setText(lpak.get("disable", language))
        
    def settings_change_aur_status():
        global aur_status
        if aur_status == "enable":
            aur_status = "disable"
            button_repo_aur.setText(lpak.get("enable", language))
        else:
            aur_status = "enable"
            button_repo_aur.setText(lpak.get("disable", language))        

    def settings_change_flatpak_status():
        global flatpak_status
        if flatpak_status == "enable":
            flatpak_status = "disable"
            button_repo_flatpak.setText(lpak.get("enable", language))
        else:
            flatpak_status = "enable"
            button_repo_flatpak.setText(lpak.get("disable", language))    
       
    def change_aur_method(button, label):
        global aur_method
        if aur_method == "paru":
            aur_method = "yay"
        else:
            aur_method = "paru"       
        label.setText(lpak.get("aur method", language)+": "+aur_method)
               
    def setting_change_appimagedir(button):
        new_dir_temp = pq.QFileDialog.getExistingDirectory(settings_page, lpak.get("select a folder", language))
        response = pq.QMessageBox.question(settings_page,
            lpak.get("confirm change", language),
            lpak.get("attenction this action will clear existing appimages dataset", language),
            pq.QMessageBox.StandardButton.Yes | pq.QMessageBox.StandardButton.No,
            pq.QMessageBox.StandardButton.No
        )
        if response == pq.QMessageBox.StandardButton.Yes:    
            with open(f"{working_dir}/appimages.data", "w") as f:
                f.write("")
            new_dir = new_dir_temp
            
        else:
            return
    
    def update_arch_store():   
        if script_installation_status == False:     
            def after_operations():            
                button_update_archStore.setText(lpak.get("updated", language))                
            
            def start_thread_operations(label, button):
            

                global proc
                
                # Aggiorna subito la UI (thread principale)
                button.setDisabled(True)
                label.setText(lpak.get("install in progress", language))
                progress_bar.setRange(0, 0)
                operations_window.repaint()
            
                proc = QProcess(operations_window) 

                def close_updates():
                    operations_window.close()


                def on_finished(exitCode, exitStatus):
                    global install_status
                    install_status = False
                    progress_bar.setRange(0, 1)
                    button.setText(lpak.get("finished", language))
                    label.setText(lpak.get("updated, please restart", language))
                    try:
                        button.pressed.disconnect()
                    except TypeError:
                        pass
                    after_operations()
                    button.setDisabled(False)
                    button.clicked.connect(close_updates)
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

                proc.start("pkexec", ["bash", "/tmp/arch_store_actions.sh"])
                
            response = pq.QMessageBox.question(settings_page,
                lpak.get("Select a version", language),
                lpak.get("Do you want to install the stable version?", language),
                pq.QMessageBox.StandardButton.Yes | pq.QMessageBox.StandardButton.No,
                pq.QMessageBox.StandardButton.No
            )

            if response == pq.QMessageBox.StandardButton.Yes:
                remove_other_version_command = "sudo pacman -Rns arch-store-git --noconfirm"       
                makepkg_command = f"{aur_method} -S arch-store --noconfirm"
            else:
                remove_other_version_command = "sudo pacman -Rns arch-store --noconfirm" 
                makepkg_command = f"{aur_method} -S arch-store-git --noconfirm"
            
            with open(f"/tmp/arch_store_actions.sh", "w") as f:
                f.write("#!/bin/bash\n")
                f.write(remove_other_version_command+"\n")
                f.write(makepkg_command+"\n")
            
            operations_window = pq.QWidget()
            operations_window.setWindowTitle(lpak.get("start update", language))    
            operations_window.setWindowIcon(QIcon("icon.png"))
            layout = pq.QVBoxLayout(operations_window)
            install_label = pq.QLabel(lpak.get("click to start update", language))
            start_button = pq.QPushButton(lpak.get("start update", language))
            start_button.pressed.connect(lambda: start_thread_operations(install_label, start_button))
            progress_bar = pq.QProgressBar()     

            layout.addWidget(install_label)
            layout.addWidget(progress_bar) 
            layout.addWidget(start_button)

            operations_window.show()
        else:
            response = pq.QMessageBox.question(settings_page,
                lpak.get("Do you want to open GitHub?", language),
                lpak.get("It appears that you installed ArchStore from the script. Would you like to open GitHub to rerun the script?", language),
                pq.QMessageBox.StandardButton.Yes | pq.QMessageBox.StandardButton.No,
                pq.QMessageBox.StandardButton.No
            )

            if response == pq.QMessageBox.StandardButton.Yes:
                webbrowser.open("https://github.com/Samuobe/Arch-Store?tab=readme-ov-file#automatic-script")


    #Other
    def settings_reset_settings(working_dir, avaible_languages, language):
        os.remove(f"{working_dir}/settings.conf")        
        load_config_data(working_dir, avaible_languages, language)
        show_allert(lpak.get("restart required", language), lpak.get("please restart to apply the changes", language))  

    settings_page = pq.QDialog()
    settings_page.setWindowTitle(lpak.get("arch store settings", language))
    settings_page.setGeometry(0, 0, 900, 600)   
    layout = pq.QGridLayout(settings_page)    
    settings_page.setWindowIcon(QIcon(f"icon.png"))

    settings_label_title = pq.QLabel(lpak.get("settings", language))
    settings_label_repo = pq.QLabel(lpak.get("enable disable repo", language))
    settings_label_title.setStyleSheet("color: black; font: bold 12pt 'Arial';")
    settings_label_repo.setStyleSheet("font-weight: bold; font-style: italic;")

    #pacman repo
    label_repo_pacman=pq.QLabel("Pacman")
    if pacman_status == "enable":
        text_setting_repo_pacman = lpak.get("disable", language)
    else:
        text_setting_repo_pacman = lpak.get("enable", language)
    button_repo_pacman = pq.QPushButton(text_setting_repo_pacman)
    button_repo_pacman.pressed.connect(lambda: settings_change_pacman_status(language, working_dir))
    #aur repo
    label_repo_aur=pq.QLabel("Aur")
    if aur_status == "enable":
        text_setting_repo_aur = lpak.get("disable", language)
    else:
        text_setting_repo_aur = lpak.get("enable", language)
    button_repo_aur = pq.QPushButton(text_setting_repo_aur)
    button_repo_aur.pressed.connect(settings_change_aur_status)
    #flatpak repo
    label_repo_flatpak=pq.QLabel("Flatpak")
    if flatpak_status == "enable":
        text_setting_repo_flatpak = lpak.get("disable", language)
    else:
        text_setting_repo_flatpak = lpak.get("enable", language)
    button_repo_flatpak = pq.QPushButton(text_setting_repo_flatpak)
    button_repo_flatpak.pressed.connect(settings_change_flatpak_status)
    #RESET
    button_reset_settings= pq.QPushButton(lpak.get("reset settings", language))
    button_reset_settings.pressed.connect(lambda: settings_reset_settings(working_dir, avaible_languages, language))
    #update Arch Store
    button_update_archStore = pq.QPushButton(lpak.get("Update ArchStore", language))
    button_update_archStore.pressed.connect(update_arch_store)
    #change AUR method
    label_aur_method = pq.QLabel(lpak.get("aur method", language)+": "+aur_method)
    button_change_aur_method = pq.QPushButton(lpak.get("change", language))
    button_change_aur_method.pressed.connect(lambda button=button_change_aur_method, label=label_aur_method: change_aur_method(button, label))
    #other label
    label_other_settings = pq.QLabel(lpak.get("other", language))
    label_other_settings.setStyleSheet("font-weight: bold; font-style: italic;")
    #language      
    menu_select_language = pq.QComboBox()
    menu_select_language.addItems(avaible_languages)
    menu_select_language.setCurrentText(language)
    label_language=pq.QLabel(lpak.get("language", language))    
    #appimagedir
    appimagesdir_label = pq.QLabel(lpak.get("appimages installation path", language))
    appimagesdir_button = pq.QPushButton(lpak.get("change appimage path", language))
    appimagesdir_button.pressed.connect(lambda button =appimagesdir_button: setting_change_appimagedir(button))
    #confirm settings
    confirm_button = pq.QPushButton(lpak.get("confirm changes", language))
    confirm_button.pressed.connect(confirm_changes)
    #crediti
    def github_button():
        webbrowser.open("https://github.com/IlNonoP/Arch-Store")
    author_label = pq.QLabel(lpak.get("made whit heart by Samuobe", language))
    project_link = pq.QPushButton(lpak.get("github project", language))
    project_link.pressed.connect(github_button)
    #Version
    version_label = pq.QLabel(lpak.get("version", language))
    if script_installation_status == False:
        archstore_installation_method = "AUR"
    else:
        archstore_installation_method = "Script"
    version_label_var = pq.QLabel(f"{version}   ({lpak.get("Installated with", language)} {lpak.get(archstore_installation_method, language)})")
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
    layout.addWidget(button_update_archStore, 1, 3)
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
    #
    layout.addWidget(label_language, 8, 0)
    layout.addWidget(menu_select_language, 8, 1)    

    layout.addWidget(appimagesdir_label, 9, 0)
    layout.addWidget(appimagesdir_button, 9, 1)

    layout.addWidget(confirm_button, 10, 0)

    layout.addWidget(line_separazione, 12, 0, 1, 3)  # row=12, colspan=3
    layout.addWidget(author_label, 13, 0)
    layout.addWidget(project_link, 13, 1)

    layout.addWidget(version_label, 15, 0)
    layout.addWidget(version_label_var, 15, 1)

    layout.setRowStretch(layout.rowCount(), 1)

    settings_page.show()

    return settings_page