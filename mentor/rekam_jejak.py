#!/usr/bin/env python3
"""
rekam_jejak.py - merekam jejak asli TurtleBot3 dari topic /odom (ALAT MENTOR)

Robot terus menyiarkan posisinya sendiri di topic /odom. Script ini berlangganan
topic itu, mencatat setiap titik ke file CSV, lalu menggambarnya jadi SVG dengan
POLA IDEAL ditumpuk di belakangnya sebagai pembanding. Jadi tidak perlu spidol,
lakban, atau rekam video.

File ini SENGAJA berdiri sendiri (tidak mengimpor tb3_gerak.py) supaya folder
mentor/ tetap utuh walau folder siswa/ sudah disalin ke laptop lain.

=== CARA PAKAI ===

Di terminal 1 - nyalakan robot:
    ros2 launch turtlebot3_bringup robot.launch.py

Di terminal 2 - mulai merekam (biarkan jalan):
    python3 rekam_jejak.py --rekam tim_01

Di terminal 3 - suruh tim menjalankan polanya:
    cd ~/treasure_hunt_round2
    python3 jalankan_pola.py RIMBA OMBAK KILAT SENJA GUNTUR

Setelah robot berhenti, kembali ke terminal 2 dan tekan Ctrl+C.
Hasilnya: rekaman/tim_01.csv dan rekaman/tim_01.svg

Pilihan lain:
    python3 rekam_jejak.py --rekam tim_01 --durasi 90   berhenti otomatis 90 detik
    python3 rekam_jejak.py --gambar rekaman/tim_01.csv  gambar ulang dari CSV
    python3 rekam_jejak.py --topic /robot1/odom         kalau nama topic berbeda
    python3 rekam_jejak.py --ideal                      gambar pola ideal saja
"""

import csv
import math
import os
import sys

sys.dont_write_bytecode = True

AKAR = os.path.dirname(os.path.abspath(__file__))
FOLDER_REKAMAN = os.path.join(AKAR, "rekaman")

# Pola jawaban ronde 2 (bentuk RUMAH): (maju meter, putar derajat ke kiri)
POLA_IDEAL = [
    ("RIMBA", 1.20, 90),   # garis dasar
    ("OMBAK", 0.80, 45),   # dinding kanan
    ("KILAT", 0.85, 90),   # atap kanan
    ("SENJA", 0.85, 45),   # atap kiri
    ("GUNTUR", 0.80, 90),  # dinding kiri
]

# simpan titik baru kalau robot sudah bergerak sejauh ini (meter)
JARAK_MINIMAL_CATAT = 0.01


# =============================================================================
#  geometri
# =============================================================================

def jejak_ideal():
    x = y = 0.0
    sudut = 0.0
    titik = [(0.0, 0.0)]
    for _, maju, putar in POLA_IDEAL:
        x += maju * math.cos(sudut)
        y += maju * math.sin(sudut)
        titik.append((x, y))
        sudut += math.radians(putar)
    return titik


def selaraskan(titik, sudut_awal_rad):
    """Geser & putar jejak rekaman supaya mulai di (0,0) menghadap sumbu +X.

    Penting karena odometry robot tidak selalu nol saat perekaman dimulai
    (misalnya robot sudah pernah digerakkan manual sebelumnya).
    """
    if not titik:
        return titik
    x0, y0 = titik[0]
    c, s = math.cos(-sudut_awal_rad), math.sin(-sudut_awal_rad)
    hasil = []
    for x, y in titik:
        dx, dy = x - x0, y - y0
        hasil.append((dx * c - dy * s, dx * s + dy * c))
    return hasil


def _jarak_ke_segmen(p, a, b):
    (px, py), (ax, ay), (bx, by) = p, a, b
    dx, dy = bx - ax, by - ay
    panjang2 = dx * dx + dy * dy
    if panjang2 == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / panjang2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def panjang_jalur(titik, langkah=0.05):
    """Panjang jalur, diukur tiap >=5 cm.

    Kalau dihitung dari tiap titik mentah, derau odometry (±0.5 cm per sampel)
    ikut dijumlahkan dan panjangnya jadi terlihat jauh lebih besar dari aslinya.
    """
    if len(titik) < 2:
        return 0.0
    total = 0.0
    acuan = titik[0]
    for p in titik[1:]:
        d = math.hypot(p[0] - acuan[0], p[1] - acuan[1])
        if d >= langkah:
            total += d
            acuan = p
    return total + math.hypot(titik[-1][0] - acuan[0], titik[-1][1] - acuan[1])


def simpangan_maksimal(rekaman, ideal):
    """Seberapa jauh titik rekaman terjauh dari garis pola ideal (meter)."""
    if len(rekaman) < 2 or len(ideal) < 2:
        return 0.0
    terjauh = 0.0
    for p in rekaman:
        terdekat = min(_jarak_ke_segmen(p, a, b) for a, b in zip(ideal, ideal[1:]))
        terjauh = max(terjauh, terdekat)
    return terjauh


# =============================================================================
#  gambar
# =============================================================================

