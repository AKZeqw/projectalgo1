import pandas as pd
import datetime as dt
import os
from prettytable import PrettyTable
from prettytable import from_csv

def clear_terminal():
    os.system('cls')

def kembali():
    inputan_kembali = input('Tekan enter untuk kembali...')
    if inputan_kembali == '':
        clear_terminal()
    else:
        kembali()

def login():
    users = pd.read_csv('users.csv')
    username = input('Masukkan Username: ').lower()
    if username in users['username'].values:
        baris_user = users[users['username'] == username]
        password = input('Masukkan Password: ')
        if password == baris_user['password'].values[0]:
            role = baris_user['role'].values[0]
            if role == 'admin':
                menu_admin()
            elif role == 'pembeli':
                clear_terminal()
                menu_pembeli(username)
        else:
            print('Password salah')
            kembali()
            menu_awal()
    else:
        print('Username tidak ditemukan')
        kembali()
        menu_awal()

def daftar():
    if not os.path.exists('users.csv'):
        df = pd.DataFrame(columns=['username','password','role'])
        df.to_csv('users.csv', index=False)
    else:
        df = pd.read_csv('users.csv')
    print('Kosongi username jika ingin kembali ke menu awal')
    username = input('Masukkan username (Harus lebih dari 4 huruf): ').lower()
    if username == '':
        kembali()
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
                kembali()
                menu_awal()

def menu_awal():
    clear_terminal()
    print(r'''
============================================================
 __  __                                                  _ 
|  \/  |                         /\                     | |
| \  / |  ___  _ __   _   _     /  \   __      __  __ _ | |
| |\/| | / _ \| '_ \ | | | |   / /\ \  \ \ /\ / / / _` || |
| |  | ||  __/| | | || |_| |  / ____ \  \ V  V / | (_| || |
|_|  |_| \___||_| |_| \__,_| /_/    \_\  \_/\_/   \__,_||_|
============================================================
1. Registrasi
2. Login
3. Keluar
============================================================
''')
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
        print('Pilihan menu tidak ditemukan!')
        kembali()
        menu_awal()


def daftar_produk_pembeli(username):
    daftar = PrettyTable()
    daftar.field_names = ['Id', 'Produk', 'Kategori', 'Harga', 'Stok']
    produk = pd.read_csv('produk_toko.csv')
    for daftar_produk in produk.values:
        if daftar_produk[5] == 'Tersedia':
            daftar.add_row([daftar_produk[0], daftar_produk[1], daftar_produk[2], daftar_produk[3], daftar_produk[4]])
    print(daftar)
    kembali()
    menu_pembeli(username)

def transaksi(username, produk, jumlah, total_harga, alamat, status):
    waktu = dt.datetime.now()
    riwayat = pd.read_csv('riwayat_transaksi.csv')
    id_transaksi = (len(riwayat) + 1)
    transaksi = {
        'ID': int(id_transaksi), 
        'Username': username,
        'Produk': produk,
        'Jumlah': jumlah,
        'Total Harga': total_harga,
        'Alamat': alamat,
        'Waktu': waktu,
        'Status': status,
    }
    transaksi_df = pd.DataFrame([transaksi])
    riwayat = pd.concat([riwayat, transaksi_df], ignore_index=True)
    riwayat['ID'] = riwayat['ID'].astype(int)
    riwayat = riwayat[['ID', 'Username', 'Produk', 'Jumlah', 'Total Harga', 'Alamat', 'Waktu', 'Status']]  # Memastikan ID berada di depan
    riwayat.to_csv('riwayat_transaksi.csv', index=False)

def riwayat_transaksi_pembeli(username):
    riwayat = pd.read_csv('riwayat_transaksi.csv')
    tabel_riwayat = PrettyTable()
    tabel_riwayat.field_names = ['ID', 'Username', 'Produk', 'Jumlah', 'Total Harga', 'Waktu', 'Status']
    for index in range(len(riwayat)):
        transaksi = riwayat.iloc[index]
        if transaksi['Username'] == username:
            tabel_riwayat.add_row([transaksi['ID'], transaksi['Username'], transaksi['Produk'],transaksi['Jumlah'], transaksi['Total Harga'], transaksi['Waktu'], transaksi['Status']])
    if len(tabel_riwayat.rows) == 0:
        print(f"Tidak ada riwayat transaksi untuk username '{username}'.")
    else:
        print(tabel_riwayat)
    kembali()
    menu_pembeli(username)

