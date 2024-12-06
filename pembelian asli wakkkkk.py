import csv
import datetime as dt
import os
import pandas as pd
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

def daftar_produk_pembeli():
    daftar = PrettyTable()
    daftar.field_names = ['Id', 'Produk', 'Kategori', 'Harga', 'Stok']
    produk = pd.read_csv('produk_toko.csv')
    for daftar_produk in produk.values:
        if daftar_produk[5] == 'Tersedia':
            daftar.add_row([daftar_produk[0], daftar_produk[1], daftar_produk[2], daftar_produk[3], daftar_produk[4]])
    print(daftar)

def transaksi(username, produk, jumlah, total_harga, alamat, status):
    waktu = dt.datetime.now()
    riwayat = pd.read_csv('transaksi.csv')
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
    riwayat.to_csv('transaksi.csv', index=False)

def riwayat_transaksi_pembeli(username):
    riwayat = pd.read_csv('transaksi.csv')
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

def pembelian(username):
    daftar_produk = pd.read_csv('produk_toko.csv')
    daftar_beli = []
    total_pembelian = 0

    while True:
        try:
            clear_terminal()
            daftar_produk_pembeli()
            id_produk = input("Masukkan ID Produk yang ingin dibeli (atau ketik 'keluar' untuk keluar): ")
            if id_produk.lower() == 'keluar':
                kembali()
                clear_terminal()
                menu_pembeli(username)
                break
            elif not id_produk.isdigit():
                print("Input ID produk tidak valid")
                kembali()
                continue

            id_produk = int(id_produk)
            produk_dipilih = daftar_produk.loc[
                (daftar_produk['ID'] == id_produk) & 
                (daftar_produk['Status'].str.lower() == 'tersedia')
            ]

            if produk_dipilih.empty:
                print("Produk tidak ditemukan")
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
            clear_terminal() 
            kembali()
        elif lanjut == 'iya':
            daftar_produk.loc[daftar_produk['ID'] == id_produk, 'Stok'] -= jumlah
            daftar_produk.to_csv('produk_toko.csv', index=False)
            alamat = input("Masukkan alamat pengiriman: ")
            for pembelian in daftar_beli:
                transaksi(username, pembelian[0], pembelian[1], pembelian[2], alamat, 'Diproses')
            print("Pembelian berhasil! Terima kasih.")
            kembali()
        else:
            print("masukkan yang benar!")
            kembali()
    else:
        print("Tidak ada produk yang dibeli.")

def menu_pembeli(username):
    while True:
        print('''
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
'Selamat datang, {username}!'
==========================================================================

''')
        pilihan = input("Silahkan pilih menu 1-5: ")
        if pilihan == '1':
            clear_terminal()
            daftar_produk_pembeli()
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
            continue

