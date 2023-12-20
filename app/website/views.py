from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Matkul
from . import db
from flask_login import login_required, current_user
import csv

views = Blueprint('views', __name__)

hasil = []
list_ruangan = [
    "Bengkel Kerja Listrik E-104",
    "Laboratorium Biologi Umum/Struktur Tumbuhan N-105",
    "Bengkel Kerja Mekanik dan Gelas E-107",
    "Ruang Kreatif N-110",
    "Laboratorium Fisiologi N-118",
    "Laboratorium Struktur Hewan N-205",
    "Laboratorium Mikrobiologi N-210",
    "Laboratorium Bumi dan Antariksa N-220",
    "Ruang Kelas E-201",
    "Smart Classroom E-210",
    "Ruang Kelas S-301",
    "Ruang Kelas S-302",
    "Ruang Kelas S-303",
    "Ruang Kelas S-304",
    "Ruang Kelas S-305",
    "Ruang Kelas S-306",
    "Ruang Kelas E-301",
    "Laboratorium Pengajaran MIPA Sek. Lanjutan E-302",
    "Ruang Komputer E-305",
    "Ruang Komputer E-306",
    "Laboratorium Elektronika N-305",
    "Laboratorium Fisika Dasar N-309",
    "Laboratorium Fisika Lanjutan 1 N-313",
    "Laboratorium Fisika Lanjutan 2 N-318",
    "Laboratorium Kimia Dasar dan Analitik N-405",
    "Laboratorium Kimia Organik/Biokimia dan Kimia Makanan N-410",
    "Ruang Kegiatan Akademik dan Kemahasiswaan Internal FPMIPA E-405",
    "Ruang Kegiatan Akademik dan Kemahasiswaan Internal FPMIPA E-406",
    "Laboratorium Kimia Fisik/Anorganik N-505",
    "Laboratorium Kimia Organik dan Biokimia N-510",
    "Laboratorium Kimia Instrumen N-519",
    "Ruang B-105",
    "Laboratorium Komputasi Pemodelan Kimia B-106",
    "Laboratorium Pembelajaran Fisika B-108",
    "Ruang Kelas B-113",
    "Ruang Kelas B-114",
    "Ruang Kelas B-115",
    "Laboratorium Biologi IPSE B-201",
    "Ruang Kelas B-203",
    "IPSE Meeting Room B-204",
    "Ruang Kelas B-205",
    "Laboratorium Fisika IPSE B-207",
    "Laboratorium Multimedia IPSE B-209",
    "Ruang Kelas B-210",
    "Laboratorium Kimia IPSE B-213",
    "Ruang Kelas B-301",
    "Ruang Kelas B-303",
    "Ruang Kelas B-304",
    "Ruang Kelas B-305",
    "Laboratorium Riset Bioteknologi B-307",
    "Microteaching Room B-309",
    "Laboratorium Riset Bioteknologi 2 B-311",
    "Laboratorium Media Pembelajaran B-314",
    "Laboratorium Riset Kimia Makanan B-401",
    "Laboratorium Riset B-403",
    "Laboratorium Riset Kimia B-404",
    "Ruangan Kelas B-405",
    "Laboratorium Fisika Instrumentasi B-407",
    "Laboratorium Fisika Komputasi B-408",
    "Laboratorium Rekayasa Teknologi B-409/B-410",
    "Laboratorium Kimia Material B-413",
    "Laboratorium Riset Kimia Lingkungan B-414",
    "Ruang Kelas C-101",
    "Ruang Kelas C-102",
    "Ruang Kelas C-103",
    "Ruang Kelas C-104",
    "Ruang Kelas C-105",
    "Ruang Kelas C-106",
    "Ruang Kelas C-107",
    "Ruang Kelas C-108",
    "Laboratorium Praktikum C-201",
    "Laboratorium Kecerdasan Buatan C-202",
    "Laboratorium Sistem Jaringan dan Teknik Komputer C-203",
    "Laboratorium Umum C-204",
    "Laboratorium Digital, Pedagogik, dan Didactik C-205",
    "Laboratorium Lingkungan Pembelajaran Cerdas C-206",
    "Laboratorium Rekayasa Perangkat Lunak dan Sistem Informasi C-207",
    "RuangLaboratorium Pembelajaran C-208",
    "Ruang Kelas C-301",
    "Ruang Kelas C-302",
    "Ruang Kelas C-303",
    "Ruang Kelas C-304",
    "Ruang Kelas C-305",
    "Ruang Kelas C-306",
    "Ruang Kelas C-307",
    "Ruang Kelas C-308",
    "Ruang Kelas C-309"
]

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST': 
        hasil.clear()
        tanggal_str = str(request.form.get('tanggal'))
        jam_str = str(request.form.get('jam'))
        durasi = int(request.form.get('durasi'))
        tanggal = datetime.strptime(tanggal_str + " " + jam_str, '%Y-%m-%d %H:%M')
        for ruangan in list_ruangan:
            available = True
            for i in range(0,durasi):
                tanggal_check = tanggal + timedelta(minutes=(i*50))
                if Matkul.query.filter_by(ruangan = ruangan, tanggal = tanggal_check).first() is not None:
                    available = False
            if available:
                hasil.append(ruangan)
        return redirect(url_for('views.result'))
    return render_template("home.html", user=current_user)

