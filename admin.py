import pandas as pd
import os
import datetime
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

def menu_admin():
    print(r'''
 __  __  ______  _   _  _    _             _____   __  __  _____  _   _ 
|  \/  ||  ____|| \ | || |  | |     /\    |  __ \ |  \/  ||_   _|| \ | |
| \  / || |__   |  \| || |  | |    /  \   | |  | || \  / |  | |  |  \| |
| |\/| ||  __|  | . ` || |  | |   / /\ \  | |  | || |\/| |  | |  | . ` |
| |  | || |____ | |\  || |__| |  / ____ \ | |__| || |  | | _| |_ | |\  |
|_|  |_||______||_| \_| \____/  /_/    \_\|_____/ |_|  |_||_____||_| \_|
''')
    print('''
========================================
1. Mengelola Produk Toko
2. Menjual Produk ke Petani dan Pembeli
3. Membeli Hasil dari Petani
4. Melihat Riwayat Transaksi
5. Keluar
========================================
''')

    inputan = input('Pilih menu: [1-5]: ')
    if inputan == '1':
        kelola_produk_admin()
    elif inputan == '2':
        jual_produk_admin()
    elif inputan == '3':
        beli_produk_admin()
    elif inputan == '4':
        riwayat_transaksi_admin()
    elif inputan == '5':
        clear_terminal()
    else:
        print('Piihan menu tidak ditemukan')
        menu_admin()

def kelola_produk_admin():
    produk = pd.read_csv('produk_toko.csv')
    print('''
=============================
    MENGELOLA PRODUK TOKO    
=============================
1. Daftar Produk
2. Tambah Produk
3. Edit Produk
7. Kembali ke Menu
=============================
''')
    inputan = input('Pilih menu: [1-7]:')
    if inputan.isdigit():
        if inputan == '1':
            clear_terminal()
            daftar = from_csv(open('produk_toko.csv'))
            # daftar.sortby = 'Kategori'
            print(daftar)
            kembali()
            kelola_produk_admin()
        elif inputan == '2':
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
                            produk_baru = pd.DataFrame([[id,nama_produk,kategori,harga,stok,'Tersedia']], columns=['Id','Produk','Kategori','Harga','Stok','Status'])
                            tabel_tambah_produk = PrettyTable()
                            tabel_tambah_produk.field_names = ['Id','Produk','Kategori','Harga','Stok','Status']
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
        elif inputan == '3':
            daftar = from_csv(open('produk_toko.csv'))
            daftar.sortby = 'Status'
            print(daftar)
            inputan_id_ubah = input(f'Masukkan id produk yang ingin diedit [Pilih 1-{len(produk)}]: ')
            if inputan_id_ubah.isdigit():
                inputan_id_ubah = int(inputan_id_ubah)
                if 0 < int(inputan_id_ubah) <= (len(produk)):
                    produk_dipilih = PrettyTable()
                    produk_dipilih.field_names = ['Id','Produk','Kategori','Harga','Stok','Status']
                    for baris in produk.values:
                        if baris[0] == inputan_id_ubah:
                            produk_dipilih.add_row(baris)
                    while True:
                        print(f'''
=============================
          MENU EDIT
=============================
1. Edit Nama Produk
2. Edit Stok Produk
3. Edit Harga Produk
4. Edit Kategori Produk
5. Edit Status Produk
6. Kembali
=============================
ID PRODUK = {inputan_id_ubah}
=============================
''')
                        inputan = input('Pilih Menu [1-6]: ')
                        if inputan.isdigit():
                            if inputan == '1':
                                clear_terminal()
                                print(produk_dipilih)
                                inputan_nama_produk_baru = input('Masukkan nama baru untuk produk: ').capitalize()
                                produk.loc[produk['Id'] == inputan_id_ubah, 'Produk'] = inputan_nama_produk_baru
                                inputan_konfirmasi_nama = input(f'Apakah anda yakin mengubah nama dari produk dengan id {inputan_id_ubah}? (iya/tidak): ').lower()
                                if inputan_konfirmasi_nama == 'iya':
                                    produk.to_csv('produk_toko.csv', index=False)
                                    print(f'Nama produk dengan ID {inputan_id_ubah} berhasil diubah menjadi {inputan_nama_produk_baru}.')
                                    kembali()
                                    clear_terminal()
                                    continue
                                elif inputan_konfirmasi_nama == 'tidak':
                                    print('Nama produk gagal diubah')
                                    kembali()
                                    clear_terminal()
                                    continue

                                else:
                                    print('Inputan tidak sesuai')
                                    print('Nama produk gagal diubah')
                                    kembali()
                                    clear_terminal()
                                    continue
                            elif inputan == '6':
                                clear_terminal()
                                kelola_produk_admin()
                                break

                else:
                    print('ID tidak ditemukan')
            else:
                print('Inputan harus berupa angka')
        elif inputan == '4':
            clear_terminal()
            menu_admin()
        else:
            print('Inputan harus berupa angka')
    else:
        print('Inputan harus berupa angka')
        kembali()
        kelola_produk_admin()





kelola_produk_admin()