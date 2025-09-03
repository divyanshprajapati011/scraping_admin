# # admin_app/admin.py
# import streamlit as st
# import pandas as pd

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import hashlib

# DB_CONFIG = {
        
#         "user":"postgres.fpkyghloouywbxbdmqlp",
#         "password": "@Deep7067",
#         "host": "aws-1-ap-south-1.pooler.supabase.com",
#         "port": "6543",
#         "dbname": "postgres",
#         "sslmode": "require"
# }

# def get_connection():
#     return psycopg2.connect(**DB_CONFIG)

# def hash_password(password: str) -> str:
#     return hashlib.sha256(password.encode()).hexdigest()



# st.set_page_config(page_title="Admin Panel", layout="wide")

# st.subheader("🛠️ Admin Login")
# username = st.text_input("Admin Username")
# password = st.text_input("Admin Password", type="password")

# ADMIN_USER = "admin"
# ADMIN_PASS = "admin123"

# if st.button("Login as Admin"):
#     if username == ADMIN_USER and password == ADMIN_PASS:
#         st.success("✅ Admin logged in")
#         tab1, tab2, tab3 = st.tabs(["Users", "Login History", "Scrape History"])

#         # Users tab
#         with tab1:
#             db = get_connection(); cur = db.cursor()
#             cur.execute("SELECT username, email FROM users ORDER BY username")
#             rows = cur.fetchall()
#             cur.close(); db.close()
#             df_users = pd.DataFrame(rows, columns=["Username", "Email"])
#             st.dataframe(df_users)
#             if not df_users.empty:
#                 st.download_button("⬇️ Download CSV", df_users.to_csv(index=False).encode("utf-8"), file_name="users.csv")
        
#         # Login History tab
#         with tab2:
#             db = get_connection(); cur = db.cursor()
#             cur.execute("""
#                 SELECT u.username, l.login_time, l.ip_address
#                 FROM login_history l
#                 JOIN users u ON u.user_id = l.user_id
#                 ORDER BY l.login_time DESC
#             """)
#             rows = cur.fetchall(); cur.close(); db.close()
#             df_login = pd.DataFrame(rows, columns=["Username", "Login Time", "IP"])
#             st.dataframe(df_login)
#             if not df_login.empty:
#                 st.download_button("⬇️ Download CSV", df_login.to_csv(index=False).encode("utf-8"), file_name="login_history.csv")

#         # Scrape History tab
#         with tab3:
#             db = get_connection(); cur = db.cursor()
#             cur.execute("""
#                 SELECT u.username, s.query, s.results_count, s.created_at
#                 FROM scrape_history s
#                 JOIN users u ON u.user_id = s.user_id
#                 ORDER BY s.created_at DESC
#             """)
#             rows = cur.fetchall(); cur.close(); db.close()
#             df_scrape = pd.DataFrame(rows, columns=["Username", "Query", "Results", "Time"])
#             st.dataframe(df_scrape)
#             if not df_scrape.empty:
#                 st.download_button("⬇️ Download CSV", df_scrape.to_csv(index=False).encode("utf-8"), file_name="scrape_history.csv")
#     else:
#         st.error("❌ Wrong Admin Credentials")



import streamlit as st
import psycopg2
import pandas as pd

# ================== DB CONNECTION ==================
def get_connection():
    return psycopg2.connect(
        user="postgres.fpkyghloouywbxbdmqlp",
        password="@Deep706743",
        host="aws-1-ap-south-1.pooler.supabase.com",
        port="6543",
        dbname="postgres",
        sslmode="require",
    )

# ================== APP CONFIG ==================
st.set_page_config(page_title="Admin Panel 👨‍💼", layout="wide")
st.title("👨‍💼 Admin Dashboard")

# ================== ADMIN AUTH ==================
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"   # 👉 Change this

if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

def admin_login():
    with st.form("admin_login_form"):
        u = st.text_input("Admin Username")
        p = st.text_input("Admin Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if u == ADMIN_USER and p == ADMIN_PASS:
                st.session_state.admin_logged = True
                st.success("✅ Logged in as Admin")
            else:
                st.error("❌ Invalid credentials")

if not st.session_state.admin_logged:
    st.warning("🔒 Please login as Admin")
    admin_login()
    st.stop()

# ================== FETCH TABLE DATA ==================
def fetch_table(query):
    db = get_connection()
    cur = db.cursor()
    cur.execute(query)
    cols = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    cur.close(); db.close()
    return pd.DataFrame(rows, columns=cols)

# ================== ADMIN DASHBOARD ==================
tabs = st.tabs(["👤 Users", "📌 Login History", "🔍 Search History"])
# , "📊 Scraping Results"
with tabs[0]:
    st.subheader("👤 Registered Users")
    df = fetch_table("SELECT user_id, username, email, mobile_number ,created_at FROM users ORDER BY user_id DESC;")
    st.dataframe(df, use_container_width=True)
    st.download_button("⬇ Download Users", df.to_csv(index=False).encode("utf-8"), "users.csv")

with tabs[1]:
    st.subheader("📌 Login History")
    df = fetch_table("SELECT l.id,l.user_id,u.username,l.login_time,l.ip_address FROM login_history l JOIN users u ON l.user_id = u.user_id ORDER BY l.id DESC;")
    st.dataframe(df, use_container_width=True)
    st.download_button("⬇ Download Login History", df.to_csv(index=False).encode("utf-8"), "login_history.csv")

with tabs[2]:
    st.subheader("🔍 Search History")
    df = fetch_table("SELECT l.user_id,u.username,l.query , l.searched_at FROM search_history l JOIN users u ON l.user_id = u.user_id ORDER BY l.id DESC;")
    st.dataframe(df, use_container_width=True)
    st.download_button("⬇ Download Search History", df.to_csv(index=False).encode("utf-8"), "search_history.csv")

# with tabs[3]:
#     st.subheader("📊 Scraping Results")
#     df = fetch_table("SELECT * FROM scraping_results ORDER BY scraped_at DESC;")
#     st.dataframe(df, use_container_width=True)
#     st.download_button("⬇ Download Scraping Results", df.to_csv(index=False).encode("utf-8"), "scraping_results.csv")

# ================== LOGOUT ==================
if st.button("🚪 Logout Admin"):
    st.session_state.admin_logged = False
    st.experimental_rerun()









