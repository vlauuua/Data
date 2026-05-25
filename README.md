# 🍽️ Nutrify — Indonesian Food Nutrition Analytics


## 📌 Deskripsi Proyek

Project ini merupakan bagian dari submission Side Quest tim Data Science yang berfokus pada analisis data nutrisi makanan Indonesia menggunakan Python dan Streamlit. Dashboard dibuat untuk membantu pengguna memahami kandungan nutrisi dari berbagai makanan secara interaktif dan informatif.

---

## 📊 Dataset

Dataset nutrisi makanan Indonesia yang berisi informasi berikut:

| Kolom | Deskripsi |
|-------|------------|
| `food_name` | Nama makanan |
| `calories` | Jumlah kalori per 100g |
| `protein` | Kandungan protein per 100g |
| `fat` | Kandungan lemak per 100g |
| `carbohydrates` | Kandungan karbohidrat per 100g |
| `sugar` | Kandungan gula per 100g |
| `sodium` | Kandungan natrium per 100g |
| `fiber` | Kandungan serat per 100g |
| `calories_from_macro` | Total estimasi kalori dari makronutrien |
| `protein_per_calorie` | Rasio protein terhadap kalori |
| `fat_per_calorie` | Rasio lemak terhadap kalori |
| `carbs_per_calorie` | Rasio karbohidrat terhadap kalori |
| `calorie_category` | Kategori kalori makanan |
| `is_high_protein` | Penanda makanan tinggi protein |
| `is_high_fiber` | Penanda makanan tinggi serat |
| `is_high_sodium` | Penanda makanan tinggi sodium |

---

## 📈 Dashboard Streamlit

Dashboard menyediakan beberapa halaman analisis seperti:

| Halaman | Deskripsi |
|----------|------------|
| Overview | Ringkasan statistik nutrisi |
| Nutrisi Tertinggi | Top makanan berdasarkan nutrisi |
| Rasio Makronutrien | Analisis protein, lemak, dan karbohidrat |
| Distribusi Kalori | Distribusi dan filter kalori |
| Korelasi Nutrisi | Heatmap dan scatter plot |
| Cari & Bandingkan | Search dan compare makanan |

---

## 🚀 Cara Menjalankan dashboard

### 1. Clone Repository

```bash
git clone https://github.com/vlauuua/Data.git
```

### 2. Masuk ke Folder Project

```bash
cd Data
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan Streamlit

```bash
streamlit run dashboard/nutrify_dashboard.py
```

### 5. Buka di Browser

```bash
http://localhost:8501
```
---

## 📝 Catatan

- Nutrisi ditampilkan berdasarkan hasil pencarian makanan pengguna
- Dataset menggunakan nilai nutrisi per 100 gram sajian
- Informasi nutrisi berasal dari database CSV
