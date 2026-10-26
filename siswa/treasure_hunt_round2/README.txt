TURTLEBOT3 TREASURE HUNT - RONDE 2
==================================
"Pecahan Pola"

CERITA
------
Di ronde 1 kalian sudah berhasil menemukan treasure.txt hanya dengan
perintah terminal. Sekarang levelnya naik.

Seorang teknisi menulis sebuah POLA GERAK untuk TurtleBot3, lalu memecahnya
menjadi 5 file terpisah dan menyembunyikannya di dalam folder-folder misi ini.
Setiap file hanya satu potong gerakan. Potongan itu TIDAK BERNOMOR.

Satu-satunya cara mengetahui urutannya adalah dengan mengikuti petunjuk dari
folder ke folder - persis seperti ronde 1. Urutan kalian MENEMUKAN pecahan
itulah urutan yang benar.

Kalau urutannya benar, jejak roda robot akan menggambar sebuah bentuk yang
jelas dan robot kembali tepat ke titik start. Kalau urutannya salah, robot
tetap jalan - tapi jejaknya cuma garis acak. Pola tidak terbentuk.


YANG HARUS KALIAN LAKUKAN
-------------------------
1. Mulai dari folder ini, ikuti petunjuk di dalam file .txt
2. Setiap kali menemukan file bernama  pecahan_XXXXX.py
   -> CATAT namanya di lembar jawab, berurutan sesuai saat kalian menemukannya
3. Setelah kelima pecahan terkumpul dan treasure.txt ditemukan,
   susun polanya dan jalankan di robot


PERINTAH YANG BOLEH DIPAKAI
---------------------------
  pwd          melihat kalian sedang ada di folder mana
  ls           melihat isi folder
  ls -a        melihat isi folder termasuk yang tersembunyi
  cd NAMA      masuk ke folder
  cd ..        naik satu folder
  cat FILE     membaca isi file

MULAI
-----
  cd ~/treasure_hunt_round2
  pwd
  ls
  cat README.txt
  cat operations/briefing.txt


ATURAN
------
1. DILARANG memakai find, locate, grep, tree, atau pencarian otomatis lain.
2. DILARANG membuka file .py dengan editor untuk mencari urutan. Baca
   petunjuk .txt saja. (Boleh cat file pecahan untuk melihat isinya -
   di situ tidak ada nomor urut, jadi tidak membantu kalau tidak mengikuti
   petunjuk.)
3. Urutan pecahan hanya boleh ditentukan dari urutan penemuan.


MENJALANKAN POLA
----------------
Mode simulasi (TANPA robot - jejaknya digambar di terminal).
Pakai ini dulu untuk mengecek tebakan kalian:

  python3 jalankan_pola.py NAMA1 NAMA2 NAMA3 NAMA4 NAMA5 --simulasi

Mode robot sungguhan (TurtleBot3 harus sudah menyala dan terhubung):

  python3 jalankan_pola.py NAMA1 NAMA2 NAMA3 NAMA4 NAMA5

Perintah bantu lain:

  python3 jalankan_pola.py --daftar     lihat pecahan apa saja yang sudah ada
  python3 jalankan_pola.py A B C D E --cek    cek urutan saja, robot tak bergerak
  python3 operations/pecahan_RIMBA.py --simulasi    coba satu pecahan saja


KEAMANAN
--------
- Pola butuh ruang kosong kira-kira 2 x 2 meter. Bersihkan lantainya.
- Satu orang wajib siap menekan Ctrl+C atau mengangkat robot kalau melenceng.
- Jangan jalankan robot di atas meja.


SKOR
----
  Menemukan kelima pecahan            40
  Urutan pecahan benar                30
  Pola terbentuk di robot sungguhan   20
  Bisa menjelaskan pwd/ls/cd/cat      10
