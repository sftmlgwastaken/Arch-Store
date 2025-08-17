import os
import tkinter as tk
import subprocess
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
import threading
import library.lpak as lpak
import webbrowser
import getpass

#from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
import PyQt6.QtWidgets as pq
from PyQt6.QtCore import QObject, pyqtSignal, QThread

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

#Auto-set variables
working_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(working_dir)
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
        with open("settings.conf", "w") as f:
            f.write("pacman=enable\n")
            f.write("aur=enable\n")
            f.write("flatpak=enable\n")
            f.write("aur_method=yay\n")
            f.write("language=English\n")
            f.write(f"AppImmageDir={working_dir}/AppImages")
    def read_config_data():
        global setting_repo_pacman, setting_repo_aur, setting_repo_flatpak, aur_method, language, AppImagesDir
        with open("settings.conf", "r") as f:
            file_configuration_data = [line.rstrip('\n') for line in f.readlines()]
        setting_repo_pacman=file_configuration_data[0].split("=")[1]
        setting_repo_aur=file_configuration_data[1].split("=")[1]
        setting_repo_flatpak=file_configuration_data[2].split("=")[1]
        aur_method=file_configuration_data[3].split("=")[1]
        language=file_configuration_data[4].split("=")[1]
        AppImagesDir=file_configuration_data[5].split("=")[1]
    if not os.path.isfile("settings.conf"):
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



###############
#SETTINGS DATA#

