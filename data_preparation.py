# Csomagok importálása
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from datetime import datetime
from statsmodels.nonparametric.smoothers_lowess import lowess
from sklearn.linear_model import LinearRegression

# Adatbázis importálása és előkészítése
MASTER = pd.read_csv('EUROPE_COVID19_master.csv', sep=';')

MASTER.date = pd.to_datetime(MASTER['date'], format='%d-%b-%y')
MASTER.date = MASTER.date.dt.date

MASTER.country.unique()
MASTER.nuts0_id.unique()

# Ukrajna, Szerbia hiányzik !!!
Hungary = MASTER[MASTER.nuts0_id == "HU"]  # 20 db - NUTS3 (20)
Austria = MASTER[MASTER.nuts0_id == "AT"]  # 35 db - NUTS3 (35)
Slovakia = MASTER[MASTER.nuts0_id == "SK"]  # 8 db - NUTS3 (8)
# Romania = MASTER[MASTER.nuts0_id == "RO"] 42 db - NUTS3 (42) KÉSŐI ADATGYŰJTÉS
Croatia = MASTER[MASTER.nuts0_id == "HR"]  # 21 db - NUTS3 (21)
Slovenia = MASTER[MASTER.nuts0_id == "SI"]  # 12 db - NUTS3 (12)
Switzerland = MASTER[MASTER.nuts0_id == "CH"]  # 26 db - NUTS3 (26)
Italy = MASTER[MASTER.nuts0_id == "IT"]  # 106 db - NUTS3 (107) - 1 hiányzik!!!
Germany = MASTER[MASTER.nuts0_id == "DE"] # 401 db - NUTS3 (400) - 1-gyel több!!!
Poland = MASTER[MASTER.nuts0_id == "PL"]  # 17 db - NUTS2 (17 db) !!!

COUNTRIES = [Hungary, Austria, Slovakia, Croatia,
             Slovenia, Switzerland, Italy, Germany, Poland]

for countries in COUNTRIES:
    print(countries.country.unique(),

          countries.groupby('nuts_id').agg(
        count=('date', 'count'),
        start_date=('date', 'min'),
        end_date=('date', 'max')
    ).reset_index())

# Románoktól megválni
# Március 31 előtti dátumokat konzisztensen beírni Budapest/Győr 
# Korabeli sajtó, 30+ embert szétszálazni már nem érdemes, 10-15 embernek utánamenni
# Átlátszó koronamonitor adatforrás! Hátha megvan korábbra

# Hiányzó adatok:
for countries in COUNTRIES:
    print(countries.country.unique(), len(countries.cases_daily),
          countries.cases_daily.isna().sum())
    
    


# Hiányzó adatok pótlása:
new_countries_list = []

for countries in COUNTRIES:
    countries = countries.reset_index(drop=True)
    for i in range(len(countries)):
        if pd.isna(countries.loc[i, 'cases_daily']):
            if i == 0:
                # Ha az első index, akkor egyenlő az első szummával
                countries.loc[i, 'cases_daily'] = countries.loc[i, 'cases']
            elif countries.loc[i, 'nuts_id'] == countries.loc[i-1, 'nuts_id']:
                # Ha az előző nuts régió megegyezik a hiányzó értékével, akkor kiszámolom a különbségből
                countries.loc[i, 'cases_daily'] = countries.loc[i,'cases'] - countries.loc[i-1, 'cases']
            elif countries.loc[i, 'nuts_id'] != countries.loc[i-1, 'nuts_id']:
                # Ha régiót váltunk, akkor megint az első szummával egyenlő
                countries.loc[i, 'cases_daily'] = countries.loc[i, 'cases']
                
    for i in range(len(countries)):
        if pd.isna(countries.loc[i, 'cases_daily_pop']):
            countries.loc[i, 'cases_daily_pop'] = countries.loc[i, 'cases_daily']/countries.loc[i, 'population']*10000
            
    new_countries_list.append(countries)
    

COUNTRIES = new_countries_list

for countries in COUNTRIES:
    print(countries.country.unique(), len(countries.cases_daily),
          countries.cases_daily.isna().sum(), countries.cases_daily_pop.isna().sum())


