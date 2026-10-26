#!/usr/bin/env python3
"""
PECAHAN POLA: OMBAK
Bagian pola : sisi kanan
Ditemukan di: folder fieldwork/observations

File ini hanya SATU POTONG dari sebuah pola. Dijalankan sendiri, robot cuma
bergerak sedikit lalu berhenti. Pola utuh baru muncul kalau kelima pecahan
dijalankan dalam URUTAN YANG BENAR lewat jalankan_pola.py

Cara memakai:
  python3 pecahan_OMBAK.py --simulasi   # lihat gerakannya tanpa robot
  python3 pecahan_OMBAK.py              # jalankan di TurtleBot3 sungguhan

Kata kunci pecahan ini: BERPUTAR
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

# ---- data gerak pecahan OMBAK ----------------------------------------------
SEGMEN = tb3_gerak.Segmen(
    nama="OMBAK",
    kata="BERPUTAR",
    maju_m=0.80,          # meter
    putar_deg=45,      # derajat, positif = putar ke kiri
    catatan="sisi kanan",
)

if __name__ == "__main__":
    print(__doc__)
    sys.exit(tb3_gerak.jalankan([SEGMEN]))
