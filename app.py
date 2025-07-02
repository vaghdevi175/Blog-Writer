import streamlit as st
from blog_generator import show_main_page, show_blog_detail

# ---------- Session State Initialization ----------
default_state = {
    "page": "main",
    "history": [],
    "topic": "",
    "tone": "",
    "blog": "",
    "image_urls": [],
    "current_blog_idx": None,
    "chat_history": [],
    "show_more_images": False,
}

for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- Page Routing ----------
def main():
    if st.session_state.page == "main":
        show_main_page()
    elif st.session_state.page == "detail":
        show_blog_detail()
    else:
        st.error("Unknown page.")

if __name__ == "__main__":
    main()
