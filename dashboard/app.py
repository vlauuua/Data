import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Nutrify Dashboard", page_icon="🍽️", layout="wide")

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv('dashboard/clean_dataset.csv')

    df['health_score'] = (
        df['protein'] * 2 +
        df['fiber']   * 3 -
        df['fat']         -
        df['sodium']  * 0.01
    ).round(2)

    df['calorie_category'] = pd.cut(
        df['calories'],
        bins=[-1, 100, 300, 500, float('inf')],
        labels=['Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi']
    )

    df['fat_category'] = pd.cut(
        df['fat'],
        bins=[-1, 5, 15, 30, float('inf')],
        labels=['Sangat Rendah (<5g)', 'Rendah (5-15g)', 'Sedang (15-30g)', 'Tinggi (>30g)']
    )

    return df

df = load_data()

# ============================================================
# SIDEBAR NAVIGASI
# ============================================================
st.sidebar.title("🍽️ Nutrify")
st.sidebar.markdown("Dashboard Analitik Nutrisi Makanan Indonesia")
st.sidebar.markdown("---")

page = st.sidebar.radio("Halaman", [
    "Overview",
    "Nutrisi Tertinggi",
    "Rasio Makronutrien",
    "Distribusi Kalori",
    "Korelasi Nutrisi",
    "Makanan Sehat vs Kurang Sehat",
    "Cari & Bandingkan Makanan"
])

# ============================================================
# PAGE: OVERVIEW
# ============================================================
if page == "Overview":
    st.title("🍽️ Nutrify Dashboard")
    st.caption("Analitik Nutrisi Makanan Indonesia")
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Makanan", f"{len(df)}")
    c2.metric("Rata-rata Kalori", f"{df['calories'].mean():.0f} kcal")
    c3.metric("Rata-rata Protein", f"{df['protein'].mean():.1f} g")
    c4.metric("Rata-rata Lemak", f"{df['fat'].mean():.1f} g")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Rata-rata Karbohidrat", f"{df['carbohydrates'].mean():.1f} g")
    c6.metric("Rata-rata Gula", f"{df['sugar'].mean():.1f} g")
    c7.metric("Rata-rata Natrium", f"{df['sodium'].mean():.1f} mg")
    c8.metric("Rata-rata Serat", f"{df['fiber'].mean():.1f} g")
    st.markdown("---")

    num_cols  = ['calories', 'protein', 'fat', 'carbohydrates', 'sugar', 'sodium', 'fiber']
    units     = ['kcal', 'g', 'g', 'g', 'g', 'mg', 'g']

    st.subheader("Statistik Deskriptif")
    st.dataframe(df[num_cols].describe().round(2), use_container_width=True)

