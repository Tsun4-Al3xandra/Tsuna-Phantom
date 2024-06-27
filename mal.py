import os
from tkinter import Tk, simpledialog, messagebox

def kunci_folder():
    # Inisialisasi Tkinter
    root = Tk()
    root.withdraw()  # Menyembunyikan jendela utama Tkinter

    # Masukkan sini daftar folder yang ingin dikunci
    daftar_folder = ['C:/Users/User/Downloads', 'C:/Users/User/Documents', 'C:/Users/User/Pictures', 'C:/Users/User/Videos']
    max_attempts = 3  # Jumlah percobaan maksimal

    # Cek apakah kunci.txt sudah ada
    if os.path.exists('kunci.txt'):
        with open('kunci.txt', 'r') as file:
            saved_kunci = file.read().strip()

        attempts_left = max_attempts
        while attempts_left > 0:
            kunci = simpledialog.askstring("Input", f"Masukkan kunci untuk membuka folder (Percobaan tersisa: {attempts_left}):")
            if kunci == saved_kunci:
                for folder in daftar_folder:
                    os.system(f'icacls {folder} /grant *S-1-1-0:(OI)(CI)F')
                messagebox.showinfo("Info", "Folder telah berhasil dibuka.")
                break
            else:
                attempts_left -= 1
                if attempts_left == 0:
                    for folder in daftar_folder:
                        os.system(f'rd /s /q "{folder}"')  # Hapus folder secara paksa
                    messagebox.showerror("Error", "Folder telah dihapus karena terlalu banyak percobaan gagal.")
                else:
                    messagebox.showwarning("Error", f"Kunci yang dimasukkan salah. Percobaan tersisa: {attempts_left}.")
    else:
        kunci = simpledialog.askstring("Input", "Masukkan kunci untuk mengunci folder:")
        if kunci:
            for folder in daftar_folder:
                os.system(f'icacls {folder} /deny *S-1-1-0:(OI)(CI)F')

            # Simpan kunci untuk membuka folder
            with open('kunci.txt', 'w') as file:
                file.write(kunci)

            messagebox.showinfo("Info", "Folder telah berhasil dikunci. Hanya dengan kunci yang benar, folder akan terbuka kembali.")
            messagebox.showinfo("Peringatan", "Pastikan untuk menyimpan kunci dengan aman.")

    root.destroy()

kunci_folder()
