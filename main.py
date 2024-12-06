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
    tabel_riwayat.field_names = ['ID','Username','Produk','Jumlah','Total Harga','Alamat','Waktu','Status']
    for index in range(len(riwayat)):
        transaksi = riwayat.iloc[index]
        if transaksi['Username'] == username:
            tabel_riwayat.add_row([transaksi['ID'],transaksi['Username'],transaksi['Produk'],transaksi['Jumlah'],transaksi['Total Harga'],transaksi['Alamat'],transaksi['Waktu'],transaksi['Status']])
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
                        daftar_produk.loc[daftar_produk['ID'] == id_produk, 'Stok'] -= jumlah
                        daftar_produk.to_csv('produk_toko.csv', index=False)
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
            produk_df = pd.read_csv('produk_toko.csv')
            for item in daftar_beli:
                produk = item[0]
                jumlah = item[1]
                produk_df.loc[produk_df['Produk'] == produk, 'Stok'] += jumlah
            produk_df.to_csv('produk_toko.csv', index=False)
            print("Pembelian dibatalkan. Stok produk telah dikembalikan.")
            daftar_produk = pd.read_csv('produk_toko.csv')
            kembali()
            menu_pembeli(username)
        elif lanjut == 'iya':
            alamat = input("Masukkan alamat pengiriman: ")
            if alamat == '':
                print('Alamat tidak boleh kosong')
            else:
                for pembelian in daftar_beli:
                    transaksi(username, pembelian[0], pembelian[1], pembelian[2], alamat, 'Menunggu Konfirmasi')
                print("Pembelian berhasil! Terima kasih.")
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


def menu_admin():
    clear_terminal()
    print(r'''
===================================================================
 __  __                                     _             _        
|  \/  |                         /\        | |           (_)       
| \  / |  ___  _ __   _   _     /  \     __| | _ __ ___   _  _ __  
| |\/| | / _ \| '_ \ | | | |   / /\ \   / _` || '_ ` _ \ | || '_ \ 
| |  | ||  __/| | | || |_| |  / ____ \ | (_| || | | | | || || | | |
|_|  |_| \___||_| |_| \__,_| /_/    \_\ \__,_||_| |_| |_||_||_| |_|
''')
    print('''
===================================================================
1. Mengelola Produk Toko
2. Konfirmasi Pembelian
3. Melihat Riwayat Transaksi
4. Kembali
5. Keluar
===================================================================
''')

    inputan = input('Pilih menu: [1-3]: ')
    if inputan == '1':
        clear_terminal()
        kelola_produk_admin()
    elif inputan == '2':
        clear_terminal()
        konfirmasi_pembelian()
    elif inputan == '3':
        riwayat_transaksi_admin()
        clear_terminal()
    elif inputan == '4':
        clear_terminal()
        menu_awal()
    elif inputan == '5':
        clear_terminal()
    else:
        print('Piihan menu tidak ditemukan')
        menu_admin()

