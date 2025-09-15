from nltk.tokenize import RegexpTokenizer
from nltk import FreqDist, bigrams, trigrams
from nltk.corpus import stopwords

# ==========================
# 📌 Stopwords setup
# ==========================
try:
    stop = set(stopwords.words('english'))
except:
    import nltk
    nltk.download('stopwords')
    stop = set(stopwords.words('english'))

stop.update(['rated', 'n', 'nan', 'x', 'RATED', 'Rated'])

# ==========================
# 📌 Cuisine Review Analysis
# ==========================
def analyze_cuisine_reviews(df, cuisine_name, sample_size=500):
    cuisine_df = df[df['cuisines'].str.contains(cuisine_name, na=False)].copy()

    if cuisine_df.empty:
        st.warning(f"No data available for {cuisine_name}")
        return

    tokenizer = RegexpTokenizer(r"[a-zA-Z]+")
    sample_df = cuisine_df.head(sample_size)
    reviews_tokens = sample_df['reviews_list'].fillna("").str.lower().apply(tokenizer.tokenize)
    reviews_tokens_clean = reviews_tokens.apply(lambda r: [t for t in r if t not in stop])
    total_words = [word for review in reviews_tokens_clean for word in review]

    # 🔹 Unigrams
    fd_uni = FreqDist(total_words)
    df_uni = pd.DataFrame(fd_uni.most_common(20), columns=['word', 'count']).set_index('word')
    st.subheader(f"Top 20 Unigrams for {cuisine_name}")
    st.bar_chart(df_uni)

    # 🔹 Bigrams
    fd_bi = FreqDist(bigrams(total_words))
    df_bi = pd.DataFrame(
        {'bigram': [' '.join(b) for b, _ in fd_bi.most_common(20)],
         'count': [c for _, c in fd_bi.most_common(20)]}
    ).set_index('bigram')
    st.subheader(f"Top 20 Bigrams for {cuisine_name}")
    st.bar_chart(df_bi)

    # 🔹 Trigrams
    fd_tri = FreqDist(trigrams(total_words))
    df_tri = pd.DataFrame(
        {'trigram': [' '.join(t) for t, _ in fd_tri.most_common(20)],
         'count': [c for _, c in fd_tri.most_common(20)]}
    ).set_index('trigram')
    st.subheader(f"Top 20 Trigrams for {cuisine_name}")
    st.bar_chart(df_tri)
