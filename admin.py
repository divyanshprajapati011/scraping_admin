# admin_app/admin.py
import streamlit as st
import pandas as pd
from Shared.db import get_connection

st.set_page_config(page_title="Admin Panel", layout="wide")

st.subheader("🛠️ Admin Login")
username = st.text_input("Admin Username")
password = st.text_input("Admin Password", type="password")

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

if st.button("Login as Admin"):
    if username == ADMIN_USER and password == ADMIN_PASS:
        st.success("✅ Admin logged in")
        tab1, tab2, tab3 = st.tabs(["Users", "Login History", "Scrape History"])

        # Users tab
        with tab1:
            db = get_connection(); cur = db.cursor()
            cur.execute("SELECT username, email FROM users ORDER BY username")
            rows = cur.fetchall()
            cur.close(); db.close()
            df_users = pd.DataFrame(rows, columns=["Username", "Email"])
            st.dataframe(df_users)
            if not df_users.empty:
                st.download_button("⬇️ Download CSV", df_users.to_csv(index=False).encode("utf-8"), file_name="users.csv")
        
        # Login History tab
        with tab2:
            db = get_connection(); cur = db.cursor()
            cur.execute("""
                SELECT u.username, l.login_time, l.ip_address
                FROM login_history l
                JOIN users u ON u.user_id = l.user_id
                ORDER BY l.login_time DESC
            """)
            rows = cur.fetchall(); cur.close(); db.close()
            df_login = pd.DataFrame(rows, columns=["Username", "Login Time", "IP"])
            st.dataframe(df_login)
            if not df_login.empty:
                st.download_button("⬇️ Download CSV", df_login.to_csv(index=False).encode("utf-8"), file_name="login_history.csv")

        # Scrape History tab
        with tab3:
            db = get_connection(); cur = db.cursor()
            cur.execute("""
                SELECT u.username, s.query, s.results_count, s.created_at
                FROM scrape_history s
                JOIN users u ON u.user_id = s.user_id
                ORDER BY s.created_at DESC
            """)
            rows = cur.fetchall(); cur.close(); db.close()
            df_scrape = pd.DataFrame(rows, columns=["Username", "Query", "Results", "Time"])
            st.dataframe(df_scrape)
            if not df_scrape.empty:
                st.download_button("⬇️ Download CSV", df_scrape.to_csv(index=False).encode("utf-8"), file_name="scrape_history.csv")
    else:
        st.error("❌ Wrong Admin Credentials")