# ============================================================
# PAGE: NUTRISI TERTINGGI
# ============================================================
elif page == "Nutrisi Tertinggi":
    st.title("🏆 Makanan dengan Nutrisi Tertinggi")
    st.caption("Pertanyaan Bisnis 1 — Makanan mana yang menyediakan kalori, protein, lemak, dan karbohidrat tertinggi?")
    st.markdown("---")

    col_map   = {"Kalori":"calories", "Protein":"protein", "Lemak":"fat", "Karbohidrat":"carbohydrates"}
    color_map = {"Kalori":"#f44336", "Protein":"#4caf50", "Lemak":"#ff9800", "Karbohidrat":"#2196f3"}
    unit_map  = {"Kalori":"kcal", "Protein":"g", "Lemak":"g", "Karbohidrat":"g"}

    nutrisi = st.selectbox("Pilih Nutrisi", list(col_map.keys()))
    top_n   = st.slider("Tampilkan Top", 5, 20, 10)

    col  = col_map[nutrisi]
    unit = unit_map[nutrisi]
    top  = df.nlargest(top_n, col)[['food_name', col]].sort_values(col)

    fig, ax = plt.subplots(figsize=(8, max(4, top_n * 0.4)))
    bars = ax.barh(top['food_name'], top[col], color=color_map[nutrisi], edgecolor='white')
    ax.set_xlabel(f'{nutrisi} ({unit})')
    ax.set_title(f'Top {top_n} — {nutrisi} Tertinggi')
    for bar in bars:
        w = bar.get_width()
        ax.text(w + max(top[col])*0.01, bar.get_y() + bar.get_height()/2,
                f'{w:.1f} {unit}', va='center', fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("---")
    top1 = df.nlargest(1, col).iloc[0]
    st.info(f"**{nutrisi} tertinggi:** {top1['food_name'].title()} — {top1[col]:.1f} {unit} per 100g")

    st.subheader("Data")
    st.dataframe(top.sort_values(col, ascending=False).reset_index(drop=True), use_container_width=True)

# ============================================================
# PAGE: RASIO MAKRONUTRIEN
# ============================================================
elif page == "Rasio Makronutrien":
    st.title("🥗 Rasio Makronutrien")
    st.caption("Pertanyaan Bisnis 2 — Bagaimana rasio umum antara protein, lemak, dan karbohidrat?")
    st.markdown("---")

    avg_p = df['protein'].mean()
    avg_f = df['fat'].mean()
    avg_c = df['carbohydrates'].mean()
    total = avg_p + avg_f + avg_c

    c1, c2, c3 = st.columns(3)
    c1.metric("Rata-rata Protein",     f"{avg_p:.1f}g", f"{avg_p/total*100:.1f}%")
    c2.metric("Rata-rata Lemak",       f"{avg_f:.1f}g", f"{avg_f/total*100:.1f}%")
    c3.metric("Rata-rata Karbohidrat", f"{avg_c:.1f}g", f"{avg_c/total*100:.1f}%")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Proporsi Rata-rata")
        fig, ax = plt.subplots()
        ax.pie([avg_p, avg_f, avg_c],
               labels=['Protein','Lemak','Karbohidrat'],
               colors=['#4caf50','#ff9800','#2196f3'],
               autopct='%1.1f%%', startangle=90)
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("Bandingkan Makanan")
        selected = st.multiselect("Pilih makanan", df['food_name'].tolist(),
                                  default=df['food_name'].tolist()[:5])
        if selected:
            df_sel = df[df['food_name'].isin(selected)].set_index('food_name')
            fig, ax = plt.subplots(figsize=(8, 4))
            x     = np.arange(len(selected))
            width = 0.25
            bars_p = ax.bar(x - width, df_sel.loc[selected,'protein'],       width, label='Protein',     color='#4caf50')
            bars_f = ax.bar(x,         df_sel.loc[selected,'fat'],           width, label='Lemak',       color='#ff9800')
            bars_c = ax.bar(x + width, df_sel.loc[selected,'carbohydrates'], width, label='Karbohidrat', color='#2196f3')
            for bars in [bars_p, bars_f, bars_c]:
                for bar in bars:
                    h = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2, h + 0.2,
                            f'{h:.1f}g', ha='center', fontsize=6, rotation=90)
            ax.set_xticks(x)
            ax.set_xticklabels([f.title() for f in selected], rotation=30, ha='right', fontsize=8)
            ax.set_ylabel('Gram per 100g')
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

    st.markdown("---")
    st.info(f"**Insight:** Karbohidrat mendominasi {avg_c/total*100:.1f}% dari total makronutrien, mencerminkan pola konsumsi masyarakat Indonesia yang berbasis nasi, gula, dan bahan berpati.")

