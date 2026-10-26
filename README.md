# TurtleBot3 Treasure Hunt

Game terminal Linux untuk anak SMA, dua ronde, ujungnya robot bergerak sendiri.

| | |
|---|---|
| **Ronde 1** | Treasure hunt murni. Cari `treasure.txt` hanya dengan `pwd` `ls` `cd` `cat`. |
| **Ronde 2** | Hunt + robot. Cari 5 pecahan script gerak. Urutan penemuan = urutan pola. Benar → jejak roda menggambar RUMAH dan robot pulang ke titik start. Salah → garis acak. |

## Struktur repo

```
siswa/     <- yang dibagikan ke peserta
  treasure_hunt/           ronde 1
  treasure_hunt_round2/    ronde 2 (berisi 5 pecahan pola tersembunyi)

mentor/    <- JANGAN dibagikan, ada kunci jawabannya
  KUNCI_JAWABAN.md         jawaban, rundown sesi, rubrik skor, cara bikin varian
  rekam_jejak.py           rekam jejak asli robot dari topic /odom
  bagikan_ke_siswa.sh      salin folder siswa/ ke ~ dengan bersih
  POLA_RUMAH.svg           gambar pola jawaban
  hasil_simulasi_*.txt     transkrip simulasi urutan benar & salah
  rekaman/                 CSV contoh + hasil rekaman tiap tim
```

## Mulai dari mana

**Mentor** — baca [`mentor/KUNCI_JAWABAN.md`](mentor/KUNCI_JAWABAN.md).

**Membagikan ke komputer siswa** — jalankan di tiap komputer peserta:

```bash
bash mentor/bagikan_ke_siswa.sh
```

**Siswa** — mulai dari `cd ~/treasure_hunt` lalu `cat README.txt`.

## Butuh apa

- **Mode simulasi**: cuma `python3`. Tanpa ROS, tanpa robot. Jejaknya digambar
  ASCII di terminal + file SVG. Pakai ini supaya 10 tim tidak mengantre satu robot.
- **Mode robot**: ROS 2 (Humble/Jazzy) + TurtleBot3 bringup jalan, topic
  `/cmd_vel` dan `/odom` hidup, `ROS_DOMAIN_ID` laptop dan robot sama.
  Gerakannya closed-loop baca `/odom`, bukan berbasis timer.
- **Arena**: ruang kosong ±2 × 2 meter, lantai bersih.
