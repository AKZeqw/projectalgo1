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
    os.system('cls')

def login():
    users = pd.read_csv('users.csv')
    username = input('Masukkan Username: ')
    if username in users['username'].values:
        baris_user = users[users['username'] == username]
        password = input('Masukkan Password: ')
        if password == baris_user['password'].values[0]:
            role = baris_user['role'].values[0] #Mengecek role
            if role == 'admin':
                'menu admin'
            # elif role == 'petani':
            #     'menu petani'
            elif role == 'pembeli':
                menu_pembeli(username)
        else:
            print('Password salah') #Jika password salah
            kembali()
            menu_awal()
    else:
        print('Username tidak ditemukan') #Jika username salah
        kembali()
        menu_awal()

def kembali():
    inputan_kembali = input('Tekan enter untuk kembali...')
    if inputan_kembali == '':
        clear_terminal()
    else:
        kembali()


def daftar():
    if not os.path.exists('users.csv'):
        df = pd.DataFrame(columns=['username','password','role'])
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
                pengguna_baru = pd.DataFrame([[username, password1,'pembeli']], columns=['username','password','role'])
                df = pd.concat([df, pengguna_baru], ignore_index=True)
                
                df.to_csv('users.csv', index=False)
                print('Pengguna berhasil didaftarkan!')


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

#Diskon petani untuk pembelian

def lihat_produk():
    try:
        produk = pd.read_csv('product_toko.csv')
        print("\nDaftar Produk:")
        print(produk.to_string(index=False))
    except FileNotFoundError:
        print("Belum ada produk yang tersedia.")
    input("\nTekan Enter untuk kembali ke menu...")

def lihat_produkg():
    try:
        produkg = pd.read_csv('produkg.csv')
        print("\nDaftar Produk:")
        print(produkg.to_string(index=False))
    except FileNotFoundError:
        print("Belum ada produk yang tersedia.")
    input("\nTekan Enter untuk kembali ke menu...")



def lakukan_pembelian(username):
    try:
        produk = pd.read_csv('product_toko.csv')
        print("\nDaftar Produk:")
        print(produk.to_string(index=False))
        produk_id = input("\nMasukkan ID Produk yang ingin dibeli: ")
        if produk_id in produk['Id'].astype(str).values:
            jumlah = int(input("Masukkan jumlah pembelian: "))
            produk_terpilih = produk[produk['Id'].astype(str) == produk_id]
            total_harga = jumlah * produk_terpilih['Harga'].values[0]
            print(f"Total harga: {total_harga}")
            alamat = input("Masukkan alamat pengiriman: ")
            konfirmasi = input("Apakah Anda ingin melanjutkan pembelian? (y/n): ")
            if konfirmasi.lower() == 'y':
                transaksi_baru = pd.DataFrame(
                    [[username, produk_terpilih['Produk'].values[0], jumlah, total_harga, alamat, dt.datetime.now()]],
                    columns=['username', 'Produk', 'jumlah', 'total_harga', 'alamat', 'tanggal']
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


def lihat_riwayat(username):
    try:
        transaksi = pd.read_csv('transaksi.csv')
        riwayat = transaksi[transaksi['username'] == username]
        if riwayat.empty:
            print("Belum ada riwayat transaksi untuk user ini.")
        else:
            print("\nRiwayat Transaksi Anda:")
            print(riwayat.to_string(index=False))
    except FileNotFoundError:
        print("Belum ada riwayat transaksi.")
    input("\nTekan Enter untuk kembali ke menu...")


def menu_pembeli(username):
    while True:
        print(f"\nSelamat datang, {username}!")
        print('''
1. Lihat List Produk dan Harga petani
2. lihat produk alat pertanian
3. Lakukan Pembelian
4. Lihat Riwayat Transaksi
5. Keluar
''')
        pilihan = input("Silahkan pilih menu: ")
        if pilihan == '1':
            lihat_produk()
        elif pilihan == '2':
            lihat_produkg()
        elif pilihan == '3':
            lakukan_pembelian(username)
        elif pilihan == '4':
            lihat_riwayat(username)
        elif pilihan == '5':
            break
        login()


menu_awal()