# LOESS backcasting az első 3 hónapra, abból visszavetíteni az első magyar adatregisztrálás napjáig 
# az esetszámokat mindegyik régióra, utána skálázni 0-1 közé, hogy a végső összeg (márc 31) 
# legyen 215 Hungary esetben a szumma a végén
# többi régióban is
# időpont meghatározása viszont országonként

# FIRST OFFICIAL RECORDED CASES
# SOURCE: https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Europe
# https://en.wikipedia.org/wiki/COVID-19_pandemic_by_country_and_territory#Timeline_of_first_confirmed_cases_by_country_or_territory

# Hungary: 03-04 (03-31) MEGCSINÁLVA
# Austria: 02-26 (02-26) EZ JÓ
# Slovakia: 03-06 (03-06) EZ JÓ
# Croatia: 02-25 (03-21) MEGCSINÁLVA
# Slovenia: 03-04 (03-04) EZ JÓ
# Switzerland: 02-25 (03-06) NEM KELL
# Italy: 01-31 (02-24) NEM KELL
# Germany: 01-27 (03-02) NEM KELL
# Poland: 03-04 (03-18) MEGCSINÁLVA

# INTERVALLUM: 2020-03-06 - 2022-01-07!

HUNGARY = [COUNTRIES[0][COUNTRIES[0]["nuts_id"] == nuts].copy() for nuts in COUNTRIES[0]["nuts_id"].unique()]
AUSTRIA = [COUNTRIES[1][COUNTRIES[1]["nuts_id"] == nuts].copy() for nuts in COUNTRIES[1]["nuts_id"].unique()]
SLOVAKIA = [COUNTRIES[2][COUNTRIES[2]["nuts_id"] == nuts].copy() for nuts in COUNTRIES[2]["nuts_id"].unique()]
CROATIA = [COUNTRIES[3][COUNTRIES[3]["nuts_id"] == nuts].copy() for nuts in COUNTRIES[3]["nuts_id"].unique()]
SLOVENIA = [COUNTRIES[4][COUNTRIES[4]["nuts_id"] == nuts].copy() for nuts in COUNTRIES[4]["nuts_id"].unique()]
SWITZERLAND = [COUNTRIES[5][COUNTRIES[5]["nuts_id"] == nuts].copy() for nuts in COUNTRIES[5]["nuts_id"].unique()]
ITALY = [COUNTRIES[6][COUNTRIES[6]["nuts_id"] == nuts].copy() for nuts in COUNTRIES[6]["nuts_id"].unique()]
GERMANY = [COUNTRIES[7][COUNTRIES[7]["nuts_id"] == nuts].copy() for nuts in COUNTRIES[7]["nuts_id"].unique()]
POLAND = [COUNTRIES[8][COUNTRIES[8]["nuts_id"] == nuts].copy() for nuts in COUNTRIES[8]["nuts_id"].unique()]



# ELSŐ SOROK HOZZÁADÁSA

# HUNGARY

new_regions_list = []
counter = 0
for regions in HUNGARY:
    regions['date'] = pd.to_datetime(regions['date'])

    # Meghatározzuk a hiányzó dátumtartományt
    start_date = pd.to_datetime("2020-03-04")
    end_date = regions['date'].min() - pd.Timedelta(days=1)
    missing_dates = pd.date_range(start=start_date, end=end_date)

    # Az első sorból mintát veszünk (meta-adatokhoz)
    template_row = regions.iloc[0].copy()
    template_row[['cases', 'cases_daily', 'cases_pop', 'cases_daily_pop']] = np.nan

    # Létrehozzuk az új sorokat
    new_rows = []
    for date in missing_dates:
        new_row = template_row.copy()
        new_row['date'] = date
        new_rows.append(new_row)

    # DataFrame-é alakítjuk a sorokat
    new_df = pd.DataFrame(new_rows)

    # Összefűzzük az eredeti DataFrame-fel, és idő szerint sorba rendezzük
    HUNGARY[counter] = pd.concat([new_df, regions], ignore_index=True)
    HUNGARY[counter] = HUNGARY[counter].sort_values(by='date').reset_index(drop=True)
    print(HUNGARY[counter])
    new_regions_list.append(HUNGARY[counter])
    counter += 1

HUNGARY = new_regions_list
    

# CROATIA

