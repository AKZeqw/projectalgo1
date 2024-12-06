import pandas as pd
import prettytable
from prettytable import PrettyTable
from prettytable import from_csv
import csv
import datetime as dt

# def status():
#     riwayat = pd.read_csv('riwayat_transaksi.csv')
#     tabel = PrettyTable()
#     for baris in riwayat:
#         if baris[6] == 'Diproses':
#             tabel.add_row(baris)
#     print(tabel)
#     id_transaksi = int(input("Masukkan ID transaksi yang statusnya ingin diubah: "))
#     if id_transaksi in riwayat['ID'].values:
#         riwayat.loc[riwayat['ID'] == id_transaksi, 'Status'] = 'Diterima'
#         riwayat.to_csv('riwayat_transaksi.csv', index=False)
#         print(f"Status transaksi dengan ID {id_transaksi} berhasil diubah menjadi Diterima.")
#     else:
#         print(f"Transaksi dengan ID {id_transaksi} tidak ditemukan.")

filter_id = []
riwayat = pd.read_csv('riwayat_transaksi.csv')
tabel = PrettyTable()
tabel.field_names = ['ID','Username','Produk','Jumlah','Total Harga','Alamat','Waktu','Status']
filter_id = []
for baris in riwayat.values:
    if baris[7] == 'Diproses':
        tabel.add_row(baris)
        filter_id.append(baris[0])
print(tabel)
print(filter_id)

# produk = pd.read_csv('produk_toko.csv')
# tabel_produk_dipilih = PrettyTable()
# tabel_produk_dipilih.field_names = ['ID','Produk','Kategori','Harga','Stok','Status']
# for baris in produk.values:
#     print(baris)
#     if baris[0] == 1:
#         tabel_produk_dipilih.add_row(baris)
# print(tabel_produk_dipilih)