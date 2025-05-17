from blog_generator import generate_blog_with_llama

def handle_user_question(topic, blog_content, question):
    prompt = f"""
You're a helpful assistant. Answer this question about the topic "{topic}".

Blog content:
\"\"\"
{blog_content}
\"\"\"

Question:
{question}
"""
    return generate_blog_with_llama(prompt)
