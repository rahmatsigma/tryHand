import socket
import sys
from datetime import datetime

# --- Perencanaan ---
# 1. Tentukan target IP. Bisa di-hardcode atau pakai input.
# 2. Tentukan jangkauan port yang akan dipindai.

# Mendapatkan target IP dari argumen command line
# Cara run: python scanner.py <ip_target>
if len(sys.argv) == 2:
    target_ip = socket.gethostbyname(sys.argv[1]) # Terjemahkan hostname ke IPv4
else:
    print("Cara penggunaan: python scanner.py <hostname_atau_ip>")
    sys.exit()

# Banner sederhana
print("-" * 50)
print(f"Memindai target: {target_ip}")
print(f"Waktu mulai: {datetime.now()}")
print("-" * 50)

# Simpan port yang terbuka
open_ports = []

try:
    # Tentukan jangkauan port (misal, 1 sampai 1024, port umum)
    for port in range(1, 1025):
        # Buat objek socket baru untuk setiap port
        # AF_INET = IPv4
        # SOCK_STREAM = TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set timeout agar tidak menunggu terlalu lama
        socket.setdefaulttimeout(0.5) 
        
        # Coba hubungkan ke target IP di port tertentu
        hasil = s.connect_ex((target_ip, port))
        
        if hasil == 0:
            # Jika hasil == 0, koneksi berhasil = port terbuka
            print(f"Port {port}: Terbuka")
            open_ports.append(port)
        
        # Tutup koneksi socket
        s.close()

except KeyboardInterrupt:
    print("\nProses dihentikan oleh pengguna.")
    sys.exit()
except socket.gaierror:
    print("\nHostname tidak dapat ditemukan. Keluar.")
    sys.exit()
except socket.error:
    print("\nTidak dapat terhubung ke server.")
    sys.exit()

# --- Hasil Akhir ---
print("-" * 50)
print("Pemindaian Selesai.")
if open_ports:
    print(f"Port yang terbuka: {open_ports}")
else:
    print("Tidak ada port terbuka yang ditemukan di jangkauan 1-1024.")
print("-" * 50)