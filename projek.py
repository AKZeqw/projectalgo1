import pandas as pd
import csv

# Membaca CSV menggunakan Pandas
def baca_csv(nama_file):
    try:
        return pd.read_csv(nama_file)
    except FileNotFoundError:
        if nama_file == 'riwayat.csv':
            df = pd.DataFrame(columns=["username", "alamat", "id_produk", "nama_produk", "jumlah", "total"])
        else:
            df = pd.DataFrame(columns=["id_produk", "nama_produk", "harga"])
        df.to_csv(nama_file, index=False)
        return df

# Menyimpan data ke CSV
def tulis_csv(nama_file, data):
    df = baca_csv(nama_file)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(nama_file, index=False)

# Menampilkan daftar produk
def tampilkan_produk():
    print("\n=== Daftar Produk ===")
    produk = baca_csv('produk.csv')
    if produk.empty:
        print("Belum ada produk yang tersedia.")
    else:
        print(produk.to_string(index=False))

# Melakukan pembelian
def beli_produk(username, alamat):
    produk = baca_csv('produk.csv')
    if produk.empty:
        print("Belum ada produk yang dapat dibeli.")
        return
    
    tampilkan_produk()
    try:
        id_produk = int(input("\nMasukkan ID produk yang ingin dibeli: "))
        jumlah = int(input("Masukkan jumlah produk: "))
        produk_terpilih = produk.loc[produk['id_produk'] == id_produk]

        if produk_terpilih.empty:
            print("ID produk tidak valid.")
        else:
            nama_produk = produk_terpilih.iloc[0]['nama_produk']
            harga = int(produk_terpilih.iloc[0]['harga'])
            total = jumlah * harga
            print(f"Anda membeli {jumlah} {nama_produk} dengan total harga: Rp{total}")

            # Simpan transaksi ke riwayat
            tulis_csv('riwayat.csv', {
                "username": username,
                "alamat": alamat,
                "id_produk": id_produk,
                "nama_produk": nama_produk,
                "jumlah": jumlah,
                "total": total
            })
            print("Transaksi berhasil disimpan.")
    except ValueError:
        print("Input tidak valid. Pastikan Anda memasukkan angka untuk ID produk dan jumlah.")

# Melihat riwayat transaksi
def lihat_riwayat(username):
    print("\n=== Riwayat Transaksi Anda ===")
    riwayat = baca_csv('riwayat.csv')
    riwayat_user = riwayat[riwayat['username'] == username]

    if riwayat_user.empty:
        print("Belum ada transaksi.")
    else:
        print(riwayat_user.to_string(index=False))

# Menu utama
def menu(username, alamat):
    while True:
        print("\n=== Menu Pembeli ===")
        print("1. Lihat Daftar Produk")
        print("2. Beli Produk")
        print("3. Lihat Riwayat Transaksi")
        print("4. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            tampilkan_produk()
        elif pilihan == '2':
            beli_produk(username, alamat)
        elif pilihan == '3':
            lihat_riwayat(username)
        elif pilihan == '4':
            print("Terima kasih telah menggunakan aplikasi!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Inisialisasi program
def main():
    print("=== Selamat Datang di Sistem Pembeli ===")
    username = input("Masukkan username Anda: ")
    alamat = input("Masukkan alamat Anda: ")
    menu(username, alamat)

if __name__ == "__main__":
    # Buat file produk.csv jika belum ada (untuk testing)
    produk_awal = pd.DataFrame({
        "id_produk": [1, 2, 3],
        "nama_produk": ["Pestisida A", "Pestisida B", "Pupuk Organik"],
        "harga": [50000, 75000, 40000]
    })
    produk_awal.to_csv('produk.csv', index=False, mode='w')  # Hanya dijalankan jika file belum ada
    main()
