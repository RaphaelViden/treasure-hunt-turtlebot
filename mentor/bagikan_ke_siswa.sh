#!/usr/bin/env bash
# bagikan_ke_siswa.sh - salin folder misi ke home komputer siswa
#
# Jalankan DI KOMPUTER SISWA (atau di Raspberry Pi robot), dari dalam repo ini:
#
#     bash mentor/bagikan_ke_siswa.sh
#
# Script ini hanya menyalin folder siswa/. Folder mentor/ (yang berisi kunci
# jawaban) TIDAK pernah ikut tersalin.

set -euo pipefail

AKAR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TUJUAN="${1:-$HOME}"

if [ ! -d "$AKAR/siswa/treasure_hunt" ]; then
  echo "ERROR: folder siswa/ tidak ditemukan di $AKAR" >&2
  exit 1
fi

echo "Menyalin ke: $TUJUAN"
for ronde in treasure_hunt treasure_hunt_round2; do
  rm -rf "$TUJUAN/$ronde"
  cp -r "$AKAR/siswa/$ronde" "$TUJUAN/$ronde"
done

# bersihkan sisa-sisa yang bisa membocorkan atau membingungkan
find "$TUJUAN/treasure_hunt" "$TUJUAN/treasure_hunt_round2" \
     -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
rm -f "$TUJUAN/treasure_hunt_round2"/jejak_*.svg
rm -f "$TUJUAN/treasure_hunt_round2"/INSTRUKTUR.md \
      "$TUJUAN/treasure_hunt_round2"/KUNCI_JAWABAN.md \
      "$TUJUAN/treasure_hunt_round2"/POLA_RUMAH.svg 2>/dev/null || true

echo
echo "Selesai. Verifikasi isi folder siswa:"
echo
ls -1 "$TUJUAN/treasure_hunt_round2"
echo
echo "Pastikan di daftar di atas TIDAK ADA: KUNCI_JAWABAN.md, POLA_RUMAH.svg, jejak_*.svg"
echo
echo "Siswa mulai dengan:"
echo "    cd ~/treasure_hunt"
echo "    cat README.txt"
