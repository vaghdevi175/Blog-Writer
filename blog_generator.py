import streamlit as st
import requests
from image_fetcher import fetch_multiple_unsplash_images
from utils import generate_blog_with_llama, copy_to_clipboard_button
from chat_handler import handle_chat

def show_main_page():
    st.title("Blog Writer")
    st.markdown("Enter a topic and select a tone to generate a blog post with related images.")

    with st.form("blog_form"):
        topic = st.text_input("Enter blog topic")
        tone = st.selectbox("Select tone", ["", "Professional", "Friendly", "Persuasive", "Witty"], index=0)
        submitted = st.form_submit_button("Generate Blog")

         if submitted:
            if not topic.strip():
                st.error("Please enter a blog topic.")
            elif not tone.strip():
                st.error("Please select a tone.")
            else:
                st.session_state.topic = topic
                st.session_state.tone = tone
                with st.spinner("Generating blog..."):
                    prompt = f"""
                    Write a detailed {tone.lower()} blog post about "{topic}".
                    The blog should include:
                    1. An engaging introduction.
                    2. 2-3 subheadings covering important aspects of the topic.
                    3. A conclusion.
                    Make it conversational and interesting, around 500-700 words.
                    """
                    blog = generate_blog_with_llama(prompt)
                    st.session_state.history.append({
                        "topic": topic,
                        "tone": tone,
                        "content": blog,
                        "images": [],
                        "chat_history": []
                    })
                    st.session_state.current_blog_idx = len(st.session_state.history) - 1
                    st.session_state.page = "detail"
                    st.rerun()

    st.markdown("---")
    st.subheader("Recent Blogs")

    if not st.session_state.history:
        st.info("No blogs generated yet.")
        return

    for i in range(0, len(st.session_state.history), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < len(st.session_state.history):
                blog = st.session_state.history[idx]
                with cols[j]:
                    st.markdown(
                        f"""
                        <div style="border: 1px solid #ccc; border-radius: 10px; padding: 12px;
                        background-color: #fdfdfd; height:100px; display: flex; flex-direction: column;
                        justify-content: space-between; box-shadow: 1px 1px 5px rgba(0,0,0,0.05);">
                            <div>
                                <h5 style="margin-bottom: 8px;">{blog['topic']}</h5>
                                <p style="color: #888;">Tone: {blog['tone']}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True,
                    )
                    if st.button("Read More", key=f"readmore_{idx}"):
                        st.session_state.current_blog_idx = idx
                        st.session_state.page = "detail"
                        st.rerun()


def show_blog_detail():
    idx = st.session_state.current_blog_idx
    if idx is None or idx < 0 or idx >= len(st.session_state.history):
        st.error("Invalid blog index.")
        return

    blog = st.session_state.history[idx]
    topic = blog["topic"]
    tone = blog["tone"]
    content = blog["content"]
    images = blog.get("images", [])

    if st.button("⬅ Back"):
        st.session_state.page = "main"
        st.session_state.show_more_images = False
        st.session_state.topic = ""
        st.rerun()

    copy_to_clipboard_button(content)

    # Format content for title
    lines = content.splitlines()
    new_content_lines = []
    replaced_main_title = False

    for line in lines:
        if not replaced_main_title and line.startswith("**") and line.endswith("**"):
            new_content_lines.append(f'<h2 style="font-weight:bold;">{line[2:-2].strip()}</h2>')
            replaced_main_title = True
        else:
            new_content_lines.append(line)

    st.markdown("\n".join(new_content_lines), unsafe_allow_html=True)

    download_format = st.selectbox("Download blog as:", [".txt", ".md"], index=0)
    filename = f"{topic}{download_format}"
    st.download_button(" Download Blog", data=content, file_name=filename, mime="text/plain")

    if st.button("Generate Related Images"):
        with st.spinner("Fetching images..."):
            imgs = fetch_multiple_unsplash_images(topic)
            st.session_state.history[idx]["images"] = imgs
            st.rerun()

    if images:
        st.markdown("### Related Images")
        for i in range(0, len(images), 3):
            cols = st.columns(3)
            for j in range(3):
                img_idx = i + j
                if img_idx < len(images):
                    with cols[j]:
                        st.image(images[img_idx], use_container_width=True)
                        st.download_button(
                            f"Download Image {img_idx+1}",
                            data=requests.get(images[img_idx]).content,
                            file_name=f"image_{img_idx+1}.jpg",
                            mime="image/jpeg",
                            key=f"download_img_{img_idx}"
                        )

    # Pass blog-specific chat history to chat handler
    handle_chat(topic, content, blog)