def tulis_svg(berkas, rekaman=None, ideal=None, judul="", catatan=()):
    skala, tepi = 230.0, 60
    semua = list(rekaman or []) + list(ideal or [])
    if not semua:
        print("Tidak ada titik untuk digambar.")
        return None
    xs = [p[0] for p in semua]
    ys = [p[1] for p in semua]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    w = (maxx - minx) * skala + 2 * tepi
    h = (maxy - miny) * skala + 2 * tepi + 26 * len(catatan)

    def px(x, y):
        return ((x - minx) * skala + tepi, (maxy - y) * skala + tepi)

    def jalur(titik):
        return " ".join(f"{a:.1f},{b:.1f}" for a, b in (px(x, y) for x, y in titik))

    bag = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
        f'viewBox="0 0 {w:.0f} {h:.0f}">',
        f'<rect width="{w:.0f}" height="{h:.0f}" fill="#fdfcf7"/>',
    ]
    if ideal:
        bag.append(
            f'<polyline points="{jalur(ideal)}" fill="none" stroke="#b9b2a2" '
            f'stroke-width="6" stroke-dasharray="12 9" stroke-linejoin="round"/>')
        for n, (x, y) in enumerate(ideal):
            cx, cy = px(x, y)
            bag.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="#b9b2a2"/>')
            if n:
                bag.append(
                    f'<text x="{cx + 9:.1f}" y="{cy - 9:.1f}" font-family="monospace" '
                    f'font-size="14" fill="#9b9385">{n}</text>')
    if rekaman:
        bag.append(
            f'<polyline points="{jalur(rekaman)}" fill="none" stroke="#1f6f4a" '
            f'stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>')
        ax, ay = px(*rekaman[0])
        bx, by = px(*rekaman[-1])
        bag.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="8" fill="#c0392b"/>')
        bag.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="8" fill="#1f6f4a"/>')
        bag.append(f'<text x="{ax + 12:.1f}" y="{ay + 5:.1f}" font-family="monospace" '
                   f'font-size="15" fill="#c0392b">START</text>')
        bag.append(f'<text x="{bx + 12:.1f}" y="{by + 5:.1f}" font-family="monospace" '
                   f'font-size="15" fill="#1f6f4a">AKHIR</text>')

    baris_y = h - 26 * len(catatan) - 8
    if judul:
        bag.append(f'<text x="{tepi}" y="{baris_y:.0f}" font-family="monospace" '
                   f'font-size="18" font-weight="bold" fill="#333">{judul}</text>')
    for i, c in enumerate(catatan, 1):
        bag.append(f'<text x="{tepi}" y="{baris_y + 24 * i:.0f}" font-family="monospace" '
                   f'font-size="15" fill="#555">{c}</text>')
    bag.append("</svg>")

    os.makedirs(os.path.dirname(berkas) or ".", exist_ok=True)
    with open(berkas, "w") as f:
        f.write("\n".join(bag) + "\n")
    return berkas


def laporkan(rekaman, ideal, judul, berkas_svg):
    tutup = math.hypot(rekaman[-1][0] - rekaman[0][0],
                       rekaman[-1][1] - rekaman[0][1]) if rekaman else 0.0
    simpang = simpangan_maksimal(rekaman, ideal)
    panjang = panjang_jalur(rekaman)
    catatan = [
        f"titik terekam        : {len(rekaman)}",
        f"panjang jalur asli   : {panjang:.2f} m  (ideal 4.50 m)",
        f"akhir ke start       : {tutup * 100:.1f} cm  (ideal ~0 cm)",
        f"simpangan maks dari pola ideal : {simpang * 100:.1f} cm",
    ]
    print("\n--- HASIL REKAMAN ---")
    for c in catatan:
        print("  " + c)
    if simpang < 0.15 and tutup < 0.20:
        putusan = "POLA TERBENTUK - bentuk rumah dan robot pulang ke start"
    elif simpang < 0.15:
        putusan = "BENTUK BENAR tapi tidak menutup rapat - cek kalibrasi/slip roda"
    else:
        putusan = "POLA TIDAK TERBENTUK - periksa urutan pecahan tim ini"
    print("  putusan              : " + putusan)
    catatan.append("putusan: " + putusan)
    hasil = tulis_svg(berkas_svg, rekaman, ideal, judul, catatan)
    if hasil:
        print(f"\n  Gambar: {hasil}")
    return hasil


# =============================================================================
#  mode --gambar : dari CSV, tanpa ROS
# =============================================================================

def baca_csv(berkas):
    titik, sudut0 = [], 0.0
    with open(berkas) as f:
        for i, baris in enumerate(csv.DictReader(f)):
            titik.append((float(baris["x"]), float(baris["y"])))
            if i == 0:
                sudut0 = math.radians(float(baris["sudut_derajat"]))
    return titik, sudut0


