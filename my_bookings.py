"""
My Bookings Page
Filename: my_bookings.py
"""

import streamlit as st
from db_utils import get_user_bookings

def show_my_bookings():
    """Display user bookings page"""
    st.title("My Bookings")
    bookings = get_user_bookings(st.session_state.user_id)

    if bookings:
        for booking in bookings:
            st.markdown(f"""
            <div style='background: #ffffff; border: 2px solid #e2e8f0; border-radius: 12px; 
                        padding: 28px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                        transition: all 0.3s ease;'>
                <h3 style='color: #1e293b; margin: 0 0 16px 0; font-weight: 700; font-size: 22px;'>{booking['title']}</h3>
                <p style='color: #475569; margin: 8px 0; font-size: 15px;'><strong>📅 Date:</strong> {booking['show_date']} at {booking['show_time']}</p>
                <p style='color: #475569; margin: 8px 0; font-size: 15px;'><strong>🎫 Seats:</strong> {booking['seat_numbers']}</p>
                <p style='color: #10b981; margin: 8px 0; font-size: 14px; font-weight: 600;'>✅ Booked on {booking['booking_date']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No bookings yet. Start booking movies!")