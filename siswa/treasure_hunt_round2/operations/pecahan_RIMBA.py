#!/usr/bin/env python3
"""
PECAHAN POLA: RIMBA
Bagian pola : garis dasar
Ditemukan di: folder operations

File ini hanya SATU POTONG dari sebuah pola. Dijalankan sendiri, robot cuma
bergerak sedikit lalu berhenti. Pola utuh baru muncul kalau kelima pecahan
dijalankan dalam URUTAN YANG BENAR lewat jalankan_pola.py

Cara memakai:
  python3 pecahan_RIMBA.py --simulasi   # lihat gerakannya tanpa robot
  python3 pecahan_RIMBA.py              # jalankan di TurtleBot3 sungguhan

Kata kunci pecahan ini: RODA
(catat kata ini beserta urutan kamu menemukannya!)
"""

import os
import sys

sys.dont_write_bytecode = True  # jangan bikin folder __pycache__

# cari tb3_gerak.py di folder induk, lalu pakai mesin geraknya
_jalur = os.path.dirname(os.path.abspath(__file__))
while not os.path.exists(os.path.join(_jalur, "tb3_gerak.py")):
    _induk = os.path.dirname(_jalur)
    if _induk == _jalur:
        sys.exit("tb3_gerak.py tidak ditemukan. Jangan pindahkan file ini keluar "
                 "dari folder treasure_hunt_round2.")
    _jalur = _induk
sys.path.insert(0, _jalur)

import tb3_gerak

# ---- data gerak pecahan RIMBA ----------------------------------------------
SEGMEN = tb3_gerak.Segmen(
    nama="RIMBA",
    kata="RODA",
    maju_m=1.20,          # meter
    putar_deg=90,      # derajat, positif = putar ke kiri
    catatan="garis dasar",
)

if __name__ == "__main__":
    print(__doc__)
    sys.exit(tb3_gerak.jalankan([SEGMEN]))