new_regions_list = []
counter = 0
for regions in CROATIA:
    regions['date'] = pd.to_datetime(regions['date'])

    # Meghatározzuk a hiányzó dátumtartományt
    start_date = pd.to_datetime("2020-02-25")
    end_date = regions['date'].min() - pd.Timedelta(days=1)
    missing_dates = pd.date_range(start=start_date, end=end_date)

    # Az első sorból mintát veszünk (meta-adatokhoz)
    template_row = regions.iloc[0].copy()
    template_row[['cases', 'cases_daily', 'cases_pop', 'cases_daily_pop']] = np.nan

    # Létrehozzuk az új sorokat
    new_rows = []
    for date in missing_dates:
        new_row = template_row.copy()
        new_row['date'] = date
        new_rows.append(new_row)

    # DataFrame-é alakítjuk a sorokat
    new_df = pd.DataFrame(new_rows)

    # Összefűzzük az eredeti DataFrame-fel, és idő szerint sorba rendezzük
    CROATIA[counter] = pd.concat([new_df, regions], ignore_index=True)
    CROATIA[counter] = CROATIA[counter].sort_values(by='date').reset_index(drop=True)
    print(CROATIA[counter])
    new_regions_list.append(CROATIA[counter])
    counter += 1

CROATIA = new_regions_list


# POLAND

new_regions_list = []
counter = 0
for regions in POLAND:
    regions['date'] = pd.to_datetime(regions['date'])

    # Meghatározzuk a hiányzó dátumtartományt
    start_date = pd.to_datetime("2020-03-04")
    end_date = regions['date'].min() - pd.Timedelta(days=1)
    missing_dates = pd.date_range(start=start_date, end=end_date)

    # Az első sorból mintát veszünk (meta-adatokhoz)
    template_row = regions.iloc[0].copy()
    template_row[['cases', 'cases_daily', 'cases_pop', 'cases_daily_pop']] = np.nan

    # Létrehozzuk az új sorokat
    new_rows = []
    for date in missing_dates:
        new_row = template_row.copy()
        new_row['date'] = date
        new_rows.append(new_row)

    # DataFrame-é alakítjuk a sorokat
    new_df = pd.DataFrame(new_rows)

    # Összefűzzük az eredeti DataFrame-fel, és idő szerint sorba rendezzük
    POLAND[counter] = pd.concat([new_df, regions], ignore_index=True)
    POLAND[counter] = POLAND[counter].sort_values(by='date').reset_index(drop=True)
    print(POLAND[counter])
    new_regions_list.append(POLAND[counter])
    counter += 1

POLAND = new_regions_list




# LOESS

# HUNGARY

for i in range(0, len(HUNGARY)):

    HUNGARY[i]['date'] = pd.to_datetime(HUNGARY[i]['date'])
    
    # 2. Különválasztjuk a becsléshez használt adatokat (2020-04-01-től), és nem hiányzókat
    training_data = HUNGARY[i][(HUNGARY[i]['date'] > pd.Timestamp("2020-03-31")) & HUNGARY[i]['cases_daily'].notna()].copy()
    training_data['day_number'] = (training_data['date'] - training_data['date'].min()).dt.days
    
    # 3. LOESS illesztés
    loess_result = lowess(
        endog=training_data['cases_daily'],
        exog=training_data['day_number'],
        frac=0.1,
        return_sorted=False
    )
    
    # PLOT A DOLGOZATBA
    
    # 4. Lineáris modell LOESS eredményen (backcasting)
    model = LinearRegression()
    model.fit(training_data[['day_number']].iloc[:90], loess_result[:90])
    
    # 5. Kiválasztjuk a becsülendő napokat (2020-03-31 és előtte)
    missing_days = HUNGARY[i][HUNGARY[i]['date'] <= pd.Timestamp("2020-03-31")].copy()
    missing_days['day_number'] = (missing_days['date'] - training_data['date'].min()).dt.days
    
    # 6. Becsült értékek
    estimated_cases = model.predict(missing_days[['day_number']])
    
    # 7. Kitöltés a becsült értékekkel
    HUNGARY[i].loc[HUNGARY[i]['date'] <= pd.Timestamp("2020-03-31"), 'cases_daily'] = estimated_cases
    
    # 8. Dátum szerinti rendezés
    HUNGARY[i] = HUNGARY[i].sort_values(by='date').reset_index(drop=True)
    
    sum_case = HUNGARY[i].loc[HUNGARY[i]['date'] == pd.Timestamp('2020-03-31'), 'cases'].values[0]
    
    sum_predicted = HUNGARY[i]['cases_daily'].iloc[:28].sum()
    
    HUNGARY[i].loc[:27, 'cases_daily'] = HUNGARY[i].loc[:27, 'cases_daily'] / sum_predicted * sum_case