def open_setting(window):
    #Edit repo
    def settings_change_pacman_status():
        with open("settings.conf", "r") as f:
            file_configuration_data = [line.rstrip('\n') for line in f.readlines()]
        if setting_repo_pacman == "enable":
            new_status = "disable"
            button_repo_pacman.config(text=lpak.get("enable", language))
        else:
            new_status = "enable"
            button_repo_pacman.config(text=lpak.get("disable", language))
        with open("settings.conf", "w") as f:
            f.write("pacman="+new_status+"\n")
            for line in file_configuration_data:
                if not "pacman=" in line:
                    f.write(line+"\n")   
        load_config_data()
    def settings_change_aur_status():
        with open("settings.conf", "r") as f:
            file_configuration_data = [line.rstrip('\n') for line in f.readlines()]
        if setting_repo_aur == "enable":
            new_status = "disable"
            button_repo_aur.config(text=lpak.get("enable", language))
        else:
            new_status = "enable"
            button_repo_aur.config(text=lpak.get("disable", language))
        with open("settings.conf", "w") as f:
            f.write(file_configuration_data[0]+"\n")
            f.write("aur="+new_status+"\n")
            for line in file_configuration_data:
                if not "aur=" in line and not "pacman=" in line:
                    f.write(line+"\n")   
        load_config_data()

    def settings_change_flatpak_status():
        with open("settings.conf", "r") as f:
            file_configuration_data = [line.rstrip('\n') for line in f.readlines()]
        if setting_repo_flatpak == "enable":
            new_status = "disable"
            button_repo_flatpak.config(text=lpak.get("enable", language))
        else:
            new_status = "enable"
            button_repo_flatpak.config(text=lpak.get("disable", language))
        with open("settings.conf", "w") as f:
            f.write(file_configuration_data[0]+"\n")
            f.write(file_configuration_data[1]+"\n")
            f.write("flatpak="+new_status+"\n")
            for line in file_configuration_data:
                if not "flatpak=" in line and not "aur=" in line and not "pacman=" in line:
                    f.write(line+"\n")   
            load_config_data()
    def settings_change_language(settings_page):
        with open("settings.conf", "r") as f:
            file_configuration_data = [line.rstrip('\n') for line in f.readlines()]
        language = menu_select_language.get()
        with open("settings.conf", "w") as f:
            for line in file_configuration_data:
                if not "language=" in line:
                    f.write(line+"\n")
                else:
                    f.write("language="+language+"\n")
        load_config_data()
        root.destroy()        

    def change_aur_method(button, label):
        if aur_method == "paru":
            new_method = "yay"
        else:
            new_method = "paru"
        with open("settings.conf", "r") as f:
            file_configuration_data = [line.rstrip('\n') for line in f.readlines()]        
        with open("settings.conf", "w") as f:
            for line in file_configuration_data:
                if not "aur_method=" in line:
                    f.write(line+"\n")
                else:
                    f.write("aur_method="+new_method+"\n")
        load_config_data()
        label.config(text=lpak.get("aur method", language)+": "+aur_method)
        button.config(text=lpak.get("changed", language))
        
        
    def setting_change_appimagedir(button):
        new_dir = filedialog.askdirectory(parent=settings_page, title=lpak.get("select a folder", language))
        response = messagebox.askyesno(
            lpak.get("confirm change", language),
            lpak.get("attenction this action will clear existing appimages dataset", language),
            parent=settings_page
        )
        if response:    
            with open("appimages.data", "w") as f:
                f.write("")
            with open("settings.conf", "r") as f:
                file_configuration_data = [line.rstrip('\n') for line in f.readlines()]
            with open("settings.conf", "w") as f:
                for line in file_configuration_data:
                    if not "AppImmageDir=" in line:
                        f.write(line+"\n")
                    else:
                        f.write("AppImmageDir="+new_dir+"\n")
            button.config(text=lpak.get("changed", language))
            load_config_data()
        else:
            return
    #Other
    def settings_reset_settings(window):
        os.remove("settings.conf")
        load_config_data()
        root.destroy()
    settings_page = tk.Toplevel(window)
    settings_page.title(lpak.get("arch store settings", language))
    settings_page.geometry("900x600")
    settings_page.minsize(600, 600)
    icon = tk.PhotoImage(file="icon.png")
    settings_page.iconphoto(False, icon)

    settings_label_title = tk.Label(settings_page, text=lpak.get("settings", language), font=("Helvetica", 18, "bold italic"))
    settings_label_repo = tk.Label(settings_page, text=lpak.get("enable disable repo", language), font=("Helvetica", 12, "bold"))
    #pacman repo
    label_repo_pacman=tk.Label(settings_page, text="Pacman")
    if setting_repo_pacman == "enable":
        text_setting_repo_pacman = lpak.get("disable", language)
    else:
        text_setting_repo_pacman = lpak.get("enable", language)
    button_repo_pacman = tk.Button(settings_page, text=text_setting_repo_pacman, command=settings_change_pacman_status)
    #aur repo
    label_repo_aur=tk.Label(settings_page, text="Aur")
    if setting_repo_aur == "enable":
        text_setting_repo_aur = lpak.get("disable", language)
    else:
        text_setting_repo_aur = lpak.get("enable", language)
    button_repo_aur = tk.Button(settings_page, text=text_setting_repo_aur, command=settings_change_aur_status)
    #flatpak repo
    label_repo_flatpak=tk.Label(settings_page, text="Flatpak")
    if setting_repo_flatpak == "enable":
        text_setting_repo_flatpak = lpak.get("disable", language)
    else:
        text_setting_repo_flatpak = lpak.get("enable", language)
    button_repo_flatpak = tk.Button(settings_page, text=text_setting_repo_flatpak, command=settings_change_flatpak_status)
    button_reset_settings= tk.Button(settings_page, text=lpak.get("reset settings", language), command=lambda window=window: settings_reset_settings(window))
    #change AUR method
    label_aur_method = tk.Label(settings_page, text=lpak.get("aur method", language)+": "+aur_method)
    button_change_aur_method = tk.Button(settings_page, text=lpak.get("change", language))
    button_change_aur_method.config(command=lambda button=button_change_aur_method, label=label_aur_method: change_aur_method(button, label))
    #other label
    label_other_settings = tk.Label(settings_page, text=lpak.get("other", language), font=("Helvetica", 12, "bold"))
    #language      
    menu_select_language = ttk.Combobox(settings_page, values=avaible_languages)
    menu_select_language.set(language)
    label_language=tk.Label(settings_page, text=lpak.get("language", language))
    button_language_confirm=tk.Button(settings_page, text=lpak.get("confirm change language", language), command=lambda settings_page=settings_page: settings_change_language(settings_page))    
    #appimagedir
    appimagesdir_label = tk.Label(settings_page, text=lpak.get("appimages installation path", language))
    appimagesdir_button = tk.Button(settings_page, text=lpak.get("change appimage path", language))
    appimagesdir_button.config(command=lambda button =appimagesdir_button: setting_change_appimagedir(button))
    #crediti
    def github_button():
        webbrowser.open("https://github.com/IlNonoP/Arch-Store")
    author_label = tk.Label(settings_page, text=lpak.get("made whit heart by Samuobe", language))
    project_link = tk.Button(settings_page, text=lpak.get("github project", language), command=github_button) 
    line_separazione = ttk.Separator(settings_page, orient="horizontal")
    #
    empty_label = tk.Label(settings_page, text=" ")
    #
    settings_label_title.grid(row=0, columnspan=2)
    button_reset_settings.grid(row=0, column = 3)    
    settings_label_repo.grid(row=1, column=0)
    label_repo_pacman.grid(row=2, column=0)
    button_repo_pacman.grid(row=2, column=1)
    label_repo_flatpak.grid(row=3, column=0)
    button_repo_flatpak.grid(row=3, column=1)
    label_repo_aur.grid(row=4, column=0)
    button_repo_aur.grid(row=4, column=1)
    label_aur_method.grid(row=5, column=0)
    button_change_aur_method.grid(row=5, column=1)  
    empty_label.grid(row=6)
    label_other_settings.grid(row=7, column=0)
    #
    label_language.grid(row=8, column=0)
    menu_select_language.grid(row=8, column=1)
    button_language_confirm.grid(row=9, columnspan=1)
    appimagesdir_label.grid(row=10, column=0)
    appimagesdir_button.grid(row=10, column=1)
    #
    line_separazione.grid(column=0, row=12, columnspan=3, sticky='ew', pady=10)
    author_label.grid(column=0, row=13)
    project_link.grid(column=1, row=13)
    settings_page.mainloop()

