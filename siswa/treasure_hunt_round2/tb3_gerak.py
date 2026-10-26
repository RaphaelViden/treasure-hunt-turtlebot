#!/usr/bin/env python3
"""
tb3_gerak.py - mesin gerak bersama untuk semua pecahan pola TurtleBot3.

File ini TIDAK berisi pola. File ini hanya tahu cara:
  1. menjalankan satu segmen gerak (maju X meter, lalu putar Y derajat), dan
  2. menghitung / menggambar jejak yang akan dibuat robot.

Dipakai oleh:
  - pecahan_*.py        -> menjalankan satu segmen
  - jalankan_pola.py    -> menyusun semua segmen jadi satu pola

Dua mode:
  mode robot     -> butuh ROS 2 + TurtleBot3 (publish ke /cmd_vel, baca /odom)
  mode simulasi  -> tidak butuh ROS, hanya menghitung dan menggambar jejak
"""

import math
import os
import sys

# --- spesifikasi TurtleBot3 Burger -------------------------------------------
RADIUS_RODA = 0.033                       # meter
LINGKAR_RODA = 2 * math.pi * RADIUS_RODA  # ~0.2074 m per putaran roda

# --- kecepatan aman untuk di dalam ruangan / lab ------------------------------
KECEPATAN_MAJU = 0.12   # m/s
KECEPATAN_PUTAR = 0.5   # rad/s


class Segmen:
    """Satu potong gerakan: maju beberapa meter, lalu berputar di tempat."""

    def __init__(self, nama, kata, maju_m, putar_deg, catatan=""):
        self.nama = nama              # nama pecahan, mis. "RIMBA"
        self.kata = kata              # satu kata kunci untuk verifikasi urutan
        self.maju_m = maju_m          # jarak maju dalam meter
        self.putar_deg = putar_deg    # + = putar kiri (CCW), - = putar kanan
        self.catatan = catatan        # keterangan bagian pola

    @property
    def putaran_roda(self):
        return self.maju_m / LINGKAR_RODA

    def ringkas(self):
        arah = "kiri" if self.putar_deg >= 0 else "kanan"
        return (
            f"{self.nama:<8} maju {self.maju_m:.2f} m "
            f"({self.putaran_roda:.2f} putaran roda), "
            f"putar {abs(self.putar_deg):.0f} derajat ke {arah}"
        )


# =============================================================================
#  MODE SIMULASI - hitung jejak tanpa robot
# =============================================================================

def hitung_jejak(segmen_list, x0=0.0, y0=0.0, sudut0_deg=0.0):
    """Kembalikan daftar titik [(x, y), ...] yang dilewati robot."""
    x, y, sudut = x0, y0, math.radians(sudut0_deg)
    titik = [(x, y)]
    for s in segmen_list:
        x += s.maju_m * math.cos(sudut)
        y += s.maju_m * math.sin(sudut)
        titik.append((x, y))
        sudut += math.radians(s.putar_deg)
    return titik


def jarak_ke_awal(titik):
    """Seberapa jauh titik akhir dari titik awal (meter). Pola tertutup ~ 0."""
    (x0, y0), (xn, yn) = titik[0], titik[-1]
    return math.hypot(xn - x0, yn - y0)


def gambar_ascii(titik, lebar=64, tinggi=26, aspek=2.0):
    """Gambar jejak sebagai teks di terminal, dengan rasio bentuk dijaga.

    'aspek' = satu karakter terminal kira-kira 2x lebih tinggi daripada lebar,
    jadi skala vertikal dibuat setengah skala horizontal supaya pola tidak gepeng.
    """
    xs = [p[0] for p in titik]
    ys = [p[1] for p in titik]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    rx = (maxx - minx) or 1.0
    ry = (maxy - miny) or 1.0

    # sel per meter: horizontal penuh, vertikal dibagi 'aspek'
    skala = min((lebar - 1) / rx, (tinggi - 1) * aspek / ry)
    kol_pakai = max(int(rx * skala) + 1, 1)
    bar_pakai = max(int(ry * skala / aspek) + 1, 1)
    geser_kol = (lebar - kol_pakai) // 2
    geser_bar = (tinggi - bar_pakai) // 2

    kanvas = [[" "] * lebar for _ in range(tinggi)]

    def ke_sel(x, y):
        kol = geser_kol + int(round((x - minx) * skala))
        bar = geser_bar + int(round((maxy - y) * skala / aspek))
        return bar, kol

    for (x1, y1), (x2, y2) in zip(titik, titik[1:]):
        langkah = max(int(math.hypot(x2 - x1, y2 - y1) * skala * 4), 2)
        for i in range(langkah + 1):
            t = i / langkah
            bar, kol = ke_sel(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t)
            if 0 <= bar < tinggi and 0 <= kol < lebar:
                kanvas[bar][kol] = "*"

    for n, (x, y) in enumerate(titik):
        bar, kol = ke_sel(x, y)
        if 0 <= bar < tinggi and 0 <= kol < lebar:
            kanvas[bar][kol] = "S" if n == 0 else str(n)

    garis = ["+" + "-" * lebar + "+"]
    garis += ["|" + "".join(b) + "|" for b in kanvas]
    garis += ["+" + "-" * lebar + "+"]
    return "\n".join(garis)


