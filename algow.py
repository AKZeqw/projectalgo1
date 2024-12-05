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


def transaksi(username, produk, jumlah, total_harga, alamat, status, alasan):
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
        'Alasan': alasan
    }
    riwayat = pd.read_csv('transaksi.csv')
    riwayat['Alasan'] = riwayat['Alasan'].fillna("") 
    transaksi_df = pd.DataFrame([transaksi])
    riwayat = pd.concat([riwayat, transaksi_df], ignore_index=True)
    riwayat.to_csv('transaksi.csv', index=False)


def pembelian(username):
    # coba()
    produk = coba()
    daftar_beli = []  
    total_pembelian = 0  

    while True:
        while True:
            id_produk = input("Masukkan ID Produk: ")
            valid_produk = False
            for produkk in produk.values:
                if str(produkk[0]) == id_produk:  
                    valid_produk = True
                    print(f"Produk: {produkk[1]} | Harga: {produkk[3]} | Stok: {produkk[4]}")
                    if produkk[4] == 0:
                        print("Produk habis. Pembelian ditolak.")
                        alasan = "Stok Habis"
                        status = "Ditolak"
                        transaksi(username, produkk[1], 0, 0, "-", status, alasan)
                        break
                    else:
                        while True:
                            try:
                                jumlah = int(input("Masukkan jumlah pembelian: "))
                                if jumlah <= 0:
                                    print("Jumlah pembelian harus lebih besar dari 0.")
                                elif jumlah > produkk[4]:
                                    print("Jumlah melebihi stok. Silakan masukkan jumlah yang lebih kecil.")
                                else:
                                    break
                            except ValueError:
                                print("Input tidak valid. Harap masukkan angka untuk jumlah pembelian.")
                        total_harga = jumlah * produkk[3]
                        total_pembelian += total_harga  
                        daftar_beli.append([produkk[1], jumlah, total_harga])
                        print(f"Total harga untuk {produkk[1]}: {total_harga}")
                    break
            if valid_produk:
                break
            else:
                print("ID Produk tidak ditemukan. Silakan coba lagi.")
        

        while True:
            lanjut = input("Apakah Anda ingin membeli produk lain? [y/n]: ").lower()
            if lanjut in ['y', 'n']:
                break
            else:
                print("Pilihan tidak valid. Harap masukkan 'y' untuk ya atau 'n' untuk tidak.")
        
        if lanjut == 'n':
            break
               

    if total_pembelian > 0:
        print("\nTotal Pembelian:")
        for produk, jumlah, harga in daftar_beli:
            print(f"Produk: {produk} | Jumlah: {jumlah} | Harga: {harga}")
        print(f"\nTotal Pembelian: {total_pembelian}")
            

        while True:
            konfirmasi = input("Apakah Anda ingin melanjutkan pembelian? [y/n]: ").lower()
            if konfirmasi in ['y', 'n']:
                break
            else:
                print("Pilihan tidak valid. Harap masukkan 'y' untuk ya atau 'n' untuk tidak.")
        
        if konfirmasi == 'y':
            alamat = input("Masukkan alamat pengiriman: ")
            for produk_dibeli in daftar_beli:
                transaksi(username, produk_dibeli[0], produk_dibeli[1], produk_dibeli[2], alamat, "Menunggu Konfirmasi", "")
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




pembelian(username='am')
print ('hallow')