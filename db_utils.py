"""
Database Utility Functions
Filename: db_utils.py
"""

import streamlit as st
import pymysql
import hashlib
from datetime import datetime

# Database Configuration
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'database': 'movie_booking',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, email):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            hashed_pw = hash_password(password)
            cursor.execute(
                "INSERT INTO Users (username, password_hash, email) VALUES (%s, %s, %s)",
                (username, hashed_pw, email)
            )
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Registration failed: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def login_user(username, password):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            hashed_pw = hash_password(password)
            cursor.execute(
                "SELECT * FROM Users WHERE username = %s AND password_hash = %s",
                (username, hashed_pw)
            )
            user = cursor.fetchone()
            return user
        finally:
            cursor.close()
            conn.close()
    return None

def get_movies():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM Movies ORDER BY release_year DESC, rating DESC")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    return []

def get_showtimes(movie_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Showtimes WHERE movie_id = %s AND available_seats > 0 ORDER BY show_date, show_time",
                (movie_id,)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    return []

def get_booked_seats(showtime_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT seat_numbers FROM Bookings WHERE showtime_id = %s",
                (showtime_id,)
            )
            results = cursor.fetchall()
            booked_seats = []
            for row in results:
                if row['seat_numbers']:
                    booked_seats.extend(row['seat_numbers'].split(','))
            return booked_seats
        finally:
            cursor.close()
            conn.close()
    return []

def book_tickets(user_id, showtime_id, selected_seats):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            num_tickets = len(selected_seats)
            seat_numbers = ','.join(selected_seats)

            cursor.execute(
                "SELECT available_seats FROM Showtimes WHERE showtime_id = %s",
                (showtime_id,)
            )
            result = cursor.fetchone()
            if result and result['available_seats'] >= num_tickets:
                cursor.execute(
                    "INSERT INTO Bookings (user_id, showtime_id, tickets_booked, booking_date, seat_numbers) VALUES (%s, %s, %s, %s, %s)",
                    (user_id, showtime_id, num_tickets, datetime.now(), seat_numbers)
                )
                cursor.execute(
                    "UPDATE Showtimes SET available_seats = available_seats - %s WHERE showtime_id = %s",
                    (num_tickets, showtime_id)
                )
                conn.commit()
                return True
            else:
                st.error("Not enough seats available!")
                return False
        except Exception as e:
            st.error(f"Booking failed: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def get_user_bookings(user_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT b.booking_id, m.title, s.show_date, s.show_time, 
                       b.tickets_booked, b.booking_date, b.seat_numbers
                FROM Bookings b
                JOIN Showtimes s ON b.showtime_id = s.showtime_id
                JOIN Movies m ON s.movie_id = m.movie_id
                WHERE b.user_id = %s
                ORDER BY b.booking_date DESC
            """, (user_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    return []