import streamlit as st
from movies_recommendation import data, recommend
import pandas as pd

st.title("Movie Recommendation System 🎬")

# chuẩn hóa cột title
data["title"] = data["title"].str.strip()

movie_list = data["title"].tolist()
selected_movie = st.selectbox("Nhập tên phim:", movie_list)

# khởi tạo session_state
if "show_count" not in st.session_state:
    st.session_state.show_count = 10  # mặc định hiển thị 10 phim
if "load_more_count" not in st.session_state:
    st.session_state.load_more_count = 0  # đếm số lần nhấn xem thêm

if selected_movie:
    st.subheader(f"Top phim giống với {selected_movie}:")

    all_recommendations = recommend(selected_movie, top_n=50)
    top_titles = [t.strip() for t in all_recommendations.index]

    rec_df = pd.DataFrame({"Movie": top_titles[: st.session_state.show_count]})
    rec_df = rec_df.merge(data[["title", "genres"]], left_on="Movie", right_on="title", how="left")
    rec_df = rec_df.drop(columns=["title"])
    rec_df["genres"] = rec_df["genres"].apply(lambda x: x.replace(" ", " / "))
    rec_df = rec_df.rename(columns={"genres": "Genres"})
    rec_df = rec_df.reset_index(drop=True)

    st.table(rec_df)

    # nút xem thêm chỉ hoạt động tối đa 3 lần
    if st.session_state.load_more_count < 3:
        if st.button("Xem thêm"):
            st.session_state.show_count += 10
            st.session_state.load_more_count += 1
            st.rerun()
    else:
        st.info("Bạn đã xem hết số phim được phép hiển thị thêm.")
