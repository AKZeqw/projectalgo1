import pandas as pd
import prettytable
from prettytable import PrettyTable
from prettytable import from_csv
import csv

produk = pd.read_csv('produk_toko.csv')

inputan_id_ubah = 1
edit_nama_produk = PrettyTable()
edit_nama_produk.field_names = ['Id','Produk','Kategori','Harga','Stok']

for baris in produk.values:
    print(baris)
    if baris[0] == inputan_id_ubah:
        edit_nama_produk.add_row(baris)

print(edit_nama_produk)