# ============================================================
# PAGE: DISTRIBUSI KALORI
# ============================================================
elif page == "Distribusi Kalori":
    st.title("📊 Distribusi Kalori")
    st.caption("Pertanyaan Bisnis 3 — Berapa persentase makanan dengan kalori di bawah 100 dan di atas 500?")
    st.markdown("---")

    low  = (df['calories'] < 100).sum()
    high = (df['calories'] > 500).sum()
    mid  = len(df) - low - high
    tot  = len(df)

    c1, c2, c3 = st.columns(3)
    c1.metric("Kalori < 100",   f"{low}",  f"{low/tot*100:.1f}%")
    c2.metric("Kalori 100–500", f"{mid}",  f"{mid/tot*100:.1f}%")
    c3.metric("Kalori > 500",   f"{high}", f"{high/tot*100:.1f}%")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Proporsi Kategori")
        fig, ax = plt.subplots()
        ax.pie([low, mid, high],
               labels=[f'< 100 kcal\n({low})', f'100–500 kcal\n({mid})', f'> 500 kcal\n({high})'],
               colors=['#4caf50','#ffc107','#f44336'],
               autopct='%1.1f%%', startangle=90, explode=(0.05, 0, 0.05))
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("Filter Berdasarkan Kalori")
        cal_range = st.slider("Range Kalori (kcal)",
                              int(df['calories'].min()),
                              int(df['calories'].max()),
                              (0, int(df['calories'].max())))
        df_fil = df[(df['calories'] >= cal_range[0]) & (df['calories'] <= cal_range[1])]
        st.write(f"**{len(df_fil)}** makanan ditemukan")
        st.dataframe(df_fil[['food_name','calories','calorie_category']]
                     .sort_values('calories', ascending=False)
                     .reset_index(drop=True),
                     use_container_width=True)

    st.markdown("---")
    st.info(f"**Insight:** Mayoritas makanan ({mid/tot*100:.1f}%) berada di kisaran kalori sedang (100–500 kcal). Hanya {high/tot*100:.1f}% yang sangat tinggi kalori (>500 kcal).")

# ============================================================
# PAGE: KORELASI NUTRISI 
# ============================================================
elif page == "Korelasi Nutrisi":
    st.title("🔗 Korelasi Lemak & Kalori")
    st.caption("Pertanyaan Bisnis 4 — Apakah makanan tinggi kalori cenderung juga tinggi lemak?")
    st.markdown("---")

    corr_val = df['fat'].corr(df['calories'])
    label    = "Kuat ✅" if abs(corr_val)>0.7 else "Sedang ⚠️" if abs(corr_val)>0.4 else "Lemah"

    c1, c2 = st.columns(2)
    c1.metric("Korelasi (r)", f"{corr_val:.2f}")
    c2.metric("Kekuatan Korelasi", label)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Scatter Plot Lemak vs Kalori")
        fig, ax = plt.subplots()
        ax.scatter(df['fat'], df['calories'], alpha=0.5, color='steelblue', edgecolors='white', s=40)
        m, b   = np.polyfit(df['fat'], df['calories'], 1)
        x_line = np.linspace(df['fat'].min(), df['fat'].max(), 100)
        ax.plot(x_line, m*x_line+b, color='red', linewidth=2, label=f'r = {corr_val:.2f}')
        ax.set_xlabel('Lemak (g)')
        ax.set_ylabel('Kalori (kcal)')
        ax.legend()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("Distribusi Kalori per Kategori Lemak")
        fig, ax = plt.subplots()
        fat_cats = df['fat_category'].cat.categories
        fat_data = [df[df['fat_category']==c]['calories'].dropna() for c in fat_cats]
        ax.boxplot(fat_data, labels=fat_cats)
        ax.set_xticklabels(fat_cats, rotation=20, ha='right', fontsize=8)
        ax.set_ylabel('Kalori (kcal)')
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    st.subheader("Heatmap Korelasi Semua Nutrisi")
    num_cols = ['calories','protein','fat','carbohydrates','sugar','sodium','fiber']
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(df[num_cols].corr(), annot=True, fmt='.2f', cmap='coolwarm', ax=ax, linewidths=0.5)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("---")
    st.info(f"**Insight:** Korelasi r = {corr_val:.2f} menunjukkan hubungan positif {label.lower()} antara lemak dan kalori. Lemak menyumbang 9 kcal/gram (dua kali lipat protein dan karbohidrat).")