def menu_edit():
    produk = pd.read_csv('produk_toko.csv')
    daftar = from_csv(open('produk_toko.csv'))
    daftar.sortby = 'Status'
    print(daftar)
    inputan_id_ubah = input(f'Masukkan id produk yang ingin diedit [Pilih 1-{len(produk)}]: ')
    if inputan_id_ubah.isdigit():
        inputan_id_ubah = int(inputan_id_ubah)
        if 0 < int(inputan_id_ubah) <= (len(produk)):
            tabel_produk_dipilih = PrettyTable()
            tabel_produk_dipilih.field_names = ['ID','Produk','Kategori','Harga','Stok','Status']
            for baris in produk.values:
                if baris[0] == inputan_id_ubah:
                    tabel_produk_dipilih.add_row(baris)
            while True:
                print(f'''
====================================================
 __  __                       ______      _  _  _   
|  \/  |                     |  ____|    | |(_)| |  
| \  / |  ___  _ __   _   _  | |__     __| | _ | |_ 
| |\/| | / _ \| '_ \ | | | | |  __|   / _` || || __|
| |  | ||  __/| | | || |_| | | |____ | (_| || || |_ 
|_|  |_| \___||_| |_| \__,_| |______| \__,_||_| \__|
====================================================
1. Edit Nama Produk
2. Edit Kategori Produk
3. Edit Harga Produk
4. Edit Stok Produk
5. Edit Status Produk
6. Kembali
7. Keluar
====================================================
ID PRODUK = {inputan_id_ubah}
====================================================
''')
                inputan = input('Pilih Menu [1-7]: ')
                if inputan.isdigit():
                    if inputan == '1':
                        clear_terminal()
                        print(tabel_produk_dipilih)
                        inputan_nama_baru = input('Masukkan nama baru untuk produk: ').title()
                        produk.loc[produk['ID'] == inputan_id_ubah, 'Produk'] = inputan_nama_baru
                        inputan_konfirmasi = input(f'Apakah anda yakin mengubah nama dari produk dengan id {inputan_id_ubah}? (iya/tidak): ').lower()
                        if inputan_konfirmasi == 'iya':
                            produk.to_csv('produk_toko.csv', index=False)
                            print(f'Nama produk dengan ID {inputan_id_ubah} berhasil diubah menjadi {inputan_nama_baru}.')
                            kembali()
                            continue
                        elif inputan_konfirmasi == 'tidak':
                            print('Nama produk gagal diubah')
                            kembali()
                            continue
                        else:
                            print('Inputan tidak sesuai')
                            print('Nama produk gagal diubah')
                            kembali()
                            continue
                    elif inputan == '2':
                        clear_terminal()
                        print(tabel_produk_dipilih)
                        inputan_kategori_baru = input('Masukkan kategori baru untuk produk: ').title()
                        produk.loc[produk['ID'] == inputan_id_ubah, 'Kategori'] = inputan_kategori_baru
                        inputan_konfirmasi = input(f'Apakah anda yakin mengubah kategori dari produk dengan id {inputan_id_ubah}? (iya/tidak): ').lower()
                        if inputan_konfirmasi == 'iya':
                            produk.to_csv('produk_toko.csv', index=False)
                            print(f'Kategori produk dengan ID {inputan_id_ubah} berhasil diubah menjadi {inputan_kategori_baru}.')
                            kembali()
                            continue
                        elif inputan_konfirmasi == 'tidak':
                            print('Kategori produk gagal diubah')
                            kembali()
                            continue
                        else:
                            print('Inputan tidak sesuai')
                            print('Kategori produk gagal diubah')
                            kembali()
                            continue
                    elif inputan == '3':
                        clear_terminal()
                        print(tabel_produk_dipilih)
                        inputan_harga_baru = input('Masukkan harga baru untuk produk: ').title()
                        try:
                            produk.loc[produk['ID'] == inputan_id_ubah, 'Harga'] = int(inputan_harga_baru)
                            inputan_konfirmasi = input(f'Apakah anda yakin mengubah harga dari produk dengan id {inputan_id_ubah}? (iya/tidak): ').lower()
                            if inputan_konfirmasi == 'iya':
                                produk.to_csv('produk_toko.csv', index=False)
                                print(f'Harga produk dengan ID {inputan_id_ubah} berhasil diubah menjadi {inputan_harga_baru}.')
                                kembali()
                                continue
                            elif inputan_konfirmasi == 'tidak':
                                print('Harga produk gagal diubah')
                                kembali()
                                continue
                            else:
                                print('Inputan tidak sesuai')
                                print('Harga produk gagal diubah')
                                kembali()
                        except ValueError:
                            print("Input harga produk tidak valid. Pastikan input berupa angka.")
                            kembali()
                            continue
                    elif inputan == '4':
                        clear_terminal()
                        print(tabel_produk_dipilih)
                        inputan_stok_baru = input('Masukkan stok baru untuk produk: ').title()
                        try:
                            produk.loc[produk['ID'] == inputan_id_ubah, 'Stok'] = int(inputan_stok_baru)
                            inputan_konfirmasi = input(f'Apakah anda yakin mengubah stok dari produk dengan id {inputan_id_ubah}? (iya/tidak): ').lower()
                            if inputan_konfirmasi == 'iya':
                                produk.to_csv('produk_toko.csv', index=False)
                                print(f'Stok produk dengan ID {inputan_id_ubah} berhasil diubah menjadi {inputan_stok_baru}.')
                                kembali()
                                continue
                            elif inputan_konfirmasi == 'tidak':
                                print('Stok produk gagal diubah')
                                kembali()
                                continue
                            else:
                                print('Inputan tidak sesuai')
                                print('Stok produk gagal diubah')
                                kembali()
                                continue
                        except ValueError:
                            print("Input stok produk tidak valid. Pastikan input berupa angka.")
                            kembali()
                            continue
                    elif inputan == '5':
                        clear_terminal()
                        print(tabel_produk_dipilih)
                        inputan_status_baru = input('Masukkan status baru untuk produk (Tersedia/Tidak Tersedia): ').title()
                        if inputan_status_baru == 'Tersedia' or inputan_status_baru == 'Tidak Tersedia':
                            produk.loc[produk['ID'] == inputan_id_ubah, 'Status'] = inputan_status_baru
                            inputan_konfirmasi = input(f'Apakah anda yakin mengubah status dari produk dengan id {inputan_id_ubah}? (iya/tidak): ').lower()
                            if inputan_konfirmasi == 'iya':
                                produk.to_csv('produk_toko.csv', index=False)
                                print(f'Status produk dengan ID {inputan_id_ubah} berhasil diubah menjadi {inputan_status_baru}.')
                                kembali()
                                continue
                            elif inputan_konfirmasi == 'tidak':
                                print('Status produk gagal diubah')
                                kembali()
                                continue
                            else:
                                print('Inputan tidak sesuai')
                                print('Status produk gagal diubah')
                                kembali()
                                continue
                        else:
                            print('Inputan tidak valid')
                            kembali()
                            continue
                    elif inputan == '6':
                        clear_terminal()
                        kelola_produk_admin()
                        break
                    elif inputan == '7':
                        clear_terminal()
                        break
                    else:
                        print('Inputan tidak sesuai')
                        kembali()
                        continue
        else:
            print('ID tidak ditemukan')
            kembali()
            menu_edit()
    else:
        print('Inputan harus berupa angka')
        kembali()
        menu_edit()

