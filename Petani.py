import datetime

hasil_panen_petani= []
riwayat_transaksi = []

def tampilkan_menu():
    print("/n=== menu petani ===")
    print("1. Tambahkan produk")
    print("2. lihat produk")
    print("3. konfirmasi transaksi")
    print("4. lihat riwayat transaksi")
    print("5. keluar")

def tambah_produk():
    nama_produk = input("masukkan nama hasil panen: ")
    harga_produk = float(input("masukkan harga hasil panen (per unit): "))
    jumlah_produk = int(input("masukkan jumlah hasil panen (per kg): "))
    hasil_panen_petani.append({
        "nama" : nama_produk,
        "harga" : harga_produk,
        "jumlah" : jumlah_produk
    })

def lihat_produk():
    if not hasil_panen_petani:
        print("belum ada produk yang ditambahkan.")
    else:
        print("/n=== daftar produk ===")
        for i, produk in enumerate(hasil_panen_petani):
            print(f"{i + 1}, {produk['nama']} - Rp{produk['harga']} ({produk['jumlah']} unit)")

def konfirmasi_transaksi():
    lihat_produk()
    if not hasil_panen_petani:
        return
    indeks = int(input("pilih nomor produk untuk transaksi: "))
    if indeks < 0 or indeks >= len(hasil_panen_petani):
        print("Produk tidak ditemukan.")
        return
    jumlah_beli = int(input("Masukkan jumlah produk yang dibeli: "))
    if jumlah_beli > hasil_panen_petani[indeks]['jumlah']:
        print("Jumlah melebihi stok.")
        return
    total_harga = jumlah_beli * hasil_panen_petani[indeks]['harga']
    hasil_panen_petani[indeks]['jumlah'] -= jumlah_beli
    if hasil_panen_petani[indeks]['jumlah'] == 0:
        hasil_panen_petani.pop(indeks)
    tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    riwayat_transaksi.append({
        "nama": hasil_panen_petani[indeks]['nama'],
        "jumlah": jumlah_beli,
        "total": total_harga,
        "tanggal": tanggal
    })
    print(f"Transaksi berhasil! Total harga: Rp{total_harga}")

def lihat_riwayat():
    if not riwayat_transaksi:
        print("Belum ada riwayat transaksi.")
    else:
        print("\n=== Riwayat Transaksi ===")
        for transaksi in riwayat_transaksi:
            print(f"{transaksi['tanggal']} - {transaksi['nama']} ({transaksi['jumlah']} unit): Rp{transaksi['total']}")

while True:
    tampilkan_menu()
    pilihan = input("Pilih menu: ")
    if pilihan == "1":
        tambah_produk()
    elif pilihan == "2":
        lihat_produk()
    elif pilihan == "3":
        konfirmasi_transaksi()
    elif pilihan == "4":
        lihat_riwayat()
    elif pilihan == "5":
        print("Keluar dari program. Terima kasih!")
        break
    else:
        print("Pilihan tidak valid.")