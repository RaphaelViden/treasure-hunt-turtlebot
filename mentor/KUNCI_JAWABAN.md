# Kunci Jawaban & Panduan Mentor — Ronde 2

> **Seluruh folder `mentor/` ini jangan pernah disalin ke komputer siswa.**
> Pakai `bash mentor/bagikan_ke_siswa.sh` untuk membagikan — script itu hanya
> menyalin `siswa/`, jadi kunci jawaban tidak mungkin ikut terbawa.

## Jawaban

Urutan pecahan yang benar — sama dengan urutan folder di rantai petunjuk:

| # | Pecahan | Lokasi | Gerakan | Kata kunci | Bagian pola |
|---|---------|--------|---------|------------|-------------|
| 1 | `RIMBA`  | `operations/` | maju 1.20 m, putar kiri 90° | RODA | garis dasar |
| 2 | `OMBAK`  | `fieldwork/observations/` | maju 0.80 m, putar kiri 45° | BERPUTAR | dinding kanan |
| 3 | `KILAT`  | `telemetry/` | maju 0.85 m, putar kiri 90° | POLA | atap kanan |
| 4 | `SENJA`  | `diagnostics/network/` | maju 0.85 m, putar kiri 45° | RUMAH | atap kiri |
| 5 | `GUNTUR` | `documentation/procedures/completion/` | maju 0.80 m, putar kiri 90° | TERBENTUK | dinding kiri |

Kalimat kunci: **"RODA BERPUTAR POLA RUMAH TERBENTUK"**

Perintah penuhnya:

```bash
cd siswa/treasure_hunt_round2
python3 jalankan_pola.py RIMBA OMBAK KILAT SENJA GUNTUR --simulasi
```

Output lengkapnya sudah tersimpan di `hasil_simulasi_benar.txt` dan
`hasil_simulasi_salah.txt`, jadi kamu tidak perlu menjalankan apa pun untuk
tahu jawabannya.

## Pola yang terbentuk: RUMAH

Lihat `POLA_RUMAH.svg` (buka di browser) untuk gambar jejak yang benar.

```
            atap (apex)
                /\
               /  \
              /    \
             +------+   <- dinding 0.80 m
             |      |
             |      |
             +======+   <- dasar 1.20 m (START di sudut kanan bawah)
```

- Bidang kerja: **1.20 m lebar × 1.40 m tinggi** → siapkan ruang kosong ±2 × 2 m.
- Total jarak tempuh: 4.50 m (≈21.7 putaran roda Burger).
- Total putaran: tepat 360°, jadi robot **kembali ke titik start dengan arah hadap semula**.
- Selisih titik akhir ke titik awal secara matematis: 0.2 cm.

## Kenapa urutan salah = pola gagal

Total jarak (4.50 m) dan total putaran (360°) **selalu sama** untuk urutan apa pun,
karena hanya dipermutasi. Yang berubah adalah *arah hadap robot saat tiap jarak
ditempuh*. Jadi jejaknya jadi bangun terbuka yang acak dan robot berhenti jauh dari
start. Ini poin pengajarannya: **urutan perintah itu bermakna, bukan cuma daftar.**

Contoh untuk ditunjukkan di kelas (urutan salah):

```bash
python3 jalankan_pola.py KILAT RIMBA GUNTUR OMBAK SENJA --simulasi
# -> jarak titik akhir ke titik awal: 68.1 cm, bentuk tidak menutup
```

## Persiapan sebelum sesi

### 1. Bagikan folder misi ke komputer siswa

Jalankan di tiap komputer siswa (atau di Raspberry Pi robot), dari dalam repo:

```bash
bash mentor/bagikan_ke_siswa.sh
```

Hasilnya `~/treasure_hunt` dan `~/treasure_hunt_round2` yang sudah bersih
dari kunci jawaban, gambar pola, dan `__pycache__`. Script-nya menampilkan
daftar isi folder di akhir — pastikan tidak ada `KUNCI_JAWABAN.md`,
`POLA_RUMAH.svg`, atau `jejak_*.svg` di situ.