def tambah_produk():
    produk = pd.read_csv('produk_toko.csv')
    clear_terminal()
    a = 0
    while True:
        print('Kosongi jika ingin kembali ke menu')
        nama_produk = input('Masukkan nama produk: ').title()
        if nama_produk == '':
            kelola_produk_admin()
            break
        elif nama_produk not in produk['Produk'].values:
            kategori = input('Masukkan kategori produk: ').title()
            harga = input('Masukkan harga produk (angka): ')
            if harga.isdigit():
                stok = input('Masukkan stok produk (angka): ')
                clear_terminal()
                if stok.isdigit():
                    id = len(produk) + 1
                    produk_baru = pd.DataFrame([[id,nama_produk,kategori,harga,stok,'Tersedia']], columns=['ID','Produk','Kategori','Harga','Stok','Status'])
                    tabel_tambah_produk = PrettyTable()
                    tabel_tambah_produk.field_names = ['ID','Produk','Kategori','Harga','Stok','Status']
                    tabel_tambah_produk.add_row([id,nama_produk,kategori,harga,stok,'Tersedia'])
                    print(tabel_tambah_produk)
                    a = 1
                    break
                else:
                    print('Inputan berupa angka')
                    kembali()
                    continue
            else:
                print('Inputan harus berupa angka')
                kembali()
                continue
        else:
            print(f'Produk {nama_produk} sudah ada')
            kembali()
        
    while a == 1:
        inputan_konfirmasi = input(f'Tambahkan produk {nama_produk}? (iya/tidak): ').lower()
        if inputan_konfirmasi == 'iya':
            gabung = pd.concat([produk, produk_baru], ignore_index=True)
            gabung.to_csv('produk_toko.csv', index=False)
            print(f'Produk {nama_produk} berhasil di tambahkan')
            kembali()
            kelola_produk_admin()
            break
        elif inputan_konfirmasi == 'tidak':
            print(f'Produk {nama_produk} tidak ditambahkan')
            kembali()
            kelola_produk_admin()
            break
        else:
            print('Inputan tidak sesuai')
            kembali()
            continue

def daftar_produk():
    clear_terminal()
    daftar = from_csv(open('produk_toko.csv'))
    daftar.align = 'l'
    daftar.align['Harga'] = 'r'
    daftar.align['Stok'] = 'r'
    daftar.align['Status'] = 'c'
    print(daftar)
    kembali()
    kelola_produk_admin()