def tulis_svg(titik, berkas, judul="Jejak TurtleBot3"):
    """Simpan jejak sebagai gambar SVG (bisa dibuka di browser)."""
    skala = 220.0   # piksel per meter
    tepi = 50
    xs = [p[0] for p in titik]
    ys = [p[1] for p in titik]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    w = (maxx - minx) * skala + 2 * tepi
    h = (maxy - miny) * skala + 2 * tepi

    def px(x, y):
        return ((x - minx) * skala + tepi, (maxy - y) * skala + tepi)

    jalur = " ".join(f"{a:.1f},{b:.1f}" for a, b in (px(x, y) for x, y in titik))

    bagian = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
        f'viewBox="0 0 {w:.0f} {h:.0f}">',
        f'<rect width="{w:.0f}" height="{h:.0f}" fill="#fdfcf7"/>',
        f'<polyline points="{jalur}" fill="none" stroke="#1f6f4a" '
        f'stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>',
    ]
    for n, (x, y) in enumerate(titik):
        cx, cy = px(x, y)
        warna = "#c0392b" if n == 0 else "#1f6f4a"
        bagian.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="6" fill="{warna}"/>')
        bagian.append(
            f'<text x="{cx + 10:.1f}" y="{cy - 8:.1f}" font-family="monospace" '
            f'font-size="15" fill="#555">{"START" if n == 0 else n}</text>'
        )
    bagian.append(
        f'<text x="{tepi}" y="{h - 14:.0f}" font-family="monospace" '
        f'font-size="16" fill="#333">{judul}</text>'
    )
    bagian.append("</svg>")

    with open(berkas, "w") as f:
        f.write("\n".join(bagian) + "\n")
    return berkas


def jalankan_simulasi(segmen_list, berkas_svg=None):
    titik = hitung_jejak(segmen_list)
    print("\n--- RENCANA GERAK (mode simulasi, robot tidak bergerak) ---")
    for i, s in enumerate(segmen_list, 1):
        print(f"  {i}. {s.ringkas()}")
    total = sum(s.maju_m for s in segmen_list)
    putar = sum(s.putar_deg for s in segmen_list)
    print(f"\n  Total jarak  : {total:.2f} m ({total / LINGKAR_RODA:.1f} putaran roda)")
    print(f"  Total putaran: {putar:.0f} derajat")
    print(f"  Jarak titik akhir ke titik awal: {jarak_ke_awal(titik) * 100:.1f} cm")
    print("\n--- JEJAK YANG AKAN TERBENTUK ---")
    print(gambar_ascii(titik))
    if berkas_svg:
        tulis_svg(titik, berkas_svg)
        print(f"\n  Gambar jejak disimpan di: {berkas_svg}")
    return titik


# =============================================================================
#  MODE ROBOT - butuh ROS 2 + TurtleBot3
# =============================================================================

def _sudut_dari_quaternion(q):
    sin_yaw = 2.0 * (q.w * q.z + q.x * q.y)
    cos_yaw = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(sin_yaw, cos_yaw)


def _selisih_sudut(a, b):
    return math.atan2(math.sin(a - b), math.cos(a - b))


