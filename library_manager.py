import streamlit as st
import pandas as pd

# Dark Mode Toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # Default to dark mode

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Custom CSS for Dark and Light Mode
dark_mode_css = """
    <style>
        body {
            background-color: #1e1e1e;
            color: #E0E0E0;
            font-family: 'Arial', sans-serif;
        }
        .main {
            background-color: #222222;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
        }
        h1, h2, h3 {
            color: #FFCC00;
        }
        .stButton>button {
            background-color: #444444;
            color: #E0E0E0;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #555555;
            transform: scale(1.05);
        }
        /* Fixing Input & Select Colors */
        .stTextInput input, .stSelectbox select {
            background-color: white;
            color: black !important;  /* White text for dark mode */
            border: 2px solid #FFD700;
        }
    </style>
"""

light_mode_css = """
    <style>
        body {
            background-color: #f5f5f5;
            color: #000;
            font-family: 'Arial', sans-serif;
        }
        .main {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        h1, h2, h3 {
            color: #333;
        }
        .stButton>button {
            background-color: #dddddd;
            color: #000;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #bbbbbb;
            transform: scale(1.05);
        }
        /* Fixing Input & Select Colors */
        .stTextInput input, .stSelectbox select {
            background-color: #ffffff;
            color: black !important; /* Black text for light mode */
            border: 2px solid #555;
        }
    </style>
"""

# Apply the correct CSS based on dark mode
st.markdown(dark_mode_css if st.session_state.dark_mode else light_mode_css, unsafe_allow_html=True)

# Toggle Button for Dark Mode
st.sidebar.button("🌙 Toggle Dark Mode" if st.session_state.dark_mode else "☀️ Toggle Light Mode", on_click=toggle_dark_mode)

# Initialize library data
if 'books' not in st.session_state:
    st.session_state.books = pd.DataFrame(columns=["Title", "Author", "Year", "Status", "Genre", "Language", "Rating"])

# Book functions
def add_book(title, author, year, status, genre, language, rating):
    new_book = pd.DataFrame([[title, author, year, status, genre, language, rating]], 
                            columns=["Title", "Author", "Year", "Status", "Genre", "Language", "Rating"])
    st.session_state.books = pd.concat([st.session_state.books, new_book], ignore_index=True)

def remove_book(title):
    st.session_state.books = st.session_state.books[st.session_state.books['Title'] != title]

def search_books(query):
    return st.session_state.books[st.session_state.books['Title'].str.contains(query, case=False) |
                                   st.session_state.books['Author'].str.contains(query, case=False)]

def display_stats():
    total_books = len(st.session_state.books)
    read_books = len(st.session_state.books[st.session_state.books['Status'] == 'Read'])
    read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0

    st.write(f"📚 Total Books: **{total_books}**")
    st.write(f"✅ Read Books: **{read_books}** ({read_percentage:.2f}%)")

# Streamlit UI
def library_app():
    st.title("📚 Personal Library Manager")
    
    menu = ["🏠 Home", "➕ Add a Book", "❌ Remove a Book", "🔍 Search for a Book", "📊 Display Stats", "🚪 Exit"]
    choice = st.sidebar.selectbox("📌 Menu", menu)

    if choice == "🏠 Home":
        st.markdown("### 📖 Welcome to your Personal Library!")
        st.write("Manage your books effortlessly!")

    elif choice == "➕ Add a Book":
        st.markdown("### ➕ Add a New Book")
        title = st.text_input("📕 Book Title")
        author = st.text_input("✍️ Author")
        year = st.text_input("📅 Year")
        status = st.selectbox("📌 Status", ["Unread", "Read"])
        genre = st.text_input("📚 Genre (e.g. Fiction, Non-Fiction, Fantasy)")
        language = st.text_input("🌍 Language (e.g. English, Spanish)")
        rating = st.slider("⭐ Rating", min_value=1, max_value=5, step=1)

        if st.button("✅ Add Book"):
            if title and author and year and genre and language:
                add_book(title, author, year, status, genre, language, rating)
                st.success(f"✅ Book **'{title}'** added successfully!")
            else:
                st.error("❌ Please provide all details to add a book.")

    elif choice == "❌ Remove a Book":
        st.markdown("### ❌ Remove a Book")
        title = st.text_input("Enter the Title of the Book to Remove")

        if st.button("🗑 Remove Book"):
            if title in st.session_state.books['Title'].values:
                remove_book(title)
                st.success(f"✅ Book **'{title}'** removed successfully!")
            else:
                st.error("❌ Book not found.")

    elif choice == "🔍 Search for a Book":
        st.markdown("### 🔍 Search for a Book")
        query = st.text_input("Enter Book Title or Author to Search")

        if query:
            search_result = search_books(query)
            if not search_result.empty:
                for _, row in search_result.iterrows():
                    st.markdown(f"📖 **{row['Title']}**")
                    st.write(f"✍️ Author: {row['Author']}")
                    st.write(f"📅 Year: {row['Year']}")
                    st.write(f"📌 Status: {row['Status']}")
                    st.write(f"📚 Genre: {row['Genre']}")
                    st.write(f"🌍 Language: {row['Language']}")
                    st.write(f"⭐ Rating: {row['Rating']}")
                    st.markdown("---")
            else:
                st.write("❌ No books found matching your search.")

    elif choice == "📊 Display Stats":
        st.markdown("### 📊 Library Stats")
        display_stats()

    elif choice == "🚪 Exit":
        st.write("👋 Exiting... Thank you for using the Library Manager!")
        st.stop()

if __name__ == "__main__":
    with st.container():
        library_app()