#END SETTINGS##
###############

###########
###OTHER###
def open_appimages_settings(window):
        def update_appimage_window(name, program_user_base, window):
            appimage_path = filedialog.askopenfilename(
                parent=window, 
                title=lpak.get("select an appimage", language),
                filetypes=[("AppImage", "*.AppImage")]
            )
            if not appimage_path:  
                return
            os.remove(AppImagesDir+f"/{name}-{program_user_base}.AppImage")
            os.system(f"mv '{appimage_path}' '{AppImagesDir}/{name}-{program_user_base}.AppImage'")
            messagebox.showinfo(
                lpak.get("update completed", language),
                lpak.get("update completed", language),
                parent=window  
            )            

        def remove_appimage(name, program_user_base, window):            
            os.remove(AppImagesDir+f"/{name}-{program_user_base}.AppImage")
            os.remove(AppImagesDir+f"/{name}-{program_user_base}.png")
            if program_user_base == "-":
                cmd = f"rm '/usr/share/applications/{name}-archstore.desktop'"
                subprocess.run(["pkexec", "bash", "-c", cmd])                
            else:
                desktop_path = os.path.expanduser(f"~/.local/share/applications/{name}-archstore.desktop")
                os.remove(desktop_path)
            with open("appimages.data", "r") as f:
                appimage_data = f.readlines()
            with open("appimages.data", "w") as f:
                for line in appimage_data:
                    if line != f"{name}|{program_user_base}":
                        f.write(line)
            messagebox.showinfo(
                lpak.get("remove completed", language),
                lpak.get("remove completed", language),
                parent=window
            )

        def start_add_appimage():
            def select_file_appimage(button, parent_window):
                appimage_path = filedialog.askopenfilename(
                    parent=parent_window,  # <-- rende il dialog figlio del Toplevel
                    title=lpak.get("select an appimage", language),
                    filetypes=[("AppImage", "*.AppImage")]
                )
                if appimage_path:  # solo se l'utente ha selezionato qualcosa
                    button.config(text=appimage_path)
            def select_file_icon(button, parent_window):
                icon_path = filedialog.askopenfilename(
                    parent=parent_window,  # finestra Toplevel di riferimento
                    title=lpak.get("select an icon", language),
                    filetypes=[(lpak.get("PNG", language), "*.png")]
                )
                button.config(text=icon_path)

            def confirm_appimage_install(name_text, path_but, icon_but, category_selection, add_appimage_window):
                name = name_text.get()
                path = path_but.cget("text")
                icon = icon_but.cget("text")
                category = category_selection.get()
                if "|" in name or name == None or name == "":
                    messagebox.showwarning(lpak.get("illegal caracter", language), lpak.get("you can't use the following caracther", language)+": |", parent=add_appimage_window)
                    return
                if not os.path.isfile(path):
                    messagebox.showwarning(lpak.get("invalid appimage location", language), lpak.get("the appimage you selected was not found", language)+": |", parent=add_appimage_window)
                    return
                if not os.path.isfile(icon):
                    messagebox.showwarning(lpak.get("invalid icon location", language), lpak.get("the icon you selected was not found", language)+": |", parent=add_appimage_window  )
                    return     
                response = messagebox.askyesno(
                    lpak.get("confirm installation", language),
                    lpak.get("do you want to install it for all users", language),
                    parent=add_appimage_window
                )
                if response:
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
                with open("appimages.data", "r") as f:
                    appimage_file_data = f.readlines()
                with open ("appimages.data", "w") as f:
                    for line in appimage_file_data:
                        f.write(line)                        
                    f.write(f"\n{name}|{program_user}")
                messagebox.showinfo(
                    lpak.get("installation completed", language),
                    lpak.get("installation completed", language),
                    parent=add_appimage_window  
                )

            add_appimage_window = tk.Toplevel(appimages_window)
            add_appimage_window.geometry("900x500")
            add_appimage_window.title(lpak.get("add appimage", language))
            appimage_name_label = tk.Label(add_appimage_window, text=lpak.get("name", language))
            appimage_name_textbox = tk.Entry(add_appimage_window, width=20, )
            appimage_path_label = tk.Label(add_appimage_window, text=lpak.get("path", language))
            appimage_path_button = tk.Button(add_appimage_window, text=lpak.get("select an appimage", language))
            appimage_path_button.config(command=lambda path_button=appimage_path_button, back_top=add_appimage_window: select_file_appimage(path_button, back_top))
            appimage_ico_label = tk.Label(add_appimage_window, text=lpak.get("icon", language))
            appimage_ico_button = tk.Button(add_appimage_window, text=lpak.get("select an icon", language))
            appimage_ico_button.config(command=lambda ico_button = appimage_ico_button, back_top=add_appimage_window: select_file_icon(ico_button, back_top))      
            avaible_appimage_types = ["Utility", "Game", "Graphics", "Network", "AudioVideo", "Development", "Office", "Presentation"]
            menu_select_type = ttk.Combobox(add_appimage_window, values=avaible_appimage_types)
            label_language=tk.Label(add_appimage_window, text=lpak.get("app type", language))
            appimage_confirm_button = tk.Button(add_appimage_window, text=lpak.get("install appimage",language), command=lambda name=appimage_name_textbox, path=appimage_path_button, icon=appimage_ico_button, tipe=menu_select_type, window=add_appimage_window: confirm_appimage_install(name, path, icon, tipe, window))
            #
            appimage_name_label.grid(row=0, column=0, sticky="w")
            appimage_name_textbox.grid(row=0, column=1, pady=1, sticky="e")
            appimage_path_label.grid(row=1, column=0, sticky="w")
            appimage_path_button.grid(row=1, column=1, sticky="e")
            appimage_ico_label.grid(row=2, column=0, sticky="w")
            appimage_ico_button.grid(row=2, column=1, sticky="e")
            label_language.grid(row=3, column=0, sticky="w")
            menu_select_type.grid(row=3, column=1, sticky="e")
            appimage_confirm_button.grid(row=4, columnspan=2, sticky="w")
            add_appimage_window.mainloop()

        appimages_window = tk.Toplevel(window)
        appimages_window.title(lpak.get("manage appimages", language))
        icon = tk.PhotoImage(file="icon.png")
        appimages_window.iconphoto(False, icon)
        appimages_window.geometry("600x500")        

        # Scrollable
        container = tk.Frame(appimages_window)
        container.grid(row=0, column=0, sticky="nsew")
        appimages_window.grid_rowconfigure(0, weight=1)
        appimages_window.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #end scrollable

        if not os.path.isfile("appimages.data"):
            with open("appimages.data", "w") as f:
                pass
      
        with open("appimages.data", "r") as f:
            appimages_data = f.readlines()
        row = 0
        header_font = font.Font(weight="bold")

        if appimages_data == []:
            no_appimage_apps_label = tk.Label(scrollable_frame, text=lpak.get("no appimages app", language))
            no_appimage_apps_label.grid(row=row, column=0, sticky="w", padx=5, pady=5)
        else:
            # 
            actions_label = tk.Label(scrollable_frame, text=lpak.get("actions", language), font=header_font)
            name_label = tk.Label(scrollable_frame, text=lpak.get("name", language), font=header_font)
            user_label = tk.Label(scrollable_frame, text=lpak.get("user", language), font=header_font)
            actions_label.grid(row=row, column=0)
            name_label.grid(row=row, column=3)
            user_label.grid(row=row, column=5)
            # 
            ttk.Separator(scrollable_frame, orient="horizontal").grid(row=row+1, column=0, columnspan=6, sticky='ew', pady=6)
            row += 2

            for app in appimages_data:
                try:
                    name, user= app.strip().split("|")                
                    if user == "-" or user == user_name:
                        remove_appimage_button = tk.Button(scrollable_frame, text=lpak.get("remove", language), command=lambda name=name, user=user, window=appimages_window: remove_appimage(name, user, window))
                        update_appimage_button = tk.Button(scrollable_frame, text=lpak.get("update", language), command=lambda name=name, user=user, window=appimages_window: update_appimage_window(name, user, window))
                        appimage_name_label = tk.Label(scrollable_frame, text=name)
                        appimage_user = tk.Label(scrollable_frame, text=user)

                        remove_appimage_button.grid(row=row, column=0)
                        update_appimage_button.grid(row=row, column=1)
                        appimage_name_label.grid(row=row, column=3)
                        appimage_user.grid(row=row, column=5)
                        

                        # linea separatrice dopo ogni riga di dati
                        ttk.Separator(scrollable_frame, orient="horizontal").grid(row=row+1, column=0, columnspan=6, sticky='ew', pady=5)
                        row += 2

                except:
                    pass

            # linee verticali
            ttk.Separator(scrollable_frame, orient="vertical").grid(column=2, row=1, rowspan=row-1, sticky='ns')
            ttk.Separator(scrollable_frame, orient="vertical").grid(column=4, row=1, rowspan=row-1, sticky='ns')
            ttk.Separator(scrollable_frame, orient="vertical").grid(column=6, row=1, rowspan=row-1, sticky='ns')
            
        add_appimage_button=tk.Button(appimages_window, text=lpak.get("add appimage", language), command=start_add_appimage)
        add_appimage_button.grid(row=1, columnspan=4)
        appimages_window.mainloop()