# ============================================================
# PAGE: MAKANAN SEHAT
# ============================================================
elif page == "Makanan Sehat vs Kurang Sehat":
    st.title("💪 Makanan Sehat vs Kurang Sehat")
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("High Protein ≥15g",  f"{(df['protein']>=15).sum()}",  f"{(df['protein']>=15).mean()*100:.1f}%")
    c2.metric("High Fiber ≥5g",     f"{(df['fiber']>=5).sum()}",     f"{(df['fiber']>=5).mean()*100:.1f}%")
    c3.metric("High Sodium ≥600mg", f"{(df['sodium']>=600).sum()}", f"{(df['sodium']>=600).mean()*100:.1f}%")
    st.markdown("---")
    top_n = st.slider("Tampilkan Top N", 5, 20, 10)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🟢 Paling Sehat")
        top_h = df.nlargest(top_n, 'health_score')[['food_name','health_score']].sort_values('health_score')
        fig, ax = plt.subplots(figsize=(7, max(4, top_n*0.4)))
        bars = ax.barh(top_h['food_name'], top_h['health_score'], color='#4caf50', edgecolor='white')
        for bar in bars:
            w = bar.get_width()
            ax.text(w + 0.1, bar.get_y() + bar.get_height()/2,
                    f'{w:.1f}', va='center', fontsize=8)
        ax.set_xlabel('Health Score')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.subheader("🔴 Kurang Sehat")
        bot_h = df.nsmallest(top_n, 'health_score')[['food_name','health_score']].sort_values('health_score', ascending=False)
        fig, ax = plt.subplots(figsize=(7, max(4, top_n*0.4)))
        bars = ax.barh(bot_h['food_name'], bot_h['health_score'], color='#f44336', edgecolor='white')
        for bar in bars:
            w = bar.get_width()
            ax.text(w + 0.1, bar.get_y() + bar.get_height()/2,
                    f'{w:.1f}', va='center', fontsize=8)
        ax.set_xlabel('Health Score')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
# ============================================================
# PAGE: CARI & BANDINGKAN
# ============================================================
elif page == "Cari & Bandingkan Makanan":
    st.title("🔍 Cari & Bandingkan Makanan")
    st.markdown("---")

    tab1, tab2 = st.tabs(["Cari Makanan", "Bandingkan"])

    with tab1:
        search = st.text_input("Cari nama makanan", placeholder="contoh: ayam, nasi...")
        if search:
            results = df[df['food_name'].str.contains(search.lower(), na=False)]
            if len(results) > 0:
                for _, row in results.iterrows():
                    with st.expander(f"🍽️ {row['food_name'].title()}"):
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Kalori",      f"{row['calories']:.0f} kcal")
                        c2.metric("Protein",     f"{row['protein']:.1f} g")
                        c3.metric("Lemak",       f"{row['fat']:.1f} g")
                        c4.metric("Karbohidrat", f"{row['carbohydrates']:.1f} g")
            else:
                st.warning(f"'{search}' tidak ditemukan.")

    with tab2:
        selected = st.multiselect("Pilih makanan untuk dibandingkan",
                                  df['food_name'].tolist(),
                                  default=df['food_name'].tolist()[:4])
        if len(selected) >= 2:
            num_cols = ['calories','protein','fat','carbohydrates','sugar','sodium','fiber']
            units    = ['kcal','g','g','g','g','mg','g']
            df_cmp   = df[df['food_name'].isin(selected)].set_index('food_name')

            fig, ax = plt.subplots(figsize=(10, 5))
            x      = np.arange(len(num_cols))
            width  = 0.8 / len(selected)
            colors = ['#2196f3','#4caf50','#ff9800','#f44336','#9c27b0']
            for i, food in enumerate(selected):
                bars = ax.bar(x + i*width, df_cmp.loc[food, num_cols].values, width,
                              label=food.title(), color=colors[i % len(colors)],
                              edgecolor='white', alpha=0.85)
                for bar, unit in zip(bars, units):
                    h = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2, h + 0.5,
                            f'{h:.0f}{unit}', ha='center', fontsize=5.5, rotation=90)
            ax.set_xticks(x + width*(len(selected)-1)/2)
            ax.set_xticklabels(num_cols, rotation=30, ha='right')
            ax.set_ylabel('Nilai per 100g')
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

            st.dataframe(df_cmp[num_cols].T.round(2), use_container_width=True)
        else:
            st.info("Pilih minimal 2 makanan.")