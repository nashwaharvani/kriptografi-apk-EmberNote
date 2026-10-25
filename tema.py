"""Tema visual game-mobile EmberNote."""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&display=swap');

:root { font-family: "Fredoka", "Trebuchet MS", sans-serif; }
.stApp {
  background:
    radial-gradient(ellipse at 8% 12%, rgba(152, 91, 216, .35), transparent 38%),
    radial-gradient(ellipse at 92% 38%, rgba(105, 54, 159, .35), transparent 42%),
    linear-gradient(145deg, #2B1055 0%, #351263 52%, #241044 100%);
  background-attachment: fixed;
}
html, body, [class*="css"] { font-family: "Fredoka", "Trebuchet MS", sans-serif; }
.block-container { padding-top: 1.5rem; max-width: 900px; }
.en-navbar-brand {
  display: flex; align-items: baseline; justify-content: space-between; gap: .75rem;
  padding: .65rem 1rem; margin: 0 0 .5rem; color: #fff;
  border: 3px solid rgba(246,169,242,.6); border-radius: 20px;
  background: linear-gradient(110deg, rgba(82,35,130,.92), rgba(43,16,85,.94));
  box-shadow: inset 0 2px 0 rgba(255,255,255,.12), 0 4px 0 #1c0b39;
}
.en-navbar-brand strong { font-size: 1.3rem; font-weight: 700; }
.en-navbar-brand span { color: #f7dff8; font-size: .92rem; }
div[data-testid="stSidebar"] { display: none; }
div[data-testid="stRadio"] > div[role="radiogroup"] {
  display: flex; flex-direction: row; flex-wrap: wrap; gap: .35rem;
  padding: .55rem; border: 3px solid #35135e; border-radius: 20px;
  background: linear-gradient(180deg, #ffe1ff 0%, #f6a9f2 45%, #e987eb 100%);
  box-shadow: inset 0 3px 0 rgba(255,255,255,.8), 0 4px 0 #1c0b39;
}
div[data-testid="stRadio"] label {
  margin: 0 !important; padding: .45rem .7rem !important;
  border: 2px solid transparent; border-radius: 999px;
  color: #35135e !important; font-weight: 600;
}
div[data-testid="stRadio"] label:has(input:checked) {
  color: #fff !important; border-color: #35135e;
  background: linear-gradient(180deg, #60308b, #35135e);
  box-shadow: inset 0 2px 0 rgba(255,255,255,.2), 0 2px 0 #1c0b39;
}
[data-testid="stHeading"] h1 {
  display: inline-block; margin: .25rem 0 1rem; padding: .35rem 1.1rem;
  color: #fff; font-weight: 700; -webkit-text-stroke: 1px #35135e;
  paint-order: stroke fill; text-shadow: 0 3px 0 #35135e, 0 5px 0 rgba(35, 9, 67, .5);
  background: linear-gradient(180deg, #ffe3ff 0%, #ef8be8 48%, #d95fd8 100%);
  border: 4px solid #35135e; border-radius: 999px;
  box-shadow: inset 0 3px 0 rgba(255,255,255,.75), 0 5px 0 #1c0b39;
}
.en-hero {
  padding: 1.5rem; margin: .35rem 0 1.1rem; border: 5px solid #35135e;
  border-radius: 30px; color: #35135e;
  background: linear-gradient(180deg, #ffe1ff 0%, #f6a9f2 36%, #e87de8 100%);
  box-shadow: inset 0 5px 0 rgba(255,255,255,.85), inset 0 -7px 0 rgba(153,54,159,.2),
    0 7px 0 #1c0b39, 0 12px 28px rgba(13,5,34,.3);
}
.en-hero h2 { margin: 0; color: #fff; font-size: clamp(1.6rem, 5vw, 2.4rem);
  line-height: 1.12; font-weight: 700; -webkit-text-stroke: 1.3px #35135e;
  paint-order: stroke fill; text-shadow: 0 3px 0 #35135e; }
.en-hero p { margin: .65rem 0 0; color: #49215f; font-size: 1.05rem; font-weight: 600; }
.en-card {
  height: 100%; box-sizing: border-box; padding: 1rem 1.1rem; margin: .35rem 0;
  color: #35135e; border: 4px solid #35135e; border-radius: 24px;
  background: linear-gradient(180deg, #ffe2ff 0%, #f6a9f2 38%, #e987eb 100%);
  box-shadow: inset 0 4px 0 rgba(255,255,255,.82), inset 0 -5px 0 rgba(153,54,159,.18),
    0 5px 0 #1c0b39;
}
.en-card h3 { margin: 0 0 .35rem; color: #57216d; font-size: 1.12rem; }
.en-card p { margin: 0; line-height: 1.45; }
.en-missions, .en-stats, .en-limits { display: grid; gap: .7rem; }
.en-missions { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.en-stats { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.en-limits { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.en-stat { text-align: center; }
.en-stat strong { display: block; font-size: 1.1rem; }
.en-note { color: #f9eaff; text-align: center; font-size: .9rem; margin: 1.2rem 0 .4rem; }
div[data-testid="stForm"], div[data-testid="stVerticalBlockBorderWrapper"] {
  border: 4px solid #35135e; border-radius: 26px;
  background: linear-gradient(180deg, #ffe1ff 0%, #f6a9f2 42%, #e987eb 100%);
  box-shadow: inset 0 4px 0 rgba(255,255,255,.8), 0 5px 0 #1c0b39;
}
div[class*="st-key-proof-result-"] {
  border: 4px solid #35135e !important; border-radius: 24px !important;
  background: linear-gradient(180deg, #ffe1ff 0%, #f6a9f2 42%, #e987eb 100%) !important;
  box-shadow: inset 0 4px 0 rgba(255,255,255,.8), 0 5px 0 #1c0b39 !important;
  padding: .4rem !important;
}
div[data-testid="stForm"] { padding: 1rem; }
div[data-testid="stVerticalBlockBorderWrapper"] { padding: .4rem; }
div[data-testid="stForm"] label, div[data-testid="stVerticalBlockBorderWrapper"] label {
  color: #35135e;
}
input, textarea, div[data-baseweb="select"] > div {
  border-radius: 14px !important; border-color: #6f358c !important;
}
.stButton > button, div[data-testid="stFormSubmitButton"] > button {
  min-height: 3rem; border: 3px solid #176b38; border-radius: 999px;
  color: #fff; font-weight: 700; text-shadow: 0 2px 0 #176b38;
  background: linear-gradient(180deg, #78f5a4 0%, #22C55E 45%, #12a94b 100%);
  box-shadow: inset 0 3px 0 rgba(255,255,255,.62), 0 4px 0 #14532d;
  transition: transform .12s ease, filter .12s ease, box-shadow .12s ease;
}
.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
  filter: brightness(1.12); transform: translateY(-2px);
  box-shadow: inset 0 3px 0 rgba(255,255,255,.7), 0 6px 0 #14532d;
  border-color: #14532d; color: #fff;
}
.stButton > button:active, div[data-testid="stFormSubmitButton"] > button:active {
  transform: translateY(3px); box-shadow: inset 0 2px 0 rgba(0,0,0,.12), 0 1px 0 #14532d;
}
.stButton > button:disabled, div[data-testid="stFormSubmitButton"] > button:disabled {
  filter: grayscale(.75); opacity: .55;
}
.stButton > button[kind="secondary"] {
  color: #5c3a2a; text-shadow: none; border-color: #9b6a24;
  background: linear-gradient(180deg, #fff4ca 0%, #f5d889 100%);
  box-shadow: inset 0 3px 0 rgba(255,255,255,.8), 0 4px 0 #78521c;
}
div[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #381565 0%, #260e49 100%);
  border-right: 3px solid rgba(246,169,242,.35);
}
div[data-testid="stCode"] {
  border: 3px solid #35135e; border-radius: 18px;
  background: linear-gradient(180deg, #ffe1ff, #f6a9f2) !important;
  box-shadow: inset 0 3px 0 rgba(255,255,255,.8), 0 4px 0 #1c0b39;
}
div[data-testid="stCode"] pre, div[data-testid="stCode"] code,
div[data-testid="stCodeBlock"] pre, div[data-testid="stCodeBlock"] code,
pre, pre code {
  color: #35135e !important; background: transparent !important;
  -webkit-text-fill-color: #35135e !important; text-shadow: none !important;
}
div[data-testid="stCode"] pre, div[data-testid="stCodeBlock"] pre, pre {
  background: linear-gradient(180deg, #ffe1ff, #f6a9f2) !important;
  border-radius: 14px !important;
}
div[data-testid="stAlert"] { border-radius: 18px; }
@media (max-width: 640px) {
  .block-container { padding: 1rem .8rem 2rem; }
  .en-navbar-brand { align-items: flex-start; flex-direction: column; gap: .1rem; }
  div[data-testid="stRadio"] label { padding: .35rem .5rem !important; font-size: .9rem; }
  .en-missions, .en-stats, .en-limits { grid-template-columns: 1fr; }
  .en-hero { padding: 1rem; border-radius: 24px; }
}
</style>
"""


def apply_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
