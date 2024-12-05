import pandas as pd
from prettytable import PrettyTable
import csv
import datetime as dt

def coba():
    daftar = PrettyTable()
    daftar.field_names = ['Id', 'Produk', 'Kategori', 'Harga', 'Stok', 'Status']
    produk1 = pd.read_csv('produk_toko.csv')
    for produk2 in produk1.values:
        if produk2[5] == 'Tersedia':
            daftar.add_row(produk2)
    print(daftar)
    return produk1


def log_transaksi(username, produk, jumlah, total_harga, alamat, status, alasan):
    waktu = dt.datetime.now().strftime("%d/%m/%Y %H:%M")
    transaksi = {
        'Username': username,
        'Produk': produk,
        'Jumlah': jumlah,
        'Total Harga': total_harga,
        'Alamat': alamat,
        'Waktu': waktu,
        'Status': status,
        'Alasan': alasan
    }
    riwayat = pd.read_csv('transaksi.csv')
    riwayat['Alasan'] = riwayat['Alasan'].fillna("") 
    transaksi_df = pd.DataFrame([transaksi])
    riwayat = pd.concat([riwayat, transaksi_df], ignore_index=True)
    riwayat.to_csv('transaksi.csv', index=False)

def pembelian(username):
    produk = coba()
    daftar_beli = []  
    total_pembelian = 0  

    while True:
        id_produk = input("Masukkan ID Produk: ")
        for produkk in produk.values:
            if str(produkk[0]) == id_produk:  
                print(f"Produk: {produkk[1]} | Harga: {produkk[3]} | Stok: {produkk[4]}")
                if produkk[4] == 0:
                    print("Produk habis. Pembelian ditolak.")
                    alasan = "Stok Habis"
                    status = "Ditolak"
                    log_transaksi(username, produkk[1], 0, 0, "-", status, alasan)
                    break
                else:
                    jumlah = int(input("Masukkan jumlah pembelian: "))
                    while jumlah > produkk[4]:
                        print("Jumlah melebihi stok. Silakan masukkan jumlah yang lebih kecil.")
                        jumlah = int(input("Masukkan jumlah pembelian: "))
                    
                    total_harga = jumlah * produkk[3]
                    total_pembelian += total_harga  
                    daftar_beli.append([produkk[1], jumlah, total_harga])
                    print(f"Total harga untuk {produkk[1]}: {total_harga}")
                    break 
        
        lanjut = input("Apakah Anda ingin membeli produk lain? [y/n]: ").lower()
        if lanjut == 'y':
            break
               

    if total_pembelian > 0:
        print("\nTotal Pembelian:")
        for produk, jumlah, harga in daftar_beli:
            print(f"Produk: {produk} | Jumlah: {jumlah} | Harga: {harga}")
        print(f"\nTotal Pembelian: {total_pembelian}")
            
        konfirmasi = input("Apakah Anda ingin melanjutkan pembelian? [y/n]: ").lower()
        if konfirmasi == 'y':
            alamat = input("Masukkan alamat pengiriman: ")
            for produk_dibeli in daftar_beli:
                log_transaksi(username, produk_dibeli[0], produk_dibeli[1], produk_dibeli[2], alamat, "Menunggu Konfirmasi", "")
            produk_toko = pd.read_csv('produk_toko.csv')
            for produk_dibeli in daftar_beli:
                produk_toko.loc[produk_toko['Produk'] == produk_dibeli[0], 'Stok'] -= produk_dibeli[1]
                produk_toko.loc[produk_toko['Stok'] == 0, 'Status'] = 'Habis'
                produk_toko.to_csv('produk_toko.csv', index=False)

            print("\nPembelian berhasil")
        else:
            print("\nPembelian dibatalkan")
    else:
        print("\nTidak ada produk yang dibeli")