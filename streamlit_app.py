import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide')

# ---- READ DATA ---
customer_pkl = pd.read_pickle('data/customer_merge.pkl')
coord = pd.read_csv('data/coordinate.csv')

# --- ROW 1 ---
st.write('# Customer Demography Dashboard')
st.write('### Welcome to the Customer Demography Dashboard!')
st.write("""I am Toni Andreas Susanto proudly presenting the Customer Demography Dashboard,
          a tool that allows you to understand thoroughly
          who our customers are. With interactive and detailed data visualization,
          This dashboard offers in-depth insight into our customer demographics.""")

# ----------------------------------------- ROW 2 --------------------------------------------------------
st.divider()
st.write('## Profession')

## --- INPUT SELECT Bar 1A---
input_select1 = st.selectbox(
    label='Top',
    options=[3, 5, 10]
)

# ----------------------------------------- ROW 3 --------------------------------------------------------

col3, col4 = st.columns(2) # Membagi tampilan menjadai 2 kolom

## ----- BAR PLOT 1A -----
# Data
rata_rata_per_kategori = customer_pkl.groupby('Profession')['Annual_Income'].mean()
rata_rata_AI_Prof = pd.DataFrame(rata_rata_per_kategori)
rata_rata_AI_Prof = rata_rata_AI_Prof.reset_index()

# px.bar
plot_prof_1 = px.bar(data_frame=rata_rata_AI_Prof.sort_values(by='Annual_Income').head(input_select1), 
                      x='Annual_Income', 
                      y='Profession',
                      labels={'Annual_Income':'Annual Income'})
# Bukan st. tetapi col1. untuk dimasukan ke bagian yg sudah dibuat di bagian kanan
col3.write('### Average Annual Profession Income')
col3.plotly_chart(plot_prof_1, use_container_width=True)  # use_container_width u/ menyesuaikan dgn lebar columns


## ----- BAR PLOT 1B -----
rata_rata_SS_Prof = customer_pkl.groupby('Profession')['Spending_Score'].mean()
rata_rata_SS_Prof = pd.DataFrame(rata_rata_SS_Prof).reset_index()
rata_rata_SS_Prof = round(rata_rata_SS_Prof, 0)

# px.bar
plot_prof_2 = px.bar(data_frame=rata_rata_SS_Prof.sort_values(by='Spending_Score').head(input_select1), 
                      x='Spending_Score', 
                      y='Profession',
                      labels={'Spending_Score':'Spending Score'})

col4.write('### Average Spending Score Profession')
col4.plotly_chart(plot_prof_2, use_container_width=True)  # use_container_width u/ menyesuaikan dgn lebar columns

# ----------------------------------------- ROW 4 --------------------------------------------------------
st.divider()
st.write('## Province')
col5, col6 = st.columns(2)


# --------- PETA 1 ----------
# Data
total_AI_Prov_map = customer_pkl.groupby('province')['Annual_Income'].sum()
total_AI_Prov_map = pd.DataFrame(total_AI_Prov_map).reset_index()
df_map_AI = total_AI_Prov_map.merge(right=coord, on='province')

# scatter_mapbox
plot_map_AI = px.scatter_mapbox(data_frame=df_map_AI,
                      zoom=3,
                      lat='latitude',
                      lon='longitude',
                      mapbox_style='open-street-map',
                      size='Annual_Income',
                      hover_name='province',
                      hover_data={'latitude': False,
                                  'longitude': False,
                                  'Annual_Income': ":,.0f"}
                      )

col5.write('### Annual Income in Province of Indonesia')
col5.plotly_chart(plot_map_AI, use_container_width=True)

# --------- PETA 2 ----------
# Data
mean_SS_Prov_map = customer_pkl.groupby('province')['Spending_Score'].mean().round(0)
mean_SS_Prov_map = pd.DataFrame(mean_SS_Prov_map).reset_index()
df_map_SS = mean_SS_Prov_map.merge(right=coord, on='province')

# scatter_mapbox
plot_map_SS = px.scatter_mapbox(data_frame=df_map_SS,
                      zoom=3,
                      lat='latitude',
                      lon='longitude',
                      mapbox_style='open-street-map',
                      size='Spending_Score',
                      hover_name='province',
                      hover_data={'latitude': False,
                                  'longitude': False}
                      )

col6.write('### Spending Score in Province of Indonesia')
col6.plotly_chart(plot_map_SS, use_container_width=True)



# ----------------------------------------- ROW 5 --------------------------------------------------------

