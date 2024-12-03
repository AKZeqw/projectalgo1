import csv
import pandas as pd
import datetime as dt
import os

teks_username = r'''
 _____           _ __  __            _   
|_   _|_ _ _ __ (_)  \/  | __ _ _ __| |_ 
  | |/ _` | '_ \| | |\/| |/ _` | '__| __|.
  | | (_| | | | | | |  | | (_| | |  | |_ 
  |_|\__,_|_| |_|_|_|  |_|\__,_|_|   \__|'''

def clear_terminal():
    os.system('cls')

def login():
    users = pd.read_csv('users.csv')
    username = input('Masukkan Username: ')
    if username in users['username'].values:
        baris_user = users[users['username'] == username]
        password = input('Masukkan Password: ')
        if password == baris_user['password'].values[0]:
            role = baris_user['role'].values[0] #Mengecek role
            if role == 'admin':
                'menu admin'
            elif role == 'petani':
                'menu petani'
            elif role == 'pembeli':
                'menu pembeli'
        else:
            print('Password salah') #Jika password salah
            kembali()
            menu_awal()
    else:
        print('Username tidak ditemukan') #Jika username salah
        kembali()
        menu_awal()

def kembali():
    inputan_kembali = input('Tekan enter untuk kembali...')
    if inputan_kembali == '':
        clear_terminal()
    else:
        kembali()


def daftar():
    if not os.path.exists('users.csv'):
        df = pd.DataFrame(columns=['username','password','role'])
        df.to_csv('users.csv', index=False)
    else:
        df = pd.read_csv('users.csv')
    print('Kosongi username jika ingin kembali ke menu awal')
    username = input('Masukkan username(Harus lebih dari 4 huruf): ')
    if username == '':
        clear_terminal()
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


def menu_awal():
    print(teks_username)
    print('''
1. Registrasi
2. Login
3. Keluar ''')
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
        clear_terminal()
        print('Pilihan menu tidak ditemukan!')
        menu_awal()

menu_awal()
#Diskon petani untuk pembelian
print("Hello word")