Salin folder yang sama ke semua tim supaya adil.

### 2. Cek Python dan ROS

Mode simulasi hanya butuh `python3` — tidak perlu ROS sama sekali.

Untuk mode robot: ROS 2 (Humble/Jazzy) + TurtleBot3 bringup jalan,
`ROS_DOMAIN_ID` laptop dan robot sama. Cek cepat:

```bash
ros2 topic list | grep -E 'cmd_vel|odom'
ros2 topic echo /odom --once
```

Kalau `/odom` tidak keluar apa-apa, `rekam_jejak.py` juga tidak akan jalan.

### 3. Siapkan arena

Ruang kosong ±2 × 2 m. Tandai titik START dengan lakban, **termasuk arah
hadap awal robot** (tempel lakban panah). Pola selalu berputar ke kiri,
jadi seluruh gambar rumah terbentuk di sisi kiri-depan robot.

## Alur sesi yang disarankan (90 menit)

| Waktu | Kegiatan |
|-------|----------|
| 10 m | Review ronde 1, demo `pwd ls cd cat` |
| 30 m | Hunting 5 pecahan (ronde 2), tim mencatat urutan di lembar jawab |
| 15 m | Uji urutan di **mode simulasi**, lihat jejak ASCII |
| 25 m | Jalankan di TurtleBot3 sungguhan, satu tim per sesi, rekam jejak |
| 10 m | Presentasi tim + penilaian |

## Merekam jejak robot

### Cara utama: rekam dari topic `/odom` (disarankan)

TurtleBot3 terus-menerus menyiarkan posisinya sendiri di topic `/odom`.
`rekam_jejak.py` berlangganan topic itu, mencatat tiap titik ke CSV, lalu
menggambarnya jadi SVG **dengan pola ideal ditumpuk sebagai pembanding**.
Tidak perlu spidol, karton, atau rekam video.

Butuh tiga terminal:

```bash
# terminal 1 - di robot / Raspberry Pi
ros2 launch turtlebot3_bringup robot.launch.py
```

```bash
# terminal 2 - laptop mentor, mulai merekam (biarkan jalan)
cd mentor
python3 rekam_jejak.py --rekam tim_01
```

```bash
# terminal 3 - laptop siswa, tim menjalankan polanya
cd ~/treasure_hunt_round2
python3 jalankan_pola.py RIMBA OMBAK KILAT SENJA GUNTUR
```

Robot berhenti → kembali ke terminal 2 → **Ctrl+C**. Keluar:

- `mentor/rekaman/tim_01.csv` — data mentah x, y, sudut, waktu
- `mentor/rekaman/tim_01.svg` — gambar jejak + pola ideal + putusan

Script langsung mencetak penilaian:

```
titik terekam        : 450
panjang jalur asli   : 4.40 m  (ideal 4.50 m)
akhir ke start       : 9.2 cm  (ideal ~0 cm)
simpangan maks dari pola ideal : 6.2 cm
putusan              : POLA TERBENTUK - bentuk rumah dan robot pulang ke start
```

Ambang putusannya: simpangan < 15 cm **dan** jarak akhir-ke-start < 20 cm
= pola terbentuk. Ubah di fungsi `laporkan()` kalau lantainya licin dan
robot sering slip.

Pilihan lain:

```bash
python3 rekam_jejak.py --rekam tim_01 --durasi 90   # berhenti otomatis
python3 rekam_jejak.py --gambar rekaman/tim_01.csv  # gambar ulang dari CSV
python3 rekam_jejak.py --topic /robot1/odom         # kalau topic di-remap
python3 rekam_jejak.py --ideal                      # gambar pola ideal saja
```

Dua CSV contoh sudah disiapkan (data sintetis, bukan dari robot asli) supaya
kamu bisa melihat bentuk laporannya sebelum hari-H:

