# from ydata_profiling import ProfileReport
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv('movies.csv', encoding="latin-1", sep = "\t")

# # data visulization to HTML
# profile = ProfileReport(data, title="Movie Recommendation Report", explorative=True)
# profile.to_file('movies_recommendation_report.html')

def split_genres(genres):
    genres = genres.replace("|", " ")
    genres = genres.replace("-","")
    return genres

data["genres"] = data["genres"].apply(split_genres)

vectorize = TfidfVectorizer()
tfidf_matrix = vectorize.fit_transform(data["genres"])
tfidf_matrix_dense =  pd.DataFrame(tfidf_matrix.todense(), index = data["title"], columns = vectorize.get_feature_names_out())

cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim_dense = pd.DataFrame(cosine_sim, index = data["title"], columns = data["title"])


def recommend(movie_name, top_n=10):
    movie_name = movie_name.strip()  # chuẩn hóa
    if movie_name not in cosine_sim_dense.index:
        return pd.Series()

    result = cosine_sim_dense.loc[movie_name]
    top_movies = result.sort_values(ascending=False).head(top_n + 1)

    # bỏ phim gốc một cách an toàn
    top_movies = top_movies.drop(movie_name, errors="ignore")

    return top_movies





