import streamlit as st
import json
import os
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from langchain.callbacks.tracers import LangChainTracer
from langchain.agents import create_sql_agent, AgentType
from database.db import get_sql_database
from langchain_groq import ChatGroq


st.set_page_config(
    page_title="GISpion",
    layout="wide" 
)

def main():
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

    st.title("GISpion👀")

    db = get_sql_database()
    llm = ChatGroq(
        api_key=os.getenv("API_KEY_GROQ"),
        model="qwen-2.5-coder-32b",
        temperature=0.0,
        max_tokens=512,
    )
    tracer = LangChainTracer(project_name="GISpion")

    agent = create_sql_agent(
        llm=llm,
        db=db,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  
        verbose=True,
        handle_parsing_errors=True
    )

    user_query = st.text_input("Ask me a question (e.g. 'Vis meg de 5 første radene i tabellen AnadromeLaksefisk_fixed'):")
    if st.button("Submit"):
        if user_query.strip():
            raw_result = agent.run(user_query, callbacks=[tracer])
            parsed = None
            try:
                parsed = json.loads(raw_result)
            except Exception:
                pass

            if parsed:
                if isinstance(parsed, list):
                    df = pd.DataFrame(parsed)
                    st.write("**Parsed as DataFrame (list)**:")
                    st.dataframe(df, use_container_width=True)
    
                elif isinstance(parsed, dict):
                    df = pd.json_normalize(parsed, max_level=1)
                    st.write("**Parsed as DataFrame (dict)**:")
                    st.dataframe(df, use_container_width=True)

                    if "geometry" in parsed:
                        gdf = gpd.GeoDataFrame.from_features(parsed["geometry"])
                        if not gdf.empty:
                            center_lat = gdf.geometry.centroid.y.mean()
                            center_lon = gdf.geometry.centroid.x.mean()
                            m = folium.Map(location=[center_lat, center_lon], zoom_start=8)
                            folium.GeoJson(gdf).add_to(m)
                            st_folium(m, width=900, height=600)
                else:
                    st.write("**Parsed object**:", parsed)
            else:
                st.write("**Raw Result:**")
                st.code(raw_result, language="plaintext")
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
