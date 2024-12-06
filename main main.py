from prettytable import PrettyTable
import csv
import datetime as dt
import os
import pandas as pd

# Fungsi untuk membersihkan terminal
def clear_terminal():
    os.system('cls')

# Fungsi untuk kembali ke menu sebelumnya
def kembali():
    inputan_kembali = input('Tekan enter untuk kembali...')
    if inputan_kembali == '':
        clear_terminal()
    else:
        kembali()

# Fungsi untuk menampilkan daftar produk pembeli
def daftar_produk_pembeli():
    daftar = PrettyTable()
    daftar.field_names = ['ID', 'Produk', 'Kategori', 'Harga', 'Stok']
    produk = pd.read_csv('produk_toko.csv')
    for daftar_produk in produk.values:
        if daftar_produk[5] == 'Tersedia':  # Pastikan hanya produk yang tersedia yang ditampilkan
            daftar.add_row([daftar_produk[0], daftar_produk[1], daftar_produk[2], daftar_produk[3], daftar_produk[4]])
    print(daftar)
    kembali()
    menu_pembeli()

# Fungsi untuk menangani transaksi pembelian
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

# Fungsi untuk menampilkan riwayat transaksi berdasarkan username
def lihat_riwayat(username):
    riwayat = pd.read_csv('transaksi.csv')

    # Pastikan kolom 'Username' tidak memiliki spasi ekstra dan cocok dengan input
    riwayat['Username'] = riwayat['Username'].str.strip()

    # Filter berdasarkan username
    riwayat_filtered = riwayat[riwayat['Username'] == username]

    if riwayat_filtered.empty:
        print(f"Tidak ada riwayat transaksi untuk username '{username}'.")
        kembali()
        return
    
    # Membuat tabel untuk menampilkan riwayat transaksi
    tabel_riwayat = PrettyTable()
    tabel_riwayat.field_names = ['ID', 'Username', 'Produk', 'Jumlah', 'Total Harga', 'Waktu', 'Status']
    
    # Memasukkan setiap transaksi sebagai baris dalam tabel
    for transaksi in riwayat_filtered.itertuples(index=False, name=None):
        # Ambil kolom yang diinginkan (melewatkan kolom ke-5)
        row = [transaksi[0], transaksi[1], transaksi[2], transaksi[3], transaksi[4], transaksi[6], transaksi[7]]  # Melewati kolom ke-5 (kolom ke-6)
        tabel_riwayat.add_row(row)  # Menambahkan transaksi ke tabel
    
    print(tabel_riwayat)


# Fungsi untuk melakukan pembelian
def pembelian(username):
    daftar_produk = pd.read_csv('produk_toko.csv')
    daftar_beli = []
    total_pembelian = 0

    while True:
        try:
            clear_terminal()
            daftar_produk_pembeli()  # Memanggil daftar produk pembeli untuk ditampilkan
            id_produk = input("Masukkan ID Produk yang ingin dibeli (atau ketik 'keluar' untuk keluar): ")
            if id_produk.lower() == 'keluar':
                kembali()
                clear_terminal()
                menu_pembeli(username)  # Kembali ke menu pembeli setelah keluar dari pembelian
                break
            elif not id_produk.isdigit():
                print("Input ID produk tidak valid")
                kembali()
                continue

            id_produk = int(id_produk)
            produk_dipilih = daftar_produk.loc[
                (daftar_produk['ID'] == id_produk) & 
                (daftar_produk['Status'].str.strip().str.lower() == 'tersedia')
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
                        daftar_produk.loc[daftar_produk['ID'] == id_produk, 'Stok'] -= jumlah
                        daftar_produk.to_csv('produk_toko.csv', index=False)

                        print(f"Total harga untuk {produk_dipilih['Produk']}: {total_harga}")

                        lanjut = input("Apakah Anda ingin membeli produk lain? (iya/tidak): ").lower()
                        if lanjut == 'tidak': 
                            clear_terminal() # Keluar dari pembelian
                            break
                        elif lanjut != 'iya':  # Validasi jawaban tidak valid
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

        alamat = input("Masukkan alamat pengiriman: ")
        for pembelian in daftar_beli:
            transaksi(username, pembelian[0], pembelian[1], pembelian[2], alamat, 'Diproses')
        print("Pembelian berhasil! Terima kasih.")
        clear_terminal()
    else:
        print("Tidak ada produk yang dibeli.")

# Fungsi menu pembeli
def menu_pembeli():
    username = input("Masukkan username Anda: ")  # Memanggil menu pembeli setelah input username
    while True:
        print(f"\nSelamat datang, {username}!")
        print('''1. Lihat List Produk dan Harga
2. Lakukan Pembelian
3. Lihat Riwayat Transaksi
4. Keluar
''')
        pilihan = input("Silahkan pilih menu 1-4: ")
        if pilihan == '1':
            clear_terminal()
            daftar_produk_pembeli()
            break  # Memanggil fungsi untuk menampilkan daftar produk
        elif pilihan == '2':
            clear_terminal()
            pembelian(username)
            break # Menjalankan pembelian
        elif pilihan == '3':
            clear_terminal()
            lihat_riwayat(username)
            break  # Menampilkan riwayat transaksi untuk username tertentu
        elif pilihan == '4':
            clear_terminal()
            kembali()
            break
        else:
            print("Pilihan tidak valid!")

# Fungsi utama untuk memulai menu awal

menu_pembeli()  # Memulai program
