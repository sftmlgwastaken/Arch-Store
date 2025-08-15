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

#fast access variables
avaible_languages = ["Italiano", "English"]

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


#Auto-set variables
working_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(working_dir)
user_name = getpass.getuser()

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
        global setting_repo_pacman, setting_repo_aur, setting_repo_flatpak, setting_aur_method, language, AppImagesDir
        with open("settings.conf", "r") as f:
            file_configuration_data = [line.rstrip('\n') for line in f.readlines()]
        setting_repo_pacman=file_configuration_data[0].split("=")[1]
        setting_repo_aur=file_configuration_data[1].split("=")[1]
        setting_repo_flatpak=file_configuration_data[2].split("=")[1]
        setting_aur_method=file_configuration_data[3].split("=")[1]
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

    settings_label_title = tk.Label(settings_page, text=lpak.get("settings", language))
    settings_label_repo = tk.Label(settings_page, text=lpak.get("enable disable repo", language))
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
    settings_label_title.grid(row=0, columnspan=2)
    button_reset_settings.grid(row=0, column = 3)
    settings_label_repo.grid(row=1, column=0)
    label_repo_pacman.grid(row=2, column=0)
    button_repo_pacman.grid(row=2, column=1)
    label_repo_aur.grid(row=3, column=0)
    button_repo_aur.grid(row=3, column=1)
    label_repo_flatpak.grid(row=4, column=0)
    button_repo_flatpak.grid(row=4, column=1)
    label_language.grid(row=5, column=0)
    menu_select_language.grid(row=5, column=1)
    button_language_confirm.grid(row=6, columnspan=1)
    appimagesdir_label.grid(row=7, column=0)
    appimagesdir_button.grid(row=7, column=1)
    #
    line_separazione.grid(column=0, row=9, columnspan=3, sticky='ew', pady=10)
    author_label.grid(column=0, row=10)
    project_link.grid(column=1, row=10)
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
                lpak.get("remotion completed", language),
                lpak.get("remotion completed", language),
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


#END OTHER#
###########

def update_all_apps():
    global install_status
    #Controlli vari
    if setting_repo_pacman == "disable" and setting_repo_aur == "disable" and setting_repo_flatpak == "disable":
        messagebox.showinfo(lpak.get("nothing enable", language), no_repo_error_text_default)
        return
    if install_status == True:
        messagebox.showinfo(lpak.get("an install instance is alredy in progress", language), lpak.get("an install instance is alredy in progress", language)) 
        return    
    #fine controlli
    with open("actions.sh", "w") as f:  #File dei comando per update
        f.write("#!/bin/bash")
        if setting_repo_pacman == "enable":
            f.write("\nsudo pacman -Syu --noconfirm")
        if setting_repo_aur == "enable":
            f.write("\nyay -Syu --noconfirm")
        if setting_repo_flatpak == "enable":
            f.write("\nflatpak upgrade --assumeyes")

    def run_update(update_window, start_button):
        global install_status
        os.chdir(working_dir)        
        command_update = ["pkexec", "bash", os.path.join(working_dir, "actions.sh")]
        process = subprocess.Popen(
            command_update,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )        
        for line in process.stdout:   # Leggi l'output riga per riga
            text_area.insert(tk.END, line)
            text_area.see(tk.END)
        process.stdout.close()
        process.wait()

        def destroy_update_window():
            update_window.destroy()
        start_button.destroy()
        exit_button = tk.Button(update_window, text=lpak.get("finished", language), command=destroy_update_window)
        exit_button.pack(pady=5)
        install_status = False

    def start_thread(update_window, start_button):
        global install_status
        if install_status == True:
            messagebox.showinfo(lpak.get("an install instance is alredy in progress", language), lpak.get("an install instance is alredy in progress", language)) 
            return
        threading.Thread(target=run_update, args=(update_window, start_button), daemon=True).start()  
        install_status = True      
    #GUI# 
    update_window = tk.Toplevel(root)
    update_window.title(lpak.get("update", language))
    icon = tk.PhotoImage(file="icon.png")
    update_window.iconphoto(False, icon)
    text_area = ScrolledText(update_window, width=100, height=30)
    text_area.pack(padx=10, pady=10)
    start_button = tk.Button(update_window, text=lpak.get("start update", language))
    start_button.config(command=lambda: start_thread(update_window, start_button))
    start_button.pack(pady=5)
    update_window.mainloop()    
    os.remove("actions.sh")
    install_status = False
    
