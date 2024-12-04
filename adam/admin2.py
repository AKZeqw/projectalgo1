import pandas as pd

# Fungsi untuk menjual produk berdasarkan role (petani atau pembeli)
def jual_produk(role, harga_produk):
    if role == 'petani':
        # Memberikan diskon 10% untuk petani
        harga_diskon = harga_produk * 0.9
        return harga_diskon
    elif role == 'pembeli':
        # Harga produk untuk pembeli tanpa diskon
        return harga_produk
    else:
        print("Role tidak dikenali. Pembelian dibatalkan.")
        return None

# Fungsi untuk memproses penjualan produk
def proses_penjualan(role):
    # Membaca data produk dari CSV
    produk_df = pd.read_csv('produk_toko.csv')

    keranjang = []  # Menyimpan produk yang dipilih dalam keranjang
    total_harga = 0  # Total harga dari semua produk di keranjang

    while True:
        # Menampilkan daftar produk yang tersedia
        print("\nDaftar Produk Tersedia:")
        print(produk_df[['Id', 'Produk', 'Harga', 'Stok', 'Status']])

        # Meminta input pengguna untuk memilih produk
        try:
            inputan_id = int(input("Masukkan ID produk yang ingin dibeli: "))
        except ValueError:
            print("ID produk tidak valid.")
            continue

        # Memeriksa apakah produk tersedia di stok
        produk_terpilih = produk_df[produk_df['Id'] == inputan_id]

        if produk_terpilih.empty:
            print("Produk tidak ditemukan.")
            continue

        # Menampilkan informasi produk yang dipilih
        produk_terpilih = produk_terpilih.iloc[0]
        print(f"\nProduk yang Anda pilih: {produk_terpilih['Produk']}, Harga: {produk_terpilih['Harga']}, Stok: {produk_terpilih['Stok']}")

        # Memeriksa ketersediaan stok
        if produk_terpilih['Stok'] <= 0:
            print(f"Produk {produk_terpilih['Produk']} saat ini tidak tersedia.")
            continue

        # Meminta input jumlah barang yang ingin dibeli
        try:
            jumlah = int(input(f"Masukkan jumlah {produk_terpilih['Produk']} yang ingin dibeli: "))
        except ValueError:
            print("Jumlah tidak valid. Harap masukkan angka.")
            continue

        # Memeriksa apakah jumlah yang diminta tersedia dalam stok
        if jumlah > produk_terpilih['Stok']:
            print(f"Stok {produk_terpilih['Produk']} tidak mencukupi. Hanya tersedia {produk_terpilih['Stok']} unit.")
            continue

        # Menghitung harga total untuk produk yang dipilih
        harga_produk = jual_produk(role, produk_terpilih['Harga'])  # Mendapatkan harga setelah diskon (jika petani)
        total_harga_produk = harga_produk * jumlah
        print(f"Harga total untuk {jumlah} unit {produk_terpilih['Produk']}: {total_harga_produk}")

        # Menambahkan produk ke dalam keranjang
        keranjang.append({
            'Produk': produk_terpilih['Produk'],
            'Harga Satuan': harga_produk,
            'Jumlah': jumlah,
            'Total Harga': total_harga_produk
        })

        # Mengurangi stok produk di DataFrame
        produk_df.loc[produk_df['Id'] == inputan_id, 'Stok'] -= jumlah

        # Menanyakan apakah ingin menambah produk lain
        lagi = input("Apakah Anda ingin menambah produk lain? (iya/tidak): ").lower()
        if lagi != 'iya':
            break

    # Menampilkan total harga di keranjang
    print("\nKeranjang Belanja Anda:")
    total_harga_keranjang = 0
    for item in keranjang:
        print(f"{item['Produk']} - {item['Jumlah']} x {item['Harga Satuan']} = {item['Total Harga']}")
        total_harga_keranjang += item['Total Harga']

    print(f"\nTotal Harga Keranjang: {total_harga_keranjang}")

    # Konfirmasi Pembelian
    inputan_konfirmasi = input(f"Apakah Anda ingin membeli produk di keranjang seharga {total_harga_keranjang}? (iya/tidak): ").lower()

    if inputan_konfirmasi == 'iya':
        # Menyimpan perubahan stok produk ke CSV
        produk_df.to_csv('produk_toko.csv', index=False)
        print(f"Pembelian berhasil. Total harga yang harus dibayar: {total_harga_keranjang}.")
    else:
        print("Pembelian dibatalkan.")

# Program utama
def main():
    # Misalnya, role pengguna sudah ditentukan setelah registrasi (bisa diambil dari session/login)
    role_pengguna = 'petani'  # Contoh, role yang sudah ditentukan sebelumnya (petani atau pembeli)
    
    print(f"\nSelamat datang, role Anda adalah {role_pengguna}!")
    
    while True:
        print("\nSelamat datang di toko kami!")
        proses_penjualan(role_pengguna)  # Memproses penjualan berdasarkan role pengguna
        lagi = input("Apakah Anda ingin melakukan pembelian lagi? (iya/tidak): ").lower()
        if lagi != 'iya':
            print("Terima kasih telah berbelanja! Sampai jumpa.")
            break

if __name__ == "__main__":
    main()