def pembelian(username):
    daftar_produk = pd.read_csv('produk_toko.csv')
    daftar_beli = []
    total_pembelian = 0

    while True:
        try:
            clear_terminal()
            daftar = PrettyTable()
            daftar.field_names = ['Id', 'Produk', 'Kategori', 'Harga', 'Stok']
            produk = pd.read_csv('produk_toko.csv')
            for baris_produk in produk.values:
                if baris_produk[5] == 'Tersedia':
                    daftar.add_row([baris_produk[0], baris_produk[1], baris_produk[2], baris_produk[3], baris_produk[4]])
            print(daftar)
            id_produk = input("Masukkan ID Produk yang ingin dibeli (atau ketik 'keluar' untuk keluar): ")
            if id_produk.lower() == 'keluar':
                kembali()
                menu_pembeli(username)
                break
            elif not id_produk.isdigit():
                print("Input ID produk tidak valid")
                kembali()
                continue

            id_produk = int(id_produk)
            produk_dipilih = produk[produk['ID'] == id_produk]
            produk_dipilih_tersedia = produk_dipilih[produk_dipilih['Status'] == 'Tersedia']

            if produk_dipilih_tersedia.empty:
                print("Produk tidak tersedia atau ID tidak valid")
                kembali()
                continue

            else:
                clear_terminal()
                produk_dipilih = produk_dipilih.iloc[0]
                tabel = PrettyTable()
                tabel.field_names = ['Produk', 'Harga', 'Stok']
                tabel.add_row([produk_dipilih['Produk'], produk_dipilih['Harga'], produk_dipilih['Stok']])
                print(tabel)

                try:
                    jumlah = int(input("Masukkan jumlah pembelian: "))
                    if jumlah <= 0:
                        print("Jumlah pembelian harus lebih besar dari 0.")
                        kembali()
                    elif jumlah > produk_dipilih['Stok']:
                        print("Jumlah melebihi stok. Silakan masukkan jumlah yang lebih kecil.")
                        kembali()
                    else:
                        total_harga = jumlah * produk_dipilih['Harga']
                        total_pembelian += total_harga
                        daftar_beli.append([produk_dipilih['Produk'], jumlah, total_harga])
                        print(f"Total harga untuk {produk_dipilih['Produk']}: {total_harga}")
                        lanjut = input("Apakah Anda ingin membeli produk lain? (iya/tidak): ").lower()
                        if lanjut == 'tidak': 
                            clear_terminal() 
                            break
                        elif lanjut != 'iya':
                            print("Input tidak valid. Kembali ke menu pembelian.")
                            kembali()
                except ValueError: 
                    print("Input jumlah pembelian tidak valid. Harap masukkan angka.")
                    kembali()
        except ValueError:
            print("Input ID produk tidak valid")
            kembali()
            clear_terminal()
            continue
    if daftar_beli:
        tabel_pembelian = PrettyTable()
        tabel_pembelian.field_names = ['Produk', 'Jumlah', 'Harga']
        for baris in daftar_beli:
            tabel_pembelian.add_row(baris)
        tabel_pembelian.add_row(['Total', '', total_pembelian])
        print(tabel_pembelian)
        lanjut = input("Apakah Anda yakin membeli? (iya/tidak): ").lower()
        if lanjut == 'tidak': 
            kembali()
            pembelian(username)
        elif lanjut == 'iya':
            daftar_produk.loc[daftar_produk['ID'] == id_produk, 'Stok'] -= jumlah
            alamat = input("Masukkan alamat pengiriman: ")
            for pembelian in daftar_beli:
                transaksi(username, pembelian[0], pembelian[1], pembelian[2], alamat, 'Diproses')
            print("Pembelian berhasil! Terima kasih.")
            daftar_produk.to_csv('produk_toko.csv', index=False)
            kembali()
            menu_pembeli(username)
        else:
            print("masukkan yang benar!")
            kembali()
    else:
        print("Tidak ada produk yang dibeli.")

def menu_pembeli(username):
    while True:
        print(f'''
==========================================================================
 __  __                       _____                    _            _  _ 
|  \/  |                     |  __ \                  | |          | |(_)
| \  / |  ___  _ __   _   _  | |__) |  ___  _ __ ___  | |__    ___ | | _ 
| |\/| | / _ \| '_ \ | | | | |  ___/  / _ \| '_ ` _ \ | '_ \  / _ \| || |
| |  | ||  __/| | | || |_| | | |     |  __/| | | | | || |_) ||  __/| || |
|_|  |_| \___||_| |_| \__,_| |_|      \___||_| |_| |_||_.__/  \___||_||_|
==========================================================================
1. Lihat List Produk dan Harga
2. Lakukan Pembelian
3. Lihat Riwayat Transaksi
4. Keluar
==========================================================================
Selamat datang, {username}!
==========================================================================

''')
        pilihan = input("Silahkan pilih menu 1-5: ")
        if pilihan == '1':
            clear_terminal()
            daftar_produk_pembeli(username)
            break
        elif pilihan == '2':
            clear_terminal()
            pembelian(username)
            break
        elif pilihan == '3':
            clear_terminal()
            riwayat_transaksi_pembeli(username)
            break
        elif pilihan == '4':
            clear_terminal()
            kembali()
            break
        else:
            print("Pilihan tidak valid!")
            kembali()
            continue

menu_awal()