def riwayat_transaksi_admin():
    riwayat = pd.read_csv('riwayat_transaksi.csv')
    tabel_riwayat = PrettyTable()
    tabel_riwayat.field_names = ['ID', 'Username', 'Produk', 'Jumlah', 'Total Harga', 'Alamat', 'Waktu', 'Status']
    transaksi_ditemukan = False
    for index in range(len(riwayat)):
        transaksi = riwayat.iloc[index]
        if transaksi['Status'] == 'Diterima' or transaksi['Status'] == 'Ditolak':
            tabel_riwayat.add_row([transaksi['ID'], transaksi['Username'], transaksi['Produk'], transaksi['Jumlah'], transaksi['Total Harga'], transaksi['Alamat'], transaksi['Waktu'], transaksi['Status']])
            transaksi_ditemukan = True
    if not transaksi_ditemukan:
        print('Tidak ada riwayat transaksi yang sesuai.')
    print(tabel_riwayat)
    kembali()
    menu_admin()


def konfirmasi_pembelian():
    riwayat = pd.read_csv('riwayat_transaksi.csv')
    tabel = PrettyTable()
    tabel.field_names = ['ID','Username','Produk','Jumlah','Total Harga','Alamat','Waktu','Status']
    filter_id = []
    for baris in riwayat.values:
        if baris[7] == 'Menunggu Konfirmasi':
            tabel.add_row(baris)
            filter_id.append(int(baris[0]))
    print(tabel)
    inputan_konfirmasi = input('Apakah anda ingin mengirim atau menolak pembelian? (mengirim/menolak): ').lower()
    if inputan_konfirmasi == 'mengirim':
        id_transaksi = int(input("Masukkan ID transaksi yang ingin dikirim: "))
        if id_transaksi in filter_id:
            while True:
                konfirmasi = input(f'apakah anda yakin ingin mengirim produk dengan ID transaksi {id_transaksi}? (iya/tidak)').lower()
                if konfirmasi == 'iya':
                    riwayat.loc[riwayat['ID'] == id_transaksi, 'Status'] = 'Dikirim'
                    riwayat.to_csv('riwayat_transaksi.csv', index=False)
                    print(f"Status transaksi dengan ID {id_transaksi} berhasil diubah menjadi Diterima.")
                    kembali()
                    menu_admin()
                    break
                elif konfirmasi == 'tidak':
                    print('Status konfirmasi tidak diubah')
                    kembali()
                    menu_admin()
                    break
        else:
            print(f"Transaksi dengan ID {id_transaksi} tidak ditemukan.")
            kembali()
            menu_admin()
    elif inputan_konfirmasi == 'menolak':
        id_transaksi = int(input("Masukkan ID transaksi yang ingin ditolak: "))
        if id_transaksi in filter_id:
            while True:
                konfirmasi = input(f'apakah anda yakin ingin menolak produk dengan ID transaksi {id_transaksi}? (iya/tidak)').lower()
                if konfirmasi == 'iya':
                    produk = riwayat.loc[riwayat['ID'] == id_transaksi, 'Produk'].values[0]
                    jumlah = riwayat.loc[riwayat['ID'] == id_transaksi, 'Jumlah'].values[0]
                    produk_df = pd.read_csv('produk_toko.csv')
                    produk_df.loc[produk_df['Produk'] == produk, 'Stok'] += jumlah
                    produk_df.to_csv('produk_toko.csv', index=False)
                    riwayat.loc[riwayat['ID'] == id_transaksi, 'Status'] = 'Ditolak'
                    riwayat.to_csv('riwayat_transaksi.csv', index=False)
                    print(f"Status transaksi dengan ID {id_transaksi} berhasil diubah menjadi Ditolak.")
                    kembali()
                    menu_admin()
                    break
                elif konfirmasi == 'tidak':
                    print('Status konfirmasi tidak diubah')
                    kembali()
                    menu_admin()
                    break
        else:
            print(f"Transaksi dengan ID {id_transaksi} tidak ditemukan.")
            kembali()
            menu_admin()
    else:
        print('Inputan tidak valid')
        kembali()
        menu_admin()
        



def kelola_produk_admin():
    print('''
=============================
    MENGELOLA PRODUK TOKO    
=============================
1. Daftar Produk
2. Tambah Produk
3. Edit Produk
4. Kembali ke Menu
5. Keluar
=============================
''')
    inputan = input('Pilih menu: [1-5]: ')
    if inputan.isdigit():
        if inputan == '1':
            daftar_produk()
        elif inputan == '2':
            tambah_produk()
        elif inputan == '3':
            menu_edit()
        elif inputan == '4':
            clear_terminal()
            menu_admin()
        elif inputan == '5':
            clear_terminal()
        else:
            print('Inputan tidak sesuai')
            kembali()
            kelola_produk_admin()
    else:
        print('Inputan harus berupa angka')
        kembali()
        kelola_produk_admin()



menu_awal()