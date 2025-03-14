import streamlit as st
import pandas as pd
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        author TEXT,
                        genre TEXT,
                        file_link TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Load library data from local database
def load_library():
    conn = sqlite3.connect("library.db")
    df = pd.read_sql("SELECT * FROM books", conn)
    conn.close()
    return df

# Save book data to local database
def save_book(title, author, genre, file_link):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, genre, file_link) VALUES (?, ?, ?, ?)",
                   (title, author, genre, file_link))
    conn.commit()
    conn.close()

# Remove book from local database
def remove_book(title):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE title = ?", (title,))
    conn.commit()
    conn.close()

# Streamlit UI
st.set_page_config(page_title="Personal Library Manager", layout="wide")

st.sidebar.title("📚 Library Menu")
menu = st.sidebar.radio("Select an option", ["View Books", "Add Book", "Remove Book", "Refresh Data"])

df = pd.DataFrame()  # Empty dataframe initially

if menu == "Refresh Data" or st.sidebar.button("🔄 Refresh Library Data"):
    df = load_library()
    st.success("Library data refreshed manually!")

st.title("📚 Personal Library Manager")

if menu == "View Books":
    st.subheader("📖 Your Library")
    if df.empty:
        st.info("No books added yet! Click 'Refresh Data' to update.")
    else:
        st.dataframe(df)
        selected_book = st.selectbox("Select a book to view/download", df["title"].tolist())
        file_link = df[df["title"] == selected_book]["file_link"].values[0]
        if st.button("Open Book PDF"):
            st.markdown(f"[Click here to open]({file_link})")

elif menu == "Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    file_link = st.text_input("Enter Local File Path / Online PDF Link")
    
    if st.button("Add Book"):
        if title and author and genre and file_link:
            save_book(title, author, genre, file_link)
            st.success(f"Book '{title}' added successfully! Click 'Refresh Data' to update the list.")
        else:
            st.error("Please fill all fields.")

elif menu == "Remove Book":
    st.subheader("🗑️ Remove a Book")
    if df.empty:
        st.info("No books available to remove. Click 'Refresh Data' to update.")
    else:
        book_to_remove = st.selectbox("Select a book to remove", df["title"].tolist())
        if st.button("Remove Book"):
            remove_book(book_to_remove)
            st.success(f"Book '{book_to_remove}' removed successfully! Click 'Refresh Data' to update the list.")
