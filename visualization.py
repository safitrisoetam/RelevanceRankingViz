import streamlit as st
import pandas as pd
import re
import time

#PAGE###########################################################################
st.set_page_config(page_title='Tugas Akhir',layout="wide",
page_icon=':books:')
#HEADER#########################################################################
st.header('Pemeringkatan Relevansi Artikel Jurnal Ilmiah Berbahasa Indonesia Menggunakan Metode Ekspansi Kueri Berdasarkan Indonesian Bidirectional Encoder Representation from Transformers')
#QUERY##########################################################################
q_awal = pd.read_excel('database.xlsx',sheet_name = 'q_awal')
base = pd.read_excel('database.xlsx',sheet_name = 'base')
manual = pd.read_excel('database.xlsx',sheet_name = 'manual')
ib = pd.read_excel('database.xlsx', sheet_name = 'ib')
bm = pd.read_excel('database.xlsx', sheet_name = 'bm')
ibqe = pd.read_excel('database.xlsx', sheet_name = 'ibqe')
bmqe = pd.read_excel('database.xlsx', sheet_name = 'bmqe')
bmwv = pd.read_excel('database.xlsx', sheet_name = 'bmwv')
ibkm = pd.read_excel('database.xlsx', sheet_name = 'ibkm')
ibhb = pd.read_excel('database.xlsx', sheet_name = 'ibhd')
skenario = pd.read_excel('database.xlsx', sheet_name = 'skenario')
metode = pd.read_excel('database.xlsx', sheet_name = 'metode')
compile = pd.read_excel('database.xlsx', sheet_name = 'compile')

##################################################
with st.expander('Lihat Data Latih'):
    manual_show = manual.drop(columns=['ID Webcrawl','Penulis Artikel','Jurnal',
    'Penerbit','Tanggal Terbit Artikel','URL Artikel'])
    dict_manual = {'Label_Aljabar':'Aljabar','Label_Analisis':'Analisis',
    'Label_Citra':'Citra','Label_Data':'Data','Label_Industri':'Industri',
    'Label_Keuangan':'Keuangan','Label_Pemodelan':'Pemodelan',
    'Label_Pemrograman':'Pemrograman','Label_Pendidikan':'Pendidikan',
    'Label_Simulasi':'Simulasi'}
    manual_show.rename(columns=dict_manual,inplace=True)
    st.dataframe(manual_show)
