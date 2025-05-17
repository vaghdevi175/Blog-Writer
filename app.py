import streamlit as st
from blog_generator import generate_blog_with_llama
from image_fetcher import fetch_multiple_unsplash_images
from chat_handler import handle_user_question
from utils import copy_to_clipboard_button, get_download_link

# Session state defaults
for key, default in {
    "page": "main",
    "history": [],
    "topic": "",
    "tone": "",
    "blog": "",
    "image_urls": [],
    "current_blog_idx": None,
    "chat_history": [],
    "show_more_images": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

def show_main_page():
    st.title("📝 Blog Writer")
    st.markdown("Enter a topic and tone to generate a blog post with related images.")

    with st.form("blog_form"):
        topic = st.text_input("Enter blog topic")
        tone = st.selectbox("Select tone", ["", "Professional", "Friendly", "Persuasive", "Witty"])
        submitted = st.form_submit_button("Generate Blog")

        if submitted:
            if not topic or not tone:
                st.error("Please fill both fields.")
            else:
                st.session_state.topic = topic
                st.session_state.tone = tone
                with st.spinner("Generating blog..."):
                    prompt = f"Write a {tone.lower()} blog post about: {topic}"
                    blog = generate_blog_with_llama(prompt)
                    st.session_state.history.append({
                        "topic": topic, "tone": tone, "content": blog, "images": []
                    })
                    st.session_state.current_blog_idx = len(st.session_state.history) - 1
                    st.session_state.page = "detail"
                    st.rerun()

    st.markdown("### 📚 Recent Blogs")
    if not st.session_state.history:
        st.info("No blogs yet.")
        return

    for idx, blog in enumerate(st.session_state.history):
        st.markdown(f"**{blog['topic']}** _(Tone: {blog['tone']})_")
        if st.button(f"Read Blog {idx+1}", key=f"read_{idx}"):
            st.session_state.current_blog_idx = idx
            st.session_state.page = "detail"
            st.rerun()

def show_blog_detail():
    idx = st.session_state.current_blog_idx
    if idx is None:
        st.error("No blog selected.")
        return

    blog = st.session_state.history[idx]
    st.button("⬅️ Back", on_click=lambda: st.session_state.update({"page": "main"}))

    st.markdown(f"### 📰 {blog['topic']} ({blog['tone']})")
    copy_to_clipboard_button(blog["content"])
    st.markdown(blog["content"])

    download_format = st.selectbox("Download format", [".txt", ".md"])
    filename = f"{blog['topic']}{download_format}"
    st.download_button("⬇️ Download Blog", blog["content"], file_name=filename)

    if st.button("Generate Related Images"):
        with st.spinner("Fetching images..."):
            imgs = fetch_multiple_unsplash_images(blog["topic"])
            st.session_state.history[idx]["images"] = imgs
            st.rerun()

    if blog["images"]:
        st.markdown("### 🖼️ Related Images")
        for img_url in blog["images"]:
            st.image(img_url, use_column_width=True)

    # Chat Q&A
    user_question = st.chat_input("Ask about this blog...")
    if user_question:
        response = handle_user_question(blog["topic"], blog["content"], user_question)
        with st.chat_message("user"):
            st.markdown(user_question)
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.chat_history.extend([
            {"role": "user", "content": user_question},
            {"role": "assistant", "content": response}
        ])

# Entry Point
def main():
    if st.session_state.page == "main":
        show_main_page()
    elif st.session_state.page == "detail":
        show_blog_detail()

if __name__ == "__main__":
    main()
