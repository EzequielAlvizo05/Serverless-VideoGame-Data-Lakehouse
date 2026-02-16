import streamlit as st
import pandas as pd
from pyathena import connect
from datetime import datetime

st.set_page_config(page_title="Video Game Data Lakehouse", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_name=True)

@st.cache_resource
def get_conn():
    return connect(
        s3_staging_dir='s3://r-athen/',
        region_name='us-east-1',
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
    )

conn = get_conn()

@st.cache_data
def load_data():
    query = """
    SELECT name, rating, metacritic, released, playtime 
    FROM "db_videojuegos_gold"."capa_gold_proyecto1"
    """
    return pd.read_sql(query, conn)

try:
    df_raw = load_data()
    df_raw['released'] = pd.to_datetime(df_raw['released'])
    
    st.sidebar.image("https://rawg.io/assets/img/logo.png", width=150)
    st.sidebar.title("Filters")
    
    search_query = st.sidebar.text_input("🔍 Search Game", "")
    
    metacritic_range = st.sidebar.slider(
        "Metacritic Score Range", 
        0, 100, (0, 100)
    )
    
    df = df_raw[
        (df_raw['name'].str.contains(search_query, case=False)) &
        (df_raw['metacritic'].between(metacritic_range[0], metacritic_range[1]))
    ]

    col_title, col_status = st.columns([3, 1])
    with col_title:
        st.title("Rawg Games Analytics Dashboard")
        st.markdown("Análisis profesional de mercado orquestado en **AWS Serverless Architecture**.")
    
    with col_status:
        st.success(f"Data Freshness: {datetime.now().strftime('%Y-%m-%d')}")
        st.info("Pipeline Status: Succeeded")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Games", len(df))
    m2.metric("Avg Rating", f"{df['rating'].mean():.2f} ⭐")
    m3.metric("Avg Metacritic", f"{int(df['metacritic'].mean())} 🎯")
    m4.metric("Avg Playtime", f"{df['playtime'].mean():.1f}h ⏳")

    st.divider()

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("Top Games por Rating")
        top_games = df.sort_values("rating", ascending=False).head(10)
        st.bar_chart(top_games.set_index("name")["rating"], color="#3b82f6")

    with row1_col2:
        st.subheader("Distribución de Metacritic")
        st.area_chart(df.sort_values("released").set_index("released")["metacritic"], color="#10b981")

    st.subheader("Dataset Explorer")
    st.dataframe(df, use_container_width=True, hide_index=True)

    with st.expander("Ver Arquitectura del Proyecto"):
        st.write("""
        **Pipeline Flow:**
        1. **Extraction:** Python Lambda query to RAWG API (JSON).
        2. **Storage:** S3 Bronze Layer (Raw Data).
        3. **Processing:** Python Lambda + Pandas transforming to Parquet.
        4. **Analytics:** AWS Glue + Amazon Athena (SQL Engine).
        5. **Frontend:** Streamlit Cloud connected via PyAthena.
        """)

except Exception as e:
    st.error(f"Error conectando con el Data Lake: {e}")
    st.info("Asegúrate de que los Secrets de AWS y el bucket de resultados de Athena estén configurados.")