def jalankan_robot(segmen_list):
    """Jalankan segmen di TurtleBot3 sungguhan lewat ROS 2."""
    try:
        import rclpy
        from rclpy.node import Node
        from rclpy.qos import QoSProfile, ReliabilityPolicy
        from geometry_msgs.msg import Twist
        from nav_msgs.msg import Odometry
    except ImportError:
        print("ERROR: ROS 2 (rclpy) tidak ditemukan.")
        print("  - Di laptop tanpa ROS, pakai mode simulasi: tambahkan --simulasi")
        print("  - Di robot/PC ROS, jalankan dulu: source /opt/ros/$ROS_DISTRO/setup.bash")
        return 1

    class Penggerak(Node):
        def __init__(self):
            super().__init__("penggerak_pola")
            self.pub = self.create_publisher(Twist, "cmd_vel", 10)
            qos = QoSProfile(depth=10)
            qos.reliability = ReliabilityPolicy.BEST_EFFORT
            self.create_subscription(Odometry, "odom", self.simpan_odom, qos)
            self.x = self.y = self.sudut = None

        def simpan_odom(self, msg):
            self.x = msg.pose.pose.position.x
            self.y = msg.pose.pose.position.y
            self.sudut = _sudut_dari_quaternion(msg.pose.pose.orientation)

        def tunggu_odom(self, batas=10.0):
            habis = self.get_clock().now().nanoseconds + batas * 1e9
            while self.x is None and self.get_clock().now().nanoseconds < habis:
                rclpy.spin_once(self, timeout_sec=0.1)
            return self.x is not None

        def berhenti(self):
            for _ in range(5):
                self.pub.publish(Twist())
                rclpy.spin_once(self, timeout_sec=0.02)

        def maju(self, jarak):
            if abs(jarak) < 1e-4:
                return
            x0, y0 = self.x, self.y
            perintah = Twist()
            perintah.linear.x = KECEPATAN_MAJU * (1 if jarak > 0 else -1)
            while rclpy.ok():
                rclpy.spin_once(self, timeout_sec=0.02)
                if math.hypot(self.x - x0, self.y - y0) >= abs(jarak):
                    break
                self.pub.publish(perintah)
            self.berhenti()

        def putar(self, derajat):
            if abs(derajat) < 0.5:
                return
            target = math.radians(abs(derajat))
            sudut0 = self.sudut
            terkumpul = 0.0
            sebelum = sudut0
            perintah = Twist()
            perintah.angular.z = KECEPATAN_PUTAR * (1 if derajat > 0 else -1)
            while rclpy.ok():
                rclpy.spin_once(self, timeout_sec=0.02)
                terkumpul += abs(_selisih_sudut(self.sudut, sebelum))
                sebelum = self.sudut
                if terkumpul >= target:
                    break
                self.pub.publish(perintah)
            self.berhenti()

    rclpy.init()
    node = Penggerak()
    kode = 0
    try:
        if not node.tunggu_odom():
            print("ERROR: /odom tidak terbaca. Pastikan TurtleBot3 sudah menyala")
            print("       dan 'ros2 launch turtlebot3_bringup robot.launch.py' jalan.")
            return 1
        print("\n--- ROBOT MULAI BERGERAK ---")
        for i, s in enumerate(segmen_list, 1):
            print(f"  {i}. {s.ringkas()}")
            node.maju(s.maju_m)
            node.putar(s.putar_deg)
        print("--- SELESAI ---")
    except KeyboardInterrupt:
        print("\nDihentikan oleh pengguna.")
        kode = 130
    finally:
        node.berhenti()
        node.destroy_node()
        rclpy.shutdown()
    return kode


# =============================================================================
#  pintu masuk umum
# =============================================================================

def jalankan(segmen_list, argumen=None, berkas_svg=None):
    """Jalankan daftar segmen. Pakai --simulasi untuk mode tanpa robot."""
    argumen = sys.argv[1:] if argumen is None else argumen
    simulasi = "--simulasi" in argumen or "-s" in argumen
    if simulasi or os.environ.get("TB3_SIMULASI") == "1":
        jalankan_simulasi(segmen_list, berkas_svg)
        return 0
    return jalankan_robot(segmen_list)


def cari_akar(mulai):
    """Naik dari folder 'mulai' sampai menemukan tb3_gerak.py."""
    jalur = os.path.abspath(mulai)
    for _ in range(8):
        if os.path.exists(os.path.join(jalur, "tb3_gerak.py")):
            return jalur
        induk = os.path.dirname(jalur)
        if induk == jalur:
            break
        jalur = induk
    raise RuntimeError("tb3_gerak.py tidak ditemukan di folder induk mana pun.")
