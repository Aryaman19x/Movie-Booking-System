"""
Browse Movies Page
Filename: browse_movies.py
"""

import streamlit as st
from db_utils import get_movies

def show_browse_movies():
    """Display browse movies page"""
    st.title("Now Showing")
    movies = get_movies()

    if movies:
        # Filter buttons
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            lang_filter = st.selectbox("Language", ["All", "Hindi", "English"])
        with col2:
            genre_filter = st.selectbox("Genre", ["All"] + list(set([m['genre'] for m in movies])))

        # Filter movies
        filtered_movies = movies
        if lang_filter != "All":
            filtered_movies = [m for m in filtered_movies if m['language'] == lang_filter]
        if genre_filter != "All":
            filtered_movies = [m for m in filtered_movies if m['genre'] == genre_filter]

        st.markdown("---")

        # Display movies in grid - 3 columns
        cols = st.columns(3)
        for idx, movie in enumerate(filtered_movies):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style='background: #ffffff; 
                            border-radius: 16px; padding: 0; overflow: hidden; 
                            border: 2px solid #e2e8f0; transition: all 0.3s ease;
                            cursor: pointer; margin-bottom: 24px;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);'>
                    <img src='{movie['poster_url']}' 
                         style='width: 100%; height: 400px; object-fit: cover;'/>
                    <div style='padding: 20px;'>
                        <h3 style='color: #1e293b; font-size: 20px; margin: 0 0 8px 0; font-weight: 700;'>{movie['title']}</h3>
                        <p style='color: #64748b; font-size: 14px; margin: 0 0 12px 0; font-weight: 600;'>{movie['genre']} • {movie['duration']} min</p>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <span style='color: #f59e0b; font-weight: 700; font-size: 18px;'>⭐ {movie['rating']}</span>
                            <span style='background: linear-gradient(135deg, #667eea, #764ba2); 
                                         color: #ffffff; padding: 6px 14px; border-radius: 20px; 
                                         font-size: 12px; font-weight: 700; letter-spacing: 0.5px;'>{movie['language']}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Book Now button
                if st.button("Book Now", key=f"book_{movie['movie_id']}", use_container_width=True):
                    st.session_state.selected_movie = movie['movie_id']
                    st.session_state.current_menu = "Book Tickets"
                    st.rerun()
    else:
        st.info("No movies available.")