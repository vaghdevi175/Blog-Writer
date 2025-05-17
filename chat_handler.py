import streamlit as st
from utils import generate_blog_with_llama
from image_fetcher import fetch_multiple_unsplash_images

def handle_chat(topic, blog_content, blog):
    if "chat_history" not in blog:
        blog["chat_history"] = []

    user_question = st.chat_input("Ask a question about the blog or images...")

    # Normalize old chat formats (if needed)
    normalized_history = []
    for entry in blog["chat_history"]:
        if "role" in entry:
            normalized_history.append(entry)
        elif "user" in entry and "bot" in entry:
            normalized_history += [
                {"role": "user", "content": entry["user"]},
                {"role": "assistant", "content": entry["bot"]}
            ]
    blog["chat_history"] = normalized_history

    # Display chat messages
    for msg in normalized_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_question:
        with st.chat_message("user"):
            st.markdown(user_question)

        wants_images = any(k in user_question.lower() for k in [
            "show image", "generate image", "picture of", "photo", "illustration", "images please"
        ])

        answer = ""
        if wants_images:
            with st.spinner("Fetching images..."):
                images = fetch_multiple_unsplash_images(topic)
                if images:
                    st.markdown("### 🖼️ Here are some images:")
                    for i in range(0, len(images), 3):
                        cols = st.columns(3)
                        for j in range(3):
                            if i + j < len(images):
                                with cols[j]:
                                    st.image(images[i + j], use_container_width=True)
                else:
                    answer = "⚠️ Couldn't find any suitable images."
        else:
            prompt = f"""
You are a helpful assistant. The blog is about **{topic}**.

Here is the blog:
\"\"\"
{blog_content}
\"\"\"

User question: {user_question}
Respond naturally and clearly.
"""
            with st.spinner("Thinking..."):
                answer = generate_blog_with_llama(prompt)

        if answer.strip():
            with st.chat_message("assistant"):
                st.markdown(answer)
            blog["chat_history"].append({"role": "user", "content": user_question})
            blog["chat_history"].append({"role": "assistant", "content": answer})

        if wants_images:
            st.rerun()
