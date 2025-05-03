import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Análisis Básico de Ventas")

# Cargar el dataset
@st.cache_data
def load_data():
    return pd.read_csv("static\datasets\sales_data.csv", parse_dates=["Date"])

df = load_data()

# Mostrar dataset completo
st.subheader("Datos Completos")
st.dataframe(df)

# Filtros en la barra lateral
st.sidebar.header("Filtros")

# Selectbox para categoría
categorias = df["Category"].unique()
category = st.sidebar.selectbox("Selecciona una categoría", categorias)

# Rango de precios
min_price = float(df["Price"].min())
max_price = float(df["Price"].max())
price_range = st.sidebar.slider("Selecciona rango de precios (USD)", 
                                min_value=min_price, 
                                max_value=max_price, 
                                value=(min_price, max_price))

# Aplicar filtros
filtered_df = df[
    (df["Category"] == category) &
    (df["Price"] >= price_range[0]) &
    (df["Price"] <= price_range[1])
]

# Mostrar datos filtrados
st.subheader("Datos Filtrados")
st.write(f"Registros encontrados: {len(filtered_df)}")
st.dataframe(filtered_df)

# Estadísticas
st.subheader("Estadísticas")
if not filtered_df.empty:
    total_sales = filtered_df["Total_Sales"].sum()
    avg_price = filtered_df["Price"].mean()

    st.metric(label="Total de Ventas (USD)", value=f"${total_sales:,.2f}")
    st.metric(label="Precio Promedio (USD)", value=f"${avg_price:,.2f}")
else:
    st.write("No hay datos para los filtros seleccionados.")
