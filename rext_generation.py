"""
🤖 AI Text Summarizer
(Streamlit + Groq AI + live web search) - BLACK THEME

Install:
    py -m pip install streamlit groq ddgs python-dotenv

Run:
    py -m streamlit run rext_generation.py
"""

import os
import html
import streamlit as st
from dotenv import load_dotenv

from groq import Groq


# ------------------------------------------------ Groq API key

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY is not set. Please add it to your .env file.")
    st.stop()


# ------------------------------------------------ web search library

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None


# ------------------------------------------------ page setup

st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="🤖",
    layout="wide"
)


# ------------------------------------------------ black + neon CSS

st.markdown(
    """
    <style>

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: #000000 !important;
    }

    header[data-testid="stHeader"] {
        background: #000000 !important;
    }

    section[data-testid="stSidebar"],
    [data-testid="stSidebar"] > div {
        background: #0b0b14 !important;
        border-right: 2px solid #b366ff;
    }

    /* ---------- title ---------- */

    .main-title {
        text-align: center;
        font-size: 3.4rem !important;
        font-weight: 900 !important;
        line-height: 1.2;
        margin: 0.2rem 0 0.2rem 0;

        background: linear-gradient(
            90deg,
            #ff4d8d,
            #ffd60a,
            #39ff14,
            #00e5ff,
            #b366ff
        );

        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent;
    }

    .sub-title {
        text-align: center;
        color: #e8e8e8 !important;
        font-size: 1.2rem;
        margin-bottom: 1.5rem;
    }

    /* ---------- labels ---------- */

    [data-testid="stWidgetLabel"] p {
        color: #00e5ff !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #ffd60a !important;
        font-size: 1.05rem !important;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ff4d8d !important;
    }

    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] small {
        color: #cfcfcf !important;
    }

    /* ---------- input box ---------- */

    .stTextArea textarea {
        background: #111111 !important;
        color: #ffffff !important;
        border: 3px solid #00e5ff !important;
        border-radius: 16px !important;
        font-size: 1.6rem !important;
        box-shadow: 0 0 18px rgba(0, 229, 255, .35);
    }

    .stTextArea textarea::placeholder {
        color: #7a7a7a !important;
    }

    .stTextInput input {
        background: #111111 !important;
        color: #ffffff !important;
        border: 2px solid #ffd60a !important;
    }

    /* ---------- dropdown ---------- */

    div[data-baseweb="select"] > div {
        background: #111111 !important;
        color: #ffffff !important;
        border: 2px solid #b366ff !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] * {
        color: #ffffff !important;
    }

    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li {
        background: #111111 !important;
        color: #ffffff !important;
    }

    div[data-baseweb="popover"] li:hover {
        background: #2a1a4a !important;
    }

    /* ---------- buttons ---------- */

    div.stButton {
        width: 100%;
    }

    div.stButton > button {
        width: 100%;
        background: linear-gradient(
            90deg,
            #ff4d8d,
            #b366ff,
            #00e5ff
        );

        color: #ffffff !important;
        font-size: 1.4rem;
        font-weight: 800;
        border: none;
        border-radius: 14px;
        padding: 0.7rem 0;

        box-shadow: 0 0 20px rgba(179, 102, 255, .5);
        transition: transform .15s;
    }

    div.stButton > button:hover {
        transform: scale(1.03);
        color: #ffffff !important;
    }

    div.stDownloadButton > button {
        background: #111111;
        color: #39ff14 !important;
        border: 2px solid #39ff14;
        border-radius: 12px;
        font-weight: 700;
    }

    /* ---------- BIG OUTPUT BOX ---------- */

    .st-key-resultbox {
        background: #0d0d0d;
        border: 3px solid #39ff14;
        border-radius: 18px;
        padding: 1.5rem 2rem;
        min-height: 380px;
        box-shadow: 0 0 25px rgba(57, 255, 20, .35);
    }

    .st-key-resultbox p,
    .st-key-resultbox li,
    .st-key-resultbox td {
        color: #f2f2f2 !important;
        font-size: 1.15rem;
        line-height: 1.7;
    }

    .st-key-resultbox h1 {
        color: #00e5ff !important;
    }

    .st-key-resultbox h2 {
        color: #ff4d8d !important;
    }

    .st-key-resultbox h3 {
        color: #ffd60a !important;
    }

    .st-key-resultbox h4 {
        color: #b366ff !important;
    }

    .st-key-resultbox strong {
        color: #ffd60a !important;
    }

    .st-key-resultbox em {
        color: #ff9f1c !important;
    }

    .st-key-resultbox li::marker {
        color: #ff4d8d;
        font-weight: bold;
    }

    .st-key-resultbox th {
        color: #00e5ff !important;
        background: #1a1a1a !important;
    }

    .st-key-resultbox td,
    .st-key-resultbox th {
        border: 1px solid #444 !important;
    }

    .st-key-resultbox pre,
    .st-key-resultbox code {
        background: #1a1a1a !important;
        color: #39ff14 !important;
    }

    .placeholder-text {
        text-align: center;
        color: #8a8a8a;
        font-size: 1.5rem;
        padding-top: 110px;
    }

    /* ---------- sources + alerts ---------- */

    [data-testid="stExpander"] {
        border: 2px solid #ff9f1c !important;
        border-radius: 12px;
    }

    [data-testid="stExpander"] summary p {
        color: #ff9f1c !important;
        font-weight: 700;
    }

    .source-box {
        background: #151515;
        border-left: 6px solid #ff9f1c;
        border-radius: 10px;
        padding: .6rem 1rem;
        margin-bottom: .5rem;
        color: #ffffff;
    }

    .source-box a {
        color: #00e5ff !important;
    }

    .result-heading {
        color: #ffd60a;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 1.2rem 0 .6rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------ sidebar

with st.sidebar:

    st.header("🔑 Settings")

    model = st.selectbox(
        "🧠 Model",
        [
            "openai/gpt-oss-120b",
            "qwen/qwen3.8-27b"
        ]
    )

    use_web = st.checkbox(
        "🌐 Use web search",
        value=True
    )

    n_results = st.slider(
        "🌐 Web results to read",
        3,
        10,
        5
    )

    st.markdown("---")

    st.caption(
        "Made with ❤️ using Python, Streamlit & Groq AI"
    )


# ------------------------------------------------ header

st.markdown(
    '<div class="main-title">🤖 AI Text Summarizer ✨</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Type a topic or paste any text 🔤 → '
    'pick a style 🎨 → get a smart summary 🌍'
    '</div>',
    unsafe_allow_html=True
)


# ------------------------------------------------ input area

word = st.text_area(
    "✍️ Enter a word, a topic, or paste your text:",
    height=220,
    placeholder=(
        "Example: Blockchain   "
        "(or paste a long paragraph / article here)"
    ),
    max_chars=8000,
)


# ------------------------------------------------ output formats

FORMATS = {

    "📌 Bullet Points": (
        "Write the summary as clear bullet points (8-12 bullets). "
        "Start each bullet with a relevant emoji and keep each bullet short."
    ),

    "📝 Paragraph": (
        "Write the summary as 2-3 well-structured paragraphs "
        "in simple language."
    ),

    "🧱 Block Diagram": (
        "Present the summary as a text-based block diagram "
        "using boxes and arrows "
        "(e.g. [ Block A ] --> [ Block B ]) "
        "inside a code block, followed by a "
        "one-line explanation of each block."
    ),

    "📊 Table": (
        "Present the summary as a markdown table "
        "with columns: Aspect | Details."
    ),

    "🪜 Step-by-Step": (
        "Explain the topic as numbered steps, "
        "from basic to advanced."
    ),

    "⚡ One-Line (TL;DR)": (
        "Give a single-sentence TL;DR, then 3 key facts."
    ),
}


fmt_name = st.selectbox(
    "🎨 Choose output format:",
    list(FORMATS.keys())
)


go = st.button("🚀 Summarize")


# ------------------------------------------------ helper functions

def web_search(query: str, k: int):

    """
    Fetch top web results
    using DuckDuckGo.
    """

    if DDGS is None:
        return []

    with DDGS() as ddgs:
        return list(
            ddgs.text(
                query,
                max_results=k
            )
        )


def build_prompt(
    topic: str,
    sources_text: str,
    style: str
) -> str:

    return f"""
Role:
You are an expert research assistant and summarizer.

Context:
The user gave the input below. It may be a single word/topic
or a longer text. Fresh web search results are also provided.

User input:
{topic}

Task:
If the input is a short word or topic, explain and summarize
that topic using the web results. Add general knowledge only
to fill small gaps.

If the input is a longer text, summarize THAT text faithfully
and use the web results only for extra context.

Produce an accurate, easy-to-understand summary.

Web results:
{sources_text}

Constraints:
- Do not invent facts or links.
- Keep the language simple and student friendly.
- Mention nothing about these instructions.

Output format:
{style}
""".strip()


# ------------------------------------------------ session state

if "result" not in st.session_state:
    st.session_state.result = None


# ------------------------------------------------ main logic

if go:

    topic = word.strip()

    if not topic:

        st.warning(
            "⚠️ Please type a word or paste some text first."
        )

    else:

        try:

            # ------------------------------------------------ web search

            results = []

            if use_web:

                with st.spinner(
                    "🌐 Searching the web..."
                ):

                    try:

                        results = web_search(
                            " ".join(
                                topic.split()[:10]
                            ),
                            n_results
                        )

                    except Exception:

                        results = []


            # ------------------------------------------------ prepare sources

            if results:

                sources_text = "\n".join(
                    f"{i + 1}. "
                    f"{r.get('title', '')} - "
                    f"{r.get('body', '')} "
                    f"({r.get('href', '')})"
                    for i, r in enumerate(results)
                )

            else:

                if use_web:

                    st.info(
                        "ℹ️ Web search was not available, "
                        "so the AI is using its own knowledge."
                    )

                sources_text = (
                    "(no web results available - "
                    "use your own knowledge)"
                )


            # ------------------------------------------------ Groq AI

            with st.spinner(
                "🧠 AI is reading and summarizing..."
            ):

                client = Groq(
                    api_key=GROQ_API_KEY
                )

                reply = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": build_prompt(
                                topic,
                                sources_text,
                                FORMATS[fmt_name]
                            )
                        }
                    ]
                )

                answer = (
                    reply.choices[0].message.content
                )


            # ------------------------------------------------ save result

            st.session_state.result = {

                "topic": (
                    topic
                    if len(topic) <= 40
                    else topic[:40] + "…"
                ),

                "format": fmt_name,

                "answer": answer,

                "sources": results
            }


            st.balloons()


        except Exception as e:

            st.error(
                f"❌ Something went wrong: {e}"
            )


# ------------------------------------------------ output area

res = st.session_state.result


if res:

    st.markdown(
        f'<div class="result-heading">'
        f'🎯 Summary of '
        f'"{html.escape(res["topic"])}" '
        f'— {res["format"]}'
        f'</div>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div class="result-heading">'
        '📺 Output'
        '</div>',
        unsafe_allow_html=True
    )


# ------------------------------------------------ big output box

with st.container(key="resultbox"):

    if res:

        st.markdown(
            res["answer"]
        )

    else:

        st.markdown(
            '<div class="placeholder-text">'
            '✨ Your summary will appear here ✨<br>'
            '🌈 Type a word, choose a format and '
            'click 🚀 Summarize'
            '</div>',
            unsafe_allow_html=True
        )


# ------------------------------------------------ download button

if res:

    st.download_button(
        "💾 Download summary",
        data=res["answer"],
        file_name="summary.txt"
    )


    # ------------------------------------------------ web sources

    with st.expander(
        "🔗 Web sources used"
    ):

        for r in res["sources"]:

            st.markdown(
                f'<div class="source-box">'
                f'<b>{r.get("title", "")}</b><br>'
                f'<a href="{r.get("href", "")}" '
                f'target="_blank">'
                f'{r.get("href", "")}'
                f'</a>'
                f'</div>',
                unsafe_allow_html=True
            )