## --- INPUT SELECT Bar 2---
input_select2 = st.selectbox(
    label='Top',
    options=[3, 5, 10],
    key='unique_key_for_selectbox'
)

col7, col8 = st.columns(2)

# --------- BAR 3 -----------
# Data
total_AI_Prov = customer_pkl.groupby('province')['Annual_Income'].sum()
total_AI_Prov = pd.DataFrame(total_AI_Prov).reset_index()
total_AI_Prov = total_AI_Prov.sort_values(by='Annual_Income').head(input_select2)

# px.bar
plot_prov1 = px.bar(data_frame=total_AI_Prov, 
                      x='Annual_Income', 
                      y='province',
                      labels={'Annual_Income':'Annual Income',
                              'province': 'Province'},
                      color_continuous_scale='RdBu')

col7.write('### Total Annual Customer Income in Each Province')
col7.plotly_chart(plot_prov1, use_container_width=True)

# --------- BAR 4 -------------
# Data
mean_SS_Prov = customer_pkl.groupby('province')['Spending_Score'].mean()
mean_SS_Prov = pd.DataFrame(mean_SS_Prov).reset_index()
mean_SS_Prov = round(mean_SS_Prov.sort_values(by='Spending_Score').head(input_select2), 0)

# px.bar
plot_prov2 = px.bar(data_frame=mean_SS_Prov, 
                      x='Spending_Score', 
                      y='province',
                      labels={'Spending_Score':'Spending Score',
                              'province': 'Province'})

col8.write('### Average Spending Score Customer in Each Province')
col8.plotly_chart(plot_prov2, use_container_width=True)



# ----------------------------------------- ROW 6 --------------------------------------------------------
st.divider()
st.write('## Generation Distribution')
col9, col10 = st.columns(2)

# ------- PLOT PIE GEN ---------
# Data
df_generasi = customer_pkl.groupby('generation')['NIK'].count()
df_generasi = pd.DataFrame(df_generasi).reset_index()
df_generasi = df_generasi.sort_values(by='NIK',ascending=False).head(4)

# Plot
plot_pie = px.pie(data_frame=df_generasi, 
       values='NIK',
       names='generation',
       color='generation',
       color_discrete_map={'Gen. Y (Millenials)':'royalblue',
                           'Gen. X':'cyan',
                           'Boomers':'lightcyan',
                           'Gen. Z (Zoomers)':'lightcyan'},
       labels={'NIK': 'Jumlah Customer',
               'generation': 'Generation'})

col9.write('### Total Customers in Each Generation')
col9.plotly_chart(plot_pie, use_container_width=True)


# ------- PLOT BAR Generation + Gender ---------

# data: multivariate
gen_gender = pd.crosstab(index=customer_pkl['generation'],
                          columns=customer_pkl['gender'],
                          colnames=[None])
gen_gender_melt = gen_gender.melt(ignore_index=False, var_name='gender', value_name='Jumlah Customer')
gen_gender_melt = gen_gender_melt.reset_index()

# plot: multivariate
plot_gen = px.bar(gen_gender_melt.sort_values(by='Jumlah Customer'), 
                   x="Jumlah Customer", y="generation", 
                   color="gender", 
                   barmode='group',
                   labels = {'generation' : 'Generation',
                             'gender': 'Gender'}
                             )

col10.write('### Comparison of Customer Gender in Each Generation')
col10.plotly_chart(plot_gen, use_container_width=True)

# ----------------------------------------- ROW 7 --------------------------------------------------------

st.divider()
st.write('## Age')

## --- INPUT SLIDER ---
input_slider = st.slider(
    label='Select Age Range',
    min_value=customer_pkl['age'].min(),
    max_value=customer_pkl['age'].max(),
    value=[20,50]
)

min_slider = input_slider[0]
max_slider = input_slider[1]

# ----------------------------------------- ROW 8 --------------------------------------------------------

# ---------- Line Chart ----------
# Data Pake Input SLider
customer_age = customer_pkl[customer_pkl['age'].between(left=min_slider, right=max_slider)]
df_umur = customer_age.groupby('age')['NIK'].count()
df_umur = pd.DataFrame(df_umur).reset_index()
df_umur = df_umur.sort_values(by='age')

# Plot
line_chart = px.line(data_frame=df_umur,
        x='age',
        y='NIK',
        markers=True,
        labels={'NIK': 'Jumlah Customer',
                'age': 'Umur'})

st.write('### Total Customers in Each Age Range')
st.plotly_chart(line_chart, use_container_width=True)