@views.route('/result')
def result():
    return render_template("result.html", output=hasil, user=current_user)

@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        ruangan = str(request.form.get('ruangan'))
        tanggal_str = str(request.form.get('tanggal'))
        jam_str = str(request.form.get('jam'))
        tanggal = datetime.strptime(tanggal_str + " " + jam_str, '%Y-%m-%d %H:%M')
        durasi = int(request.form.get('durasi'))
        available = True
        for i in range(0, durasi):
            tanggal_check = tanggal + timedelta(minutes=(i*50))
            if Matkul.query.filter_by(ruangan = ruangan, tanggal = tanggal_check).first() is not None:
                available = False
        if available:
            for i in range(0, durasi):
                jadwal = Matkul(
                    ruangan = ruangan,
                    tanggal = tanggal + timedelta(minutes=(i*50))
                )
                db.session.add(jadwal)
                db.session.commit()
            flash('Ruangan berhasil di booking!', category='success')
        else:
            flash('Ruangan tidak dapat di booking, mohon pilih ruangan lain atau waktu yang lain.', category='error')
    return render_template("admin.html", user=current_user)

@views.route('/dev', methods=['GET', 'POST'])
def init():
    if request.method == 'POST':
        tanggal_senin_pertama = str(request.form.get('tanggal'))
        data = csv.DictReader(open('init_data/rekaptulasi.csv', 'r'))
        for entry in data:
            match entry['Hari']:
                case "Senin":
                    tanggal_base = datetime.strptime(tanggal_senin_pertama + " " + entry['Jam Mulai'], '%Y-%m-%d %H:%M') + timedelta(days=0)
                case "Selasa":
                    tanggal_base = datetime.strptime(tanggal_senin_pertama + " " + entry['Jam Mulai'], '%Y-%m-%d %H:%M') + timedelta(days=1)
                case "Rabu":
                    tanggal_base = datetime.strptime(tanggal_senin_pertama + " " + entry['Jam Mulai'], '%Y-%m-%d %H:%M') + timedelta(days=2)
                case "Kamis":
                    tanggal_base = datetime.strptime(tanggal_senin_pertama + " " + entry['Jam Mulai'], '%Y-%m-%d %H:%M') + timedelta(days=3)
                case "Jumat":
                    tanggal_base = datetime.strptime(tanggal_senin_pertama + " " + entry['Jam Mulai'], '%Y-%m-%d %H:%M') + timedelta(days=4)
            for pekan_ke in range(0, 20):
                for jam_ke in range(0, int(entry['Durasi'])):
                    jadwal_matkul = Matkul(
                        ruangan = entry['Ruangan'],
                        tanggal = tanggal_base + timedelta(days=7*pekan_ke, minutes=50*jam_ke)
                    )
                    db.session.add(jadwal_matkul)
                    db.session.commit()
        return redirect(url_for('views.home'))
    return render_template("dev.html", user = current_user)