# CROATIA

for i in range(0, len(CROATIA)):

    CROATIA[i]['date'] = pd.to_datetime(CROATIA[i]['date'])
    
    # 2. Különválasztjuk a becsléshez használt adatokat (2020-04-01-től), és nem hiányzókat
    training_data = CROATIA[i][(CROATIA[i]['date'] > pd.Timestamp("2020-03-21")) & CROATIA[i]['cases_daily'].notna()].copy()
    training_data['day_number'] = (training_data['date'] - training_data['date'].min()).dt.days
    
    # 3. LOESS illesztés
    loess_result = lowess(
        endog=training_data['cases_daily'],
        exog=training_data['day_number'],
        frac=0.1,
        return_sorted=False
    )
    
    # 4. Lineáris modell LOESS eredményen (backcasting)
    model = LinearRegression()
    model.fit(training_data[['day_number']].iloc[:90], loess_result[:90])
    
    # 5. Kiválasztjuk a becsülendő napokat (2020-03-31 és előtte)
    missing_days = CROATIA[i][CROATIA[i]['date'] <= pd.Timestamp("2020-03-21")].copy()
    missing_days['day_number'] = (missing_days['date'] - training_data['date'].min()).dt.days
    
    # 6. Becsült értékek
    estimated_cases = model.predict(missing_days[['day_number']])
    
    # 7. Kitöltés a becsült értékekkel
    CROATIA[i].loc[CROATIA[i]['date'] <= pd.Timestamp("2020-03-21"), 'cases_daily'] = estimated_cases
    
    # 8. Dátum szerinti rendezés
    CROATIA[i] = CROATIA[i].sort_values(by='date').reset_index(drop=True)
    
    sum_case = CROATIA[i].loc[CROATIA[i]['date'] == pd.Timestamp('2020-03-21'), 'cases'].values[0]
    
    sum_predicted = CROATIA[i]['cases_daily'].iloc[:26].sum()
    
    CROATIA[i].loc[:25, 'cases_daily'] = CROATIA[i].loc[:25, 'cases_daily'] / sum_predicted * sum_case


# POLAND

for i in range(0, len(POLAND)):

    POLAND[i]['date'] = pd.to_datetime(POLAND[i]['date'])
    
    # 2. Különválasztjuk a becsléshez használt adatokat (2020-04-01-től), és nem hiányzókat
    training_data = POLAND[i][(POLAND[i]['date'] > pd.Timestamp("2020-03-18")) & POLAND[i]['cases_daily'].notna()].copy()
    training_data['day_number'] = (training_data['date'] - training_data['date'].min()).dt.days
    
    # 3. LOESS illesztés
    loess_result = lowess(
        endog=training_data['cases_daily'],
        exog=training_data['day_number'],
        frac=0.1,
        return_sorted=False
    )
    
    # 4. Lineáris modell LOESS eredményen (backcasting)
    model = LinearRegression()
    model.fit(training_data[['day_number']].iloc[:90], loess_result[:90])
    
    # 5. Kiválasztjuk a becsülendő napokat (2020-03-31 és előtte)
    missing_days = POLAND[i][POLAND[i]['date'] <= pd.Timestamp("2020-03-18")].copy()
    missing_days['day_number'] = (missing_days['date'] - training_data['date'].min()).dt.days
    
    # 6. Becsült értékek
    estimated_cases = model.predict(missing_days[['day_number']])
    
    # 7. Kitöltés a becsült értékekkel
    POLAND[i].loc[POLAND[i]['date'] <= pd.Timestamp("2020-03-18"), 'cases_daily'] = estimated_cases
    
    # 8. Dátum szerinti rendezés
    POLAND[i] = POLAND[i].sort_values(by='date').reset_index(drop=True)
    
    sum_case = POLAND[i].loc[POLAND[i]['date'] == pd.Timestamp('2020-03-18'), 'cases'].values[0]
    
    sum_predicted = POLAND[i]['cases_daily'].iloc[:15].sum()
    
    POLAND[i].loc[:24, 'cases_daily'] = POLAND[i].loc[:24, 'cases_daily'] / sum_predicted * sum_case


