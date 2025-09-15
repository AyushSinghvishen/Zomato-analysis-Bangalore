from www import analyze_cuisine_reviews

# ==========================
# 📌 Streamlit page config
# ==========================
st.set_page_config(page_title="Zomato Cuisine Review Analysis", layout="wide")

# ==========================
# 📌 Load data
# ==========================
@st.cache_data
def load_data():
    con = sqlite3.connect(r"zomato_dataset//zomato_rawdata.sqlite")
    df = pd.read_sql_query("SELECT * FROM Users", con)
    df = df.dropna(subset=['cuisines'])
    return df

df = load_data()

# ==========================
# 📌 Rate vs Online Order
# ==========================
df['rate'] = df['rate'].replace(('NEW', '-'), np.nan)
df['rate'] = df['rate'].apply(lambda x: float(x.split('/')[0]) if isinstance(x, str) else x)

x = pd.crosstab(df['rate'], df['online_order'])
normalize_df = x.div(x.sum(axis=1).astype(float), axis=0)

st.subheader("Online Order Distribution Across Ratings")
st.bar_chart(normalize_df * 100)

# ==========================
# 📌 Cuisine Categories
# ==========================
cuisine_categories = {
    "Middle Eastern & Mediterranean": ["Arabian", "Iranian", "Lebanese", "Mediterranean", "Middle Eastern", "Turkish"],
    "European": ["Belgian", "British", "Continental", "European", "French", "German", "Greek", "Italian", "Portuguese", "Russian", "Spanish"],
    "American & Western": ["American", "Australian", "BBQ", "Fast Food", "Finger Food", "Grill", "Roast Chicken", "South American", "Steak", "Tex-Mex"],
    "Snacks, Bakery & Beverages": ["Bakery", "Bar Food", "Beverages", "Bubble Tea", "Cafe", "Charcoal Chicken", "Coffee", "Desserts", "Drinks Only", "Healthy Food", "Hot dogs", "Ice Cream", "Jewish", "Juices", "Paan", "Salad", "Sandwich", "Street Food", "Tea", "Vegan", "Wraps"],
    "Quick Meals & Specialties": ["Biryani", "Bohri", "Burger", "Kebab", "Mithai", "Momos", "Pizza", "Raw Meats", "Rolls", "Seafood", "Sushi"],
    "Indian Regional Cuisines": ["North Indian", "Mughlai", "Awadhi", "Lucknowi", "Kashmiri", "Rajasthani", "Punjabi", "South Indian", "Andhra", "Chettinad", "Hyderabadi", "Kerala", "Tamil", "Mangalorean", "Malwani", "Konkan", "Bengali", "Assamese", "Oriya", "Bihari", "Gujarati", "Maharashtrian", "Goan", "Sindhi", "Naga", "North Eastern", "Modern Indian"],
    "Asian Cuisines": ["Chinese", "Cantonese", "Japanese", "Korean", "Mongolian", "Thai", "Vietnamese", "Burmese", "Indonesian", "Malaysian", "Singaporean", "Afghan", "Afghani", "Nepalese", "Sri Lankan", "Tibetan", "Pan Asian"]
}

# ==========================
# 📌 Sidebar filters
# ==========================
st.sidebar.title("Cuisine Selection")
category = st.sidebar.selectbox("Select Cuisine Category", list(cuisine_categories.keys()))
cuisine = st.sidebar.selectbox("Select Cuisine", cuisine_categories[category])

# ==========================
# 📌 Display analysis
# ==========================
analyze_cuisine_reviews(df, cuisine)
