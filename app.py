"""
CineBook - Main Application
Filename: app.py
Run with: streamlit run app.py
"""

import streamlit as st
from datetime import datetime
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import database functions
from db_utils import get_movies, get_showtimes, get_booked_seats, book_tickets, get_user_bookings, register_user, login_user

# Import all page modules at the TOP (IMPORTANT!)
from browse_movies import show_browse_movies
from book_tickets import show_book_tickets
from my_bookings import show_my_bookings
from admin_panel import show_admin_panel

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'selected_seats' not in st.session_state:
    st.session_state.selected_seats = []
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "Browse Movies"

# Load CSS
def load_css():
    st.markdown("""
    <style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
    }
    
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e2e8f0;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
    }
    
    [data-testid="stSidebar"] h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -1px;
        padding: 24px 0;
        text-align: center;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #475569;
        font-size: 15px;
        padding: 14px 18px;
        border-radius: 12px;
        transition: all 0.3s ease;
        font-weight: 600;
        margin: 4px 0;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: #f1f5f9;
        color: #1e293b;
        transform: translateX(4px);
    }
    
    [data-testid="stSidebar"] .stSuccess {
        background: #ecfdf5;
        border-left: 4px solid #10b981;
        color: #065f46;
        padding: 14px 18px;
        border-radius: 10px;
        font-size: 14px;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.1);
    }
    
    .main .block-container {
        padding: 50px 70px;
        max-width: 1600px;
        background: transparent;
    }
    
    h1 {
        color: #1e293b;
        font-weight: 800;
        font-size: 52px;
        letter-spacing: -2px;
        margin-bottom: 40px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    h2 {
        color: #1e293b;
        font-weight: 700;
        font-size: 32px;
        letter-spacing: -1px;
        margin-bottom: 20px;
    }
    
    h3 {
        color: #1e293b;
        font-weight: 700;
        font-size: 20px;
        letter-spacing: -0.5px;
    }
    
    p {
        color: #475569;
        font-size: 15px;
        line-height: 1.6;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        color: #1e293b;
        font-size: 16px;
        padding: 16px 20px;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    .stTextInput > label,
    .stSelectbox > label,
    .stNumberInput > label {
        color: #1e293b;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        border: none;
        border-radius: 12px;
        padding: 16px 36px;
        font-size: 16px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        letter-spacing: -0.3px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        font-size: 18px !important;
        padding: 18px 44px !important;
    }
    
    button[kind="secondary"] {
        background: #ffffff !important;
        color: #667eea !important;
        border: 2px solid #667eea !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }
    
    button[kind="secondary"]:hover {
        background: #f8f9ff !important;
        transform: translateY(-2px);
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #cbd5e1, transparent);
        margin: 40px 0;
    }
    
    .stSuccess {
        background: #ecfdf5;
        border: 2px solid #10b981;
        color: #065f46;
        padding: 18px 24px;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);
    }
    
    .stError {
        background: #fef2f2;
        border: 2px solid #ef4444;
        color: #991b1b;
        padding: 18px 24px;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.1);
    }
    
    .stWarning {
        background: #fffbeb;
        border: 2px solid #f59e0b;
        color: #92400e;
        padding: 18px 24px;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.1);
    }
    
    .stInfo {
        background: #eff6ff;
        border: 2px solid #3b82f6;
        color: #1e40af;
        padding: 18px 24px;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
    }
    
    .stDataFrame {
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .stDataFrame table {
        background: #ffffff;
    }
    
    .stDataFrame thead tr th {
        background: #f8fafc !important;
        color: #1e293b !important;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 2px solid #e2e8f0 !important;
        padding: 16px !important;
    }
    
    .stDataFrame tbody tr {
        border-bottom: 1px solid #f1f5f9 !important;
    }
    
    .stDataFrame tbody tr:hover {
        background: #f8fafc !important;
    }
    
    .stDataFrame tbody td {
        color: #475569 !important;
        font-weight: 500;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 40px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    
    [data-testid="stMetricLabel"] {
        color: #475569;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="metric-container"] {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        padding: 28px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }
    
    .stForm {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 36px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    [data-baseweb="select"] > div {
        background: #ffffff;
        border-color: #e2e8f0;
    }
    
    .js-plotly-plot {
        background: #ffffff !important;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    #MainMenu {visibility: fixed;}
    footer {visibility: fixed;}
    
    [data-testid="collapsedControl"] {
        display: block !important;
        visibility: visible !important;
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
        z-index: 999999 !important;
        background: #667eea !important;
        color: white !important;
        padding: 12px !important;
        border-radius: 0 8px 8px 0 !important;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.2) !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: #764ba2 !important;
    }
    
    @media (max-width: 768px) {
        .main .block-container {
            padding: 30px 20px;
        }
        h1 {
            font-size: 36px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="CineBook - Movie Booking",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    )

    load_css()
    st.sidebar.title("🎬 CineBook")

    # NOT LOGGED IN - Show Login/Signup
    if not st.session_state.logged_in:
        menu = st.sidebar.radio("Menu", ["Login", "Sign Up"])

        if menu == "Sign Up":
            st.title("Create Account")
            with st.form("signup_form"):
                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit = st.form_submit_button("Sign Up")

                if submit:
                    if password != confirm_password:
                        st.error("Passwords don't match!")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters!")
                    elif register_user(username, password, email):
                        st.success("Account created! Please login.")

        else:  # Login
            st.title("Welcome Back")
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")

                if submit:
                    user = login_user(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user['user_id']
                        st.session_state.username = user['username']
                        st.session_state.is_admin = user.get('is_admin', 0) == 1
                        st.session_state.current_menu = "Browse Movies"
                        st.rerun()
                    else:
                        st.error("Invalid credentials!")

    # LOGGED IN - Show Main Menu
    else:
        st.sidebar.success(f"👋 {st.session_state.username}")

        if st.session_state.is_admin:
            menu_options = ["Browse Movies", "Book Tickets", "My Bookings", "Admin Panel", "Logout"]
        else:
            menu_options = ["Browse Movies", "Book Tickets", "My Bookings", "Logout"]

        if st.session_state.current_menu not in menu_options:
            st.session_state.current_menu = "Browse Movies"

        menu = st.sidebar.radio(
            "Menu",
            menu_options,
            index=menu_options.index(st.session_state.current_menu),
            key="menu_radio"
        )
        st.session_state.current_menu = menu

        if menu == "Logout":
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.is_admin = False
            st.session_state.selected_movie = None
            st.session_state.selected_seats = []
            st.session_state.current_menu = "Browse Movies"
            st.rerun()

        elif menu == "Browse Movies":
            show_browse_movies()

        elif menu == "Book Tickets":
            show_book_tickets()

        elif menu == "My Bookings":
            show_my_bookings()

        elif menu == "Admin Panel" and st.session_state.is_admin:
            show_admin_panel()

if __name__ == "__main__":
    main()