ALL = HUNGARY + AUSTRIA + SLOVAKIA + CROATIA + SLOVENIA + SWITZERLAND + ITALY + GERMANY + POLAND


# Közös intervallumra vágás

new_countries_list = []

for countries in ALL:
    countries['date'] = pd.to_datetime(countries['date'])

    countries = countries[
        (countries['date'] >= pd.Timestamp('2020-03-06')) &
        (countries['date'] <= pd.Timestamp('2022-01-07'))
    ]

    new_countries_list.append(countries)

ALL = new_countries_list



# Idősorok előállítása

# Dátumtartomány létrehozása
date_range = pd.date_range(start='2020-03-06', end='2022-01-07', freq='D')

# Üres lista a DataFrame-ek összegyűjtéséhez
all_data = []

for df in ALL:
    df['date'] = pd.to_datetime(df['date'])  # biztosítjuk a dátum típusát
    all_data.append(df[['date', 'nuts_id', 'cases_daily']])

# Összefűzzük egy nagy DataFrame-be
combined = pd.concat(all_data, ignore_index=True)

# Pivot tábla: sor = dátum, oszlop = nuts_id, érték = cases_daily
DATA = combined.pivot_table(index='date', columns='nuts_id', values='cases_daily', aggfunc='sum')

# Minden dátumot tartalmazó teljes index beállítása
DATA = DATA.reindex(date_range)


DATA.isna().sum().sum()

for column in DATA.columns:
    n = len(DATA)
    i = 0
    while i < n:
        value = DATA.iloc[i][column]
        
        if pd.isna(value):
            counter = 1
            while i + counter < n and pd.isna(DATA.iloc[i + counter][column]):
                counter += 1
            
            # Ellenőrizzük, hogy nem léptük túl az indexet
            if i + counter < n:
                the_data = DATA.iloc[i + counter][column]
            else:
                # Ha nincs több nem NaN érték utána, pl. használj valamit:
                # Például nullával osztunk, vagy az utolsó nem NaN értéket, vagy skip
                # Itt most kihagyjuk az interpolációt:
                i += counter
                continue
            
            divide = the_data / (counter + 1)
            
            for j in range(i, i + counter + 1):
                DATA.iloc[j, DATA.columns.get_loc(column)] = divide
            
            i += counter + 1  # lépjünk túl a NaN blokkon
        else:
            i += 1


# SVÁJCCAL 2 PROBLÉMA:

# CH011: 2022-01-09 = 23808 
# ezt le kell osztani 7 nappal

manualis = 23808/7
      
DATA.loc['2022-01-03', 'CH011'] = manualis
DATA.loc['2022-01-04', 'CH011'] = manualis
DATA.loc['2022-01-05', 'CH011'] = manualis
DATA.loc['2022-01-06', 'CH011'] = manualis
DATA.loc['2022-01-07', 'CH011'] = manualis

# CH053 nagyon sok hiányos: 2021-01-22-ig van adat
# Kidobom

DATA = DATA.drop(columns=['CH053'])


# 0 üres adat
DATA.isna().sum().sum()


# Index visszanevezése, ha kell
DATA.index.name = 'date'



# OSZLOPDIAGRAMOK ELLENŐRZÉSRE NUTS3

DATA.index = pd.to_datetime(DATA.index, format='%Y.%m.%d')

# A DataFrame oszlopait 20-as csoportokra bontjuk
columns = DATA.columns
group_size = 10 #30
num_groups = (len(columns) + group_size - 1) // group_size

# Csoportonként vonaldiagram rajzolása
for i in range(num_groups):
    group_cols = columns[i * group_size : (i + 1) * group_size]
    df_group = DATA[group_cols]
    
    plt.figure(figsize=(12, 6))
    for col in group_cols:
        plt.plot(DATA.index, df_group[col], label=col)
    
    #plt.title(f'Vonaldiagram – Oszlopok {i * group_size + 1} - {i * group_size + len(group_cols)}')
    plt.xlabel('Dátum')
    plt.ylabel('Érték')
    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize='small')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    


