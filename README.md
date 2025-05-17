# Streamlit Blog Generator App

This is a Streamlit-based blog generator app powered by **OpenRouter's LLaMA model** and **Unsplash API**. It enables users to generate blog posts based on a topic and tone, view related images, engage in Q&A with the blog, and download the generated content.

---

## Features

-  Blog generation using OpenRouter's LLaMA API
-  Image fetching from Unsplash
-  Chat with AI about the blog content
-  Copy blog to clipboard
-  Download blog as `.txt` or `.md`
-  Save and view previous blogs in session
-  Clean and responsive Streamlit UI

---

## Tech Stack

- [Streamlit](https://streamlit.io/)
- [OpenRouter (LLaMA API)](https://openrouter.ai/)
- [Unsplash API](https://unsplash.com/developers)
- Python, `requests`, `dotenv`, `uuid`, `PIL`, `streamlit_chat`

---

##  Setup Instructions (Run Locally)

### 1. Clone the repository

git clone https://github.com/your-username/streamlit-blog-generator.git
cd streamlit-blog-generator

### 2. Install dependencies
pip install -r requirements.txt

### 3.Add API keys
Create a .env file in the root folder and add your keys:

OPENROUTER_API_KEY=your-openrouter-key-here

UNSPLASH_API_KEY=your-unsplash-key-here

### 4. Run the app
streamlit run app.py

## Deploy on Streamlit Cloud
1.Push your code to a GitHub repository.

2.Go to Streamlit Cloud.

3.Click “New App” and select your GitHub repo.

4.In Advanced Settings, set the following environment variables:

    OPENROUTER_API_KEY
  
    UNSPLASH_API_KEY
  
5.Click Deploy!

## How to use this:

- Enter a topic like "Artificial Intelligence" and select a tone such as "Professional".
- Click Generate Blog to create content.
- Optionally, generate related images and ask the AI questions about the blog.
- Copy the blog or download it in .txt or .md format.

