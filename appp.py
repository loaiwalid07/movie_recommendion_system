import streamlit as st
from movie_recommendion_system import *
import time
import base64

st.set_page_config(
    page_title="Movies Selector",
    page_icon='https://icon-library.com/images/movie-icon-png/movie-icon-png-2.jpg'
)
st.title('Movie Recommendation System')

st.subheader('Enter Movie that you love very much and this recommender will suggest you different Movies that you might like')

st.image('movies-.jpg', use_column_width=True)
############# Set Background #############
def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    https://i.makeagif.com/media/8-07-2015/vPFMLo.gif
    https://i.pinimg.com/originals/73/62/75/7362759c02faa8997f142569eeffd872.gif
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://i.pinimg.com/originals/73/62/75/7362759c02faa8997f142569eeffd872.gif");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
set_bg_hack_url()

#@st.cache()

fav_mov = st.selectbox(
    label='Choose your favourite Movie',
        options=data.loc[:, 'title'].values,
)

count = st.slider(
    label='Number of Movies to display',
    min_value=1,
    max_value=20,
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

            rec = get_recommendations(str(fav_mov),count+1)
            urlss=[]
            for i in range(0,len(rec)):
              urlss.append(search_in_google(rec['title'][i]))
            rec["url"]=urlss
            
            st.header('You might like these Movies')
            rec.index = rec.index + 1
            st.dataframe(rec[["title","vote_average"]])
            for j in range(1,len(rec)+1) :
               st.info(str(rec["title"][j])+f'\n_______\n'+str(rec["url"][j][0])+f'\n_______\n'+str(rec["url"][j][1])+
                        f'\n_______\n'+str(rec["url"][j][2])+f'\n_______\n'+str(rec["url"][j][3])+
                        f'\n_______\n'+str(rec["url"][j][4]))
