"""
Book Tickets Page
Filename: book_tickets.py
"""

import streamlit as st
from db_utils import get_movies, get_showtimes, get_booked_seats, book_tickets
from datetime import datetime

def show_book_tickets():
    """Display book tickets page"""
    st.title("Book Tickets")

    movies = get_movies()

    if st.session_state.selected_movie:
        movie_id = st.session_state.selected_movie
        selected_movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    else:
        if movies:
            movie_options = {f"{m['title']} ({m['language']})": m['movie_id'] for m in movies}
            selected_movie_key = st.selectbox("Select Movie", list(movie_options.keys()))
            movie_id = movie_options[selected_movie_key]
            selected_movie = next((m for m in movies if m['movie_id'] == movie_id), None)
        else:
            st.info("No movies available.")
            return

    if selected_movie:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(selected_movie['poster_url'], use_container_width=True)
        with col2:
            st.subheader(selected_movie['title'])
            st.write(f"**Genre:** {selected_movie['genre']}")
            st.write(f"**Duration:** {selected_movie['duration']} minutes")
            st.write(f"**Rating:** ⭐ {selected_movie['rating']}/10")
            st.write(f"**Language:** {selected_movie['language']}")
            st.markdown(f"<p style='color: #475569; font-size: 15px; line-height: 1.8;'>{selected_movie['description']}</p>", unsafe_allow_html=True)

        st.markdown("---")

        showtimes = get_showtimes(movie_id)

        if showtimes:
            st.subheader("Select Showtime")
            showtime_options = {
                f"{s['show_date']} at {s['show_time']} - {s['available_seats']} seats": s['showtime_id']
                for s in showtimes
            }
            selected_showtime_key = st.selectbox("Showtime", list(showtime_options.keys()))
            showtime_id = showtime_options[selected_showtime_key]

            st.markdown("---")
            st.markdown("<p style='text-align: center; color: #64748b; font-size: 13px; letter-spacing: 3px; font-weight: 700;'>SCREEN</p>", unsafe_allow_html=True)
            st.markdown("<div style='background: linear-gradient(to bottom, #cbd5e1, #94a3b8); height: 8px; border-radius: 50%; margin: 16px auto 40px; max-width: 500px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'></div>", unsafe_allow_html=True)

            booked_seats = get_booked_seats(showtime_id)

            rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
            seats_per_row = 10

            for row in rows:
                cols = st.columns([0.5] + [1]*seats_per_row + [0.5])
                with cols[0]:
                    st.markdown(f"<p style='text-align: center; color: #666666; font-weight: 700;'>{row}</p>", unsafe_allow_html=True)

                for seat_num in range(1, seats_per_row + 1):
                    seat_id = f"{row}{seat_num}"
                    with cols[seat_num]:
                        if seat_id in booked_seats:
                            st.button("🔴", key=f"seat_{seat_id}", disabled=True, use_container_width=True, help="Booked")
                        elif seat_id in st.session_state.selected_seats:
                            if st.button("🟡", key=f"seat_{seat_id}", use_container_width=True, help="Click to unselect"):
                                st.session_state.selected_seats.remove(seat_id)
                                st.rerun()
                        else:
                            if st.button("🟢", key=f"seat_{seat_id}", use_container_width=True, help="Click to select"):
                                st.session_state.selected_seats.append(seat_id)
                                st.rerun()

            st.markdown("---")

            st.markdown("""
            <div style='display: flex; gap: 32px; justify-content: center; padding: 24px; 
                        background: #ffffff; border-radius: 12px; border: 2px solid #e2e8f0;
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);'>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <span style='font-size: 24px;'>🟢</span>
                    <span style='color: #1e293b; font-size: 15px; font-weight: 600;'>Available</span>
                </div>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <span style='font-size: 24px;'>🟡</span>
                    <span style='color: #1e293b; font-size: 15px; font-weight: 600;'>Selected</span>
                </div>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <span style='font-size: 24px;'>🔴</span>
                    <span style='color: #1e293b; font-size: 15px; font-weight: 600;'>Booked</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.session_state.selected_seats:
                st.markdown(f"""
                <div style='background: #eff6ff; border: 2px solid #667eea; 
                            border-radius: 12px; padding: 24px; margin: 24px 0;
                            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);'>
                    <p style='color: #1e293b; font-size: 16px; font-weight: 700; margin: 0;'>
                        SELECTED SEATS: <span style='color: #667eea;'>{', '.join(sorted(st.session_state.selected_seats))}</span> 
                        ({len(st.session_state.selected_seats)} tickets)
                    </p>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Clear Selection", type="secondary", use_container_width=True):
                        st.session_state.selected_seats = []
                        st.rerun()
                with col2:
                    if st.button("Confirm Booking", type="primary", use_container_width=True):
                        selected_seats_copy = st.session_state.selected_seats.copy()
                        if book_tickets(st.session_state.user_id, showtime_id, selected_seats_copy):
                            st.session_state.selected_seats = []
                            st.session_state.selected_movie = None

                            st_info = [s for s in showtimes if s['showtime_id'] == showtime_id][0]

                            st.markdown(f"""
                            <div style="
                                margin-top: 24px;
                                padding: 24px 28px;
                                border-radius: 16px;
                                border: 2px dashed #64748b;
                                background: linear-gradient(135deg,#0f172a,#020617);
                                color: #e5e7eb;
                                box-shadow: 0 10px 30px rgba(15,23,42,0.6);
                                position: relative;
                                overflow: hidden;
                            ">
                                <div style="
                                    position:absolute;
                                    inset: 0;
                                    background-image: radial-gradient(circle at 0 0,rgba(96,165,250,0.2),transparent 60%),
                                                      radial-gradient(circle at 100% 100%,rgba(251,191,36,0.2),transparent 60%);
                                    opacity: 0.9;
                                "></div>
                                <div style="position:relative; z-index:1;">
                                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                                        <h3 style="margin:0; font-size:22px; font-weight:800; letter-spacing:1px;">
                                            🎟️ CINEBOOK E‑TICKET
                                        </h3>
                                        <span style="font-size:13px; text-transform:uppercase; letter-spacing:2px; color:#a5b4fc;">
                                            CONFIRMED
                                        </span>
                                    </div>
                                    <hr style="border:none; border-top:1px dashed #4b5563; margin:12px 0;" />
                                    <div style="display:flex; flex-wrap:wrap; gap:16px; margin-top:8px;">
                                        <div style="min-width:160px;">
                                            <div style="font-size:11px; text-transform:uppercase; color:#9ca3af; letter-spacing:1px;">Movie</div>
                                            <div style="font-size:16px; font-weight:700; color:#e5e7eb;">{selected_movie['title']}</div>
                                        </div>
                                        <div style="min-width:120px;">
                                            <div style="font-size:11px; text-transform:uppercase; color:#9ca3af; letter-spacing:1px;">Date</div>
                                            <div style="font-size:15px; font-weight:600;">{str(st_info['show_date'])}</div>
                                        </div>
                                        <div style="min-width:100px;">
                                            <div style="font-size:11px; text-transform:uppercase; color:#9ca3af; letter-spacing:1px;">Time</div>
                                            <div style="font-size:15px; font-weight:600;">{str(st_info['show_time'])}</div>
                                        </div>
                                        <div style="min-width:160px;">
                                            <div style="font-size:11px; text-transform:uppercase; color:#9ca3af; letter-spacing:1px;">Seats</div>
                                            <div style="font-size:15px; font-weight:700; color:#a5b4fc;">{", ".join(sorted(selected_seats_copy))}</div>
                                        </div>
                                        <div style="min-width:90px;">
                                            <div style="font-size:11px; text-transform:uppercase; color:#9ca3af; letter-spacing:1px;">Tickets</div>
                                            <div style="font-size:20px; font-weight:800; color:#fbbf24; text-align:center;">{len(selected_seats_copy)}</div>
                                        </div>
                                    </div>
                                    <hr style="border:none; border-top:1px dashed #4b5563; margin:16px 0 8px 0;" />
                                    <div style="display:flex; justify-content:space-between; align-items:center; font-size:11px; color:#9ca3af;">
                                        <span>Full details and Booking ID are available in My Bookings.</span>
                                        <span>{datetime.now().strftime("%Y-%m-%d %H:%M")}</span>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.info("Please select seats to continue")
        else:
            st.warning("No showtimes available for this movie.")