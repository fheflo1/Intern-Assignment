import streamlit as st
from database.db import get_sql_database
from chatbot.agent import SQLAgent
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

def main():
    st.title("👨‍🦯‍➡️GISpion👀")

    db = get_sql_database()
    agent = SQLAgent(db)

    user_query = st.text_input("Ask me a question:")

    if st.button("Submit"):
        if user_query.strip():
            
            sql_query, result = agent.ask(user_query)

            if sql_query is None:
                st.write("**Error:**", result)
            else:
                st.write("**SQL query:**", sql_query)

                if isinstance(result, str):
                    st.write("**Result:**", result)
                elif isinstance(result, pd.DataFrame):
                    st.write("**DataFrame Result:**")
                    st.dataframe(result)
                elif isinstance(result, gpd.GeoDataFrame):
                    st.write("**GeoDataFrame Result:**")
                    st.dataframe(result.head())

                    if not result.empty and "geometry" in result.columns:
                        center_lat = result.geometry.centroid.y.mean()
                        center_lon = result.geometry.centroid.x.mean()
                        m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
                        folium.GeoJson(
                            data=result,
                            name="GeoData",
                            tooltip=folium.GeoJsonTooltip(fields=list(result.columns))
                        ).add_to(m)

                        st_folium(m, width=800, height=600)
                    else:
                        st.info("No geometry column found¨to visualize.")
                else:
                    st.write("**Result:**", result)
        else:
            st.write("Please enter a question.")


if __name__ == '__main__':
    main()