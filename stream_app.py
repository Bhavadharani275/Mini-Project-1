import streamlit as st
import pandas as pd
from db_config import get_connection
import sql_queries
import altair as alt

st.set_page_config(page_title="🎾 Tennis Analysis", layout="wide")

# Load DB connection
conn = get_connection()
cursor = conn.cursor(dictionary=True)

#sidebar header
st.sidebar.title("Content")

page_split = st.sidebar.radio("",("🏠 Dashboard",
                                  ":mag: Search & Filter Competitors", 
                                  ":sports_medal: Competitors by Rank",
                                  ":file_folder: Categories & Competitions",
                                  ":stadium: Venues & complexes",
                                  ":earth_africa: Country-wise Analysis"))

# Dashboard Header
if page_split==("🏠 Dashboard"):
    st.markdown(
    "<h1 style='text-align:center;'>🎾 Tennis Dashboard</h1>",
    unsafe_allow_html=True)

# Summary Section
    st.header(":bar_chart: Summary Statistics")
    summary = sql_queries.fetch_summary(cursor)

    competitors, countries, points = st.columns(3, border=True)
    competitors.metric("Total Competitors :busts_in_silhouette:", summary['total_competitors'])
    countries.metric("Countries Represented :earth_africa:", summary['total_countries'])
    points.metric("Highest Points :trophy:", summary['highest_points'])

# top 5 ranks in dashboard
    st.title(":sports_medal: Leaderboard Board")
    board = sql_queries.fetch_Leaderboard(cursor,limit=5)
    df_leaderboard = pd.DataFrame(board)
    df_leaderboard['Medal'] = df_leaderboard['Rank'].apply(
        lambda rank: ":first_place_medal:" if rank == 1 else (":second_place_medal:" if rank == 2 else (":third_place_medal:" if rank == 3 else "")))
    st.table(df_leaderboard)

# Search & Filters
elif page_split==(":mag: Search & Filter Competitors"):
    st.header(":mag: Search & Filter Competitors")

    name_input = st.text_input("Search by name")
    country_filter = st.text_input("Filter by country")
    min_points = st.slider("Minimum Points", 0, 10000, 5000)
    
    search_filter = sql_queries.fetch_search_and_filter_competitors(cursor,name_input,country_filter,min_points)
    if search_filter:
        search_results = pd.DataFrame(search_filter)
        st.table(search_results)
    else:
        st.info("No results found.")


# Leaderboard Section
elif page_split ==(":sports_medal: Competitors by Rank"):
    st.header(":sports_medal: Competitors by Rank")
    ranks_range = st.slider("Ranks",1,600,(1,10))
    start_rank, end_rank = ranks_range
    top_competitors = sql_queries.fetch_top_competitors(cursor,start_rank, end_rank)
    if top_competitors:
        df_top_leaderboard = pd.DataFrame(top_competitors)
        st.table(df_top_leaderboard)
    else: 
        st.info("No Ranks found.")        


 # Country-Wise Stats
elif page_split==(":earth_africa: Country-wise Analysis"):
    st.header(":earth_africa: Country-wise Analysis")
    country_wise = sql_queries.fetch_Country_Wise_Stats(cursor)
    df_country_stats = pd.DataFrame(country_wise)
    st.table(df_country_stats)


# search by category and competitions
elif page_split == ":file_folder: Categories & Competitions":
    
    categories, types, genders = sql_queries.fetch_category_gender_type(cursor)
    
    # Add a "None" option at the start for each dropdown
    categories.insert(0, "None")
    types.insert(0, "None")
    genders.insert(0, "None")
    
    #dispaly selcetbox in sidebar
    category_name = st.sidebar.selectbox("Category name", categories)
    gender = st.sidebar.selectbox("Gender", genders)
    type_t = st.sidebar.selectbox("Type", types)

    results = sql_queries.fetch_category_comptition(cursor,category_name, gender, type_t)

    if results:
        df = pd.DataFrame(results)
    
        gender_counts = df['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']

        # Create the chart(bar chart)
        chart = alt.Chart(gender_counts).mark_bar().encode(
        x=alt.X('Gender', title='Gender'),
        y=alt.Y('Count', title='Number of Events'),
        color='Gender'
        ).properties(
        title=f'📊 Event Count by Gender for Category {category_name}')

        st.altair_chart(chart, use_container_width=True)

        st.header("📁 **Categories & Competitions**")
        st.dataframe(df)
    else:
        st.info("No results found.")

    
# search venues and complexes
elif page_split == ":stadium: Venues & complexes":
    st.header("🏟️ Venues & complexes")

    complexes, venues, city, country = sql_queries.fetch_country_city(cursor)

    # Add a "None" option at the start for each dropdown
    complexes.insert(0, "None")
    venues.insert(0, "None")
    city.insert(0, "None")
    country.insert(0, "None")
    
    #dispaly selcetbox in sidebar
    complex_name = st.sidebar.selectbox("Complex name", complexes)
    venues_name = st.sidebar.selectbox("Venues name", venues)
    city_name = st.sidebar.selectbox("City", city)
    country_name = st.sidebar.selectbox("Country name",country)

    result = sql_queries.fetch_venues_complexes(cursor,complex_name,venues_name,city_name,country_name)

    if result:
        df = pd.DataFrame(result)
        st.dataframe(df)
    else:
        st.info("No results found.")

# Close DB
cursor.close()
conn.close()