def mode_gambar(berkas_csv):
    if not os.path.exists(berkas_csv):
        print(f"File tidak ada: {berkas_csv}")
        return 1
    titik, sudut0 = baca_csv(berkas_csv)
    if not titik:
        print("CSV kosong.")
        return 1
    nama = os.path.splitext(os.path.basename(berkas_csv))[0]
    laporkan(selaraskan(titik, sudut0), jejak_ideal(),
             f"Jejak {nama} vs pola ideal",
             os.path.join(os.path.dirname(berkas_csv) or ".", nama + ".svg"))
    return 0


# =============================================================================
#  mode --rekam : butuh ROS 2
# =============================================================================

def mode_rekam(nama, topic, durasi):
    try:
        import rclpy
        from rclpy.node import Node
        from rclpy.qos import QoSProfile, ReliabilityPolicy
        from nav_msgs.msg import Odometry
    except ImportError:
        print("ERROR: ROS 2 (rclpy) tidak ditemukan.")
        print("  Jalankan dulu: source /opt/ros/$ROS_DISTRO/setup.bash")
        print("  Tanpa robot, kamu masih bisa: python3 rekam_jejak.py --ideal")
        return 1

    os.makedirs(FOLDER_REKAMAN, exist_ok=True)
    berkas_csv = os.path.join(FOLDER_REKAMAN, nama + ".csv")

    class Perekam(Node):
        def __init__(self):
            super().__init__("perekam_jejak")
            qos = QoSProfile(depth=50)
            qos.reliability = ReliabilityPolicy.BEST_EFFORT
            self.create_subscription(Odometry, topic, self.terima, qos)
            self.baris = []
            self.t0 = None

        def terima(self, msg):
            p = msg.pose.pose.position
            q = msg.pose.pose.orientation
            sudut = math.degrees(math.atan2(
                2.0 * (q.w * q.z + q.x * q.y),
                1.0 - 2.0 * (q.y * q.y + q.z * q.z)))
            t = self.get_clock().now().nanoseconds / 1e9
            if self.t0 is None:
                self.t0 = t
            if self.baris:
                xl, yl = self.baris[-1][1], self.baris[-1][2]
                if math.hypot(p.x - xl, p.y - yl) < JARAK_MINIMAL_CATAT:
                    return
            self.baris.append((round(t - self.t0, 3), p.x, p.y, round(sudut, 2)))
            if len(self.baris) % 20 == 0:
                print(f"\r  terekam {len(self.baris)} titik...", end="", flush=True)

    rclpy.init()
    node = Perekam()
    print(f"\nMerekam topic {topic} -> {berkas_csv}")
    print("Suruh tim menjalankan jalankan_pola.py sekarang.")
    print("Tekan Ctrl+C kalau robot sudah berhenti.\n")
    batas = None if not durasi else node.get_clock().now().nanoseconds + durasi * 1e9
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.2)
            if batas and node.get_clock().now().nanoseconds > batas:
                print("\n  Batas waktu tercapai.")
                break
    except KeyboardInterrupt:
        print("\n  Perekaman dihentikan.")
    finally:
        baris = node.baris
        node.destroy_node()
        rclpy.shutdown()

    if not baris:
        print(f"\nTidak ada data dari {topic}.")
        print("  Cek: ros2 topic list | grep odom")
        print("  Cek: ros2 topic echo /odom --once")
        print("  Pastikan ROS_DOMAIN_ID laptop dan robot sama.")
        return 1

    with open(berkas_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["waktu_detik", "x", "y", "sudut_derajat"])
        w.writerows(baris)
    print(f"\n  CSV: {berkas_csv}  ({len(baris)} titik)")

    titik = [(b[1], b[2]) for b in baris]
    laporkan(selaraskan(titik, math.radians(baris[0][3])), jejak_ideal(),
             f"Jejak {nama} vs pola ideal",
             os.path.join(FOLDER_REKAMAN, nama + ".svg"))
    return 0


# =============================================================================

def main(arg):
    topic = "/odom"
    durasi = 0
    for i, a in enumerate(arg):
        if a == "--topic" and i + 1 < len(arg):
            topic = arg[i + 1]
        if a == "--durasi" and i + 1 < len(arg):
            durasi = float(arg[i + 1])

    if "--ideal" in arg:
        berkas = tulis_svg(os.path.join(AKAR, "POLA_RUMAH.svg"),
                           ideal=jejak_ideal(),
                           judul="Pola ideal ronde 2 - RUMAH",
                           catatan=["dasar 1.20 m, dinding 0.80 m, atap 45 derajat",
                                    "total 4.50 m, putaran total 360 derajat"])
        print(f"Gambar pola ideal: {berkas}")
        return 0

    if "--gambar" in arg:
        i = arg.index("--gambar")
        if i + 1 >= len(arg):
            print("Pakai: python3 rekam_jejak.py --gambar rekaman/tim_01.csv")
            return 1
        return mode_gambar(arg[i + 1])

    if "--rekam" in arg:
        i = arg.index("--rekam")
        nama = arg[i + 1] if i + 1 < len(arg) and not arg[i + 1].startswith("-") else "jejak"
        return mode_rekam(nama, topic, durasi)

    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
