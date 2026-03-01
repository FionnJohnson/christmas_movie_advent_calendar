
# imports
import pandas as pd
import streamlit as st
from movie_logic import randomise

films_df = pd.read_csv('../data/cleaned_movies.csv')

# -----------------------------
# Session State Initialisation
# -----------------------------

# Streamlit reruns script on every interaction, so any variables that need to persist between interactions 
# must be stored in session_state.

# calender: stores the film index for each of the 24 advent days
# counter: tracks which advent day is currently being filled
# current_film: stores the film currently being displayed

if 'calendar' not in st.session_state:
    st.session_state.calendar = [None] * 24

if 'counter' not in st.session_state:
    st.session_state.counter = 0

if "current_film" not in st.session_state:
    st.session_state.current_film = None


# -------------------------------
# Page Layout and markdown styles
# -------------------------------


st.set_page_config(page_title="Christmas Film Advent Calendar ", layout="wide")


st.markdown("<h1 style='text-align: center;'>Christmas Film Advent Calendar🎄</h1>",
            unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center;'> For each day of Advent you can press"
            " the button and reveal a new Christmas film to watch. </h3>",
            unsafe_allow_html=True)
st.space()



# -----------------------------
# Buttons and button logic
# -----------------------------


with st.container(border=False, horizontal_alignment="center"):
    col1, col2 = st.columns(2, border=False)

    with col1:
        left, center, right = st.columns([1, 2, 1])
        with right:
            button_pressed = st.button(
                "Pick today's film ",
                width = 300,
                disabled = st.session_state.counter >= 24)
    with col2:
        reset_button = st.button("Reset calendar here", width = 200)


if button_pressed and st.session_state.counter < 24:
    film = randomise(films_df, st.session_state.calendar)       # returns a random film as a single entry dataframe

    st.session_state.calendar[st.session_state.counter] = int(film.index[0])     # updates the next slot of the calender with the film index
    st.session_state.current_film = film.iloc[0]        # converting into a series

    st.session_state.counter += 1
    st.rerun()


if reset_button:
    st.session_state.counter = 0
    # st.session_state.already_chosen = []
    st.session_state.calendar = [None] * 24
    st.rerun()



# -----------------------------------
# Advent cards 
# -----------------------------------

col1, col2 = st.columns(2, border=False)

with col1:
    for row in range(4):
        cols= st.columns(6, border=True, width=800)

        for col in range(6):
            index = row * 6 + col

            with cols[col]:

                if st.session_state.calendar[index] is None:
                    st.markdown(
                        f"<div style = 'height: 120px;"
                        f"display: flex; align-items: center; "
                        f"justify-content:center;"
                        f"font-size: 24px;'>"
                        f"{index + 1}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<div style = 'height: 90px;"
                        f"display: flex; align-items: center; "
                        f"justify-content:center;"
                        f"text-align: center;"
                        f"font-size: 16px;'>"
                        f"{films_df.iloc[st.session_state.calendar[index]]['title']}</div>",
                        unsafe_allow_html=True
                    )
                    
                    clicked = st.button(f"{index + 1}")

                    if clicked:
                        film_idx = st.session_state.calendar[index]
                        st.session_state.current_film = films_df.iloc[film_idx]



# -----------------------------
# Film descriptions
# -----------------------------

with col2:
    if st.session_state.counter > 0:
        with st.container(border=True, horizontal_alignment="center", height=400):

            film = pd.series = st.session_state.current_film

            st.markdown(f"<h3 style='text-align: center;'> {film['title']}</h3>",
                        unsafe_allow_html=True)

            col1, col2 = st.columns(2, border=False)

            with col1:
                st.write(f"Release year: {film['release_year']}")
                st.write(f"Rated: {film['rating']}")
                st.write(f"Length: {film['runtime']}")

            with col2:
                st.write(f"Director: {film['director']}")
                st.write(f"Stars: {film['stars']}")

            st.divider()

            st.markdown(f"<p style='text-align: center;'> Description: \n\n{film['description']}</p>",
                        unsafe_allow_html=True)


