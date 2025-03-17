import os
import streamlit as st
from dotenv import load_dotenv
from database.db import get_sql_database
from langchain_groq import ChatGroq

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.callbacks.tracers import LangChainTracer

import json 
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium




def main():
    load_dotenv()

    db = get_sql_database()

    #llm = GroqLangChainWrapper()
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
        tracer=LangChainTracer(),
        agent_type="zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True,
        callbacks=[tracer]
    )

    

    st.title("👨‍🦯‍➡️GISpion👀")

    user_query = st.text_input("Ask me a question:")
    if st.button("Submit"):
        if user_query.strip():

            raw_result = agent.run(user_query, callbacks=[tracer])

            st.write("**Raw Result:**", raw_result)
            parsed = None
            try:
                parsed = json.loads(raw_result)
            except Exception:
                pass
            if parsed:
                if isinstance(parsed, list):
                    df = pd.DataFrame(parsed)
                    st.write("**DataFrame Result:**")
                    st.dataframe(df)
                elif isinstance(parsed, dict):
                    if "geometry" in parsed:
                        gdf = gpd.GeoDataFrame.from_features(parsed["geometry"])
                        st.write("**GeoDataFrame Result:**")
                        st.dataframe(gdf.head())
                        center_lat = gdf.geometry.centroid.y.mean()
                        center_lon = gdf.geometry.centroid.x.mean()
                        m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
                        folium.GeoJson(
                            data=gdf,
                            name="GeoData",
                            tooltip=folium.GeoJsonTooltip(fields=list(gdf.columns))
                        ).add_to(m)
                        st_folium(m, width=800, height=600)
                    else:
                        st.write("**Result:**", parsed)
        else:
            st.write("Please enter a question.")

if __name__ == '__main__':
    main()
