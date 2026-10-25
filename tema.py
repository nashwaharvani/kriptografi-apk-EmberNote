"""Tema pixel-art retro 8-bit EmberNote."""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');

:root {
  --pixel-purple: #4B1D8F;
  --pixel-yellow: #FFD84D;
  --pixel-pink: #FF6EC7;
  --pixel-cyan: #5CE1E6;
  --pixel-green: #4ADE80;
  --pixel-white: #FFFDF7;
  --pixel-dark: #1B0B3A;
  --pixel-black: #000;
}
html, body, [class*="css"] { font-family: "VT323", monospace; }
.stApp {
  color: var(--pixel-white);
  background-color: var(--pixel-purple);
  background-image:
    radial-gradient(circle at 12% 12%, rgba(255,216,77,.12) 0 2px, transparent 3px),
    radial-gradient(circle at 84% 26%, rgba(92,225,230,.12) 0 2px, transparent 3px),
    linear-gradient(180deg, #54229a 0%, #4B1D8F 72%, #35136c 100%);
  background-size: 32px 32px, 48px 48px, auto;
  background-attachment: fixed;
}
.block-container { max-width: 1000px; padding-top: 1.2rem; padding-bottom: 3rem; }
h1, h2, h3, .en-pixel-title, .en-navbar-brand strong,
.stButton button, div[data-testid="stFormSubmitButton"] button {
  font-family: "Press Start 2P", "Courier New", monospace !important;
  line-height: 1.6 !important;
}
[data-testid="stHeading"] h1 {
  display: inline-block; padding: .65rem .8rem; margin: .4rem 0 .8rem;
  color: var(--pixel-yellow); font-size: clamp(.85rem, 3vw, 1.15rem);
  text-shadow: 3px 3px 0 var(--pixel-dark);
  background: var(--pixel-purple); border: 4px solid var(--pixel-black);
  border-radius: 0; box-shadow: 4px 4px 0 var(--pixel-black);
}
h2, h3 { color: var(--pixel-yellow); text-shadow: 2px 2px 0 var(--pixel-dark); }
h2 { font-size: clamp(.8rem, 2.4vw, 1rem) !important; }
h3 { font-size: clamp(.62rem, 1.8vw, .8rem) !important; }
p, li, label, .stMarkdown, .stCaption, .stAlert, [data-testid="stWidgetLabel"] {
  color: var(--pixel-white);
  font-family: "VT323", "Courier New", monospace;
  font-size: 1.25rem;
  line-height: 1.35;
}
.en-navbar-brand {
  display: flex; justify-content: space-between; align-items: center; gap: 1rem;
  padding: .7rem .9rem; margin-bottom: .55rem; color: var(--pixel-white);
  border: 4px solid var(--pixel-black); border-radius: 0;
  background: var(--pixel-dark); box-shadow: 4px 4px 0 var(--pixel-black);
}
.en-navbar-brand strong { color: var(--pixel-yellow); font-size: .75rem; }
.en-navbar-brand span { font-size: 1.2rem; }
.en-pixel-hero {
  position: relative; padding: 1.3rem; margin: 1rem 0;
  text-align: center; color: var(--pixel-white);
  border: 4px solid var(--pixel-black); background: var(--pixel-dark);
  box-shadow: 4px 4px 0 var(--pixel-black);
}
.en-pixel-title {
  margin: 0; color: var(--pixel-yellow); font-size: clamp(1rem, 4vw, 1.6rem);
  line-height: 1.8; text-shadow: 3px 3px 0 #000;
}
.en-pixel-subtitle { margin: .6rem 0 0; color: var(--pixel-cyan); font-size: 1.45rem; }
.en-dialog {
  position: relative; padding: 1rem 1.15rem; margin: .5rem 0 1.2rem;
  color: var(--pixel-dark); border: 4px solid var(--pixel-black);
  border-radius: 0; background: var(--pixel-white);
  box-shadow: 4px 4px 0 var(--pixel-black);
}
.en-dialog:after {
  content: ""; position: absolute; left: 2rem; bottom: -14px; width: 18px; height: 18px;
  background: var(--pixel-white); border-right: 4px solid var(--pixel-black);
  border-bottom: 4px solid var(--pixel-black); transform: skewY(35deg);
}
.en-dialog h3 { margin: 0 0 .55rem; color: var(--pixel-purple); text-shadow: none; }
.en-dialog p { margin: 0; color: var(--pixel-dark); font-size: 1.35rem; }
.en-pixel-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .75rem; }
.en-pixel-card, .en-stat-card {
  height: 100%; padding: .85rem; color: var(--pixel-white);
  border: 4px solid var(--pixel-black); border-radius: 0;
  background: var(--pixel-purple); box-shadow: 4px 4px 0 var(--pixel-black);
}
.en-pixel-card h3 { margin: 0 0 .55rem; color: var(--pixel-yellow); }
.en-pixel-card p { margin: 0; font-size: 1.18rem; }
.en-rule-card { border-color: var(--pixel-yellow); background: var(--pixel-dark); }
.en-stats { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: .65rem; }
.en-stat-card { text-align: center; color: var(--pixel-dark); border-color: var(--pixel-black); background: var(--pixel-cyan); }
.en-stat-card strong { display: block; color: var(--pixel-dark); font-size: 1.1rem; }
.en-stat-card span { font-size: 1.15rem; }
.en-home-actions { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .8rem; margin: 1rem 0; }
div[class*="st-key-home-actions"] [data-testid="stHorizontalBlock"] {
  display: grid !important; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .8rem;
}
div[class*="st-key-home-actions"] [data-testid="stColumn"] {
  width: auto !important; min-width: 0 !important;
}
.en-grass {
  height: 18px; margin: 1.5rem -1rem -3rem;
  background: repeating-linear-gradient(90deg, var(--pixel-green) 0 12px, #249b58 12px 20px);
  border-top: 4px solid #000; image-rendering: pixelated;
}
.en-footer {
  padding: .9rem; margin-top: 1.4rem; text-align: center;
  color: var(--pixel-yellow); font: .7rem/1.8 "Press Start 2P", monospace;
  border: 4px solid #000; background: var(--pixel-dark); box-shadow: 4px 4px 0 #000;
}
div[data-testid="stRadio"] > div[role="radiogroup"] {
  display: flex; flex-direction: row; flex-wrap: wrap; gap: .35rem;
  justify-content: center;
  padding: .5rem; border: 4px solid #000; border-radius: 0;
  background: var(--pixel-pink); box-shadow: 4px 4px 0 #000;
}
div[class*="st-key-top_page"] > div[data-testid="stRadio"] > div[role="radiogroup"] {
  width: 100%; box-sizing: border-box; justify-content: center;
}
div[class*="st-key-top_page"], div[class*="st-key-top_page"] > div[data-testid="stRadio"] {
  width: 100%;
}
div[data-testid="stRadio"] label {
  margin: 0 !important; padding: .35rem .55rem !important;
  border: 2px solid transparent; border-radius: 0;
  color: var(--pixel-dark) !important; font-size: 1.12rem !important;
}
div[data-testid="stRadio"] label[data-selected="true"] {
  color: var(--pixel-yellow) !important; border: 2px solid #000;
  background: var(--pixel-dark); box-shadow: 2px 2px 0 #000;
}
div[data-testid="stSidebar"] {
  background: #35136c; border-right: 4px solid #000;
}
div[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: .75rem; }
div[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] {
  flex-direction: column; align-items: stretch;
}
div[data-testid="stForm"], div[data-testid="stVerticalBlockBorderWrapper"] {
  padding: .75rem; border: 4px solid #000 !important; border-radius: 0 !important;
  background: var(--pixel-dark) !important; box-shadow: 4px 4px 0 #000 !important;
}
div[data-testid="stForm"] label { color: var(--pixel-yellow) !important; }
input, textarea, div[data-baseweb="select"] > div {
  color: var(--pixel-dark) !important; background: var(--pixel-white) !important;
  border: 3px solid #000 !important; border-radius: 0 !important;
  font: 1.25rem "VT323", monospace !important;
}
textarea { min-height: 120px; }
div[data-testid="stSelectbox"] label { color: var(--pixel-cyan) !important; }
div[data-testid="stButton"] button, div[data-testid="stFormSubmitButton"] button {
  min-height: 3rem; padding: .5rem .8rem;
  color: var(--pixel-dark); font-size: .62rem; line-height: 1.8;
  border: 4px solid #000; border-radius: 0;
  background: var(--pixel-yellow); box-shadow: 4px 4px 0 #000;
  text-shadow: none; transition: transform .08s ease, box-shadow .08s ease;
}
div[data-testid="stButton"] button:hover, div[data-testid="stFormSubmitButton"] button:hover {
  color: var(--pixel-dark); border-color: #000; transform: translateY(-2px);
  background: var(--pixel-cyan); box-shadow: 4px 6px 0 #000;
}
div[data-testid="stButton"] button:active, div[data-testid="stFormSubmitButton"] button:active {
  transform: translate(3px, 3px); box-shadow: 1px 1px 0 #000;
}
div[data-testid="stButton"] button:disabled, div[data-testid="stFormSubmitButton"] button:disabled {
  opacity: .55; filter: grayscale(1);
}
div[data-testid="stCode"] {
  position: relative; border: 4px solid #000; border-radius: 0;
  background: var(--pixel-white) !important; box-shadow: 4px 4px 0 #000;
}
div[data-testid="stCode"]::after {
  content: ""; position: absolute; left: 1.25rem; bottom: -12px; width: 14px; height: 14px;
  background: var(--pixel-white); border-right: 4px solid #000; border-bottom: 4px solid #000;
  transform: skewY(35deg);
}
div[data-testid="stCode"] pre, div[data-testid="stCode"] code,
div[data-testid="stCodeBlock"] pre, div[data-testid="stCodeBlock"] code {
  color: var(--pixel-dark) !important; background: transparent !important;
  -webkit-text-fill-color: var(--pixel-dark) !important;
  font: 1.3rem "VT323", monospace !important; text-shadow: none !important;
}
div[data-testid="stCode"] pre, div[data-testid="stCodeBlock"] pre {
  background: var(--pixel-white) !important; border-radius: 0 !important;
}
div[class*="st-key-proof-result-"] {
  border: 4px solid #000 !important; border-radius: 0 !important;
  background: var(--pixel-dark) !important; box-shadow: 4px 4px 0 #000 !important;
}
div[data-testid="stAlert"] {
  color: var(--pixel-dark); border: 3px solid #000; border-radius: 0;
  background: var(--pixel-cyan);
}
div[class*="st-key-game-over"] {
  padding: .8rem; margin-bottom: .8rem; text-align: center;
  color: var(--pixel-dark); font: .7rem/1.8 "Press Start 2P", monospace;
  border: 4px solid #000; background: var(--pixel-green);
  box-shadow: 4px 4px 0 #000; text-shadow: 2px 2px 0 #fff;
}
img { image-rendering: pixelated; }
@media (max-width: 700px) {
  .block-container { padding: .8rem .8rem 2.5rem; }
  .en-navbar-brand { align-items: flex-start; flex-direction: column; gap: .2rem; }
  .en-pixel-grid, .en-stats, .en-home-actions,
  div[class*="st-key-home-actions"] [data-testid="stHorizontalBlock"] {
    grid-template-columns: 1fr;
  }
  div[data-testid="stRadio"] > div[role="radiogroup"] { gap: .15rem; }
  div[data-testid="stRadio"] label { padding: .3rem .4rem !important; font-size: 1rem !important; }
  .en-grass { margin-left: -.8rem; margin-right: -.8rem; }
}
</style>
"""


def apply_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