# POZITÍV ÉS NEGATÍV OUTLIEREK KEZELÉSE (3-3 SZOMSZÉDDAL)

# Módosított negatív értékek száma:
negatives = (DATA < 0).sum().sum()
# 1345 ÉRTÉK
1345/(673*645)


# Módosított outlierek száma:
counter = 0    

for col in DATA.columns:
    if not np.issubdtype(DATA[col].dtype, np.number):
        continue

    Q3 = DATA[col].quantile(0.75)
    Q1 = DATA[col].quantile(0.25)
    IQR = Q3 - Q1
    threshold = Q3 + 3 * IQR

    for i in range(len(DATA[col])):
        val = DATA[col].iloc[i]

        # Feltétel: ha túl nagy vagy negatív
        if val > threshold or val < 0:
            neighbors = []

            # Nézzük meg az előző 3 értéket
            for j in range(i - 3, i):
                if 0 <= j < len(DATA[col]):
                    neighbor_val = DATA[col].iloc[j]
                    if pd.notna(neighbor_val) and neighbor_val >= 0:
                        neighbors.append(neighbor_val)

            # Nézzük meg a következő 3 értéket
            for j in range(i + 1, i + 4):
                if j < len(DATA[col]):
                    neighbor_val = DATA[col].iloc[j]
                    if pd.notna(neighbor_val) and neighbor_val >= 0:
                        neighbors.append(neighbor_val)

            # Ha van legalább egy érvényes szomszéd, számoljuk az átlagukat
            if neighbors:
                avg_val = sum(neighbors) / len(neighbors)
                DATA.at[DATA.index[i], col] = avg_val
                counter = counter + 1

# ÍGY MÁR 0 VAN
(DATA < 0).sum().sum()

# FELFELE OUTLIEREK:
counter - negatives
# 12953

# 12953/(673*645)
# 2,98%


# OSZLOPDIAGRAMOK ELLENŐRZÉSRE NUTS3 OUTLIEREK KEZELÉSE UTÁN

DATA.index = pd.to_datetime(DATA.index, format='%Y.%m.%d')

# A DataFrame oszlopait 20-as csoportokra bontjuk
columns = DATA.columns
group_size = 30
num_groups = (len(columns) + group_size - 1) // group_size

# Csoportonként vonaldiagram rajzolása
for i in range(num_groups):
    group_cols = columns[i * group_size : (i + 1) * group_size]
    df_group = DATA[group_cols]
    
    plt.figure(figsize=(12, 6))
    for col in group_cols:
        plt.plot(DATA.index, df_group[col], label=col)
    
    plt.title(f'Vonaldiagram – Oszlopok {i * group_size + 1} - {i * group_size + len(group_cols)}')
    plt.xlabel('Dátum')
    plt.ylabel('Érték')
    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize='small')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# HUNGARY ÖSSZEVONÁSA

# 1. 'HU' kezdetű oszlopok kiválasztása
hu_cols = [col for col in DATA.columns if col.startswith('HU')]

# 2. Csoportosítás a 'HU' utáni két karakter szerint
group_map = {}
for col in hu_cols:
    if len(col) > 4:
        key = col[2:4]  # HU123 → '12'
        group_map.setdefault(key, []).append(col)

# 3. Új oszlopokat tartalmazó DataFrame
grouped_cols = pd.DataFrame(index=DATA.index)

for key, cols in group_map.items():
    new_col_name = f'HU{key}'
    grouped_cols[new_col_name] = DATA[cols].sum(axis=1)

# 4. Eredeti HU oszlopok törlése
DATA = DATA.drop(columns=hu_cols)

# 5. Új összevont oszlopok hozzáadása
DATA = pd.concat([DATA, grouped_cols], axis=1)

# Kész
print(DATA.head())



# AUSTRIA ÖSSZEVONÁSA

at_cols = [col for col in DATA.columns if col.startswith('AT')]

group_map = {}
for col in at_cols:
    if len(col) > 4:
        key = col[2:4]
        group_map.setdefault(key, []).append(col)

grouped_cols = pd.DataFrame(index=DATA.index)

