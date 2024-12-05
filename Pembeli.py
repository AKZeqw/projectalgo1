import pandas as pd
from prettytable import PrettyTable
import csv
import datetime as dt
import os

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
            daftar.add_row([daftar_produk[0],daftar_produk[1],daftar_produk[2],daftar_produk[3],daftar_produk[4]])
    print(daftar)


def transaksi(username, produk, jumlah, total_harga, alamat, status):
    waktu = dt.datetime.now()
    riwayat = pd.read_csv('transaksi.csv')
    id_transaksi = len(riwayat)+1
    transaksi = {
        'ID': id_transaksi, 
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
    riwayat.to_csv('transaksi.csv', index=False)


# def pembelian(username):

#     daftar_produk = pd.read_csv('produk_toko.csv')
#     daftar_beli = []
#     total_pembelian = 0
#     a = 0

#     while True:
#         try:
#             clear_terminal()
#             daftar_produk_pembeli()
#             id_produk = int(input("Masukkan ID Produk yang ingin dibeli: "))
#             for produk in daftar_produk.values:
#                 if produk[0] == id_produk and produk[5] == "Tersedia":
#                     tabel = PrettyTable()
#                     tabel.field_names = ['Produk','Harga','Stok']
#                     tabel.add_row([produk[1],produk[3],produk[4]])
#                     clear_terminal()
#                     print(tabel)
#                     if produk[4] == 0:
#                         print("Stok produk habis")
#                         kembali()
#                         clear_terminal()
#                         break
#                     else:
#                         try:
#                             jumlah = int(input("Masukkan jumlah pembelian: "))
#                             if jumlah <= 0:
#                                 print("Jumlah pembelian harus lebih besar dari 0.")
#                                 kembali()
#                                 clear_terminal()
#                                 break
#                             elif jumlah > produk[4]:
#                                 print("Jumlah melebihi stok. Silakan masukkan jumlah yang lebih kecil.")
#                                 kembali()
#                                 clear_terminal()
#                                 break
#                             else:
#                                 break
#                         except ValueError:
#                             print("Input jumlah pembelian tidak valid. Harap masukkan angka untuk jumlah pembelian.")
#                     total_harga = jumlah * produk[3]
#                     total_pembelian += total_harga
#                     daftar_beli.append([produk[1], jumlah, total_harga])
#                     print(f"Total harga untuk {produk[1]}: {total_harga}")
#                     a = 1
#                 break
                        
#             while a == 1:
#                 lanjut = input("Apakah Anda ingin membeli produk lain? (iya/tidak): ").lower()
#                 if lanjut == 'iya':
#                     break
#                 elif lanjut == 'tidak':
#                     tabel_pembelian = PrettyTable()
#                     tabel_pembelian.field_names = ['Produk','Jumlah','Harga']
#                     for baris in daftar_beli:
#                         tabel_pembelian.add_row(baris)
#                     tabel_pembelian.add_row(['','',total_pembelian])
#                     print(tabel_pembelian)

#                     break
#                 else:
#                     print('Inputan tidak valid')
#         except ValueError:
#             print('Input ID produk tidak valid. Pastikan input berupa angka.')
#             kembali()

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
                menu_pembeli()
                break
            elif not id_produk.isdigit():
                print("Input ID produk tidak valid")
                kembali()
                continue

            id_produk = int(id_produk)
            produk_dipilih = daftar_produk.loc[
                (daftar_produk['ID'] == id_produk) & (daftar_produk['Status'] == 'Tersedia')
            ]
            
            if produk_dipilih.empty:
                print("Produk tidak ditemukan")
                kembali()
                continue
            else:
                produk_dipilih = produk_dipilih.iloc[0]
                clear_terminal()
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
                        if lanjut == 'tidak':  # Keluar dari pembelian
                            break
                        elif lanjut != 'iya':  # Validasi jawaban tidak valid
                            print("Input tidak valid. Kembali ke menu pembelian.")
                            kembali()
                except ValueError:  # Jumlah tidak valid
                    print("Input jumlah pembelian tidak valid. Harap masukkan angka.")
                    kembali()
        except ValueError:
            print("Input ID produk tidak valid")
            kembali()
            clear_terminal()
            continue

    if daftar_beli:  # Menampilkan hasil pembelian
        tabel_pembelian = PrettyTable()
        tabel_pembelian.field_names = ['Produk', 'Jumlah', 'Harga']
        for baris in daftar_beli:
            tabel_pembelian.add_row(baris)
        tabel_pembelian.add_row(['Total', '', total_pembelian])
        print(tabel_pembelian)

        alamat = input("Masukkan alamat pengiriman: ")
        for pembelian in daftar_beli:
            transaksi(username, pembelian[0], pembelian[1], pembelian[2], alamat, 'Diproses')

        print("Pembelian berhasil! Terima kasih.")
    else:  # Tidak ada produk yang dibeli
        print("Tidak ada produk yang dibeli.")


pembelian('agung')



# pembelian(username='am')
# print ('hallow')