def pembelian(username):
    daftar_produk = pd.read_csv('produk_toko.csv')
    daftar_beli = []
    total_pembelian = 0

    while True:
        clear_terminal()
        daftar_produk_pembeli()
        id_produk = input("Masukkan ID Produk yang ingin dibeli (atau ketik 'keluar' untuk keluar): ")

        if id_produk.lower() == 'keluar':  # Keluar dari proses pembelian
            break
        elif not id_produk.isdigit():  # Validasi ID produk
            print("Input ID produk tidak valid. Harap masukkan angka.")
            kembali()
            continue

        id_produk = int(id_produk)
        # produk_ditemukan = False

        for baris in daftar_produk.values:
            if baris[0] == id_produk and baris[5] == 'Tersedia':
                # produk_ditemukan = True
                produk = baris[1]
                harga = baris[3]
                stok = baris[4]

                tabel = PrettyTable()
                tabel.field_names = ['Produk', 'Harga', 'Stok']
                tabel.add_row([produk, harga, stok])
                print(tabel)

                try:
                    jumlah = int(input("Masukkan jumlah pembelian: "))
                    if jumlah <= 0:
                        print("Jumlah pembelian harus lebih besar dari 0.")
                        kembali()
                        clear_terminal()
                        continue
                    elif jumlah > stok:
                        print("Jumlah melebihi stok. Silakan masukkan jumlah yang lebih kecil.")
                        kembali()
                        clear_terminal()
                        continue
                    else:
                        total_harga = jumlah * harga
                        total_pembelian += total_harga
                        daftar_beli.append([produk, jumlah, total_harga])

                        print(f"Total harga untuk {produk}: {total_harga}")

                        lanjut = input("Apakah Anda ingin membeli produk lain? [iya/tidak]: ").lower()
                        if lanjut == 'tidak':
                            break
                        elif lanjut != 'iya':
                            print("Input tidak valid. Kembali ke menu pembelian.")
                            kembali()
                        else:
                            print('Inputan tidak valid')

                except ValueError:
                    print("Input jumlah pembelian tidak valid. Harap masukkan angka.")
                    kembali()
                break

            else:
                print("Produk tidak ditemukan")
                kembali()

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
    else:  # Jika tidak ada pembelian
        print("Tidak ada produk yang dibeli.")
