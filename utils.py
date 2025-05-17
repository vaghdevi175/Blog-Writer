from openai import OpenAI
import streamlit.components.v1 as components
import base64
import logging

logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

def generate_blog_with_llama(prompt, model="meta-llama/llama-4-maverick:free"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"OpenRouter error: {e}")
        return "API call failed."

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
