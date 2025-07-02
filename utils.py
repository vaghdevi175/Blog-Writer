from openai import OpenAI
import streamlit.components.v1 as components
import base64
import logging
logging.basicConfig(level=logging.ERROR) 
logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR-OPEN-API-KEY",
)

def generate_blog_with_llama(prompt, model="mistralai/mistral-small-3.1-24b-instruct-2503"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        if response and response.choices:
            message = response.choices[0].message
            content = message.content.strip() if hasattr(message, 'content') else message["content"].strip()
            return content
        else:
            logger.error("No choices returned from API.")
            return "⚠️ No response from the API."
    except Exception as e:
        logger.error(f"OpenRouter error: {e}")
        return "⚠️ API call failed."


def copy_to_clipboard_button(text, button_label="Copy Blog Content"):
    safe_text = text.replace('\\', '\\\\').replace('`', '\\`').replace('\n', '\\n')
    components.html(f"""
        <button id="copy-btn" style="padding:8px 16px; font-size:16px;">{button_label}</button>
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
