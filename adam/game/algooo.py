
import csv
import pandas as pd
import datetime as dt
import os

teks_username = r'''
 _____           _ __  __            _   
|_   _|_ _ _ __ (_)  \/  | __ _ _ __| |_ 
  | |/ _` | '_ \| | |\/| |/ _` | '__| __|.
  | | (_| | | | | | |  | | (_| | |  | |_ 
  |_|\__,_|_| |_|_|_|  |_|\__,_|_|   \__|'''

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi kembali ke menu sebelumnya
def kembali():
    input('Tekan enter untuk kembali...')
    clear_terminal()

# Menu awal
def menu_awal():
    print(teks_username)
    print('''
1. Registrasi
2. Login
3. Keluar ''')
    inputan = input('Silahkan pilih menu [1-3]: ')
    if inputan == '1':
        clear_terminal()
        daftar()
    elif inputan == '2':
        clear_terminal()
        login()
    elif inputan == '3':
        clear_terminal()
    else:
        clear_terminal()
        print('Pilihan menu tidak ditemukan!')
        menu_awal()

# Fungsi registrasi
def daftar():
    if not os.path.exists('users.csv'):
        df = pd.DataFrame(columns=['username', 'password', 'role'])
        df.to_csv('users.csv', index=False)
    else:
        df = pd.read_csv('users.csv')
    print('Kosongi username jika ingin kembali ke menu awal')
    username = input('Masukkan username(Harus lebih dari 4 huruf): ')
    if username == '':
        clear_terminal()
        menu_awal()
    elif len(username) < 5:
        print('Username tidak memenuhi syarat')
        kembali()
        daftar()
    elif len(username) > 4:
        if username in df['username'].values:
            print('Username sudah terdaftar. Silakan coba username lain.')
            kembali()
            daftar()
        else:
            password1 = input('Masukkan password: ')
            password2 = input('Konfirmasi password: ')
            
            if password1 != password2:
                print('Password tidak cocok. Silakan coba lagi.')
                kembali()
                daftar()
            elif password1 == password2:
                pengguna_baru = pd.DataFrame([[username, password1, 'pembeli']], columns=['username', 'password', 'role'])
                df = pd.concat([df, pengguna_baru], ignore_index=True)
                
                df.to_csv('users.csv', index=False)
                print('Pengguna berhasil didaftarkan!')
                kembali()

# Fungsi login
def login():
    users = pd.read_csv('users.csv')
    username = input('Masukkan Username: ')
    if username in users['username'].values:
        baris_user = users[users['username'] == username]
        password = input('Masukkan Password: ')
        if password == baris_user['password'].values[0]:
            role = baris_user['role'].values[0]  # Mengecek role
            if role == 'pembeli':
                menu_pembeli(username)
            else:
                print(f"Menu untuk role {role} belum diimplementasikan.")
        else:
            print("Password salah.")
            input("\nTekan Enter untuk kembali ke menu...")
    else:
        print("Username tidak ditemukan.")
        input("\nTekan Enter untuk kembali ke menu...")

# Fungsi melihat daftar produk
def lihat_produk():
    try:
        produk = pd.read_csv('produk.csv')
        print("Daftar Produk:")
        print(produk)
    except FileNotFoundError:
        print("Belum ada produk yang tersedia.")
    input("\nTekan Enter untuk kembali ke menu...")

# Fungsi melakukan pembelian
def lakukan_pembelian(username):
    try:
        produk = pd.read_csv('produk.csv')
        print("Daftar Produk:")
        print(produk)
        produk_id = input("\nMasukkan ID Produk yang ingin dibeli: ")
        if produk_id in produk['id'].astype(str).values:
            jumlah = int(input("Masukkan jumlah pembelian: "))
            produk_terpilih = produk[produk['id'].astype(str) == produk_id]
            total_harga = jumlah * produk_terpilih['harga'].values[0]
            print(f"Total harga: {total_harga}")
            alamat = input("Masukkan alamat pengiriman: ")
            konfirmasi = input("Apakah Anda ingin melanjutkan pembelian? (y/n): ")
            if konfirmasi.lower() == 'y':
                transaksi_baru = pd.DataFrame(
                    [[username, produk_terpilih['nama'].values[0], jumlah, total_harga, alamat, dt.datetime.now()]],
                    columns=['username', 'produk', 'jumlah', 'total_harga', 'alamat', 'tanggal']
                )
                try:
                    transaksi = pd.read_csv('transaksi.csv')
                    transaksi = pd.concat([transaksi, transaksi_baru], ignore_index=True)
                except FileNotFoundError:
                    transaksi = transaksi_baru
                transaksi.to_csv('transaksi.csv', index=False)
                print("\nPembelian berhasil!")
            else:
                print("\nPembelian dibatalkan.")
        else:
            print("\nProduk tidak ditemukan.")
    except FileNotFoundError:
        print("Belum ada produk yang tersedia.")
    input("\nTekan Enter untuk kembali ke menu...")

# Fungsi melihat riwayat transaksi
def lihat_riwayat(username):
    try:
        transaksi = pd.read_csv('transaksi.csv')
        riwayat = transaksi[transaksi['username'] == username]
        if riwayat.empty:
            print("Belum ada riwayat transaksi untuk user ini.")
        else:
            print("\nRiwayat Transaksi Anda:")
            print(riwayat)
    except FileNotFoundError:
        print("Belum ada riwayat transaksi.")
    input("\nTekan Enter untuk kembali ke menu...")

# Menu pembeli
def menu_pembeli(username):
    while True:
        print(f"\nSelamat datang, {username}!")
        print('''
1. Lihat List Produk dan Harga
2. Lakukan Pembelian
3. Lihat Riwayat Transaksi
4. Keluar
''')
        pilihan = input("Silahkan pilih menu [1-4]: ")
        if pilihan == '1':
            lihat_produk()
        elif pilihan == '2':
            lakukan_pembelian(username)
        elif pilihan == '3':
            lihat_riwayat(username)
        elif pilihan == '4':
            break
        else:
            print("Pilihan tidak valid!")

# Fungsi login yang memanggil menu pembeli
def login():
    users = pd.read_csv('users.csv')
    username = input('Masukkan Username: ')
    if username in users['username'].values:
        baris_user = users[users['username'] == username]
        password = input('Masukkan Password: ')
        if password == baris_user['password'].values[0]:
            role = baris_user['role'].values[0]  # Mengecek role
            if role == 'pembeli':
                menu_pembeli(username)
            else:
                print(f"Menu untuk role {role} belum diimplementasikan.")
        else:
            print("Password salah.")
            input("\nTekan Enter untuk kembali ke menu...")
    else:
        print("Username tidak ditemukan.")
        input("\nTekan Enter untuk kembali ke menu...")
