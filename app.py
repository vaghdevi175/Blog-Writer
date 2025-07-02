import streamlit as st
from blog_generator import show_main_page, show_blog_detail

# Initialize session state
default_state = {
    "page": "main",
    "history": [],
    "topic": "",
    "tone": "",
    "current_blog_idx": None,
    "chat_history": [],
}

for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Routing
def main():
    if st.session_state.page == "main":
        show_main_page()
    elif st.session_state.page == "detail":
        show_blog_detail()
    else:
        st.error("Unknown page.")

if __name__ == "__main__":
    main()