def open_other():
    

    other_option_window = tk.Toplevel(root)
    other_option_window.title(lpak.get("other options", language))
    icon = tk.PhotoImage(file="icon.png")
    other_option_window.iconphoto(False, icon)
    other_option_window.geometry("400x400")
    other_option_window.grid_rowconfigure(0, weight=1)
    other_option_window.grid_columnconfigure(0, weight=1)
    setting_button = tk.Button(other_option_window, text=lpak.get("settings", language), command=lambda window=other_option_window: open_setting(window))
    appimage_button = tk.Button(other_option_window, text=lpak.get("manage appimages", language), command=lambda window=other_option_window: open_appimages_settings(window))
    appimage_button.grid(row=0, columnspan=2, sticky="n")
    setting_button.grid(columnspan=2, row=1, sticky="n")

    other_option_window.mainloop()


def show_allert(title, message):
    msg = pq.QMessageBox()
    msg.setIcon(pq.QMessageBox.Icon.Information)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.setStandardButtons(pq.QMessageBox.StandardButton.Ok | pq.QMessageBox.StandardButton.Cancel)
    retval = msg.exec()
    
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
    with open("actions.sh", "w") as f:
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
        os.chdir(working_dir)
        install_status = True
        update_button.setDisabled(True)
        text_area.setText(lpak.get("update in progress", language))
        progress_bar.setRange(0, 0) # modalità indeterminata

        update_window.repaint()
           
        proc = subprocess.run(["pkexec", "bash", os.path.join(working_dir, "actions.sh")])
        
            
        install_status = False
        progress_bar.setRange(0, 1)  # ferma barra
        update_button.setText(lpak.get("finished", language))
        #update_button.pressed.connect(close_settings)
        try:
            update_button.pressed.disconnect()
        except TypeError:
            pass
      
        update_button.setDisabled(False)
        update_button.clicked.connect(close_settings)
        update_window.update()

    update_window = pq.QWidget()
    update_window.setGeometry(100, 100, 400, 200)
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

    os.remove("actions.sh")


  
    

    
