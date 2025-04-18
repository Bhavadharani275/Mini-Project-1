
def fetch_summary(cursor):
    cursor.execute("""
        SELECT 
            (SELECT COUNT(*) FROM competitors) AS total_competitors,
            (SELECT COUNT(DISTINCT country) FROM competitors) AS total_countries,
            (SELECT MAX(points) FROM Competitor_rankings) AS highest_points
    """)
    return cursor.fetchone()


def fetch_Leaderboard(cursor,limit=5):
    cursor.execute("""
        SELECT c.Name, c.Country, r.Rank, r.Points 
        FROM competitors c
        JOIN Competitor_rankings r ON c.competitor_id = r.competitor_id
        ORDER BY r.points DESC
        LIMIT %s
    """, (limit,))
    return cursor.fetchall()


def fetch_top_competitors(cursor,start_rank, end_rank):
    cursor.execute("""
        SELECT c.Name, c.Country, r.Rank, r.Points 
        FROM competitors c
        JOIN Competitor_rankings r ON c.competitor_id = r.competitor_id
        WHERE r.rank BETWEEN %s AND %s
        ORDER BY r.points DESC,r.rank
    """,(start_rank, end_rank))
    return cursor.fetchall()


def fetch_search_and_filter_competitors(cursor,name_input,country_filter,min_points):
    query = """
        SELECT c.Name, c.Country, r.Rank, r.Points, r.Competitions_played
        FROM competitors c
        JOIN Competitor_rankings r ON c.competitor_id = r.competitor_id
        WHERE (c.name LIKE %s)
          AND (c.country LIKE %s)
          AND (r.points >= %s)
        ORDER BY r.points DESC
    """
    cursor.execute(query,(f"%{name_input}%", f"%{country_filter}%", min_points))
    return cursor.fetchall()


def fetch_Country_Wise_Stats(cursor):
    cursor.execute("""
        SELECT c.Country, COUNT(*) AS Total_competitors, AVG(r.points) AS Avg_points
        FROM competitors c
        JOIN Competitor_rankings r ON c.competitor_id = r.competitor_id
        GROUP BY c.country
        ORDER BY c.country
    """)
    return cursor.fetchall()

def fetch_category_gender_type(cursor):
    cursor.execute("SELECT DISTINCT category_name FROM categories ORDER BY category_name")
    categories = [row['category_name'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT type FROM competitions ORDER BY type")
    types = [row['type'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT gender FROM competitions ORDER BY gender")
    genders = [row['gender'] for row in cursor.fetchall()]
    return categories, types, genders


def fetch_category_comptition(cursor,category_name, gender, type_t):
    query = """
        SELECT Cat.Category_name, Comp.Competition_name, Comp.Type, Comp.Gender
        FROM Competitions Comp
        JOIN Categories Cat ON Comp.category_id = Cat.category_id
        WHERE (%s = 'None' OR Cat.category_name = %s)
          AND (%s = 'None' OR Comp.gender = %s)
          AND (%s = 'None' OR Comp.type = %s)
        ORDER BY Cat.Category_name
    """
    cursor.execute(query,(category_name, category_name, gender, gender, type_t, type_t))
    return cursor.fetchall()


def fetch_country_city(cursor):
    cursor.execute("SELECT DISTINCT complex_name FROM complexes ORDER BY complex_name")
    complexes = [row['complex_name'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT venue_name FROM venues ORDER BY venue_name")
    venues = [row['venue_name'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT city_name FROM venues ORDER BY city_name")
    city = [row['city_name'] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT country_name FROM venues ORDER BY country_name")
    country = [row['country_name'] for row in cursor.fetchall()]
    return complexes, venues, city,country


def fetch_venues_complexes(cursor,complex_name, venues_name, city_name, country_name):
    query = """
        SELECT c.complex_name,v.venue_name,v.city_name,v.country_name
        FROM venues v
        JOIN complexes c ON c.complex_id = v.complex_id
        WHERE (%s = 'None' OR c.complex_name = %s)
          AND (%s = 'None' OR v.venue_name = %s)
          AND (%s = 'None' OR v.city_name = %s)
          AND (%s = 'None' OR v.country_name = %s)
        ORDER BY v.country_name
    """
    cursor.execute(query,(complex_name, complex_name, venues_name, venues_name, city_name, city_name, country_name, country_name))
    return cursor.fetchall()