def start_selectionated_operations(program_name):
    global start_operation_button, operation_list_label, install_pacman_packages, remove_pacman_packages, install_aur_packages, remove_aur_packages, install_flatpak_packages, remove_flatpak_packages, install_status
    if install_status == True:
        tk.messagebox.Message(text=lpak.get("an install instance is alredy in progress", language))
        return
    install_status = True
    #pacman
    if install_pacman_packages != []:
        install_pacman_command = "sudo pacman -S "
        for package in install_pacman_packages:
            install_pacman_command=install_pacman_command+package+" "
    else:
        install_pacman_command = "echo "+lpak.get("no pacman install actions", language)
    if remove_pacman_packages != []:
        remove_pacman_command = "sudo pacman -Rn "
        for package in remove_pacman_packages:
            remove_pacman_command = remove_pacman_command+package+" "
    else:
        remove_pacman_command = "echo "+lpak.get("no pacman remove actions", language)
    #aur
    if install_aur_packages != []:
        install_aur_command = "yay -S "
        for package in install_aur_packages:
            install_aur_command = install_aur_command+package+" "
    else:
        install_aur_command = "echo "+lpak.get("no install aur actions", language)
    if remove_aur_packages != []:
        remove_aur_command = "yay -Rn "
        for package in remove_aur_packages:
            remove_aur_command = remove_aur_command + package+" "
    else:
        remove_aur_command = "echo "+lpak.get("no remove aur actions", language)
    #flatpak
    if install_flatpak_packages != []:
        install_flatpak_command = "flatpak install "
        for package in install_flatpak_packages:
            install_flatpak_command = install_flatpak_command+package
    else:
        install_flatpak_command = "echo "+lpak.get("no install flatpak actions", language)
    if remove_flatpak_packages != []:
        remove_flatpak_command = "flatpak remove "
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
            messagebox.showinfo(lpak.get("an install instance is alredy in progress", language), lpak.get("an install instance is alredy in progress", language)) 
            return
        threading.Thread(target=run_operations, args=(operations_window, start_button), daemon=True).start()
        install_status == True

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
                button.config(text=lapk.get("do not remove", language))
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
                button.config(text=lpak.get("do not remove", language))
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
  