################################################################################
with st.form(key='satu'):
    row_1, row_2, row_3, row_4 = st.columns([0.55, 0.95, 1.3, 1])
    pilih_kueri = row_1.selectbox ('Pilih Kueri Awal',
        ('','Aljabar','Analisis','Citra','Data','Industri','Keuangan','Pemodelan',
        'Pemrograman','Pendidikan','Simulasi'), key='pil_q')
    pilih_sken = row_2.selectbox('Pilih Skenario',('','Pencarian Judul dan Abstrak',
        'Pencarian Judul','Pencarian Abstrak'), key='pil_sken')
    pilih_met = row_3.selectbox('Pilih Metode',('','IndoBERT', 'IndoBERT + QE',
        'IndoBERT + QE Refinement K-Means', 'IndoBERT + QE Refinement UMAP + HDBSCAN',
        'Okapi-BM25','Okapi-BM25 + QE', 'Okapi-BM25 + Word2Vec + QE'),
        key='pil_met')
    submit_button1 = st.form_submit_button(label='Cari Artikel!')
    if submit_button1:
        if pilih_kueri == 'Aljabar':
            if pilih_sken == 'Pencarian Judul dan Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Matriks','Max Plus','Matriks Skew Hermitian'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Matriks':
                        show = compile[[f'BM25+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Max Plus':
                        show = compile[[f'BM25+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Matriks Skew Hermitian':
                        show = compile[[f'BM25+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Matriks','Max Plus','Matriks Skew Hermitian'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Matriks':
                        show = compile[[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Max Plus':
                        show = compile[[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Matriks Skew Hermitian':
                        show = compile[[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Matriks','Kode Siklik','Teorema Polya II'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Matriks':
                        show = compile[[f'IndoBERT+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kode Siklik':
                        show = compile[[f'IndoBERT+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Teorema Polya II':
                        show = compile[[f'IndoBERT+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Himpunan','Bilangan Bulat','Bilangan Bulat Positif'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Himpunan':
                        show = compile[[f'K-Means_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bilangan Bulat':
                        show = compile[[f'K-Means_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bilangan Bulat Positif':
                        show = compile[[f'K-Means_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Ruang','Ruang Norm','Ring Reguler Stable'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Ruang':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Norm':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ring Reguler Stable':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Aljabar':
            if pilih_sken == 'Pencarian Judul':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Max Plus','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Max Plus':
                        show = compile[[f'BM25+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Matriks','Fuzzy Smarandache','Premi Tunggal Bersih'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Matriks':
                        show = compile[[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Fuzzy Smarandache':
                        show = compile[[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Premi Tunggal Bersih':
                        show = compile[[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Persamaan','Ruang Norm','Subnear Ring Fuzzy'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Persamaan':
                        show = compile[[f'IndoBERT+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Norm':
                        show = compile[[f'IndoBERT+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Subnear Ring Fuzzy':
                        show = compile[[f'IndoBERT+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Graf','Solusi Persamaan','Lengkap Berarah Graf'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Graf':
                        show = compile[[f'K-Means_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Solusi Persamaan':
                        show = compile[[f'K-Means_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Lengkap Berarah Graf':
                        show = compile[[f'K-Means_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Graf','Graf Lintasan','Lengkap Berarah Graf'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Graf':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Graf Lintasan':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Lengkap Berarah Graf':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Aljabar':
            if pilih_sken == 'Pencarian Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Sifat','Max Plus','Ideal Fuzzy Smarandache'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Sifat':
                        show = compile[[f'BM25+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Max Plus':
                        show = compile[[f'BM25+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ideal Fuzzy Smarandache':
                        show = compile[[f'BM25+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Penelitian','Fuzzy Smarandache','Ideal Fuzzy Smarandache'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Penelitian':
                        show = compile[[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Fuzzy Smarandache':
                        show = compile[[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ideal Fuzzy Smarandache':
                        show = compile[[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Struktur','Fuzzy Smarandache','Teorema Polya II'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Struktur':
                        show = compile[[f'IndoBERT+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Fuzzy Smarandache':
                        show = compile[[f'IndoBERT+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Teorema Polya II':
                        show = compile[[f'IndoBERT+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Himpunan','Bilangan Bulat','Bilangan Bulat Positif'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Himpunan':
                        show = compile[[f'K-Means_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bilangan Bulat':
                        show = compile[[f'K-Means_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bilangan Bulat Positif':
                        show = compile[[f'K-Means_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Graf','Persamaan Diferensial','Bilangan Bulat Positif'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Graf':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Persamaan Diferensial':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bilangan Bulat Positif':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Analisis':
            if pilih_sken == 'Pencarian Judul dan Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Data','Titik Kesetimbangan','Kemampuan Berpikir Kreatif'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Data':
                        show = compile[[f'BM25+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Titik Kesetimbangan':
                        show = compile[[f'BM25+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kemampuan Berpikir Kreatif':
                        show = compile[[f'BM25+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Hasil','Grup Sunspot','Membangkitkan Flare Soft'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Hasil':
                        show = compile[[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Grup Sunspot':
                        show = compile[[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Membangkitkan Flare Soft':
                        show = compile[[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Harga Saham','Regresi Data Panel'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'IndoBERT+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Harga Saham':
                        show = compile[[f'IndoBERT+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Regresi Data Panel':
                        show = compile[[f'IndoBERT+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Regresi','Model Regresi','Hasil Belajar Matematika'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Regresi':
                        show = compile[[f'K-Means_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Regresi':
                        show = compile[[f'K-Means_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Hasil Belajar Matematika':
                        show = compile[[f'K-Means_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Graf','Ruang Metrik','Ruang Metrik Cone'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Graf':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Metrik':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Metrik Cone':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Analisis':
            if pilih_sken == 'Pencarian Judul':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Persegi Ajaib','Penduduk Kota Pasuruan'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'BM25+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Persegi Ajaib':
                        show = compile[[f'BM25+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Penduduk Kota Pasuruan':
                        show = compile[[f'BM25+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Data','Kemampuan Berpikir','Membangkitkan Flare Soft'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Data':
                        show = compile[[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kemampuan Berpikir':
                        show = compile[[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Membangkitkan Flare Soft':
                        show = compile[[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Matriks','Valuasi Diskrit','Tinjauan Grup Cogenerated'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Matriks':
                        show = compile[[f'IndoBERT+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Valuasi Diskrit':
                        show = compile[[f'IndoBERT+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Tinjauan Grup Cogenerated':
                        show = compile[[f'IndoBERT+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Ring','Near Ring','Fuzzy Sliding Mode'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Ring':
                        show = compile[[f'K-Means_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Near Ring':
                        show = compile[[f'K-Means_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Fuzzy Sliding Mode':
                        show = compile[[f'K-Means_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Ruang','Ruang Metrik','Ruang Metrik Cone'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Ruang':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Metrik':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Metrik Cone':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Analisis':
            if pilih_sken == 'Pencarian Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Data','Titik Kesetimbangan','Kemampuan Berpikir Kreatif'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Data':
                        show = compile[[f'BM25+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Titik Kesetimbangan':
                        show = compile[[f'BM25+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kemampuan Berpikir Kreatif':
                        show = compile[[f'BM25+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Faktor','Kreatif Matematik','Kemampuan Berpikir Kreatif'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Faktor':
                        show = compile[[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kreatif Matematik':
                        show = compile[[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kemampuan Berpikir Kreatif':
                        show = compile[[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Model Grey','Model Grey Markov'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'IndoBERT+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Grey':
                        show = compile[[f'IndoBERT+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Grey Markov':
                        show = compile[[f'IndoBERT+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Regresi','Titik Kesetimbangan','Angka Reproduksi Dasar'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Regresi':
                        show = compile[[f'K-Means_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Titik Kesetimbangan':
                        show = compile[[f'K-Means_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Angka Reproduksi Dasar':
                        show = compile[[f'K-Means_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Matriks','Model Regresi','Solusi Persamaan Diferensial'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Matriks':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Regresi':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Solusi Persamaan Diferensial':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Citra':
            if pilih_sken == 'Pencarian Judul dan Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Bifurkasi HOPF','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bifurkasi HOPF':
                        show = compile[[f'BM25+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Hasil','Premi Tunggal','Hidup Unit Link'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Hasil':
                        show = compile[[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Premi Tunggal':
                        show = compile[[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Hidup Unit Link':
                        show = compile[[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Data','Data Mining','PTSP Kota Banda'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Data':
                        show = compile[[f'IndoBERT+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Data Mining':
                        show = compile[[f'IndoBERT+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'PTSP Kota Banda':
                        show = compile[[f'IndoBERT+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Matriks','Ruang Metrik','Ruang Metrik Cone'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Matriks':
                        show = compile[[f'K-Means_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Metrik':
                        show = compile[[f'K-Means_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Metrik Cone':
                        show = compile[[f'K-Means_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Tanaman','Tanaman Jagung','Pertumbuhan Tanaman Jagung'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Tanaman':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Tanaman Jagung':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Pertumbuhan Tanaman Jagung':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Citra':
            if pilih_sken == 'Pencarian Judul':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Kedalaman Spiritual','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kedalaman Spiritual':
                        show = compile[[f'BM25+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Titik Setimbang','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Titik Setimbang':
                        show = compile[[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Ring','Ruang Norm','Subnear Ring Fuzzy'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Ring':
                        show = compile[[f'IndoBERT+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Norm':
                        show = compile[[f'IndoBERT+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Subnear Ring Fuzzy':
                        show = compile[[f'IndoBERT+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Wavelet','Transformasi Wavelet','Support Vector Machine'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Wavelet':
                        show = compile[[f'K-Means_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Transformasi Wavelet':
                        show = compile[[f'K-Means_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Support Vector Machine':
                        show = compile[[f'K-Means_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Wavelet','Transformasi Wavelet','Tangan Digital Elgamal'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Wavelet':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Transformasi Wavelet':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Tangan Digital Elgamal':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Citra':
            if pilih_sken == 'Pencarian Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Bifurkasi HOPF','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bifurkasi HOPF':
                        show = compile[[f'BM25+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Asuransi','Asuransi Jiwa','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Asuransi':
                        show = compile[[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Asuransi Jiwa':
                        show = compile[[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Data Mining','Ring Valuasi Diskrit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'IndoBERT+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Data Mining':
                        show = compile[[f'IndoBERT+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ring Valuasi Diskrit':
                        show = compile[[f'IndoBERT+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Matriks','Ruang Metrik','Ruang Metrik Cone'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Matriks':
                        show = compile[[f'K-Means_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Metrik':
                        show = compile[[f'K-Means_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Metrik Cone':
                        show = compile[[f'K-Means_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Ruang','Menggunakan Metode','Jaringan Syaraf Tiruan'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Ruang':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Menggunakan Metode':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Jaringan Syaraf Tiruan':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Data':
            if pilih_sken == 'Pencarian Judul dan Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Model Grey','Jaringan Saraf Tiruan'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'BM25+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Grey':
                        show = compile[[f'BM25+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Jaringan Saraf Tiruan':
                        show = compile[[f'BM25+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Penelitian','Kota Pasuruan','PTSP Kota Banda'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Penelitian':
                        show = compile[[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kota Pasuruan':
                        show = compile[[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'PTSP Kota Banda':
                        show = compile[[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Curah Hujan','Pendapatan Asli Daerah'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'IndoBERT+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Curah Hujan':
                        show = compile[[f'IndoBERT+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Pendapatan Asli Daerah':
                        show = compile[[f'IndoBERT+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Kota','Curah Hujan','Jumlah Curah Hujan'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Kota':
                        show = compile[[f'K-Means_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Curah Hujan':
                        show = compile[[f'K-Means_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Jumlah Curah Hujan':
                        show = compile[[f'K-Means_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Regresi','Regresi Logistik','Regresi Logistik Ordial'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Regresi':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Regresi Logistik':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Regresi Logistik Ordial':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Data':
            if pilih_sken == 'Pencarian Judul':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Jawa Barat','Membangkitkan Flare Soft'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'BM25+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Jawa Barat':
                        show = compile[[f'BM25+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Membangkitkan Flare Soft':
                        show = compile[[f'BM25+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Jawa Barat','Jaringan Saraf Tiruan'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Jawa Barat':
                        show = compile[[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Jaringan Saraf Tiruan':
                        show = compile[[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Analisis','Ruang Norm','Submodul Prima Gabungan'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Analisis':
                        show = compile[[f'IndoBERT+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Norm':
                        show = compile[[f'IndoBERT+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Submodul Prima Gabungan':
                        show = compile[[f'IndoBERT+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Analisis','Provinsi Maluku','Saraf Tiruan Backpropagation'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Analisis':
                        show = compile[[f'K-Means_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Provinsi Maluku':
                        show = compile[[f'K-Means_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Saraf Tiruan Backpropagation':
                        show = compile[[f'K-Means_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Analisis','Metode Analisis','Indeks Pembangunan Manusia'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Analisis':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Metode Analisis':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Indeks Pembangunan Manusia':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Data':
            if pilih_sken == 'Pencarian Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Model Grey','Jaringan Saraf Tiruan'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'BM25+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Grey':
                        show = compile[[f'BM25+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Jaringan Saraf Tiruan':
                        show = compile[[f'BM25+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Penelitian','Model Grey','Model Grey Markov'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Penelitian':
                        show = compile[[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Grey':
                        show = compile[[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Grey Markov':
                        show = compile[[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Curah Hujan','Model Grey Markov'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'IndoBERT+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Curah Hujan':
                        show = compile[[f'IndoBERT+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Grey Markov':
                        show = compile[[f'IndoBERT+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Masyarakat','Provinsi Maluku','Angka Kematian Bayi'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Masyarakat':
                        show = compile[[f'K-Means_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Provinsi Maluku':
                        show = compile[[f'K-Means_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Angka Kematian Bayi':
                        show = compile[[f'K-Means_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Terinfeksi','Individu Terjangkit','Rentan Terpapar Terinfeksi'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Terinfeksi':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Individu Terjangkit':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Rentan Terpapar Terinfeksi':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Industri':
            if pilih_sken == 'Pencarian Judul dan Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Diagram Kontrol','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Diagram Kontrol':
                        show = compile[[f'BM25+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Penelitian','Kinerja Diagram','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Penelitian':
                        show = compile[[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kinerja Diagram':
                        show = compile[[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Citra','Diagram Kontrol','Kinerja Diagram Kontrol'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Citra':
                        show = compile[[f'IndoBERT+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Diagram Kontrol':
                        show = compile[[f'IndoBERT+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kinerja Diagram Kontrol':
                        show = compile[[f'IndoBERT+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Mahasiswa','Harga Saham','Kinerja Diagram Kontrol'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Mahasiswa':
                        show = compile[[f'K-Means_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Harga Saham':
                        show = compile[[f'K-Means_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kinerja Diagram Kontrol':
                        show = compile[[f'K-Means_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Diferensial','Persamaan Diferensial','Persamaan Diferensial Fraksional'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Diferensial':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Persamaan Diferensial':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Persamaan Diferensial Fraksional':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Industri':
            if pilih_sken == 'Pencarian Judul':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Program Studi','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Program Studi':
                        show = compile[[f'BM25+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Minimal','Model Terbaik','Regresi Data Panel'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Minimal':
                        show = compile[[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Terbaik':
                        show = compile[[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Regresi Data Panel':
                        show = compile[[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Ruang','Ruang Norm','Tinjauan Grup Cogenerated'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Ruang':
                        show = compile[[f'IndoBERT+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Norm':
                        show = compile[[f'IndoBERT+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Tinjauan Grup Cogenerated':
                        show = compile[[f'IndoBERT+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Sistem','Mode Control','Mode Control SME'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Sistem':
                        show = compile[[f'K-Means_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Mode Control':
                        show = compile[[f'K-Means_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Mode Control SME':
                        show = compile[[f'K-Means_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Persamaan','Persamaan Diferensial','Persamaan Diferensial Fraksional'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Persamaan':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Persamaan Diferensial':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Persamaan Diferensial Fraksional':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Industri':
            if pilih_sken == 'Pencarian Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Diagram Kontrol','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Diagram Kontrol':
                        show = compile[[f'BM25+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Penelitian','Diagram Kontrol','Jiwa Seumur Hidup'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Penelitian':
                        show = compile[[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Diagram Kontrol':
                        show = compile[[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Jiwa Seumur Hidup':
                        show = compile[[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Pertumbuhan Ekonomi','Tingkat Pengangguran Terbuka'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'IndoBERT+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Pertumbuhan Ekonomi':
                        show = compile[[f'IndoBERT+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Tingkat Pengangguran Terbuka':
                        show = compile[[f'IndoBERT+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Kota','Hasil Penelitian','Penyakit Jantung Koroner'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Kota':
                        show = compile[[f'K-Means_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Hasil Penelitian':
                        show = compile[[f'K-Means_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Penyakit Jantung Koroner':
                        show = compile[[f'K-Means_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Fuzzy','Tujuan Penelitian','Persamaan Diferensial Fraksional'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Fuzzy':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Tujuan Penelitian':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Persamaan Diferensial Fraksional':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Keuangan':
            if pilih_sken == 'Pencarian Judul dan Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Kedalaman Spiritual','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kedalaman Spiritual':
                        show = compile[[f'BM25+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Regresi','Unit Link','Metode Point To'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Regresi':
                        show = compile[[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Unit Link':
                        show = compile[[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Metode Point To':
                        show = compile[[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Ms. Excel','Aset Bebas Risiko'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'IndoBERT+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ms. Excel':
                        show = compile[[f'IndoBERT+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Aset Bebas Risiko':
                        show = compile[[f'IndoBERT+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Asuransi','Titik Kesetimbangan','Regresi Logistik Biner'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Asuransi':
                        show = compile[[f'K-Means_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Titik Kesetimbangan':
                        show = compile[[f'K-Means_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Regresi Logistik Biner':
                        show = compile[[f'K-Means_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Persamaan','Solusi Persamaan','Solusi Persamaan Diferensial'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Persamaan':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Solusi Persamaan':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Solusi Persamaan Diferensial':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Keuangan':
            if pilih_sken == 'Pencarian Judul':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Unit Link','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Unit Link':
                        show = compile[[f'BM25+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Dampak','Regresi Nonparametrik','Metode Point To'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Dampak':
                        show = compile[[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Regresi Nonparametrik':
                        show = compile[[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Metode Point To':
                        show = compile[[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Ruang','Ruang Norm','Subnear Ring Fuzzy'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Ruang':
                        show = compile[[f'IndoBERT+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Norm':
                        show = compile[[f'IndoBERT+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Subnear Ring Fuzzy':
                        show = compile[[f'IndoBERT+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Algoritma','Sliding Mode','Sliding Mode Control'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Algoritma':
                        show = compile[[f'K-Means_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Sliding Mode':
                        show = compile[[f'K-Means_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Sliding Mode Control':
                        show = compile[[f'K-Means_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Solusi','Solusi Persamaan','Solusi Persamaan Diferensial'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Solusi':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Solusi Persamaan':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Solusi Persamaan Diferensial':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Keuangan':
            if pilih_sken == 'Pencarian Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Kedalaman Spiritual','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kedalaman Spiritual':
                        show = compile[[f'BM25+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Hasil','Unit Link','Metode Point To'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Hasil':
                        show = compile[[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Unit Link':
                        show = compile[[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Metode Point To':
                        show = compile[[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Data','Harga Saham','Tingkat Pengangguran Terbuka'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Data':
                        show = compile[[f'IndoBERT+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Harga Saham':
                        show = compile[[f'IndoBERT+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Tingkat Pengangguran Terbuka':
                        show = compile[[f'IndoBERT+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Asuransi','Tujuan Penelitian','Mean Square Error'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Asuransi':
                        show = compile[[f'K-Means_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Tujuan Penelitian':
                        show = compile[[f'K-Means_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Mean Square Error':
                        show = compile[[f'K-Means_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Faktor','Penelitian Adalah','Digunakan Penelitian Adalah'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Faktor':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Penelitian Adalah':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Digunakan Penelitian Adalah':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Pemodelan':
            if pilih_sken == 'Pencarian Judul dan Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Regresi Linier','Indeks Pembangunan Manusia'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'BM25+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Regresi Linier':
                        show = compile[[f'BM25+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Indeks Pembangunan Manusia':
                        show = compile[[f'BM25+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Hutan Bakau','Indeks Pembangunan Manusia'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Hutan Bakau':
                        show = compile[[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Indeks Pembangunan Manusia':
                        show = compile[[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Tanaman Jagung','Pertumbuhan Tanaman Jagung'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'IndoBERT+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Tanaman Jagung':
                        show = compile[[f'IndoBERT+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Pertumbuhan Tanaman Jagung':
                        show = compile[[f'IndoBERT+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Ruang','Persamaan Diferensial','Persamaan Diferensial Fraksional'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Ruang':
                        show = compile[[f'K-Means_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Persamaan Diferensial':
                        show = compile[[f'K-Means_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Persamaan Diferensial Fraksional':
                        show = compile[[f'K-Means_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Penyakit','Penyebaran Penyakit','Penyebaran Penyakit SARS'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Penyakit':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Penyebaran Penyakit':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Penyebaran Penyakit SARS':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Pemodelan':
            if pilih_sken == 'Pencarian Judul':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Tanaman Jagung','Pertumbuhan Tanaman Jagung'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'BM25+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Tanaman Jagung':
                        show = compile[[f'BM25+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Pertumbuhan Tanaman Jagung':
                        show = compile[[f'BM25+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Variabel','Regresi Linear','Model Regresi Linier'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Variabel':
                        show = compile[[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Regresi Linear':
                        show = compile[[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Regresi Linier':
                        show = compile[[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Analisis','Transformasi Wavelet','Wavelet Prapengolahan Sinyal'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Analisis':
                        show = compile[[f'IndoBERT+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Transformasi Wavelet':
                        show = compile[[f'IndoBERT+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Wavelet Prapengolahan Sinyal':
                        show = compile[[f'IndoBERT+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Model Matematika','Jaringan Saraf Tiruan'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'K-Means_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Matematika':
                        show = compile[[f'K-Means_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Jaringan Saraf Tiruan':
                        show = compile[[f'K-Means_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Model Matematika','Model Matematika Penyebaran'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Matematika':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Matematika Penyebaran':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Pemodelan':
            if pilih_sken == 'Pencarian Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Model Regresi','Indeks Pembangunan Manusia'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'BM25+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Regresi':
                        show = compile[[f'BM25+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Indeks Pembangunan Manusia':
                        show = compile[[f'BM25+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Hasil','Mata Kuliah','Indeks Pembangunan Manusia'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Hasil':
                        show = compile[[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Mata Kuliah':
                        show = compile[[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Indeks Pembangunan Manusia':
                        show = compile[[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Titik Ekuilibrium','Equilibrium Point is'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'IndoBERT+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Titik Ekuilibrium':
                        show = compile[[f'IndoBERT+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Equilibrium Point is':
                        show = compile[[f'IndoBERT+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Persamaan','Persamaan Diferensial','Solusi Persamaan Diferensial'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Persamaan':
                        show = compile[[f'K-Means_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Persamaan Diferensial':
                        show = compile[[f'K-Means_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Solusi Persamaan Diferensial':
                        show = compile[[f'K-Means_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Penyakit','Model Penyebaran','Bilangan Reproduksi Dasar'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Penyakit':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Penyebaran':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bilangan Reproduksi Dasar':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Pemrograman':
            if pilih_sken == 'Pencarian Judul dan Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Kedalaman Spiritual','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kedalaman Spiritual':
                        show = compile[[f'BM25+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Data','Kedalaman Spiritual','Bersih Asuransi Jiwa'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Data':
                        show = compile[[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kedalaman Spiritual':
                        show = compile[[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bersih Asuransi Jiwa':
                        show = compile[[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Algoritma','Kode Siklik','Worm Berbasis Wi'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Algoritma':
                        show = compile[[f'IndoBERT+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kode Siklik':
                        show = compile[[f'IndoBERT+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Worm Berbasis Wi':
                        show = compile[[f'IndoBERT+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Graf','Ruang Norm','Solusi Persamaan Diferensial'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Graf':
                        show = compile[[f'K-Means_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Norm':
                        show = compile[[f'K-Means_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Solusi Persamaan Diferensial':
                        show = compile[[f'K-Means_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Algoritma','Algoritma Genetika','Dimensional Principal Component'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Algoritma':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Algoritma Genetika':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Dimensional Principal Component':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Pemrograman':
            if pilih_sken == 'Pencarian Judul':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Unit Link','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Unit Link':
                        show = compile[[f'BM25+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Prediksi','Flare Soft','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Prediksi':
                        show = compile[[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Flare Soft':
                        show = compile[[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Ring','Valuasi Diskrit','Tinjauan Grup Cogenerated'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Ring':
                        show = compile[[f'IndoBERT+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Valuasi Diskrit':
                        show = compile[[f'IndoBERT+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Tinjauan Grup Cogenerated':
                        show = compile[[f'IndoBERT+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Persamaan','Persamaan Diferensial','Solusi Persamaan Diferensial'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Persamaan':
                        show = compile[[f'K-Means_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Persamaan Diferensial':
                        show = compile[[f'K-Means_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Solusi Persamaan Diferensial':
                        show = compile[[f'K-Means_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Algoritma','Nearest Neighbor','Penerapan Hirearchucal Clustering'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Algoritma':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Nearest Neighbor':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Penerapan Hirearchucal Clustering':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Pemrograman':
            if pilih_sken == 'Pencarian Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Kedalaman Spiritual','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kedalaman Spiritual':
                        show = compile[[f'BM25+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Data','Kedalaman Spiritual','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Data':
                        show = compile[[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kedalaman Spiritual':
                        show = compile[[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Algoritma','Teorema Polya','Teorema Polya II'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Algoritma':
                        show = compile[[f'IndoBERT+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Teorema Polya':
                        show = compile[[f'IndoBERT+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Teorema Polya II':
                        show = compile[[f'IndoBERT+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Parameter','Diagram Kontrol','Jaringan Syaraf Tiruan'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Parameter':
                        show = compile[[f'K-Means_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Diagram Kontrol':
                        show = compile[[f'K-Means_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Jaringan Syaraf Tiruan':
                        show = compile[[f'K-Means_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Penyebaran','Penyebaran Penyakit','Log Logistic Parameter'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Penyebaran':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Penyebaran Penyakit':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Log Logistic Parameter':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Pendidikan':
            if pilih_sken == 'Pencarian Judul dan Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Penelitian','Rumah Tangga','Indeks Pembangunan Manusia'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Penelitian':
                        show = compile[[f'BM25+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Rumah Tangga':
                        show = compile[[f'BM25+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Indeks Pembangunan Manusia':
                        show = compile[[f'BM25+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Mahasiswa','Unit Link','Materi Linear Programming'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Mahasiswa':
                        show = compile[[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Unit Link':
                        show = compile[[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Materi Linear Programming':
                        show = compile[[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Faktor','Provinsi Maluku','Status Gizi Buruk'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Faktor':
                        show = compile[[f'IndoBERT+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Provinsi Maluku':
                        show = compile[[f'IndoBERT+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Status Gizi Buruk':
                        show = compile[[f'IndoBERT+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Belajar','Model Pembelajaran','Belajar Matematika Siswa'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Belajar':
                        show = compile[[f'K-Means_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Pembelajaran':
                        show = compile[[f'K-Means_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Belajar Matematika Siswa':
                        show = compile[[f'K-Means_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Provinsi','Provinsi Maluku','Indeks Pembangunan Manusia'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Provinsi':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Provinsi Maluku':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Indeks Pembangunan Manusia':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Pendidikan':
            if pilih_sken == 'Pencarian Judul':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Mata Kuliah','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Mata Kuliah':
                        show = compile[[f'BM25+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Dasar','Data Time','Membangkitkan Flare Soft'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Dasar':
                        show = compile[[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Data Time':
                        show = compile[[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Membangkitkan Flare Soft':
                        show = compile[[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Ruang','Ruang Norm','Subnear Ring Fuzzy'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Ruang':
                        show = compile[[f'IndoBERT+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Norm':
                        show = compile[[f'IndoBERT+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Subnear Ring Fuzzy':
                        show = compile[[f'IndoBERT+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Faktor','Analisis Regresi','Indeks Pembangunan Manusia'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Faktor':
                        show = compile[[f'K-Means_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Analisis Regresi':
                        show = compile[[f'K-Means_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Indeks Pembangunan Manusia':
                        show = compile[[f'K-Means_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Faktor','Faktor Mempengaruhi','Faktor Mempengaruhi Indeks'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Faktor':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Faktor Mempengaruhi':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Faktor Mempengaruhi Indeks':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Pendidikan':
            if pilih_sken == 'Pencarian Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Penelitian','Unit Link','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Penelitian':
                        show = compile[[f'BM25+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Unit Link':
                        show = compile[[f'BM25+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Linear','Unit Link','Metode Point To'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Linear':
                        show = compile[[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Unit Link':
                        show = compile[[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Metode Point To':
                        show = compile[[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Data','Tingkat Pengangguran','Tingkat Pengangguran Terbuka'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Data':
                        show = compile[[f'IndoBERT+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Tingkat Pengangguran':
                        show = compile[[f'IndoBERT+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Tingkat Pengangguran Terbuka':
                        show = compile[[f'IndoBERT+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Belajar','Model Pembelajaran','Belajar Matematika Siswa'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Belajar':
                        show = compile[[f'K-Means_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Pembelajaran':
                        show = compile[[f'K-Means_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Belajar Matematika Siswa':
                        show = compile[[f'K-Means_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Individu','Individu Terinfeksi','Kelas Rentan Terpapar'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Individu':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Individu Terinfeksi':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kelas Rentan Terpapar':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Simulasi':
            if pilih_sken == 'Pencarian Judul dan Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_1_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Penyebaran SARS','Bilangan Reproduksi Dasar'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'BM25+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Penyebaran SARS':
                        show = compile[[f'BM25+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bilangan Reproduksi Dasar':
                        show = compile[[f'BM25+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Data','Kalman Filter','Rentan Terpapar Infeksi'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Data':
                        show = compile[[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Kalman Filter':
                        show = compile[[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Rentan Terpapar Infeksi':
                        show = compile[[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Bebas Risiko','Aset Bebas Risiko'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'IndoBERT+QE_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bebas Risiko':
                        show = compile[[f'IndoBERT+QE_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Aset Bebas Risiko':
                        show = compile[[f'IndoBERT+QE_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Hujan','Reproduksi Dasar','Angka Reproduksi Dasar'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Hujan':
                        show = compile[[f'K-Means_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Reproduksi Dasar':
                        show = compile[[f'K-Means_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Angka Reproduksi Dasar':
                        show = compile[[f'K-Means_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Penyakit','Reproduksi Dasar','Bilangan Reproduksi Dasar'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Penyakit':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Reproduksi Dasar':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bilangan Reproduksi Dasar':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_1_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Simulasi':
            if pilih_sken == 'Pencarian Judul':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_2_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Metode','Unit Link','Seumur Hidup Unit'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Metode':
                        show = compile[[f'BM25+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Unit Link':
                        show = compile[[f'BM25+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Seumur Hidup Unit':
                        show = compile[[f'BM25+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Model Matematika','Bilangan Reproduksi Dasar'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Matematika':
                        show = compile[[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bilangan Reproduksi Dasar':
                        show = compile[[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Ruang','Ruang Norm','Tinjauan Grup Cogenerated'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Ruang':
                        show = compile[[f'IndoBERT+QE_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Norm':
                        show = compile[[f'IndoBERT+QE_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Tinjauan Grup Cogenerated':
                        show = compile[[f'IndoBERT+QE_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Ruang','Ruang Metrik','Solusi Persamaan Difusi'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Ruang':
                        show = compile[[f'K-Means_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Ruang Metrik':
                        show = compile[[f'K-Means_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Solusi Persamaan Difusi':
                        show = compile[[f'K-Means_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Penyebaran','Penyebaran Penyakit','Model Penyebaran Virus'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Penyebaran':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Penyebaran Penyakit':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Penyebaran Virus':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_2_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
        if pilih_kueri == 'Simulasi':
            if pilih_sken == 'Pencarian Abstrak':
                if pilih_met == 'IndoBERT':
                    show = compile[[f'IndoBERT_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'IndoBERT_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'IndoBERT_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25':
                    show = compile[[f'BM25_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                    show = show.sort_values(by=[f'BM25_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                    show_rename = {f'BM25_3_{pilih_kueri}':'Nilai Relevansi'}
                    show.rename(columns=show_rename,inplace=True)
                    show = show[show['Nilai Relevansi'] > 0]
                    show.reset_index(drop=True)
                    st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri}"')
                    st.dataframe(show)
                elif pilih_met == 'Okapi-BM25 + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Penyebaran SARS','Bilangan Reproduksi Dasar'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'BM25+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Penyebaran SARS':
                        show = compile[[f'BM25+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bilangan Reproduksi Dasar':
                        show = compile[[f'BM25+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'Okapi-BM25 + Word2Vec + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Populasi','Suku Difusi','Bilangan Reproduksi Dasar'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Populasi':
                        show = compile[[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Suku Difusi':
                        show = compile[[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bilangan Reproduksi Dasar':
                        show = compile[[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'BM25+Word2Vec_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'BM25+Word2Vec_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Model','Modul Bebas','Model Siklus Bisnis'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Model':
                        show = compile[[f'IndoBERT+QE_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Modul Bebas':
                        show = compile[[f'IndoBERT+QE_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Siklus Bisnis':
                        show = compile[[f'IndoBERT+QE_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'IndoBERT+QE_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'IndoBERT+QE_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement K-Means':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Analisis','Model Pembelajaran','Bilangan Reproduksi Dasar'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Analisis':
                        show = compile[[f'K-Means_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Model Pembelajaran':
                        show = compile[[f'K-Means_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Bilangan Reproduksi Dasar':
                        show = compile[[f'K-Means_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'K-Means_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'K-Means_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
                elif pilih_met == 'IndoBERT + QE Refinement UMAP + HDBSCAN':
                    pilih_qe = row_4.selectbox('Pilih Kueri Ekspansi',
                    ('Laju','Titik Kesetimbangan','Laju Kesembuhan Parameter'),key='pil_qe')
                    ############################################################
                    if pilih_qe == 'Laju':
                        show = compile[[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Unigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Titik Kesetimbangan':
                        show = compile[[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Bigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    elif pilih_qe == 'Laju Kesembuhan Parameter':
                        show = compile[[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}','Judul Artikel','Abstrak Artikel']]
                        show = show.sort_values(by=[f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}'],ascending=False,ignore_index=True)
                        show_rename = {f'UMAP+HDBSCAN_Trigram_3_{pilih_kueri}':'Nilai Relevansi'}
                        show.rename(columns=show_rename,inplace=True)
                        show = show[show['Nilai Relevansi'] > 0]
                        show.reset_index(drop=True)
                        st.write(f'Ditemukan {len(show)} artikel relevan untuk kueri "{pilih_kueri} {pilih_qe}"')
                        st.dataframe(show)
                    ############################################################
################################################################################
