import json
import re
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import os

# ------------------------------
# File handler untuk akun - DIPERBAIKI
# ------------------------------
class AccountHandler:
    ACCOUNT_FILE = "akun_mahasiswa.json"
    
    @staticmethod
    def baca_akun():
        """Membaca dan memperbaiki data akun dari file JSON"""
        try:
            # Cek apakah file ada
            if not os.path.exists(AccountHandler.ACCOUNT_FILE):
                print("📄 File akun tidak ditemukan, membuat akun default...")
                return AccountHandler.buat_akun_default()
            
            with open(AccountHandler.ACCOUNT_FILE, "r", encoding="utf-8") as file:
                akun = json.load(file)
                print(f"📁 Data akun dibaca: {list(akun.keys())}")
                
                # Cek dan perbaiki struktur data
                perlu_perbaikan = False
                akun_diperbaiki = {}
                
                for username, data in akun.items():
                    if isinstance(data, dict) and "password" in data:
                        # Data sudah benar
                        akun_diperbaiki[username] = data
                    else:
                        # Data perlu diperbaiki
                        print(f"⚠️  Memperbaiki struktur akun untuk: {username}")
                        perlu_perbaikan = True
                        
                        if isinstance(data, str):
                            # Jika data adalah string (password lama)
                            password = data
                        elif isinstance(data, dict):
                            # Jika ada field password tapi tidak sesuai
                            password = data.get("password", "default123")
                        else:
                            password = "default123"
                        
                        akun_diperbaiki[username] = {
                            "password": password,
                            "role": "user" if username != "admin" else "admin",
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                
                # Simpan jika perlu perbaikan
                if perlu_perbaikan:
                    print("💾 Menyimpan data akun yang telah diperbaiki...")
                    AccountHandler.simpan_akun(akun_diperbaiki)
                
                return akun_diperbaiki
                
        except json.JSONDecodeError as e:
            print(f"❌ Error JSON: {e}, membuat akun default...")
            return AccountHandler.buat_akun_default()
        except Exception as e:
            print(f"❌ Error membaca akun: {e}, membuat akun default...")
            return AccountHandler.buat_akun_default()
    
    @staticmethod
    def buat_akun_default():
        """Membuat akun default"""
        akun_default = {
            "admin": {
                "password": "1234", 
                "role": "admin", 
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "dzaki ramadhan": {
                "password": "141005", 
                "role": "user", 
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        AccountHandler.simpan_akun(akun_default)
        return akun_default
    
    @staticmethod
    def simpan_akun(data):
        """Menyimpan data akun ke file JSON"""
        try:
            with open(AccountHandler.ACCOUNT_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            print("✅ Data akun berhasil disimpan")
        except Exception as e:
            print(f"❌ Error menyimpan akun: {e}")
    
    @staticmethod
    def tambah_akun(username, password, role="user"):
        """Menambahkan akun baru"""
        akun = AccountHandler.baca_akun()
        akun[username.lower()] = {
            "password": password,
            "role": role,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        AccountHandler.simpan_akun(akun)

# ------------------------------
# Model: Mahasiswa
# ------------------------------
class Mahasiswa:
    def __init__(self, nama, nim, prodi):
        self.__nama = nama
        self.__nim = nim
        self.__prodi = prodi

    def get_nama(self): return self.__nama
    def get_nim(self): return self.__nim
    def get_prodi(self): return self.__prodi

    def set_nama(self, nama): self.__nama = nama
    def set_prodi(self, prodi): self.__prodi = prodi

    def to_dict(self):
        return {"nama": self.__nama, "nim": self.__nim, "prodi": self.__prodi}

# ------------------------------
# File handler untuk data mahasiswa
# ------------------------------
class FileHandler:
    FILE_NAME = "data_mahasiswa.json"

    @staticmethod
    def baca_data():
        try:
            if not os.path.exists(FileHandler.FILE_NAME):
                print("📄 File data mahasiswa tidak ditemukan, akan dibuat otomatis")
                return []
                
            with open(FileHandler.FILE_NAME, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Mahasiswa(d["nama"], d["nim"], d["prodi"]) for d in data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"❌ Error membaca file JSON: {e}")
            return []
        except Exception as e:
            print(f"❌ Error membaca data: {e}")
            return []

    @staticmethod
    def simpan_data(data):
        # data: list of Mahasiswa
        try:
            with open(FileHandler.FILE_NAME, "w", encoding="utf-8") as file:
                json.dump([m.to_dict() for m in data], file, indent=4, ensure_ascii=False)
            print("✅ Data mahasiswa berhasil disimpan")
        except Exception as e:
            print(f"❌ Error menyimpan data: {e}")

# ------------------------------
# Sorting strategies (operate on list of Mahasiswa)
# ------------------------------
class Sorting:
    def sort(self, data): 
        return data

class BubbleSort(Sorting):
    def sort(self, data):
        arr = data[:]
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j].get_nim() > arr[j + 1].get_nim():
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

class SelectionSort(Sorting):
    def sort(self, data):
        arr = data[:]
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if arr[j].get_nim() < arr[min_idx].get_nim():
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

class InsertionSort(Sorting):
    def sort(self, data):
        arr = data[:]
        for i in range(1, len(arr)):
            key = arr[i]
            j = i-1
            while j >= 0 and arr[j].get_nim() > key.get_nim():
                arr[j+1] = arr[j]
                j -= 1
            arr[j+1] = key
        return arr

class MergeSort(Sorting):
    def sort(self, data):
        if len(data) <= 1:
            return data[:]
        mid = len(data)//2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        return self.merge(left, right)

    def merge(self, left, right):
        result = []
        left = left[:]
        right = right[:]
        while left and right:
            if left[0].get_nim() < right[0].get_nim():
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        return result + left + right

# ------------------------------
# Login System (FULL SCREEN) - DIPERBAIKI
# ------------------------------
class LoginSystem:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        
        # Set full screen
        self.root.title("SISTEM LOGIN - APLIKASI MANAJEMEN DATA MAHASISWA")
        try:
            self.root.state("zoomed")
        except:
            pass
        self.root.configure(bg="#1a1a2e")
        
        self.show_login()

    def show_login(self):
        """Menampilkan form login full screen"""
        self.clear_frame()
        
        # Main container
        main_container = tk.Frame(self.root, bg="#1a1a2e")
        main_container.pack(fill="both", expand=True, padx=100, pady=50)
        
        # Left Panel (Tugas)
        left_panel = tk.Frame(main_container, bg="#0f3460", width=400)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Title di kiri
        title_frame = tk.Frame(left_panel, bg="#0f3460")
        title_frame.pack(expand=True)
        
        tk.Label(title_frame, 
                text="💻", 
                font=("Arial", 60),
                bg="#0f3460",
                fg="white").pack(pady=(0, 10))
        
        tk.Label(title_frame, 
                text="TUGAS ALGORITMA", 
                font=("Arial", 20, "bold"),
                bg="#0f3460",
                fg="white").pack()
        
        tk.Label(title_frame, 
                text="PEMROGRAMAN II", 
                font=("Arial", 18, "bold"),
                bg="#0f3460",
                fg="#4cc9f0").pack(pady=(5, 10))
        
        tk.Label(title_frame, 
                text="Universitas Pamulang", 
                font=("Arial", 14),
                bg="#0f3460",
                fg="#b8c6db").pack(pady=(5, 30))
        
        # Deskripsi tugas
        tugas_text = """
Buatlah sebuah aplikasi "Manajemen Data Mahasiswa" 
berbasis teks (console) atau GUI sederhana yang 
minimal mencakup fitur berikut:

✓ Input, edit, hapus, dan tampilkan data mahasiswa 
  (menggunakan array, pointer, fungsi).

✓ Penyimpanan dan pembacaan data dari file 
  (File I/O).

✓ Penerapan konsep OOP (class, objek, enkapsulasi, 
  pewarisan, polimorfisme).

✓ Fitur pencarian data (Linear Search, Binary 
  Search, Sequential Search).

✓ Fitur pengurutan data (Insertion, Selection, 
  Merge, Bubble, Shell Sort → minimal 2).

✓ Validasi input menggunakan Regular Expression 
  (Regex).

✓ Penanganan error menggunakan Try–Catch & 
  Exception.

✓ Estimasi Time Complexity untuk beberapa fitur 
  utama.

✓ Guidelines & Best Practices (penamaan variabel, 
  modularisasi kode, komentar).
"""
        
        tugas_label = tk.Label(left_panel, 
                              text=tugas_text, 
                              font=("Arial", 10),
                              bg="#0f3460",
                              fg="white",
                              justify="left",
                              anchor="w")
        tugas_label.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Right Panel (Login Form)
        right_panel = tk.Frame(main_container, bg="#16213e", width=400)
        right_panel.pack(side="right", fill="both", expand=True)
        right_panel.pack_propagate(False)
        
        # Form container
        form_container = tk.Frame(right_panel, bg="#16213e")
        form_container.pack(expand=True, padx=50, pady=50)
        
        # Title form
        tk.Label(form_container, 
                text="MASUK KE SISTEM", 
                font=("Arial", 28, "bold"),
                bg="#16213e",
                fg="#4cc9f0").pack(pady=(0, 30))
        
        # Username field
        tk.Label(form_container, 
                text="USERNAME", 
                font=("Arial", 11, "bold"),
                bg="#16213e",
                fg="#b8c6db",
                anchor="w").pack(fill="x", pady=(10, 5))
        
        username_frame = tk.Frame(form_container, bg="#1a1a2e", height=45)
        username_frame.pack(fill="x", pady=(0, 15))
        username_frame.pack_propagate(False)
        
        tk.Label(username_frame, 
                text="👤", 
                font=("Arial", 14),
                bg="#1a1a2e",
                fg="white").pack(side="left", padx=(15, 10))
        
        self.username_entry = tk.Entry(username_frame, 
                                      font=("Arial", 12),
                                      bg="#1a1a2e",
                                      fg="white",
                                      insertbackground="white",
                                      relief="flat",
                                      width=25)
        self.username_entry.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        # Password field
        tk.Label(form_container, 
                text="PASSWORD", 
                font=("Arial", 11, "bold"),
                bg="#16213e",
                fg="#b8c6db",
                anchor="w").pack(fill="x", pady=(10, 5))
        
        password_frame = tk.Frame(form_container, bg="#1a1a2e", height=45)
        password_frame.pack(fill="x", pady=(0, 25))
        password_frame.pack_propagate(False)
        
        tk.Label(password_frame, 
                text="🔒", 
                font=("Arial", 14),
                bg="#1a1a2e",
                fg="white").pack(side="left", padx=(15, 10))
        
        self.password_entry = tk.Entry(password_frame, 
                                      font=("Arial", 12),
                                      bg="#1a1a2e",
                                      fg="white",
                                      insertbackground="white",
                                      relief="flat",
                                      show="•",
                                      width=25)
        self.password_entry.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        # Toggle password visibility
        self.show_password_var = tk.BooleanVar()
        show_password_check = tk.Checkbutton(password_frame,
                                             text="👁",
                                             variable=self.show_password_var,
                                             command=self.toggle_password_visibility,
                                             bg="#1a1a2e",
                                             fg="white",
                                             selectcolor="#1a1a2e",
                                             activebackground="#1a1a2e",
                                             activeforeground="white",
                                             relief="flat",
                                             cursor="hand2")
        show_password_check.pack(side="right", padx=(0, 10))
        
        # Login button
        login_btn = tk.Button(form_container,
                             text="🚀 LOGIN SEKARANG",
                             font=("Arial", 13, "bold"),
                             bg="#4cc9f0",
                             fg="white",
                             padx=30,
                             pady=12,
                             relief="raised",
                             borderwidth=0,
                             cursor="hand2",
                             activebackground="#3aa8d8",
                             activeforeground="white",
                             command=self.login)
        login_btn.pack(fill="x", pady=(10, 15))
        
        # Register button
        register_btn = tk.Button(form_container,
                                text="📝 BUAT AKUN BARU",
                                font=("Arial", 11),
                                bg="#9b59b6",
                                fg="white",
                                padx=30,
                                pady=10,
                                relief="raised",
                                borderwidth=0,
                                cursor="hand2",
                                activebackground="#8e44ad",
                                activeforeground="white",
                                command=self.show_register)
        register_btn.pack(fill="x", pady=(5, 0))
        
        # Info akun default
        info_frame = tk.Frame(form_container, bg="#16213e")
        info_frame.pack(fill="x", pady=(30, 0))
        
        tk.Label(info_frame, 
                text="🔑 Akun Demo:", 
                font=("Arial", 9),
                bg="#16213e",
                fg="#888").pack(side="left")
        
        demo_frame = tk.Frame(info_frame, bg="#16213e")
        demo_frame.pack(side="left", padx=(5, 0))
        
        tk.Label(demo_frame, 
                text="admin / 1234", 
                font=("Arial", 9, "bold"),
                bg="#16213e",
                fg="#4cc9f0").pack(side="left")
        
        tk.Label(demo_frame, 
                text=" • ", 
                font=("Arial", 9),
                bg="#16213e",
                fg="#888").pack(side="left")
        
        tk.Label(demo_frame, 
                text="dzaki ramadhan / 141005", 
                font=("Arial", 9, "bold"),
                bg="#16213e",
                fg="#4cc9f0").pack(side="left")
        
        # Footer
        footer = tk.Frame(right_panel, bg="#0f3460", height=40)
        footer.pack(side="bottom", fill="x")
        footer.pack_propagate(False)
        
        tk.Label(footer, 
                text=f"© {datetime.now().year} Universitas Pamulang • Algoritma Pemrograman II • Versi 2.0", 
                font=("Arial", 9),
                bg="#0f3460",
                fg="#b8c6db").pack(pady=10)
        
        # Bind Enter key untuk login
        self.username_entry.bind("<Return>", lambda e: self.login())
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Focus ke username entry
        self.username_entry.focus_set()
        
        print("✅ Login screen loaded")
    
    def toggle_password_visibility(self):
        """Toggle visibility password"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")
    
    def show_register(self):
        """Menampilkan form registrasi full screen"""
        self.clear_frame()
        
        # Main container
        main_container = tk.Frame(self.root, bg="#1a1a2e")
        main_container.pack(fill="both", expand=True, padx=100, pady=50)
        
        # Back button
        back_frame = tk.Frame(main_container, bg="#1a1a2e")
        back_frame.pack(fill="x", pady=(0, 20))
        
        back_btn = tk.Button(back_frame,
                            text="◀ KEMBALI KE LOGIN",
                            font=("Arial", 10, "bold"),
                            bg="#9b59b6",
                            fg="white",
                            padx=20,
                            pady=8,
                            relief="raised",
                            borderwidth=0,
                            cursor="hand2",
                            activebackground="#8e44ad",
                            activeforeground="white",
                            command=self.show_login)
        back_btn.pack(side="left")
        
        # Register form container
        form_container = tk.Frame(main_container, bg="#16213e")
        form_container.pack(expand=True, padx=200, pady=50)
        
        # Title
        tk.Label(form_container, 
                text="BUAT AKUN BARU", 
                font=("Arial", 28, "bold"),
                bg="#16213e",
                fg="#4cc9f0").pack(pady=(0, 40))
        
        # Form fields
        fields = [
            ("👤 USERNAME", "username_reg"),
            ("🔒 PASSWORD", "password_reg"),
            ("✅ KONFIRMASI PASSWORD", "password_confirm")
        ]
        
        self.entries = {}
        
        for i, (label_text, var_name) in enumerate(fields):
            tk.Label(form_container, 
                    text=label_text, 
                    font=("Arial", 11, "bold"),
                    bg="#16213e",
                    fg="#b8c6db",
                    anchor="w").pack(fill="x", pady=(20 if i == 0 else 15, 5))
            
            entry_frame = tk.Frame(form_container, bg="#1a1a2e", height=45)
            entry_frame.pack(fill="x", pady=(0, 10))
            entry_frame.pack_propagate(False)
            
            show = "" if "PASSWORD" not in label_text else "•"
            entry = tk.Entry(entry_frame, 
                           font=("Arial", 12),
                           bg="#1a1a2e",
                           fg="white",
                           insertbackground="white",
                           relief="flat",
                           show=show,
                           width=30)
            entry.pack(side="left", fill="both", expand=True, padx=15)
            
            self.entries[var_name] = entry
        
        # Register button
        register_btn = tk.Button(form_container,
                                text="✅ DAFTAR SEKARANG",
                                font=("Arial", 13, "bold"),
                                bg="#2ecc71",
                                fg="white",
                                padx=30,
                                pady=12,
                                relief="raised",
                                borderwidth=0,
                                cursor="hand2",
                                activebackground="#27ae60",
                                activeforeground="white",
                                command=self.register)
        register_btn.pack(fill="x", pady=(30, 10))
        
        # Rules
        rules_frame = tk.Frame(form_container, bg="#16213e")
        rules_frame.pack(fill="x", pady=(20, 0))
        
        rules = [
            "• Username minimal 3 karakter",
            "• Password minimal 4 karakter",
            "• Username harus unik",
            "• Password harus sama dengan konfirmasi"
        ]
        
        for rule in rules:
            tk.Label(rules_frame, 
                    text=rule, 
                    font=("Arial", 9),
                    bg="#16213e",
                    fg="#888",
                    anchor="w").pack(fill="x", pady=2)
        
        print("✅ Register screen loaded")
    
    def register(self):
        """Fungsi untuk registrasi akun baru"""
        print("🔧 Register function called")
        
        username = self.entries["username_reg"].get().strip()
        password = self.entries["password_reg"].get().strip()
        password_confirm = self.entries["password_confirm"].get().strip()
        
        # Validasi input
        if not username or not password or not password_confirm:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return
        
        if len(username) < 3:
            messagebox.showerror("Error", "Username minimal 3 karakter!")
            return
        
        if len(password) < 4:
            messagebox.showerror("Error", "Password minimal 4 karakter!")
            return
        
        if password != password_confirm:
            messagebox.showerror("Error", "Password dan konfirmasi password tidak cocok!")
            return
        
        # Cek apakah username sudah terdaftar
        akun = AccountHandler.baca_akun()
        if username.lower() in akun:
            messagebox.showerror("Error", f"Username '{username}' sudah terdaftar!")
            return
        
        # Simpan akun baru
        AccountHandler.tambah_akun(username.lower(), password)
        
        messagebox.showinfo("Success", "🎉 Akun berhasil dibuat!\nSilakan login dengan akun baru Anda.")
        self.show_login()
    
    def login(self):
        """Fungsi untuk proses login - DIPERBAIKI"""
        print("\n" + "="*50)
        print("🔧 Login function called")
        
        username = self.username_entry.get().strip().lower()
        password = self.password_entry.get().strip()
        
        print(f"🔧 Username entered: {username}")
        print(f"🔧 Password entered: {'*' * len(password)}")
        
        # Validasi input
        if not username or not password:
            messagebox.showerror("Error", "Username dan Password harus diisi!")
            return
        
        # Baca data akun
        try:
            akun = AccountHandler.baca_akun()
            print(f"🔧 Accounts in system: {list(akun.keys())}")
            print(f"🔧 Checking account for: {username}")
            
            # Cek apakah username ada
            if username in akun:
                account_data = akun[username]
                print(f"🔧 Found account: {type(account_data)} - {account_data}")
                
                # Cek tipe data
                if isinstance(account_data, dict):
                    if "password" in account_data:
                        stored_password = account_data["password"]
                        print(f"🔧 Stored password: {stored_password}")
                        print(f"🔧 Entered password: {password}")
                        
                        if stored_password == password:
                            role = account_data.get("role", "user")
                            print(f"✅ Password match! Role: {role}")
                            
                            messagebox.showinfo("Success", 
                                              f"✅ Login berhasil!\nSelamat datang, {username.title()} ({role})")
                            
                            # Panggil callback function
                            if self.on_login_success:
                                print("✅ Calling on_login_success callback")
                                # Gunakan after untuk mencegah masalah event loop
                                self.root.after(100, lambda: self.on_login_success(username))
                            else:
                                print("❌ Error: on_login_success callback is None")
                            return
                        else:
                            print("❌ Password tidak cocok")
                    else:
                        print("❌ Account data missing 'password' field")
                else:
                    print(f"❌ Invalid account data type: {type(account_data)}")
                    print("⚠️  Account data needs to be a dictionary")
            else:
                print(f"❌ Username '{username}' not found in accounts")
            
            # Jika sampai di sini, login gagal
            messagebox.showerror("Error", "❌ Username atau Password salah!")
            self.password_entry.delete(0, tk.END)  # Clear password field
            self.password_entry.focus_set()
            print("❌ Login failed")
            
        except Exception as e:
            print(f"❌ Error during login: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Terjadi kesalahan sistem: {str(e)}")
    
    def clear_frame(self):
        """Membersihkan semua widget di root"""
        for widget in self.root.winfo_children():
            widget.destroy()

# ------------------------------
# Main App (Setelah Login)
# ------------------------------
class AppMahasiswa:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"APLIKASI MANAJEMEN DATA MAHASISWA - Universitas Pamulang")
        
        # Set full screen
        try:
            self.root.state("zoomed")
        except:
            pass
        
        self.root.configure(bg="#f0f2f5")
        
        # Load data
        self.data = FileHandler.baca_data()

        # Variables
        self.nama_var = tk.StringVar()
        self.nim_var = tk.StringVar()
        self.prodi_var = tk.StringVar()
        self.filter_prodi_var = tk.StringVar()

        self.setup_ui()

    def setup_ui(self):
        """Setup UI dengan menu yang lebih keliatan"""
        # HEADER
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        
        # Logo dan judul
        title_frame = tk.Frame(header_frame, bg="#2c3e50")
        title_frame.pack(side="left", padx=20)
        
        tk.Label(title_frame, 
                text="🎓", 
                font=("Arial", 32),
                bg="#2c3e50",
                fg="white").pack(side="left")
        
        title_text = tk.Frame(title_frame, bg="#2c3e50")
        title_text.pack(side="left", padx=10)
        
        tk.Label(title_text, 
                text="UNIVERSITAS PAMULANG", 
                font=("Arial", 16, "bold"),
                bg="#2c3e50",
                fg="white").pack(anchor="w")
        
        tk.Label(title_text, 
                text="Algoritma Pemrograman II | Sistem Data Mahasiswa", 
                font=("Arial", 10),
                bg="#2c3e50",
                fg="#ecf0f1").pack(anchor="w")
        
        # User info dan logout
        user_frame = tk.Frame(header_frame, bg="#2c3e50")
        user_frame.pack(side="right", padx=20)
        
        tk.Label(user_frame, 
                text=f"👤 {self.username.title()}", 
                font=("Arial", 11, "bold"),
                bg="#2c3e50",
                fg="#ecf0f1").pack(side="left", padx=(0, 15))
        
        logout_btn = tk.Button(user_frame,
                              text="🚪 LOGOUT",
                              font=("Arial", 10, "bold"),
                              bg="#e74c3c",
                              fg="white",
                              padx=15,
                              pady=5,
                              relief="raised",
                              cursor="hand2",
                              activebackground="#c0392b",
                              activeforeground="white",
                              command=self.logout)
        logout_btn.pack(side="left")
        
        # MAIN NOTEBOOK (TAB MENU)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Styling untuk notebook
        style = ttk.Style()
        style.configure("TNotebook", background="#2c3e50")
        style.configure("TNotebook.Tab", 
                       font=("Arial", 11, "bold"),
                       padding=[15, 5],
                       background="#34495e",
                       foreground="white")
        style.map("TNotebook.Tab",
                 background=[("selected", "#4cc9f0")])
        
        # TAB 1: Data Mahasiswa
        data_frame = tk.Frame(notebook, bg="#f8f9fa")
        notebook.add(data_frame, text="📋 DATA MAHASISWA")
        
        # Form Input di tab 1
        form_frame = tk.LabelFrame(data_frame, 
                                  text="FORM INPUT DATA MAHASISWA",
                                  font=("Arial", 12, "bold"),
                                  bg="#ffffff",
                                  padx=20,
                                  pady=15)
        form_frame.pack(fill="x", padx=20, pady=20)
        
        # Form grid
        labels = ["Nama Lengkap:", "NIM:", "Program Studi:"]
        variables = [self.nama_var, self.nim_var, self.prodi_var]
        
        for i, (label, var) in enumerate(zip(labels, variables)):
            tk.Label(form_frame, 
                    text=label, 
                    font=("Arial", 11),
                    bg="#ffffff",
                    fg="#2c3e50").grid(row=i, column=0, sticky="w", pady=10, padx=(0, 10))
            
            tk.Entry(form_frame, 
                    textvariable=var, 
                    font=("Arial", 11),
                    width=40,
                    relief="solid",
                    borderwidth=1).grid(row=i, column=1, pady=10, padx=(0, 20))
        
        # Tombol CRUD
        crud_frame = tk.Frame(form_frame, bg="#ffffff")
        crud_frame.grid(row=0, column=2, rowspan=3, padx=(20, 0), pady=10)
        
        tambah_btn = tk.Button(crud_frame,
                              text="➕ TAMBAH DATA",
                              font=("Arial", 10, "bold"),
                              bg="#2ecc71",
                              fg="white",
                              padx=15,
                              pady=8,
                              relief="raised",
                              cursor="hand2",
                              activebackground="#27ae60",
                              activeforeground="white",
                              command=self.tambah)
        tambah_btn.pack(fill="x", pady=5)
        
        edit_btn = tk.Button(crud_frame,
                            text="✏ EDIT DATA",
                            font=("Arial", 10, "bold"),
                            bg="#3498db",
                            fg="white",
                            padx=15,
                            pady=8,
                            relief="raised",
                            cursor="hand2",
                            activebackground="#2980b9",
                            activeforeground="white",
                            command=self.edit)
        edit_btn.pack(fill="x", pady=5)
        
        hapus_btn = tk.Button(crud_frame,
                             text="🗑 HAPUS DATA",
                             font=("Arial", 10, "bold"),
                             bg="#e74c3c",
                             fg="white",
                             padx=15,
                             pady=8,
                             relief="raised",
                             cursor="hand2",
                             activebackground="#c0392b",
                             activeforeground="white",
                             command=self.hapus)
        hapus_btn.pack(fill="x", pady=5)
        
        # Tabel Data
        table_container = tk.Frame(data_frame, bg="#f8f9fa")
        table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        table_wrapper = tk.Frame(table_container, bg="#ecf0f1")
        table_wrapper.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(table_wrapper, 
                                columns=("Nama", "NIM", "Prodi"), 
                                show="headings",
                                height=15)
        
        # Configure columns
        columns = [("Nama", 350, "w"), ("NIM", 180, "center"), ("Prodi", 250, "w")]
        for col, width, anchor in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_wrapper, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_wrapper, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew", columnspan=2)
        
        table_wrapper.grid_rowconfigure(0, weight=1)
        table_wrapper.grid_columnconfigure(0, weight=1)
        
        # Bind row click
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)
        
        # TAB 2: Pencarian
        search_frame = tk.Frame(notebook, bg="#f8f9fa")
        notebook.add(search_frame, text="🔍 PENCARIAN")
        
        search_panel = tk.LabelFrame(search_frame, 
                                    text="ALGORITMA PENCARIAN DATA",
                                    font=("Arial", 12, "bold"),
                                    bg="#ffffff",
                                    padx=20,
                                    pady=20)
        search_panel.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Search by NIM
        nim_frame = tk.LabelFrame(search_panel, 
                                 text="Pencarian Berdasarkan NIM",
                                 font=("Arial", 11, "bold"),
                                 bg="#ffffff",
                                 padx=15,
                                 pady=15)
        nim_frame.pack(fill="x", pady=10)
        
        tk.Label(nim_frame, 
                text="Masukkan NIM:", 
                font=("Arial", 11),
                bg="#ffffff").pack(side="left", padx=(0, 10))
        
        self.nim_search_var = tk.StringVar()
        nim_entry = tk.Entry(nim_frame, 
                           textvariable=self.nim_search_var,
                           font=("Arial", 11),
                           width=25,
                           relief="solid",
                           borderwidth=1)
        nim_entry.pack(side="left", padx=(0, 20))
        
        btn_frame = tk.Frame(nim_frame, bg="#ffffff")
        btn_frame.pack(side="left", padx=10)
        
        linear_btn = tk.Button(btn_frame,
                              text="🔎 LINEAR SEARCH",
                              font=("Arial", 10, "bold"),
                              bg="#2980b9",
                              fg="white",
                              padx=10,
                              pady=6,
                              relief="raised",
                              cursor="hand2",
                              activebackground="#1c5a80",
                              activeforeground="white",
                              command=self.linear_search)
        linear_btn.pack(pady=2)
        
        binary_btn = tk.Button(btn_frame,
                              text="📊 BINARY SEARCH",
                              font=("Arial", 10, "bold"),
                              bg="#9b59b6",
                              fg="white",
                              padx=10,
                              pady=6,
                              relief="raised",
                              cursor="hand2",
                              activebackground="#8e44ad",
                              activeforeground="white",
                              command=self.binary_search)
        binary_btn.pack(pady=2)
        
        # Search by Nama
        nama_frame = tk.LabelFrame(search_panel, 
                                  text="Pencarian Berdasarkan Nama",
                                  font=("Arial", 11, "bold"),
                                  bg="#ffffff",
                                  padx=15,
                                  pady=15)
        nama_frame.pack(fill="x", pady=10)
        
        tk.Label(nama_frame, 
                text="Masukkan Nama:", 
                font=("Arial", 11),
                bg="#ffffff").pack(side="left", padx=(0, 10))
        
        self.nama_search_var = tk.StringVar()
        nama_entry = tk.Entry(nama_frame, 
                            textvariable=self.nama_search_var,
                            font=("Arial", 11),
                            width=25,
                            relief="solid",
                            borderwidth=1)
        nama_entry.pack(side="left", padx=(0, 20))
        
        sequential_btn = tk.Button(nama_frame,
                                  text="📝 SEQUENTIAL SEARCH",
                                  font=("Arial", 10, "bold"),
                                  bg="#e67e22",
                                  fg="white",
                                  padx=15,
                                  pady=6,
                                  relief="raised",
                                  cursor="hand2",
                                  activebackground="#d35400",
                                  activeforeground="white",
                                  command=self.sequential_search)
        sequential_btn.pack(side="left")
        
        # Filter Prodi
        filter_frame = tk.LabelFrame(search_panel, 
                                    text="Filter Data",
                                    font=("Arial", 11, "bold"),
                                    bg="#ffffff",
                                    padx=15,
                                    pady=15)
        filter_frame.pack(fill="x", pady=20)
        
        tk.Label(filter_frame, 
                text="Filter berdasarkan Prodi:", 
                font=("Arial", 11),
                bg="#ffffff").pack(side="left", padx=(0, 10))
        
        filter_entry = tk.Entry(filter_frame, 
                              textvariable=self.filter_prodi_var,
                              font=("Arial", 11),
                              width=25,
                              relief="solid",
                              borderwidth=1)
        filter_entry.pack(side="left", padx=(0, 10))
        
        filter_btn = tk.Button(filter_frame,
                              text="✅ TERAPKAN FILTER",
                              font=("Arial", 10, "bold"),
                              bg="#1abc9c",
                              fg="white",
                              padx=10,
                              pady=6,
                              relief="raised",
                              cursor="hand2",
                              activebackground="#16a085",
                              activeforeground="white",
                              command=self.filter_prodi)
        filter_btn.pack(side="left", padx=5)
        
        reset_btn = tk.Button(filter_frame,
                             text="🔄 RESET FILTER",
                             font=("Arial", 10, "bold"),
                             bg="#95a5a6",
                             fg="white",
                             padx=10,
                             pady=6,
                             relief="raised",
                             cursor="hand2",
                             activebackground="#7f8c8d",
                             activeforeground="white",
                             command=self.tampilkan)
        reset_btn.pack(side="left")
        
        # TAB 3: Sorting
        sort_frame = tk.Frame(notebook, bg="#f8f9fa")
        notebook.add(sort_frame, text="📊 SORTING")
        
        sort_panel = tk.LabelFrame(sort_frame, 
                                  text="ALGORITMA SORTING DATA",
                                  font=("Arial", 12, "bold"),
                                  bg="#ffffff",
                                  padx=20,
                                  pady=20)
        sort_panel.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Sorting algorithms
        algorithms = [
            ("🫧 BUBBLE SORT", BubbleSort(), "#3498db"),
            ("⭐ SELECTION SORT", SelectionSort(), "#2ecc71"),
            ("📥 INSERTION SORT", InsertionSort(), "#9b59b6"),
            ("🔄 MERGE SORT", MergeSort(), "#e67e22"),
            ("🔤 NAMA A-Z", "nama_asc", "#1abc9c"),
            ("🔤 NAMA Z-A", "nama_desc", "#e74c3c"),
            ("🐚 SHELL SORT", "shell", "#f39c12")
        ]
        
        for i, (text, algo, color) in enumerate(algorithms):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(sort_panel,
                          text=text,
                          font=("Arial", 11, "bold"),
                          bg=color,
                          fg="white",
                          padx=20,
                          pady=15,
                          relief="raised",
                          borderwidth=2,
                          cursor="hand2")
            
            darker_color = self.darken_color(color, 30)
            btn.config(activebackground=darker_color, activeforeground="white")
            
            if text == "🔤 NAMA A-Z":
                btn.config(command=self.sort_nama_ascending)
            elif text == "🔤 NAMA Z-A":
                btn.config(command=self.sort_nama_descending)
            elif text == "🐚 SHELL SORT":
                btn.config(command=self.shell_sort)
            else:
                btn.config(command=lambda a=algo: self.sort_data(a))
            
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            def make_hover(button, original_color):
                def on_enter(e):
                    darker = self.darken_color(original_color, 20)
                    button.config(bg=darker)
                def on_leave(e):
                    button.config(bg=original_color)
                
                button.bind("<Enter>", on_enter)
                button.bind("<Leave>", on_leave)
            
            make_hover(btn, color)
        
        for i in range(3):
            sort_panel.columnconfigure(i, weight=1)
        for i in range(3):
            sort_panel.rowconfigure(i, weight=1)
        
        # TAB 4: Informasi
        info_frame = tk.Frame(notebook, bg="#f8f9fa")
        notebook.add(info_frame, text="ℹ INFORMASI")
        
        info_panel = tk.Frame(info_frame, bg="#ffffff", padx=30, pady=30)
        info_panel.pack(fill="both", expand=True)
        
        tk.Label(info_panel,
                text="📚 INFORMASI APLIKASI",
                font=("Arial", 18, "bold"),
                bg="#ffffff",
                fg="#2c3e50").pack(pady=(0, 20))
        
        stats_frame = tk.LabelFrame(info_panel,
                                   text="📊 STATISTIK DATA",
                                   font=("Arial", 12, "bold"),
                                   bg="#ffffff",
                                   padx=20,
                                   pady=20)
        stats_frame.pack(fill="x", pady=10)
        
        total_mahasiswa = len(self.data)
        prodi_count = {}
        for m in self.data:
            prodi = m.get_prodi()
            prodi_count[prodi] = prodi_count.get(prodi, 0) + 1
        
        stats_text = f"""
        👥 Total Mahasiswa: {total_mahasiswa}
        
        📈 Distribusi Prodi:
        """
        
        for prodi, count in prodi_count.items():
            stats_text += f"  • {prodi}: {count} mahasiswa\n"
        
        tk.Label(stats_frame,
                text=stats_text,
                font=("Arial", 11),
                bg="#ffffff",
                fg="#2c3e50",
                justify="left").pack(anchor="w")
        
        features_frame = tk.LabelFrame(info_panel,
                                      text="✨ FITUR APLIKASI",
                                      font=("Arial", 12, "bold"),
                                      bg="#ffffff",
                                      padx=20,
                                      pady=20)
        features_frame.pack(fill="x", pady=20)
        
        features = [
            "✓ CRUD Data Mahasiswa (Create, Read, Update, Delete)",
            "✓ 5 Algoritma Sorting (Bubble, Selection, Insertion, Merge, Shell)",
            "✓ 3 Algoritma Searching (Linear, Binary, Sequential)",
            "✓ Sistem Login dengan Multiple User",
            "✓ Validasi NIM dengan Regular Expression",
            "✓ Penyimpanan Data JSON (File I/O)",
            "✓ Penerapan OOP (Class, Object, Encapsulation, Inheritance)",
            "✓ Error Handling dengan Try-Catch",
            "✓ Time Complexity Analysis"
        ]
        
        for feature in features:
            tk.Label(features_frame,
                    text=feature,
                    font=("Arial", 10),
                    bg="#ffffff",
                    fg="#27ae60",
                    justify="left").pack(anchor="w", pady=3)
        
        complexity_frame = tk.LabelFrame(info_panel,
                                        text="⏱ TIME COMPLEXITY",
                                        font=("Arial", 12, "bold"),
                                        bg="#ffffff",
                                        padx=20,
                                        pady=20)
        complexity_frame.pack(fill="x", pady=20)
        
        complexities = [
            "• Linear Search: O(n)",
            "• Binary Search: O(log n)",
            "• Sequential Search: O(n)",
            "• Bubble Sort: O(n²)",
            "• Selection Sort: O(n²)",
            "• Insertion Sort: O(n²)",
            "• Merge Sort: O(n log n)",
            "• Shell Sort: O(n log n)"
        ]
        
        for comp in complexities:
            tk.Label(complexity_frame,
                    text=comp,
                    font=("Arial", 10),
                    bg="#ffffff",
                    fg="#3498db",
                    justify="left").pack(anchor="w", pady=2)
        
        show_all_btn = tk.Button(info_panel,
                                text="👁️ TAMPILKAN SEMUA DATA",
                                font=("Arial", 11, "bold"),
                                bg="#4cc9f0",
                                fg="white",
                                padx=20,
                                pady=10,
                                relief="raised",
                                cursor="hand2",
                                activebackground="#3aa8d8",
                                activeforeground="white",
                                command=self.tampilkan)
        show_all_btn.pack(pady=20)
        
        footer_frame = tk.Frame(info_panel, bg="#ffffff")
        footer_frame.pack(side="bottom", fill="x", pady=(20, 0))
        
        tk.Label(footer_frame,
                text="Tugas Algoritma Pemrograman II - Universitas Pamulang | " +
                     f"User: {self.username.title()} | Total Data: {total_mahasiswa}",
                font=("Arial", 9),
                bg="#ffffff",
                fg="#7f8c8d").pack()
        
        # FOOTER UTAMA
        main_footer = tk.Frame(self.root, bg="#34495e", height=40)
        main_footer.pack(side="bottom", fill="x")
        main_footer.pack_propagate(False)
        
        footer_text = f"© {datetime.now().year} Universitas Pamulang • Algoritma Pemrograman II • User: {self.username.title()}"
        tk.Label(main_footer,
                text=footer_text,
                font=("Arial", 9),
                bg="#34495e",
                fg="#ecf0f1").pack(pady=10)
        
        # Initial display data
        self.tampilkan()
        
        print("✅ Main application loaded successfully")
    
    def darken_color(self, color, amount=20):
        """Menggelapkan warna untuk efek hover"""
        try:
            if color.startswith("#"):
                color = color[1:]
                r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
                r = max(0, r - amount)
                g = max(0, g - amount)
                b = max(0, b - amount)
                return f"#{r:02x}{g:02x}{b:02x}"
        except:
            pass
        return color

    def logout(self):
        """Kembali ke menu login"""
        self.root.destroy()
        main()

    # ----------------- row click handler -----------------
    def on_row_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected)["values"]
        if not values:
            return
        nama, nim, prodi = values
        self.nama_var.set(nama)
        self.nim_var.set(nim)
        self.prodi_var.set(prodi)

    # ----------------- CRUD -----------------
    def tambah(self):
        try:
            nama = self.nama_var.get().strip()
            nim = self.nim_var.get().strip()
            prodi = self.prodi_var.get().strip()

            if not nama or not nim or not prodi:
                raise Exception("Semua field wajib diisi!")

            if not re.match(r"^[0-9]{8,12}$", nim):
                raise Exception("NIM harus angka 8–12 digit!")

            # check duplicate nim
            if any(m.get_nim() == nim for m in self.data):
                raise Exception("NIM sudah ada. Gunakan NIM lain atau edit data yang ada.")

            self.data.append(Mahasiswa(nama, nim, prodi))
            FileHandler.simpan_data(self.data)
            self.tampilkan()
            messagebox.showinfo("Sukses", f"✅ Data {nama} berhasil ditambahkan!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def edit(self):
        try:
            selected = self.tree.focus()
            if not selected:
                messagebox.showwarning("Peringatan", "⚠ Pilih data yang ingin diubah pada tabel.")
                return
            
            values = self.tree.item(selected)["values"]
            if not values:
                return
            
            nim_selected = values[1]  # NIM dari row yang dipilih
            nama = self.nama_var.get().strip()
            prodi = self.prodi_var.get().strip()

            if not nama or not prodi:
                messagebox.showwarning("Peringatan", "Nama dan Prodi tidak boleh kosong.")
                return

            for m in self.data:
                if m.get_nim() == nim_selected:
                    old_nama = m.get_nama()
                    m.set_nama(nama)
                    m.set_prodi(prodi)
                    FileHandler.simpan_data(self.data)
                    self.tampilkan()
                    messagebox.showinfo("Sukses", f"✏ Data {old_nama} berhasil diperbarui menjadi {nama}!")
                    return
            
            messagebox.showerror("Error", "Data tidak ditemukan untuk diedit.")
        except Exception as e:
            messagebox.showerror("Error", f"Error saat edit: {e}")

    def hapus(self):
        try:
            selected = self.tree.focus()
            if not selected:
                messagebox.showwarning("Peringatan", "⚠ Pilih data yang ingin dihapus pada tabel.")
                return
            
            values = self.tree.item(selected)["values"]
            if not values:
                return
            
            nama = values[0]
            nim_selected = values[1]
            
            confirm = messagebox.askyesno("Konfirmasi", f"🗑 Hapus data {nama} (NIM: {nim_selected})?")
            if not confirm:
                return
            
            self.data = [m for m in self.data if m.get_nim() != nim_selected]
            FileHandler.simpan_data(self.data)
            self.tampilkan()
            messagebox.showinfo("Sukses", f"✅ Data {nama} berhasil dihapus!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saat hapus: {e}")

    # ----------------- display -----------------
    def tampilkan(self, filtered=None):
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        show = filtered if filtered is not None else self.data
        
        if not show:
            self.tree.insert("", "end", values=("Tidak ada data", "", ""))
            return
        
        for m in show:
            try:
                self.tree.insert("", "end", iid=m.get_nim(), values=(m.get_nama(), m.get_nim(), m.get_prodi()))
            except Exception:
                self.tree.insert("", "end", values=(m.get_nama(), m.get_nim(), m.get_prodi()))

    # ----------------- SEARCHING -----------------
    def linear_search(self):
        target = self.nim_search_var.get().strip()
        if not target:
            messagebox.showwarning("Peringatan", "Masukkan NIM untuk mencari.")
            return
        
        for m in self.data:
            if m.get_nim() == target:
                try:
                    self.tree.selection_set(target)
                    self.tree.see(target)
                except Exception:
                    for i, item in enumerate(self.tree.get_children()):
                        if self.tree.item(item)["values"][1] == target:
                            self.tree.selection_set(item)
                            self.tree.see(item)
                            break
                messagebox.showinfo("Hasil Pencarian", 
                                  f"✅ Data ditemukan!\nNama: {m.get_nama()}\nNIM: {m.get_nim()}\nProdi: {m.get_prodi()}\n\nAlgoritma: Linear Search\nTime Complexity: O(n)")
                return
        
        messagebox.showwarning("Hasil Pencarian", "❌ Data tidak ditemukan!")

    def binary_search(self):
        target = self.nim_search_var.get().strip()
        if not target:
            messagebox.showwarning("Peringatan", "Masukkan NIM untuk mencari.")
            return

        # ensure data sorted by NIM
        self.data = MergeSort().sort(self.data)
        FileHandler.simpan_data(self.data)
        self.tampilkan()

        low, high = 0, len(self.data) - 1
        steps = 0
        while low <= high:
            steps += 1
            mid = (low + high) // 2
            mid_nim = self.data[mid].get_nim()
            
            if mid_nim == target:
                try:
                    self.tree.selection_set(target)
                    self.tree.see(target)
                except Exception:
                    row = self.tree.get_children()[mid]
                    self.tree.selection_set(row)
                    self.tree.see(row)
                
                messagebox.showinfo("Hasil Pencarian", 
                                  f"✅ Data ditemukan!\nNama: {self.data[mid].get_nama()}\nNIM: {target}\nProdi: {self.data[mid].get_prodi()}\n\nAlgoritma: Binary Search\nLangkah pencarian: {steps}\nTime Complexity: O(log n)")
                return
            elif mid_nim < target:
                low = mid + 1
            else:
                high = mid - 1
        
        messagebox.showinfo("Hasil Pencarian", f"❌ Data tidak ditemukan!\nLangkah pencarian: {steps}")

    def sequential_search(self):
        target = self.nama_search_var.get().strip().lower()
        if not target:
            messagebox.showwarning("Peringatan", "Masukkan nama untuk mencari.")
            return
        
        results = []
        for m in self.data:
            if target in m.get_nama().lower():
                results.append(m)
        
        if results:
            if len(results) == 1:
                m = results[0]
                try:
                    self.tree.selection_set(m.get_nim())
                    self.tree.see(m.get_nim())
                except Exception:
                    for item in self.tree.get_children():
                        if target in self.tree.item(item)["values"][0].lower():
                            self.tree.selection_set(item)
                            self.tree.see(item)
                            break
                
                messagebox.showinfo("Hasil Pencarian", 
                                  f"✅ Data ditemukan!\nNama: {m.get_nama()}\nNIM: {m.get_nim()}\nProdi: {m.get_prodi()}\n\nAlgoritma: Sequential Search\nTime Complexity: O(n)")
            else:
                self.tampilkan(results)
                messagebox.showinfo("Hasil Pencarian", 
                                  f"✅ Ditemukan {len(results)} data yang cocok!\nMenampilkan hasil filter.\n\nAlgoritma: Sequential Search")
        else:
            messagebox.showwarning("Hasil Pencarian", "❌ Data tidak ditemukan!")

    # ----------------- SORTING -----------------
    def sort_data(self, method):
        try:
            import time
            start_time = time.time()
            
            self.data = method.sort(self.data)
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            FileHandler.simpan_data(self.data)
            self.tampilkan()
            
            algo_name = method.__class__.__name__.replace("Sort", " Sort")
            
            complexity = {
                "BubbleSort": "O(n²)",
                "SelectionSort": "O(n²)",
                "InsertionSort": "O(n²)",
                "MergeSort": "O(n log n)"
            }.get(method.__class__.__name__, "O(n²)")
            
            messagebox.showinfo("Sorting Selesai", 
                              f"✅ {algo_name} berhasil!\nWaktu eksekusi: {elapsed_time:.6f} detik\nTotal data: {len(self.data)}\nTime Complexity: {complexity}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal sorting:\n{e}")

    def shell_sort(self):
        try:
            import time
            start_time = time.time()
            
            arr = self.data[:]
            gap = len(arr) // 2
            while gap > 0:
                for i in range(gap, len(arr)):
                    temp = arr[i]
                    j = i
                    while j >= gap and arr[j-gap].get_nim() > temp.get_nim():
                        arr[j] = arr[j-gap]
                        j -= gap
                    arr[j] = temp
                gap //= 2
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            self.data = arr
            FileHandler.simpan_data(self.data)
            self.tampilkan()
            
            messagebox.showinfo("Shell Sort Selesai", 
                              f"✅ Shell Sort berhasil!\nWaktu eksekusi: {elapsed_time:.6f} detik\nTotal data: {len(self.data)}\nTime Complexity: O(n log n)")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal sorting:\n{e}")

    def sort_nama_ascending(self):
        try:
            import time
            start_time = time.time()
            
            self.data = sorted(self.data, key=lambda m: m.get_nama().lower())
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            FileHandler.simpan_data(self.data)
            self.tampilkan()
            messagebox.showinfo("Sorting Selesai", 
                              f"✅ Sorting Nama A → Z berhasil!\nWaktu eksekusi: {elapsed_time:.6f} detik\nTotal data: {len(self.data)}\nTime Complexity: O(n log n)")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal sorting nama:\n{e}")

    def sort_nama_descending(self):
        try:
            import time
            start_time = time.time()
            
            self.data = sorted(self.data, key=lambda m: m.get_nama().lower(), reverse=True)
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            FileHandler.simpan_data(self.data)
            self.tampilkan()
            messagebox.showinfo("Sorting Selesai", 
                              f"✅ Sorting Nama Z → A berhasil!\nWaktu eksekusi: {elapsed_time:.6f} detik\nTotal data: {len(self.data)}\nTime Complexity: O(n log n)")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal sorting nama:\n{e}")

    # ----------------- FILTER -----------------
    def filter_prodi(self):
        query = self.filter_prodi_var.get().strip().lower()
        if not query:
            messagebox.showwarning("Peringatan", "Masukkan kata kunci Prodi untuk filter.")
            return
        
        filtered = [m for m in self.data if query in m.get_prodi().lower()]
        
        if not filtered:
            messagebox.showinfo("Hasil Filter", "❌ Tidak ada data yang cocok dengan filter.")
            return
        
        self.tampilkan(filtered)
        messagebox.showinfo("Hasil Filter", 
                          f"✅ Ditemukan {len(filtered)} data dengan prodi mengandung '{query}'")

# ---------------------- DATA AWAL ----------------------
def starter_data():
    return [
        Mahasiswa("Azka Insan Robbani", "24101140099", "Teknik Informatika"),
        Mahasiswa("Bagus ardiansyah", "241011401958", "Teknik Informatika"),
        Mahasiswa("Fathur Rachman", "241011401713", "Teknik Informatika"),
        Mahasiswa("Tumpal Sinaga", "241011400087", "Teknik Informatika"),
        Mahasiswa("Vina Aulia", "241011401650", "Teknik Informatika"),
        Mahasiswa("Satria Apriza Fajar", "241011400103", "Teknik Informatika"),
        Mahasiswa("Davrielle saddad", "241011400085", "Teknik Informatika"),
        Mahasiswa("Jandri Hartat Gea", "241012402295", "Teknik Informatika"),
        Mahasiswa("Walman pangaribuan", "241011400094", "Teknik Informatika"),
        Mahasiswa("Muhammad Rafli", "24011400075", "Teknik Informatika"),
        Mahasiswa("Jason Cornelius Chandra", "241011401866", "Teknik Informatika"),
        Mahasiswa("Ahmad Rasyid", "241011402663", "Teknik Informatika"),
        Mahasiswa("Ferda Ayi Sukaesih Sutanto", "241011400068", "Teknik Informatika"),
        Mahasiswa("Muhammad Ikram Maulana", "241011402896", "Teknik Informatika"),
        Mahasiswa("Nazril Supriyadi", "241011400091", "Teknik Informatika"),
        Mahasiswa("Ade jahwa aulia", "241011402829", "Teknik Informatika"),
        Mahasiswa("Maulana ikhsan fadhillah", "241011400092", "Teknik Informatika"),
        Mahasiswa("Dea Amellya", "241011400089", "Teknik Informatika"),
        Mahasiswa("Risqi Eko Trianto", "241011402427", "Teknik Informatika"),
        Mahasiswa("Rizki Ramadani", "241011400098", "Teknik Informatika"),
        Mahasiswa("Muhammad Alif Fajriansyah", "241011402197", "Teknik Informatika"),
        Mahasiswa("Dzaki Ramadhan", "241011400097", "Teknik Informatika"),
        Mahasiswa("Servatius Hasta Kristanto", "241011400076", "Teknik Informatika"),
        Mahasiswa("Ahmad Firdaus", "241011401761", "Teknik Informatika"),
        Mahasiswa("Ade sofyan", "241011402338", "Teknik Informatika"),
        Mahasiswa("Dimas Ahmad", "241011402835", "Teknik Informatika"),
        Mahasiswa("Adam Darmansyah", "241011401470", "Teknik Informatika"),
        Mahasiswa("Muhammad Noer Alam Prana dipta", "241011400079", "Teknik Informatika"),
        Mahasiswa("Azmi  Al Fahriza", "241011403269", "Teknik Informatika"),
        Mahasiswa("Ahmad Irfan", "241011402053", "Teknik Informatika"),
        Mahasiswa("Gregorius Gilbert Ieli Sarjana", "241011402382", "Teknik Informatika"),
    ]

# ---------------------- MAIN FUNCTION ----------------------
def main():
    print("🚀 Memulai Sistem Data Mahasiswa Universitas Pamulang...")
    print("📁 Memuat data dari file...")
    
    # Debug: Hapus file akun yang korup jika ada
    if os.path.exists("akun_mahasiswa.json"):
        try:
            with open("akun_mahasiswa.json", "r") as f:
                content = f.read()
                # Cek apakah file berisi data yang korup
                if '"dzaki ramadhan": "141005"' in content:
                    print("⚠️  File akun mengandung data korup, akan diperbaiki otomatis...")
        except:
            pass
    
    # Buat file data awal jika belum ada
    existing = FileHandler.baca_data()
    if not existing:
        initial = starter_data()
        FileHandler.simpan_data(initial)
        print("✅ Data awal berhasil dibuat!")
    
    root = tk.Tk()
    
    def on_login_success(username):
        """Callback yang dipanggil saat login berhasil"""
        print(f"✅ Login successful for user: {username}")
        print("🔄 Closing login window and opening main application...")
        
        # Tutup window login
        root.destroy()
        
        # Buka window utama aplikasi
        main_window = tk.Tk()
        app = AppMahasiswa(main_window, username)
        main_window.mainloop()
    
    # Jalankan sistem login
    print("🔧 Starting login system...")
    login_system = LoginSystem(root, on_login_success)
    
    # Print untuk debugging
    print("✅ Login system initialized")
    print("✅ Root window created")
    print("✅ Starting mainloop...")
    
    root.mainloop()

if __name__ == "__main__":
    main()