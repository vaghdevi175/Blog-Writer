import openai
import streamlit as st
import streamlit.components.v1 as components
import base64
import logging
import os

# Setup OpenRouter credentials
openai.api_key = st.secrets["OPENROUTER_API_KEY"]
openai.base_url = "https://openrouter.ai/api/v1"  # Note: NOT `api_base` anymore

# Logging setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

# Function to generate blog content
def generate_blog_with_llama(prompt, model="deepseek/deepseek-r1-0528"):
    try:
        client = openai.OpenAI(api_key=openai.api_key, base_url=openai.base_url)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenRouter API Error: {e}")
        return f"⚠️ API call failed. Error: {e}"


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
