import pandas as pd
import prettytable
from prettytable import PrettyTable
from prettytable import from_csv
import csv

produk = pd.read_csv('produk_toko.csv')
# print()
# # inputan_id_ubah = 1
# # edit_nama_produk = PrettyTable()
# # edit_nama_produk.field_names = ['Id','Produk','Kategori','Harga','Stok']

# # for baris in produk.values:
# #     print(baris)
# #     if baris[0] == inputan_id_ubah:
# #         edit_nama_produk.add_row(baris)
a = 2
# # print(edit_nama_produk)
# def test():
#     while True:
#         i = int(input())
#         if i == 1:
#             print("t")
#             continue
#         elif i == 2:
#             print("2")
#             continue
#         else:
#             break
#     while True:
#         print("LOH")
#         break
# test()
daftar_produk = pd.read_csv('produk_toko.csv')

id_produk = int(input("Masukkan ID Produk yang ingin dibeli (atau ketik 'keluar' untuk keluar): "))
for baris in daftar_produk.values:
    if baris[0] == id_produk and baris[5] == 'Tersedia':
        print(baris)

# produk_dipilih = produk_dipilih.iloc[0]
# tabel = PrettyTable()
# tabel.field_names = ['Produk', 'Harga', 'Stok']
# tabel.add_row([produk_dipilih['Produk'], produk_dipilih['Harga'], produk_dipilih['Stok']])
# print(tabel)

# print(produk_dipilih)