for key, cols in group_map.items():
    new_col_name = f'AT{key}'
    grouped_cols[new_col_name] = DATA[cols].sum(axis=1)

DATA = DATA.drop(columns=at_cols)

DATA = pd.concat([DATA, grouped_cols], axis=1)



# SLOVAKIA ÖSSZEVONÁSA

sk_cols = [col for col in DATA.columns if col.startswith('SK')]

group_map = {}
for col in sk_cols:
    if len(col) > 4:
        key = col[2:4]
        group_map.setdefault(key, []).append(col)

grouped_cols = pd.DataFrame(index=DATA.index)

for key, cols in group_map.items():
    new_col_name = f'SK{key}'
    grouped_cols[new_col_name] = DATA[cols].sum(axis=1)

DATA = DATA.drop(columns=sk_cols)

DATA = pd.concat([DATA, grouped_cols], axis=1)



# CROATIA ÖSSZEVONÁSA! (2 db)

hr_cols = [col for col in DATA.columns if col.startswith('HR')]

group_map = {}
for col in hr_cols:
    if len(col) > 4:
        key = col[2:4]
        group_map.setdefault(key, []).append(col)

grouped_cols = pd.DataFrame(index=DATA.index)

for key, cols in group_map.items():
    new_col_name = f'HR{key}'
    grouped_cols[new_col_name] = DATA[cols].sum(axis=1)

DATA = DATA.drop(columns=hr_cols)

DATA = pd.concat([DATA, grouped_cols], axis=1)



# SLOVENIA ÖSSZEVONÁSA 

si_cols = [col for col in DATA.columns if col.startswith('SI')]

group_map = {}
for col in si_cols:
    if len(col) > 4:
        key = col[2:4]
        group_map.setdefault(key, []).append(col)

grouped_cols = pd.DataFrame(index=DATA.index)

for key, cols in group_map.items():
    new_col_name = f'SI{key}'
    grouped_cols[new_col_name] = DATA[cols].sum(axis=1)

DATA = DATA.drop(columns=si_cols)

DATA = pd.concat([DATA, grouped_cols], axis=1)



# SWITZERLAND ÖSSZEVONÁSA

ch_cols = [col for col in DATA.columns if col.startswith('CH')]

group_map = {}
for col in ch_cols:
    if len(col) > 4:
        key = col[2:4]
        group_map.setdefault(key, []).append(col)

grouped_cols = pd.DataFrame(index=DATA.index)

for key, cols in group_map.items():
    new_col_name = f'CH{key}'
    grouped_cols[new_col_name] = DATA[cols].sum(axis=1)

DATA = DATA.drop(columns=ch_cols)

DATA = pd.concat([DATA, grouped_cols], axis=1)



# ITALY ÖSSZEVONÁSA

it_cols = [col for col in DATA.columns if col.startswith('IT')]

group_map = {}
for col in it_cols:
    if len(col) > 4:
        key = col[2:4]
        group_map.setdefault(key, []).append(col)

grouped_cols = pd.DataFrame(index=DATA.index)

for key, cols in group_map.items():
    new_col_name = f'IT{key}'
    grouped_cols[new_col_name] = DATA[cols].sum(axis=1)

DATA = DATA.drop(columns=it_cols)

DATA = pd.concat([DATA, grouped_cols], axis=1)



# GERMANY ÖSSZEVONÁSA

de_cols = [col for col in DATA.columns if col.startswith('DE')]

group_map = {}
for col in de_cols:
    if len(col) > 4:
        key = col[2:4]
        group_map.setdefault(key, []).append(col)

grouped_cols = pd.DataFrame(index=DATA.index)

for key, cols in group_map.items():
    new_col_name = f'DE{key}'
    grouped_cols[new_col_name] = DATA[cols].sum(axis=1)

DATA = DATA.drop(columns=de_cols)

DATA = pd.concat([DATA, grouped_cols], axis=1)



# DARABSZÁMOK NUTS2:

# HU: 8
# AT: 9
# SK: 4
# HR: 2
# SI: 2
# CH: 7
# IT: 21
# DE: 38
# PL: 17


# MENNYI 0 ÉRTÉK?

(DATA == 0).sum().sum()

2745 / (673*108)
# 3,8% 0 érték


