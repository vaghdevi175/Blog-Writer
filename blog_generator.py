import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="your-openrouter-key-here"
)

def generate_blog_with_llama(prompt, model="meta-llama/llama-4-maverick:free"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Blog generation failed: {e}")
        return "⚠️ Error generating blog content."
