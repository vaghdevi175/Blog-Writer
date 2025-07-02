import openai
import streamlit.components.v1 as components
import base64
import logging
import os
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
import streamlit as st
openai.api_key = st.secrets["OPENROUTER_API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"  
def generate_blog_with_llama(prompt, model="mistralai/mistral-small-3.1-24b-instruct-2503"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = response['choices'][0]['message']['content'].strip()
        return content
    except Exception as e:
        logger.error(f"OpenRouter API Error: {e}")
        return "⚠️ API call failed. Check API key or model name."

def copy_to_clipboard_button(text, button_label="Copy Blog Content"):
    safe_text = text.replace('\\', '\\\\').replace('`', '\\`').replace('\n', '\\n')
    components.html(f"""
        <button id="copy-btn" style="padding:8px 16px;">{button_label}</button>
        <script>
        document.getElementById('copy-btn').onclick = () => {{
            navigator.clipboard.writeText(`{safe_text}`);
            const btn = document.getElementById('copy-btn');
            btn.textContent = 'Copied!';
            setTimeout(() => btn.textContent = '{button_label}', 1500);
        }};
        </script>
    """, height=50)


def get_download_link(text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:text/plain;base64,{b64}" download="{filename}">⬇️ Download {filename}</a>'
