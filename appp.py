import streamlit as st
from movie_recommendion_system import *
import time

st.title('Movie Recommendation System')

st.header('Enter Movie that you love very much and this recommender will suggest you different Movies that you might like')

st.image('movies-.jpg', use_column_width=True)

#@st.cache()

fav_mov = st.selectbox(
    label='Choose your favourite Movie',
        options=data.loc[:, 'title'].values,
)

count = st.slider(
    label='Number of Movies to display',
    min_value=1,
    max_value=15,
    value=7,
    step=1
)

submit = st.button('Submit')


if submit:
    if not fav_mov:
        st.subheader('Please enter at least one Movie')
    else:
        with st.spinner('Searching for Movies'):
            time.sleep(2)

            rec = get_recommendations(str(fav_mov),count)
            urlss=[]
            for i in range(0,len(rec)):
              urlss.append(search_in_google(rec['title'][i]))
            rec["url"]=urlss
            
            st.header('You might like these Movies')
            st.dataframe(rec)
            for j in range(0,len(rec)) :
                st.info(rec[["title","vote_average","url"]].iloc[j])
