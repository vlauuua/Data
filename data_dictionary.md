# 📊 Data Dictionary Dataset Indonesian Food

## Informasi Dataset
Dataset ini berisi informasi kandungan nutrisi berbagai makanan Indonesia.  

- **Jumlah data**: 2005 baris  
- **Jumlah atribut**: 17 kolom  

---

## 🗂️ Data Dictionary

| No | Nama Field           | Tipe Data        |  Deskripsi |
|----|----------------------|------------------|------------------------------|
| 1  | food_name            | String           | Nama makanan Indonesia |
| 2  | serving_size_g       | Float64          | Ukuran porsi makanan dalam gram |
| 3  | calories             | Float64          | Jumlah kalori pada makanan |
| 4  | protein              | Float64          | Kandungan protein dalam gram |
| 5  | fat                  | Float64          | Kandungan lemak dalam gram |
| 6  | carbohydrates        | Float64          | Kandungan karbohidrat dalam gram |
| 7  | sugar                | Float64          | Kandungan gula dalam gram |
| 8  | sodium               | Float64          | Kandungan sodium/natrium dalam mg |
| 9  | fiber                | Float64          | Kandungan serat dalam gram |
| 10 | calories_from_macro  | Float64          | Estimasi total kalori dari makronutrien (protein, lemak, karbohidrat) |
| 11 | protein_per_calorie  | Float64          | Rasio protein terhadap total kalori |
| 12 | fat_per_calorie      | Float64          | Rasio lemak terhadap total kalori |
| 13 | carbs_per_calorie    | Float64          | Rasio karbohidrat terhadap total kalori |
| 14 | calorie_category     | Category         | Kategori kalori (rendah, sedang, tinggi) |
| 15 | is_high_protein      | Int64 (0/1)      | Penanda makanan tinggi protein |
| 16 | is_high_fiber        | Int64 (0/1)      | Penanda makanan tinggi serat |
| 17 | is_high_sodium       | Int64 (0/1)      | Penanda makanan tinggi sodium |

---

## Keterangan Tambahan

- **String** → data berbentuk teks  
- **Float64** → data numerik desimal  
- **Int64** → data bilangan bulat  
- **Category** → data kategorikal  

### Nilai Biner
- `1` = Ya / True  
- `0` = Tidak / False  