def start_selectionated_operations(program_name):
    global start_operation_button, operation_list_label, install_pacman_packages, remove_pacman_packages, install_aur_packages, remove_aur_packages, install_flatpak_packages, remove_flatpak_packages, install_status
    #if install_status == True:
      # tk.messagebox.Message(text=lpak.get("an install instance is alredy in progress", language))
     #  return
    #install_status = True
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
    with open("actions.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("\n"+install_pacman_command)
        f.write("\n"+remove_pacman_command)
        f.write("\n"+install_aur_command)
        f.write("\n"+remove_aur_command)
        f.write("\n"+install_flatpak_command)
        f.write("\n"+remove_flatpak_command)
    def run_operations(operations_window, start_button):
        os.chdir(working_dir)        
        command_update = ["pkexec", "bash", os.path.join(working_dir, "actions.sh")]
        process = subprocess.Popen(
            command_update,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        if process.stdout!=None: # check process output is not none (you should check if its and do some)
            for line in process.stdout:
                text_area.insert(tk.END, line)
                text_area.see(tk.END)
            process.stdout.close()
            process.wait()
            start_button.destroy()
            tk.Button(operations_window, text=lpak.get("finished", language), command=lambda: close_operations(operations_window)).pack(pady=5)

    def close_operations(win):
        win.destroy()
        after_operations()
    
    def after_operations():
        global install_status
        os.remove("actions.sh")
        global install_status, install_pacman_packages, remove_pacman_packages
        install_status = False
        start_operation_button.destroy()
        operation_list_label.destroy()
        install_pacman_packages.clear()
        remove_pacman_packages.clear()
        install_aur_packages.clear()
        remove_aur_packages.clear()
        #os.remove("start_commodo.sh")
        search_program(last_search)
    
    def start_thread_operations(operations_window, start_button):
        global install_status
        if install_status == True:
            messagebox.showinfo(lpak.get("an install instance is alredy in progress", language), lpak.get("an install instance is alredy in progress", language), parent=operations_window) 
            return
        threading.Thread(target=run_operations, args=(operations_window, start_button), daemon=True).start()
        install_status = True

    operations_window = tk.Toplevel(root)
    operations_window.title(lpak.get("star actions", language))
    operations_window.protocol("WM_DELETE_WINDOW", lambda: close_operations(operations_window))
    icon = tk.PhotoImage(file="icon.png")
    operations_window.iconphoto(False, icon)
    text_area = ScrolledText(operations_window, width=100, height=30)
    text_area.pack(padx=10, pady=10)
    start_button = tk.Button(operations_window, text=lpak.get("start actions", language))
    start_button.config(command=lambda: start_thread_operations(operations_window, start_button))
    start_button.pack(pady=5)

def download_program(program_name, repository, button, status):
    global start_operation_button, program_button_download, operation_list_label
    program_name=program_name.split(" ")[0]
    if repository == "aur":
        if status[0] == "Remove" or status[0] == "Do not install":
            if status[0] == "Remove":
                button.config(text=lpak.get("do not remove", language))
                status[0] = "Do not remove" 
                remove_aur_packages.append(program_name)                
            else:
                button.config(text=lpak.get("install", language)) 
                status[0] = "Install"    
                install_aur_packages.remove(program_name) 
        elif status[0] == "Install" or status[0] == "Do not remove":
            if status[0] == "Install":
                button.config(text=lpak.get("do not install", language))
                status[0] = "Do not install" 
                install_aur_packages.append(program_name)
            else:
                button.config(text=lpak.get("remove", language))
                status[0] = "Remove" 
                remove_aur_packages.remove(program_name)         
    elif repository == "flatpak":
        if status[0] == "Remove" or status[0] == "Do not install":
            if status[0] == "Remove":
                button.config(text=lpak.get("do not remove", language)) #lpak
                status[0] = "Do not remove"
                remove_flatpak_packages.append(program_name)
            else:
                button.config(text=lpak.get("install", language))
                status[0] = "Install" 
                install_flatpak_packages.remove(program_name)
        elif status[0] == "Install" or status[0] == "Do not remove":
            if status[0] == "Install":
                status[0] = "Do not install" 
                button.config(text=lpak.get("do not install", language))
                install_flatpak_packages.append(program_name)
            else:
                button.config(text=lpak.get("remove", language))
                status[0] = "Remove" 
                remove_flatpak_packages.remove(program_name)
    else:
        
        if status[0] == "Remove" or status[0] == "Do not install":
            if status[0] == "Remove":
                button.setText(text=lpak.get("do not remove", language))
                status[0] = "Do not remove"
                remove_pacman_packages.append(program_name)
            else:
                button.config(text=lpak.get("install", language)) 
                status[0] = "Install" 
                install_pacman_packages.remove(program_name)
                
        elif status[0] == "Install" or status[0] == "Do not remove":
            if status[0] == "Install":
                button.config(text=lpak.get("do not install", language))
                status[0] = "Do not install"
                install_pacman_packages.append(program_name)
            else:
                button.config(text=lpak.get("remove", language))
                status[0] = "Remove"
                remove_pacman_packages.remove(program_name)
        else:
            print("ERROR, Invalid status!\nin: download_program()")
            exit()
    if install_pacman_packages!=[] or remove_pacman_packages!=[] or install_aur_packages !=[] or remove_aur_packages!=[] or install_flatpak_packages != [] or remove_flatpak_packages!=[]:
        start_operation_button=tk.Button(text=lpak.get("start actions", language), command=lambda program_name=program_name:start_selectionated_operations(program_name))
        start_operation_button.grid(row=1, column=3)
        #generazione resocontio modifiche
        actions_text=""
        #pacman
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
            operation_list_label.destroy()
        except:
            pass
        operation_list_label = tk.Label(text=actions_text)
        operation_list_label.grid(row=4, column=3)
    else:
        start_operation_button.destroy()
        operation_list_label.destroy()
  

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
    search_bar.clear()
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

    # Pacman
    pacman_programs.clear()
    if setting_repo_pacman == "enable":
        pacman_programs = parse_pacman_output(os.popen(f"pacman -Ss {program_search}").read())

    # AUR
    aur_programs.clear()
    if setting_repo_aur == "enable":
        aur_output = os.popen(f"{aur_method} -Ssa {program_search}").read()
        aur_programs = parse_aur_output(aur_output)

    # Flatpak
    flatpak_programs.clear()
    if setting_repo_flatpak == "enable":
        flatpak_raw = os.popen(f"flatpak search {program_search}").read().replace("\t", "    ").split("\n")
        if flatpak_raw[-1] != "":
            flatpak_programs = flatpak_raw
        flatpak_installed_programs = os.popen("flatpak list").read().split("\n")

    # Pulizia layout prima di generare interfaccia
    for i in reversed(range(scrollable_layout.count())):
        widget_to_remove = scrollable_layout.itemAt(i).widget()
        if widget_to_remove:
            widget_to_remove.deleteLater()

    # Header tabella
    headers = ["actions", "programs",  "repository", "description"]
    for idx, key in enumerate(headers):
        header_label = pq.QLabel(lpak.get(key, language))
        header_label.setStyleSheet("font: bold 14pt 'Arial'; color: #004080")
        scrollable_layout.addWidget(header_label, 0, idx*2)

    row = 1

    def create_button(text, name, repo, status):
        btn = pq.QPushButton(text)
        btn.setStyleSheet(
            "background-color: #008000; color: white; font: bold 12pt 'Arial'; padding: 4px 8px; border-radius: 5px;"
        )
        btn.pressed.connect(lambda: download_program(name, repo, btn, status))
        return btn

    # Funzione generica per aggiungere programmi Pacman/AUR
    def add_programs_list(program_list, repo_type):
        nonlocal row
        for program in program_list:
            program_repository = program.split("/")[0]
            program_commodo = program.split("/")[1]
            program_name, program_description = program_commodo.split("|")

            program_button_download = create_button(
                lpak.get("install", language), program_name, program_repository, ["Install"]
            )

            scrollable_layout.addWidget(pq.QLabel(program_name), row, 2)
            scrollable_layout.addWidget(pq.QLabel(program_description), row, 6)
            scrollable_layout.addWidget(pq.QLabel(program_repository), row, 4)
            scrollable_layout.addWidget(program_button_download, row, 0)

            line = pq.QFrame()
            line.setFrameShape(pq.QFrame.Shape.HLine)
            line.setFrameShadow(pq.QFrame.Shadow.Sunken)
            scrollable_layout.addWidget(line, row + 1, 0, 1, 7)

            row += 2

    if setting_repo_pacman == "enable":
        add_programs_list(pacman_programs, "pacman")
    if setting_repo_aur == "enable":
        add_programs_list(aur_programs, "aur")

    # Flatpak - aggiunta separata per complessità parsing
    if setting_repo_flatpak == "enable":
        for program in flatpak_programs:
            parts = [p for p in program.split("  ") if p.strip()]
            if len(parts) < 4:
                continue
            program_name, program_description, program_id, program_version = parts[:4]
            program_button_download = create_button(
                lpak.get("install", language), program_id, "flatpak", ["Install"]
            )
            scrollable_layout.addWidget(pq.QLabel(f"{program_name} ({program_version})"), row, 2)
            scrollable_layout.addWidget(pq.QLabel(program_description), row, 6)
            scrollable_layout.addWidget(pq.QLabel("flatpak"), row, 4)
            scrollable_layout.addWidget(program_button_download, row, 0)

            line = pq.QFrame()
            line.setFrameShape(pq.QFrame.Shape.HLine)
            line.setFrameShadow(pq.QFrame.Shadow.Sunken)
            scrollable_layout.addWidget(line, row + 1, 0, 1, 7)
            row += 2

    search_label.setText(lpak.get("search", language))
    search_status = False

    if not pacman_programs and not aur_programs and not flatpak_programs:
        no_program_found_label = pq.QLabel(lpak.get("no program found", language))
        no_program_found_label.setStyleSheet("color: red; font: bold 14pt 'Arial'")
        scrollable_layout.addWidget(no_program_found_label, row, 0, 1, 6)
    

    last_search = program_search
while True:
    # Inizializzazione GUI
    app = pq.QApplication(sys.argv)
    root = pq.QMainWindow()
    root.setWindowTitle(lpak.get("arch store", language))
    root.setGeometry(400, 100, 1000, 800)

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

    # Scroll area per risultati
    scroll_area = pq.QScrollArea()
    scroll_area.setWidgetResizable(True)
    scrollable_frame = pq.QWidget()
    scrollable_layout = pq.QGridLayout(scrollable_frame)
    scroll_area.setWidget(scrollable_frame)
    main_layout.addWidget(scroll_area)

    root.show()
    sys.exit(app.exec())
    

       
    if language == actual_language:
        exit()
