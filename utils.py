import base64
import streamlit as st
import streamlit.components.v1 as components

def copy_to_clipboard_button(text, label="Copy Blog"):
    safe_text = text.replace('\\', '\\\\').replace('`', '\\`').replace('\n', '\\n')
    components.html(f"""
    <button id="copy-btn">{label}</button>
    <script>
    const btn = document.getElementById('copy-btn');
    btn.onclick = () => {{
        navigator.clipboard.writeText(`{safe_text}`);
        btn.textContent = 'Copied!';
        setTimeout(() => btn.textContent = '{label}', 1500);
    }};
    </script>
    """, height=40)

def get_download_link(text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:text/plain;base64,{b64}" download="{filename}">Download {filename}</a>'
