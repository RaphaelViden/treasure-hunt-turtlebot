#!/usr/bin/env python3
"""
jalankan_pola.py - penyusun pola TurtleBot3 (Treasure Hunt Ronde 2)

Kamu sudah menemukan 5 pecahan pola di dalam folder-folder misi. Sekarang
susun pecahan itu SESUAI URUTAN KAMU MENEMUKANNYA, lalu serahkan ke robot.

Contoh pemakaian:
  python3 jalankan_pola.py KILAT RIMBA OMBAK GUNTUR SENJA --simulasi
  python3 jalankan_pola.py KILAT RIMBA OMBAK GUNTUR SENJA

Pilihan:
  --simulasi   lihat jejaknya di terminal + simpan gambar, robot tidak bergerak
  --cek        hanya periksa apakah urutanmu benar (tanpa gerak, tanpa gambar)
  --daftar     tampilkan pecahan yang berhasil ditemukan di folder misi

Kalau urutannya salah, robot tetap berjalan - tapi jejaknya tidak akan
membentuk pola apa pun. Itu bagian dari permainan: coba, lihat, perbaiki.
"""

import hashlib
import importlib.util
import os
import sys

sys.dont_write_bytecode = True  # jangan kotori folder misi dengan __pycache__

AKAR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AKAR)
import tb3_gerak  # noqa: E402

JUMLAH_PECAHAN = 5

# sidik jari (sha256) dari kalimat kunci yang benar.
# urutan yang benar TIDAK ditulis di file ini - jadi tidak bisa dicontek.
SIDIK_JARI_BENAR = "a68467db62d8223349c414d0d4d2d2a1fd1df7186360e4211b358cab63d82ccf"


def temukan_pecahan():
    """Cari semua file pecahan_*.py di dalam folder misi."""
    hasil = {}
    for folder, _, berkas_list in os.walk(AKAR):
        for berkas in sorted(berkas_list):
            if berkas.startswith("pecahan_") and berkas.endswith(".py"):
                jalur = os.path.join(folder, berkas)
                nama = berkas[len("pecahan_"):-len(".py")]
                hasil[nama.upper()] = jalur
    return hasil


def muat_segmen(nama, jalur):
    spec = importlib.util.spec_from_file_location(f"pecahan_{nama}", jalur)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul.SEGMEN


def kalimat_kunci(segmen_list):
    return " ".join(s.kata.upper() for s in segmen_list)


def periksa_urutan(segmen_list):
    kalimat = kalimat_kunci(segmen_list)
    sidik = hashlib.sha256(kalimat.encode()).hexdigest()
    return sidik == SIDIK_JARI_BENAR, kalimat


def main(argumen):
    pilihan = [a for a in argumen if a.startswith("-")]
    nama_list = [a.upper() for a in argumen if not a.startswith("-")]
    tersedia = temukan_pecahan()

    if "--daftar" in pilihan:
        print(f"\nPecahan yang ada di folder misi ({len(tersedia)}/{JUMLAH_PECAHAN}):")
        for nama in sorted(tersedia):
            print(f"  {nama:<8} -> {os.path.relpath(tersedia[nama], AKAR)}")
        if len(tersedia) < JUMLAH_PECAHAN:
            print("\n  Masih ada pecahan yang belum ketemu. Lanjutkan petunjuknya!")
        return 0

    if "--help" in pilihan or "-h" in pilihan or not nama_list:
        print(__doc__)
        print(f"Pecahan terdeteksi: {', '.join(sorted(tersedia)) or '(belum ada)'}")
        return 0

    # --- validasi nama pecahan ---
    tidak_dikenal = [n for n in nama_list if n not in tersedia]
    if tidak_dikenal:
        print(f"\nPecahan ini tidak ada di folder misi: {', '.join(tidak_dikenal)}")
        print(f"Yang tersedia: {', '.join(sorted(tersedia))}")
        print("Tips: 'python3 jalankan_pola.py --daftar'")
        return 1

    if len(set(nama_list)) != len(nama_list):
        print("\nAda pecahan yang kamu tulis dua kali. Setiap pecahan dipakai sekali.")
        return 1

    segmen_list = [muat_segmen(n, tersedia[n]) for n in nama_list]

    print("\n=== POLA YANG KAMU SUSUN ===")
    for i, s in enumerate(segmen_list, 1):
        print(f"  {i}. {s.nama:<8} [{s.catatan}]  kata: {s.kata}")

    benar, kalimat = periksa_urutan(segmen_list)
    print(f"\n  Kalimat kunci dari urutanmu: \"{kalimat}\"")

    if len(nama_list) < JUMLAH_PECAHAN:
        print(f"  Baru {len(nama_list)} dari {JUMLAH_PECAHAN} pecahan. "
              "Pola belum mungkin utuh.")
    elif benar:
        print("  STATUS: URUTAN BENAR. Pola akan terbentuk sempurna!")
    else:
        print("  STATUS: URUTAN BELUM BENAR. Jejak robot tidak akan membentuk pola.")
        print("          Periksa lagi catatan urutan penemuan pecahanmu.")

    if "--cek" in pilihan:
        return 0 if benar else 2

    berkas_svg = os.path.join(
        AKAR, "jejak_benar.svg" if benar else "jejak_percobaan.svg")
    return tb3_gerak.jalankan(segmen_list, pilihan, berkas_svg)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