def search_program(name):
    global program_button_download, search_status, last_search, no_program_found_label
    try:
        no_program_found_label.destroy()
    except:
        pass        
    if setting_repo_pacman == "disable" and setting_repo_aur == "disable" and setting_repo_flatpak == "disable":
        label_error_no_repo_enable = tk.Label(text=no_repo_error_text_default)
        label_error_no_repo_enable.grid(row=3, columnspan=4)
        return
    if search_status == True:
        return
    search_status = True
    #Clean screen
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    #Search Programs
    programs_commodo=[]
    if name == " ":
        program_search = search_bar.get('1.0', 'end-1c')
        search_bar.delete('1.0', 'end-1c')
    else:
        program_search = name
    if program_search == "":
        error_label_textbox_empty=tk.Label(scrollable_frame, text=lpak.get("so you're looking for nothing", language), font='Helvetica 18 bold')
        error_label_textbox_empty.grid(row=3, column=4)
        return
    program_search = program_search.replace("\n", "")
    search_label.config(text=lpak.get("i'm looking for", language)+" "+program_search+"...")
    root.update()    
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
    #yay
    if setting_repo_aur == "enable":
        programs_commodo.clear()
        if name == " ":
            pass
        else:
            program_search = name
        command = "yay -Ssa "+program_search
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
    program_search_label1=tk.Label(scrollable_frame, text=lpak.get("programs", language), font=("bold"))
    program_search_label2=tk.Label(scrollable_frame, text=lpak.get("description", language), font=("bold"))
    program_search_label3=tk.Label(scrollable_frame, text=lpak.get("repository", language), font=("bold"))
    program_search_label4=tk.Label(scrollable_frame, text=lpak.get("actions", language), font=("bold"))
    #
    program_search_label1.grid(row=3, column=2, sticky="w")#programs
    program_search_label2.grid(row=3, column=6, sticky="w")#Description
    program_search_label3.grid(row=3, column=4, sticky="w")#Repository
    program_search_label4.grid(row=3, column=0)#Actions
    #Generate download data
    row = 4
    if setting_repo_pacman == "enable":
        for program in pacman_programs:
            program_repository = program.split("/")[0]
            program_commodo = program.split("/")[1]
            program_name = program_commodo.split("|")[0]
            program_description = program_commodo.split("|")[1]
            program_name_label = tk.Label(scrollable_frame, text=program_name)
            program_description_label = tk.Label(scrollable_frame, text=program_description)
            program_repository_label = tk.Label(scrollable_frame, text=program_repository)
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
            program_button_download = tk.Button(scrollable_frame, text=button_download_text)
            program_button_download.config(command=lambda name=program_name, repository=program_repository, button=program_button_download, stat=status: download_program(name, repository, button, stat))
            #
            program_name_label.grid(row=row, column=2, sticky="w")
            program_description_label.grid(row=row, column=6, sticky="w")
            program_repository_label.grid(row=row, column=4, sticky="w")
            program_button_download.grid(row=row, column=0)
            #
            line_separazione = ttk.Separator(scrollable_frame, orient="horizontal")
            line_separazione.grid(column=0, row=row+1, columnspan=7, sticky='ew', pady=10)
            #
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
            if not "No matches found ( )" in program_name:
                program_name_label=tk.Label(scrollable_frame, text=program_name)
                program_repository_label=tk.Label(scrollable_frame, text=program_repository)
                program_description_label=tk.Label(scrollable_frame, text=program_description)
                program_button_download = tk.Button(scrollable_frame, text=button_download_text)
                program_button_download.config(command=lambda name=program_id, repository="flatpak", button=program_button_download, stat=status: download_program(name, repository, button, stat))
                #        
                program_name_label.grid(row=row, column=2, sticky="w")
                program_description_label.grid(row=row, column=6, sticky="w")
                program_repository_label.grid(row=row, column=4, sticky="w")
                program_button_download.grid(row=row, column=0)
                #
                line_separazione = ttk.Separator(scrollable_frame, orient="horizontal")
                line_separazione.grid(column=0, row=row+1, columnspan=7, sticky='ew', pady=10)
                #
                row = row + 2 
    if setting_repo_aur == "enable":
        for program in aur_programs:
            program_repository = program.split("/")[0]
            program_commodo = program.split("/")[1]
            program_name = program_commodo.split("|")[0]
            program_description = program_commodo.split("|")[1]
            program_name_label = tk.Label(scrollable_frame, text=program_name)
            program_description_label = tk.Label(scrollable_frame, text=program_description)
            program_repository_label = tk.Label(scrollable_frame, text=program_repository)
            test = program_name.split("(")
            try:
                test = test[2]
                button_download_text=lpak.get("remove", language)
                status = ["Remove"]
            except:
                button_download_text=lpak.get("install", language)
                status = ["Install"]
            program_button_download = tk.Button(scrollable_frame, text=button_download_text)
            program_button_download.config(command=lambda name=program_name, repository=program_repository, button=program_button_download, stat=status: download_program(name, repository, button, stat))
            #            
            program_name_label.grid(row=row, column=2, sticky="w")
            program_description_label.grid(row=row, column=6, sticky="w")
            program_repository_label.grid(row=row, column=4, sticky="w")
            program_button_download.grid(row=row, column=0)
            #
            line_separazione = ttk.Separator(scrollable_frame, orient="horizontal")
            line_separazione.grid(column=0, row=row+1, columnspan=7, sticky='ew', pady=10)
            #
            row = row + 2 
    #END RESEARCH
    search_label.config(text=lpak.get("search", language))
    search_status = False
    #
    vertical_line_action=ttk.Separator(scrollable_frame, orient="vertical")
    vertical_line_action.grid(column=1, row=3, rowspan=row-1, sticky='ns')
    vertical_line_programs=ttk.Separator(scrollable_frame, orient="vertical")
    vertical_line_programs.grid(column=3, row=3, rowspan=row-1, sticky='ns')
    vertical_line_repo=ttk.Separator(scrollable_frame, orient="vertical")
    vertical_line_repo.grid(column=5, row=3, rowspan=row-1, sticky='ns')
    #
    if pacman_programs == [] and flatpak_programs == ['No matches found'] and aur_programs == []:
        no_program_found_label = tk.Label(text=lpak.get("no program found", language))
        no_program_found_label.grid(columnspan=4, row=row)
    last_search = program_search

while True:
    actual_language = language
    #Config finestra
    root = tk.Tk()
    root.geometry("2000x1000")
    root.minsize(1310, 700)
    root.grid_rowconfigure(4, weight=1)   
    root.grid_columnconfigure(0, weight=1)
    root.title(lpak.get("arch store",language))
    icon = tk.PhotoImage(file="icon.png")
    root.iconphoto(False, icon)
    #Scrollable
    container = tk.Frame(root)
    container.grid(row=4, column=0, columnspan=3, sticky="nsew")
    canvas = tk.Canvas(container)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    #Obgect
    search_label=tk.Label(text=lpak.get("search for software", language))
    search_bar = tk.Text(height=1)
    search_button = tk.Button(text=lpak.get("search", language), command=lambda name=" ": search_program(name))
    update_button = tk.Button(text=lpak.get("update system", language), command=update_all_apps)
    ####setting_button = tk.Button(text=lpak.get("settings", language), command=open_setting)
    other_button = tk.Button(text=lpak.get("other", language), command=open_other)
    # focus sulla barra di ricerca all'avvio
    search_bar.focus_set()
    # binding tasto Invio per ricerca
    def on_search_enter(event):
        search_program(" ")
    search_bar.bind("<Return>", on_search_enter)
    #position
    search_label.grid(column=0, row=1, sticky="w")
    search_bar.grid(column=1, row=1, sticky="w")
    search_button.grid(column=0, row=2, sticky="w")
    update_button.grid(column=2, row=1, sticky="e")
    ####setting_button.grid(column=2, row=2, sticky="e")
    other_button.grid(column=2, row=2, sticky="e")
    #
    root.mainloop()        
    if language == actual_language:
        exit()