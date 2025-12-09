"""
Admin Panel Page
Filename: admin_panel.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from db_utils import get_db_connection

def show_admin_panel():
    """Display admin dashboard"""
    st.title("Admin Dashboard")

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()

        col1, col2, col3 = st.columns(3)

        cursor.execute("SELECT COUNT(*) as count FROM Users")
        user_count = cursor.fetchone()['count']
        col1.metric("Total Users", user_count)

        cursor.execute("SELECT COUNT(*) as count FROM Bookings")
        booking_count = cursor.fetchone()['count']
        col2.metric("Total Bookings", booking_count)

        cursor.execute("SELECT SUM(tickets_booked) as total FROM Bookings")
        ticket_count = cursor.fetchone()['total'] or 0
        col3.metric("Tickets Sold", ticket_count)

        st.markdown("---")

        cursor.execute("SELECT language, COUNT(*) as count FROM Movies GROUP BY language")
        lang_data = cursor.fetchall()
        if lang_data:
            df_lang = pd.DataFrame(lang_data)
            fig = px.pie(df_lang, values='count', names='language', title='Movies by Language',
                        color_discrete_sequence=['#667eea', '#764ba2', '#f59e0b', '#10b981'])
            fig.update_layout(
                paper_bgcolor='#ffffff', 
                plot_bgcolor='#ffffff', 
                font_color='#1e293b',
                font_size=14,
                title_font_size=20,
                title_font_color='#1e293b'
            )
            st.plotly_chart(fig, use_container_width=True)

        cursor.close()
        conn.close()