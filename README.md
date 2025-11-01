# ProjectAlgo1: Aplikasi E-Commerce CLI Sederhana 🛍️

Ini adalah aplikasi sistem kasir (Point of Sale) atau e-commerce sederhana berbasis konsol (CLI) yang dibangun dengan Python. Aplikasi ini mengelola produk, pengguna (Admin dan Pembeli), dan alur transaksi.

## ✨ Fitur Utama

Aplikasi ini memiliki dua peran pengguna utama dengan fungsionalitas yang berbeda.

### 🙋‍♀️ Fitur Pembeli (Buyer)

* 📝 **Registrasi**: Pengguna baru dapat mendaftarkan akun sebagai pembeli.
* 🔑 **Login**: Pengguna yang sudah terdaftar dapat masuk ke sistem.
* 🛍️ **Lihat Produk**: Pembeli dapat melihat daftar semua produk yang statusnya "Tersedia", diurutkan berdasarkan kategori.
* 🛒 **Lakukan Pembelian**: Pembeli dapat memilih satu atau beberapa produk untuk dibeli, menentukan jumlah, dan melakukan "checkout". Sistem akan meminta alamat pengiriman dan membuat transaksi baru dengan status "Menunggu Konfirmasi".
* 🧾 **Lihat Riwayat Transaksi**: Pembeli dapat melihat riwayat semua transaksi yang telah mereka lakukan, beserta statusnya.

### 🧑‍💼 Fitur Admin

* 🔑 **Login**: Admin memiliki menu khusus saat login.
* 📦 **Mengelola Produk**:
    * 📋 **Daftar Produk**: Melihat semua produk di inventaris (termasuk yang "Tidak Tersedia").
    * ➕ **Tambah Produk**: Menambahkan produk baru ke dalam daftar inventaris (`produk_toko.csv`).
    * ✏️ **Edit Produk**: Mengubah detail produk yang sudah ada, termasuk nama, kategori, harga, stok, dan status (Tersedia/Tidak Tersedia).
* ✅ **Konfirmasi Pembelian**: Admin dapat melihat daftar transaksi yang berstatus "Menunggu Konfirmasi". Dari menu ini, admin dapat:
    * 🚚 **Mengirim**: Mengubah status transaksi menjadi "Dikirim".
    * ❌ **Menolak**: Mengubah status transaksi menjadi "Ditolak" dan secara otomatis mengembalikan stok produk ke inventaris.
* 📚 **Melihat Riwayat Transaksi**: Admin dapat melihat riwayat semua transaksi yang sudah selesai diproses (status "Dikirim" atau "Ditolak").

## 💻 Teknologi yang Digunakan

* **Python**: Bahasa pemrograman utama.
* **Pandas**: Digunakan untuk membaca, memanipulasi, dan menulis data dari/ke file `.csv`.
* **PrettyTable**: Digunakan untuk menampilkan data dalam format tabel yang rapi di terminal.

## ▶️ Cara Menjalankan

1.  Pastikan Anda memiliki Python dan `pip` terinstal.
2.  Instal dependensi yang diperlukan:
    ```bash
    pip install pandas prettytable
    ```
3.  Pastikan Anda memiliki file-file data ini di direktori yang sama dengan `main.py`:
    * `users.csv`
    * `produk_toko.csv`
    * `riwayat_transaksi.csv`
4.  Jalankan aplikasi melalui terminal:
    ```bash
    python main.py
    ```

## 👤 Akun Bawaan

Berdasarkan file `users.csv`, Anda dapat login menggunakan akun berikut untuk menguji:

* **Admin** 👑:
    * Username: `admin`
    * Password: `admin`
* **Pembeli** 🧑‍💻:
    * Username: `agung`
    * Password: `agung`
