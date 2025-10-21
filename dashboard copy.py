import pandas as pd
import streamlit as st
import plotly.express as px

# --- PERUBAHAN 1: DEFINISIKAN PATH LOKAL ANDA DI SINI ---
# Ganti dengan path logo dan dataset yang benar di komputer Anda
LOGO_PATH = r"image/logo-1.png"
DATASET_PATH = r"cleaned_dataset.csv"

# 1. Mengatur Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard EDA",
    page_icon=LOGO_PATH,
    layout="wide"
)

# Menampilkan logo di samping judul utama menggunakan kolom
col_img, col_title = st.columns([0.1, 0.9])
with col_img:
    st.image(LOGO_PATH, width=80)
with col_title:
    st.title("Pengaruh Roblox Terhadap Kehidupan Mahasiswa")

st.markdown("Gusti Jogishwara Adji (24083010107), Fabio Arraya P (2408301064), Febriani Yolanda T (24083010107) - Explanatory Data Analysis (EDA)")

# 2. Fungsi untuk memuat data (sekarang bisa menerima path atau file yang diunggah)
@st.cache_data
def load_data(data_source):
    """Memuat data dari file CSV, baik dari path lokal maupun file yang diunggah."""
    try:
        df = pd.read_csv(data_source)
        return df
    except FileNotFoundError:
        st.error(f"Error: File tidak ditemukan di path '{data_source}'. Pastikan path sudah benar.")
        return None
    except Exception as e:
        st.error(f"Error: Gagal memuat data. Detail: {e}")
        return None

# 3. Sidebar (TETAP ADA UNTUK MULTIPAGE)
with st.sidebar:
    st.header("Upload Data Anda")
    st.write("Jika ingin menganalisis data lain, silakan unggah di sini:")
    uploaded_file = st.file_uploader("Pilih file CSV baru", type=["csv"])

# --- PERUBAHAN 2: MODIFIKASI LOGIKA UTAMA ---
# Tentukan sumber data: gunakan file yang diunggah jika ada, jika tidak, gunakan path lokal.
data_source = uploaded_file if uploaded_file is not None else DATASET_PATH

# Muat data dari sumber yang telah ditentukan
df = load_data(data_source)