# OSZLOPDIAGRAMOK ELLENŐRZÉSRE NUTS2
# MÁR JOBBAN NÉZ KI!

DATA.index = pd.to_datetime(DATA.index, format='%Y.%m.%d')

# A DataFrame oszlopait 20-as csoportokra bontjuk
columns = DATA.columns
group_size = 10
num_groups = (len(columns) + group_size - 1) // group_size

# Csoportonként vonaldiagram rajzolása
for i in range(num_groups):
    group_cols = columns[i * group_size : (i + 1) * group_size]
    df_group = DATA[group_cols]
    
    plt.figure(figsize=(12, 6))
    for col in group_cols:
        plt.plot(DATA.index, df_group[col], label=col)
    
    plt.title(f'Vonaldiagram – Oszlopok {i * group_size + 1} - {i * group_size + len(group_cols)}')
    plt.xlabel('Dátum')
    plt.ylabel('Érték')
    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize='small')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    
# CSAK HU
    
# Csak a 8–25. oszlopokat rajzoljuk ki (Python indexelés szerint: 7–24)
plt.figure(figsize=(12, 6))

# 18–25. oszlopok kirajzolása
for col in columns[17:25]:
    plt.plot(DATA.index, DATA[col], label=col)

plt.title('Vonaldiagram – 18–25. oszlopok')
plt.xlabel('Dátum')
plt.ylabel('Érték')
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize='small')
plt.grid(True)
plt.tight_layout()
plt.show()


# HUNGARY oszlopok kirajzolása 2020-09-13-tól

# Feltételezzük, hogy DATA.index datetime típusú
start_date = pd.to_datetime("2020-09-13")
DATA_subset = DATA.loc[DATA.index >= start_date, columns[17:25]]

# Vonaldiagram kirajzolása
plt.figure(figsize=(12, 6))
for col in DATA_subset.columns:
    plt.plot(DATA_subset.index, DATA_subset[col], label=col)

plt.title('')
plt.xlabel('Dátum')
plt.ylabel('Érték')
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize='small')
plt.grid(True)
plt.tight_layout()
plt.show()

# POLAND oszlopok kirajzolása 2020-09-13-tól

# Feltételezzük, hogy DATA.index datetime típusú
start_date = pd.to_datetime("2020-09-13")
DATA_subset = DATA.loc[DATA.index >= start_date, columns[0:17]]

# Vonaldiagram kirajzolása
plt.figure(figsize=(12, 6))
for col in DATA_subset.columns:
    plt.plot(DATA_subset.index, DATA_subset[col], label=col)

plt.title('')
plt.xlabel('Dátum')
plt.ylabel('Érték')
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize='small')
plt.grid(True)
plt.tight_layout()
plt.show()


# HUNGARY + NEIGHBORS oszlopok kirajzolása 2020-09-13-tól

start_date = pd.to_datetime("2020-09-13")
DATA_subset = DATA.loc[DATA.index >= start_date, list(DATA.columns[17:28]) + [DATA.columns[29]] + list(DATA.columns[35:38])]

# Vonaldiagram kirajzolása
plt.figure(figsize=(12, 6))
for col in DATA_subset.columns:
    plt.plot(DATA_subset.index, DATA_subset[col], label=col)

plt.title('')
plt.xlabel('Dátum')
plt.ylabel('Érték')
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize='small')
plt.grid(True)
plt.tight_layout()
plt.show()


# TELJES

start_date = pd.to_datetime("2020-07-25")
DATA_subset = DATA.loc[DATA.index >= start_date, columns[0:108]]

# Vonaldiagram kirajzolása
plt.figure(figsize=(12, 6))
for col in DATA_subset.columns:
    plt.plot(DATA_subset.index, DATA_subset[col], label=col)

plt.title('')
plt.xlabel('Dátum')
plt.ylabel('Érték')
#plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize='small')
plt.grid(True)
plt.tight_layout()
plt.show()




# DATAFRAME-BE MENTÉS
# DATA.to_csv("DATA.csv")
DATA.to_csv("DATA_proba.csv")

# NOV 20 OLYAN ÁLLAPOT, AMIT MÁR CSAK ELOLVASNI KELL
# LEADÁSI HATÁRIDŐ DEC ELSŐ HETE!