```bash
python3 rekam_jejak.py --gambar rekaman/contoh_urutan_benar.csv
python3 rekam_jejak.py --gambar rekaman/contoh_urutan_salah.csv
```

> Catatan: `rekam_jejak.py` otomatis menggeser dan memutar jejak rekaman
> supaya mulai di (0,0) menghadap sumbu +X. Jadi kamu tidak perlu mereset
> odometry robot dulu sebelum merekam.

### Cara cadangan kalau ROS bermasalah

1. **Spidol** — ikat spidol menggantung di belakang robot, jalankan di atas
   kertas karton/manila yang disambung. Hasil paling memuaskan untuk dipajang.
2. **Lakban** — tempel lakban kecil tiap kali robot berhenti berputar
   (ada 5 sudut), lalu hubungkan dengan benang.
3. **Video dari atas** — rekam dari kursi atau tangga, lalu putar cepat.

## Penilaian

| Komponen | Poin |
|----------|------|
| Menemukan kelima pecahan | 40 |
| Urutan pecahan benar (status `URUTAN BENAR`) | 30 |
| Pola terbentuk di robot sungguhan | 20 |
| Menjelaskan `pwd` / `ls` / `cd` / `cat` | 10 |

Bonus 10 poin: tim bisa menjelaskan kenapa total jarak dan total putaran tetap
sama meski urutannya salah.

## Kalau mau diubah / dibuat varian

Semua angka gerakan ada di tiap file `pecahan_*.py` pada blok `SEGMEN`
(`maju_m` dan `putar_deg`). Mengubah pola berarti:

1. Ubah `maju_m` / `putar_deg` di kelima file.
2. Ubah `kata` di kelima file kalau mau kalimat kunci baru.
3. Hitung ulang sidik jarinya dan tempel ke `SIDIK_JARI_BENAR` di `jalankan_pola.py`:
   ```bash
   python3 -c "import hashlib;print(hashlib.sha256(b'KALIMAT KUNCI BARU').hexdigest())"
   ```
4. Verifikasi: `python3 jalankan_pola.py A B C D E --simulasi` harus menutup (±0 cm).
5. Samakan `POLA_IDEAL` di `mentor/rekam_jejak.py`, lalu `python3 rekam_jejak.py --ideal`
   untuk membuat ulang gambar jawabannya.

Ganti juga nama pecahannya kalau kelas yang sama mengulang permainan — nama
`RIMBA/OMBAK/KILAT/SENJA/GUNTUR` sengaja tidak urut alfabet supaya tidak
membocorkan urutan.

## Berkas teknis

Folder `siswa/treasure_hunt_round2/` (dibagikan ke peserta):

| Berkas | Isi |
|--------|-----|
| `tb3_gerak.py` | mesin gerak: ROS 2 closed-loop pakai `/odom`, + simulator & penggambar jejak |
| `jalankan_pola.py` | menyusun pecahan, verifikasi urutan (sha256), jalankan/simulasi |
| `pecahan_*.py` | satu segmen gerak masing-masing, bisa dijalankan sendiri |

Folder `mentor/` (jangan dibagikan):

| Berkas | Isi |
|--------|-----|
| `KUNCI_JAWABAN.md` | dokumen ini |
| `rekam_jejak.py` | rekam `/odom` → CSV + SVG, tumpuk dengan pola ideal, beri putusan |
| `bagikan_ke_siswa.sh` | salin `siswa/` ke `~` dengan bersih |
| `POLA_RUMAH.svg` | gambar pola jawaban |
| `hasil_simulasi_benar.txt` | transkrip simulasi urutan benar |
| `hasil_simulasi_salah.txt` | transkrip simulasi contoh urutan salah |
| `rekaman/contoh_*.csv` | data contoh untuk mencoba `--gambar` tanpa robot |

Kecepatan default aman untuk indoor: 0.12 m/s maju, 0.5 rad/s putar
(ubah di `tb3_gerak.py` bagian `KECEPATAN_MAJU` / `KECEPATAN_PUTAR`).