# Lanjutkan sisa aplikasi seperti biasa
if df is not None:
    tab1, tab2 = st.tabs(["📄 Data Overview", "📈 Visualisasi Distribusi"])

    # --- INI ADALAH TAB 1 (LAYOUT MOCKUP BARU) ---
    with tab1:
        # --- 1. LAYOUT KOTAK-KOTAK METRIK (TETAP) ---
        jumlah_responden = df.shape[0]
        jumlah_variabel = df.shape[1]
        jumlah_fakultas = df['Fakultas'].nunique() if 'Fakultas' in df.columns else "N/A"
        jumlah_angkatan = df['Angkatan'].nunique() if 'Angkatan' in df.columns else "2022 - 2025"

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            with st.container(border=True):
                st.metric("Jumlah Responden 👥", value=jumlah_responden)
        with col2:
            with st.container(border=True):
                st.metric("Jumlah Variabel 📝", value=jumlah_variabel)
        with col3:
            with st.container(border=True):
                st.metric("Jumlah Fakultas 🏛️", value=jumlah_fakultas)
        with col4:
            with st.container(border=True):
                st.metric("Jumlah Angkatan 🎓", value=jumlah_angkatan)
        
        st.divider()

        # --- 2. LAYOUT VISUALISASI SESUAI MOCKUP ---
        col_left, col_right = st.columns(2)

        # --- KOLOM KIRI (PIE CHART TINGGI) ---
        with col_left:
            st.markdown("##### Distribusi Fakultas Responden")
            NAMA_KOLOM_FAKULTAS = 'Fakultas' 
            if NAMA_KOLOM_FAKULTAS in df.columns:
                df['Kategori Fakultas'] = df[NAMA_KOLOM_FAKULTAS].apply(
                    lambda x: 'Fakultas Ilmu Komputer' if str(x).strip().lower() == 'fakultas ilmu komputer' else 'Fakultas Lainnya'
                )
                pie_data = df['Kategori Fakultas'].value_counts().reset_index()
                pie_data.columns = ['Kategori', 'Jumlah Mahasiswa']
                fig_pie = px.pie(pie_data, names='Kategori', values='Jumlah Mahasiswa') 
                fig_pie.update_traces(textinfo='percent+label', textfont_size=12, showlegend=True)
                fig_pie.update_layout(height=550, margin=dict(t=30, b=20, l=0, r=0))
                st.plotly_chart(fig_pie, use_container_width=True, key="overview_pie_chart")
            else:
                st.warning(f"Kolom '{NAMA_KOLOM_FAKULTAS}' tidak ditemukan.")

        # --- KOLOM KANAN (2 BARCHART + 1 LINECHART) ---
        with col_right:
            col_bar1, col_bar2 = st.columns(2)
            
            with col_bar1:
                st.markdown("##### Distribusi Sentimen")
                NAMA_KOLOM_PENGARUH = 'Pengaruh kehidupan kuliah'
                if NAMA_KOLOM_PENGARUH in df.columns:
                    pengaruh_data = df[NAMA_KOLOM_PENGARUH].value_counts().reset_index()
                    pengaruh_data.columns = ['Kategori Pengaruh', 'Jumlah Responden']
                    fig_pengaruh = px.bar(
                        pengaruh_data, x='Kategori Pengaruh', y='Jumlah Responden',
                        text_auto=True, category_orders={"Kategori Pengaruh": ["Netral", "Positif", "Negatif"]},
                        color='Kategori Pengaruh', color_discrete_map={'Netral': '#D6EAF8', 'Positif': '#85C1E9', 'Negatif': '#3498DB'}
                    )
                    fig_pengaruh.update_layout(height=270, showlegend=False, margin=dict(t=30, b=10, l=10, r=10))
                    st.plotly_chart(fig_pengaruh, use_container_width=True, key="overview_bar_pengaruh")
                else:
                    st.warning(f"Kolom '{NAMA_KOLOM_PENGARUH}' tidak ditemukan.")

            with col_bar2:
                st.markdown("##### Alasan Bermain")
                NAMA_KOLOM_ALASAN = 'Alasan bermain roblox'
                if NAMA_KOLOM_ALASAN in df.columns:
                    hbar_data = df[NAMA_KOLOM_ALASAN].value_counts().reset_index()
                    hbar_data.columns = ['Alasan', 'Jumlah Responden']
                    fig_hbar = px.bar(
                        hbar_data.sort_values('Jumlah Responden', ascending=True),
                        x='Jumlah Responden', y='Alasan', orientation='h', text_auto=True
                    )
                    fig_hbar.update_layout(height=270, margin=dict(t=30, b=10, l=10, r=10))
                    st.plotly_chart(fig_hbar, use_container_width=True, key="overview_hbar_alasan")
                else:
                    st.warning(f"Kolom '{NAMA_KOLOM_ALASAN}' tidak ditemukan.")

            st.markdown("##### Pertumbuhan Pemain per Tahun")
            NAMA_KOLOM_TAHUN = 'Mulai aktif bermain'
            if NAMA_KOLOM_TAHUN in df.columns:
                line_data = df[NAMA_KOLOM_TAHUN].value_counts().sort_index().reset_index()
                line_data.columns = ['Tahun', 'Jumlah Responden']
                fig_line = px.line(line_data, x='Tahun', y='Jumlah Responden', markers=True)
                fig_line.update_layout(height=270, margin=dict(t=30, b=10, l=10, r=10))
                fig_line.update_xaxes(type='category')
                st.plotly_chart(fig_line, use_container_width=True, key="overview_line_chart")
            else:
                st.warning(f"Kolom '{NAMA_KOLOM_TAHUN}' tidak ditemukan.")
        
        st.divider()

       # --- BAGIAN BARU: PENJELASAN VISUALISASI (DUA KOLOM) ---
        st.subheader("Penjelasan Visualisasi")
        col_desc_left, col_desc_right = st.columns(2)

        with col_desc_left:
            st.markdown("##### 1. Distribusi Fakultas")
            if 'pie_data' in locals():
                try:
                    fasilkom_val = pie_data.loc[pie_data['Kategori'] == 'Fakultas Ilmu Komputer', 'Jumlah Mahasiswa'].iloc[0]
                    total_val = pie_data['Jumlah Mahasiswa'].sum()
                    st.markdown(f"Mayoritas responden (**{fasilkom_val} dari {total_val}**) berasal dari Fakultas Ilmu Komputer, yang menjadi konteks utama analisis ini.")
                except Exception as e:
                    st.info("Data penjelasan pie tidak ditemukan.")
            else:
                st.info("Data pie chart tidak tersedia.")
            
            st.markdown("##### 3. Alasan Bermain") # Penjelasan 3 dipindah ke sini
            st.markdown("Grafik menunjukkan bahwa alasan utama responden bermain Roblox adalah untuk **'Sebagai Hiburan'** dan **'Mengisi waktu luang'**.")

        with col_desc_right:
            st.markdown("##### 2. Distribusi Sentimen")
            if 'pengaruh_data' in locals():
                try:
                    positif_val = pengaruh_data.loc[pengaruh_data['Kategori Pengaruh'] == 'Positif', 'Jumlah Responden'].iloc[0]
                    st.markdown(f"Sebagian besar responden (**{positif_val} orang**) merasa Roblox memberikan **dampak positif** terhadap kehidupan perkuliahan mereka.")
                except Exception as e:
                    st.info("Data penjelasan sentimen tidak ditemukan.")
            else:
                st.info("Data sentimen tidak tersedia.")

            st.markdown("##### 4. Pertumbuhan Pemain") # Penjelasan 4 dipindah ke sini
            st.markdown("Terlihat adanya **lonjakan signifikan** jumlah pemain baru di kalangan responden, terutama dalam beberapa tahun terakhir (sekitar 2024-2025).")
            
    # --- INI ADALAH TAB 2 (TIDAK DIUBAH, TETAP UTUH SEPERTI ASLINYA) ---
    with tab2:
        st.header("Visualisasi Data Responden")
        
        # --- BARIS PERTAMA VISUALISASI ---
        col1_tab2, col2_tab2 = st.columns(2)

        with col1_tab2:
            NAMA_KOLOM_FAKULTAS = 'Fakultas' 
            if NAMA_KOLOM_FAKULTAS in df.columns:
                df['Kategori Fakultas'] = df[NAMA_KOLOM_FAKULTAS].apply(
                    lambda x: 'Fakultas Ilmu Komputer' if str(x).strip().lower() == 'fakultas ilmu komputer' else 'Fakultas Lainnya'
                )
                pie_data_tab2 = df['Kategori Fakultas'].value_counts().reset_index()
                pie_data_tab2.columns = ['Kategori', 'Jumlah Mahasiswa']
                
                fig_pie_tab2 = px.pie(
                    pie_data_tab2, 
                    names='Kategori', 
                    values='Jumlah Mahasiswa', 
                    title='Persentase Mahasiswa per Fakultas',
                )
                fig_pie_tab2.update_traces(textinfo='percent+label', textfont_size=14)
                st.plotly_chart(fig_pie_tab2, use_container_width=True, key="dist_pie_chart")
            else:
                st.warning(f"Kolom '{NAMA_KOLOM_FAKULTAS}' tidak ditemukan.")

        with col2_tab2:
            NAMA_KOLOM_ANGKATAN = 'Angkatan' # PERBAIKAN: Spasi dihapus
            if NAMA_KOLOM_ANGKATAN in df.columns:
                bar_data = df[NAMA_KOLOM_ANGKATAN].value_counts().reset_index()
                bar_data.columns = [NAMA_KOLOM_ANGKATAN, 'Jumlah Mahasiswa']
                
                fig_bar = px.bar(
                    bar_data,
                    x=NAMA_KOLOM_ANGKATAN,
                    y='Jumlah Mahasiswa',
                    title='Jumlah Mahasiswa per Angkatan',
                    text_auto=True
                )
                st.plotly_chart(fig_bar, use_container_width=True, key="dist_bar_angkatan")
            else:
                st.warning(f"Kolom '{NAMA_KOLOM_ANGKATAN}' tidak ditemukan.")

        st.divider()

        # --- BARIS KEDUA VISUALISASI ---
        col3_tab2, col4_tab2 = st.columns(2)

        with col3_tab2:
            NAMA_KOLOM_TAHUN = 'Mulai aktif bermain'
            if NAMA_KOLOM_TAHUN in df.columns:
                line_data_tab2 = df[NAMA_KOLOM_TAHUN].value_counts().sort_index().reset_index()
                line_data_tab2.columns = ['Tahun', 'Jumlah Responden']
                
                fig_line_tab2 = px.line(
                    line_data_tab2,
                    x='Tahun',
                    y='Jumlah Responden',
                    title='Distribusi Tahun Mulai Bermain Roblox',
                    markers=True
                )
                fig_line_tab2.update_xaxes(type='category')
                st.plotly_chart(fig_line_tab2, use_container_width=True, key="dist_line_chart")
            else:
                st.warning(f"Kolom '{NAMA_KOLOM_TAHUN}' tidak ditemukan.")
        
        with col4_tab2:
            NAMA_KOLOM_ALASAN = 'Alasan bermain roblox'
            if NAMA_KOLOM_ALASAN in df.columns:
                hbar_data = df[NAMA_KOLOM_ALASAN].value_counts().reset_index()
                hbar_data.columns = ['Alasan', 'Jumlah Responden']
                
                fig_hbar = px.bar(
                    hbar_data.sort_values('Jumlah Responden', ascending=True),
                    x='Jumlah Responden',
                    y='Alasan',
                    orientation='h',
                    title='Distribusi Alasan Utama Bermain Roblox',
                    text_auto=True
                )
                st.plotly_chart(fig_hbar, use_container_width=True, key="dist_hbar_alasan")
            else:
                st.warning(f"Kolom '{NAMA_KOLOM_ALASAN}' tidak ditemukan.")
        
        st.divider()

        # --- BARIS KETIGA VISUALISASI ---
        col5_tab2, col6_tab2 = st.columns(2)

        with col5_tab2:
            NAMA_KOLOM_PENGARUH = 'Pengaruh kehidupan kuliah'
            if NAMA_KOLOM_PENGARUH in df.columns:
                pengaruh_data_tab2 = df[NAMA_KOLOM_PENGARUH].value_counts().reset_index()
                pengaruh_data_tab2.columns = ['Kategori Pengaruh', 'Jumlah Responden']
                
                fig_pengaruh_tab2 = px.bar(
                    pengaruh_data_tab2,
                    x='Kategori Pengaruh',
                    y='Jumlah Responden',
                    title='Distribusi Pengaruh terhadap Kehidupan Kuliah',
                    text_auto=True,
                    category_orders={"Kategori Pengaruh": ["Netral", "Positif", "Negatif"]},
                    color='Kategori Pengaruh',
                    color_discrete_map={
                        'Netral': '#D6EAF8',
                        'Positif': '#85C1E9',
                        'Negatif': '#3498DB'
                    }
                )
                st.plotly_chart(fig_pengaruh_tab2, use_container_width=True, key="dist_bar_pengaruh")
            else:
                st.warning(f"Kolom '{NAMA_KOLOM_PENGARUH}' tidak ditemukan.")

        with col6_tab2:
            NAMA_KOLOM_SKALA = 'Hiburan untuk perkuliahan'
            if NAMA_KOLOM_SKALA in df.columns:
                bubble_data = df[NAMA_KOLOM_SKALA].value_counts().reset_index()
                bubble_data.columns = ['Skala Pengaruh', 'Jumlah Responden']

                fig_bubble = px.scatter(
                    bubble_data,
                    x='Skala Pengaruh',
                    y='Jumlah Responden',
                    size='Jumlah Responden',
                    text='Jumlah Responden',
                    title='Diagram Gelembung: Pengaruh Roblox terhadap Hiburan',
                    size_max=60
                )
                fig_bubble.update_traces(textposition='top center')
                st.plotly_chart(fig_bubble, use_container_width=True, key="dist_bubble_chart")
            else:
                st.warning(f"Kolom '{NAMA_KOLOM_SKALA}' tidak ditemukan.")

else:
    # Pesan ini hanya akan muncul jika path lokal salah dan tidak ada file yang diunggah.

    st.warning("Data tidak dapat dimuat. Periksa path file lokal Anda atau unggah file baru.")


