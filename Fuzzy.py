import pandas as pd

# 1. Baca data
df = pd.read_excel("restoran.xlsx")

# 2. Fungsi Keanggotaan Pelayanan
def pelayanan_buruk(x):
    if x <= 30:
        return 1
    elif 30 < x <= 50:
        return (50 - x) / 20
    else:
        return 0

def pelayanan_cukup(x):
    if 40 < x <= 60:
        return (x - 40) / 20
    elif 60 < x <= 80:
        return (80 - x) / 20
    else:
        return 0

def pelayanan_baik(x):
    if x >= 85:
        return 1
    elif 70 < x < 85:
        return (x - 70) / 15
    else:
        return 0

# 3. Fungsi Keanggotaan Harga
def harga_murah(x):
    if x <= 35000:
        return 1
    elif 35000 < x <= 45000:
        return (45000 - x) / 10000
    else:
        return 0

def harga_sedang(x):
    if 35000 < x <= 45000:
        return (x - 35000) / 10000
    elif 45000 < x <= 55000:
        return (55000 - x) / 10000
    else:
        return 0

def harga_mahal(x):
    if x >= 55000:
        return 1
    elif 45000 < x < 55000:
        return (x - 45000) / 10000
    else:
        return 0

# 4. Fungsi Inferensi Fuzzy
def inferensi(pelayanan, harga):
    rules = []
    rules.append(min(pelayanan_buruk(pelayanan), harga_murah(harga)) * 20)
    rules.append(min(pelayanan_buruk(pelayanan), harga_sedang(harga)) * 20)
    rules.append(min(pelayanan_buruk(pelayanan), harga_mahal(harga)) * 10)
    rules.append(min(pelayanan_cukup(pelayanan), harga_murah(harga)) * 50)
    rules.append(min(pelayanan_cukup(pelayanan), harga_sedang(harga)) * 60)
    rules.append(min(pelayanan_cukup(pelayanan), harga_mahal(harga)) * 30)
    rules.append(min(pelayanan_baik(pelayanan), harga_murah(harga)) * 90)
    rules.append(min(pelayanan_baik(pelayanan), harga_sedang(harga)) * 80)
    rules.append(min(pelayanan_baik(pelayanan), harga_mahal(harga)) * 60)
    rules.append(pelayanan_buruk(pelayanan) * 10)
    return rules

# 5. Defuzzifikasi
def defuzzifikasi(nilai_fuzzy):
    bobots = [20, 20, 10, 50, 60, 30, 90, 80, 60, 10]
    numer = 0
    denom = 0
    for i in range(len(nilai_fuzzy)):
        if nilai_fuzzy[i] > 0:
            numer += nilai_fuzzy[i] * bobots[i]
            denom += nilai_fuzzy[i]
    if denom == 0:
        return 0
    return numer / denom

# 6. Proses semua data
results = []
for _, row in df.iterrows():
    pel = row['Pelayanan']
    hrg = row['harga']
    skor = defuzzifikasi(inferensi(pel, hrg))
    results.append({
        'ID': row['id Pelanggan'],
        'Pelayanan': pel,
        'Harga': hrg,
        'Skor Kelayakan': skor
    })

# 7. Simpan 5 terbaik ke file Excel
peringkat_df = pd.DataFrame(results)
top5_df = peringkat_df.sort_values(by=['Skor Kelayakan',  'Pelayanan', 'Harga'], ascending=[False, False, True]).head(5)
print("Top 5: \n", top5_df.to_string(index=False))
top5_df.to_excel("peringkat.xlsx", index=False)