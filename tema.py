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
.block-container { max-width: none; padding: .5rem 1.25rem !important; }
@media (min-width: 768px) {
  body:has(.st-key-home-page),
  body:has(.st-key-main-page),
  body:has(.st-key-proof-page),
  body:has(.st-key-about-page) {
    overflow: hidden;
  }
  body:has(.st-key-home-page) .stApp,
  body:has(.st-key-main-page) .stApp,
  body:has(.st-key-proof-page) .stApp,
  body:has(.st-key-about-page) .stApp,
  body:has(.st-key-home-page) [data-testid="stAppViewContainer"],
  body:has(.st-key-main-page) [data-testid="stAppViewContainer"],
  body:has(.st-key-proof-page) [data-testid="stAppViewContainer"],
  body:has(.st-key-about-page) [data-testid="stAppViewContainer"] {
    height: 100vh; max-height: 100vh; overflow: hidden;
  }
  body:has(.st-key-home-page) [data-testid="stHeader"],
  body:has(.st-key-main-page) [data-testid="stHeader"],
  body:has(.st-key-proof-page) [data-testid="stHeader"],
  body:has(.st-key-about-page) [data-testid="stHeader"] {
    display: none !important;
  }
  body:has(.st-key-home-page) [data-testid="stMain"],
  body:has(.st-key-main-page) [data-testid="stMain"],
  body:has(.st-key-proof-page) [data-testid="stMain"],
  body:has(.st-key-about-page) [data-testid="stMain"],
  body:has(.st-key-home-page) [data-testid="stMainBlockContainer"],
  body:has(.st-key-main-page) [data-testid="stMainBlockContainer"],
  body:has(.st-key-proof-page) [data-testid="stMainBlockContainer"],
  body:has(.st-key-about-page) [data-testid="stMainBlockContainer"] {
    box-sizing: border-box; height: 100vh;
    max-height: 100vh; overflow: hidden;
  }
  body:has(.st-key-home-page) [data-testid="stMain"] .block-container,
  body:has(.st-key-main-page) [data-testid="stMain"] .block-container,
  body:has(.st-key-proof-page) [data-testid="stMain"] .block-container,
  body:has(.st-key-about-page) [data-testid="stMain"] .block-container {
    box-sizing: border-box; height: 100vh;
    max-height: 100vh; padding: .35rem 1rem !important;
    overflow: hidden;
  }
  body:has(.st-key-home-page) [data-testid="stMain"] .block-container > [data-testid="stVerticalBlock"],
  body:has(.st-key-main-page) [data-testid="stMain"] .block-container > [data-testid="stVerticalBlock"],
  body:has(.st-key-proof-page) [data-testid="stMain"] .block-container > [data-testid="stVerticalBlock"],
  body:has(.st-key-about-page) [data-testid="stMain"] .block-container > [data-testid="stVerticalBlock"] {
    display: flex; flex-direction: column; height: 100%; min-height: 0;
  }
  body:has(.st-key-home-page) [data-testid="stTabs"],
  body:has(.st-key-main-page) [data-testid="stTabs"],
  body:has(.st-key-proof-page) [data-testid="stTabs"],
  body:has(.st-key-about-page) [data-testid="stTabs"] {
    display: flex; flex: 1; flex-direction: column; min-height: 0; overflow: hidden;
  }
  body:has(.st-key-home-page) [data-testid="stTabs"] > div:has([role="tabpanel"]),
  body:has(.st-key-main-page) [data-testid="stTabs"] > div:has([role="tabpanel"]),
  body:has(.st-key-proof-page) [data-testid="stTabs"] > div:has([role="tabpanel"]),
  body:has(.st-key-about-page) [data-testid="stTabs"] > div:has([role="tabpanel"]) {
    display: flex; flex: 1; flex-direction: column; min-height: 0; overflow: hidden;
  }
  body:has(.st-key-home-page) [data-testid="stTabs"] [role="tabpanel"],
  body:has(.st-key-main-page) [data-testid="stTabs"] [role="tabpanel"],
  body:has(.st-key-proof-page) [data-testid="stTabs"] [role="tabpanel"],
  body:has(.st-key-about-page) [data-testid="stTabs"] [role="tabpanel"] {
    display: flex; flex: 1; flex-direction: column; min-height: 0; overflow: hidden;
  }
  body:has(.st-key-home-page) [data-testid="stTabs"] [role="tabpanel"] > [data-testid="stVerticalBlock"],
  body:has(.st-key-main-page) [data-testid="stTabs"] [role="tabpanel"] > [data-testid="stVerticalBlock"],
  body:has(.st-key-proof-page) [data-testid="stTabs"] [role="tabpanel"] > [data-testid="stVerticalBlock"],
  body:has(.st-key-about-page) [data-testid="stTabs"] [role="tabpanel"] > [data-testid="stVerticalBlock"] {
    display: flex; flex: 1; flex-direction: column; min-height: 0; overflow: hidden;
  }
  body:has(.st-key-home-page) .st-key-home-page,
  body:has(.st-key-main-page) .st-key-main-page,
  body:has(.st-key-proof-page) .st-key-proof-page,
  body:has(.st-key-about-page) .st-key-about-page {
    box-sizing: border-box; display: flex; flex: 1; flex-direction: column;
    min-height: 0; overflow-x: hidden; overflow-y: auto;
  }
  body:has(.st-key-home-page) .st-key-home-page > [data-testid="stVerticalBlock"],
  body:has(.st-key-proof-page) .st-key-proof-page > [data-testid="stVerticalBlock"],
  body:has(.st-key-about-page) .st-key-about-page > [data-testid="stVerticalBlock"] {
    display: flex; flex: 1; flex-direction: column; min-height: 0;
  }
  body:has(.st-key-home-page) .st-key-home-page [data-testid="stVerticalBlock"],
  body:has(.st-key-proof-page) .st-key-proof-page [data-testid="stVerticalBlock"],
  body:has(.st-key-about-page) .st-key-about-page [data-testid="stVerticalBlock"] {
    gap: .45rem;
  }
  body:has(.st-key-main-page) [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"]:has(> .st-key-main-page) {
    flex: 1; min-height: 0; overflow: hidden;
  }
  body:has(.st-key-main-page) .st-key-main-page {
    display: flex; flex: 1; flex-direction: column; min-height: 0;
    overflow: hidden; width: 100%;
  }
  body:has(.st-key-main-page) .st-key-main-page > [data-testid="stLayoutWrapper"]:has([data-testid="stHorizontalBlock"]) {
    display: flex; flex: 1; min-height: 0; overflow: hidden;
  }
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stHorizontalBlock"] {
    flex: 1; align-items: stretch; min-height: 0;
  }
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stColumn"] {
    display: flex; flex-direction: column; min-height: 0; overflow: hidden;
  }
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stColumn"] > [data-testid="stVerticalBlock"] {
    flex: 1; height: 100%; min-height: 0; overflow: hidden;
  }
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stColumn"] > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"]:has(.st-key-main-create-panel, .st-key-main-read-panel) {
    display: flex; flex: 1; height: 100%; min-height: 0; overflow: hidden;
  }
  body:has(.st-key-main-page) .st-key-main-create-panel,
  body:has(.st-key-main-page) .st-key-main-read-panel {
    box-sizing: border-box; height: calc(100vh - 12rem);
    max-height: calc(100vh - 12rem); min-height: 0; flex: 0 1 auto;
    overflow-x: hidden; overflow-y: auto; overscroll-behavior: contain;
  }
}
h1, h2, h3, .en-pixel-title,
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
.en-home-screen { display: flex; flex-direction: column; gap: .55rem; }
.en-home-screen > h1 {
  margin: 0; color: var(--pixel-yellow); font-size: 1rem; line-height: 1.4;
  text-shadow: 3px 3px 0 var(--pixel-dark);
}
.en-home-screen > h2,
.en-home-intro h2 { margin: 0 0 .25rem; font-size: .7rem !important; }
.en-home-intro {
  padding: .55rem .75rem; color: var(--pixel-dark);
  border: 3px solid #000; background: var(--pixel-white); box-shadow: 3px 3px 0 #000;
}
.en-home-intro h2 { color: var(--pixel-purple); text-shadow: none; }
.en-home-intro p { margin: 0; color: var(--pixel-dark); font-size: 1.15rem; line-height: 1.2; }
.en-home-steps { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .65rem; }
.en-home-steps article,
.en-about-grid article {
  padding: .6rem .7rem; border: 3px solid #000; background: var(--pixel-dark);
  box-shadow: 3px 3px 0 #000;
}
.en-home-steps h3,
.en-about-grid h3 { margin: 0 0 .25rem; color: var(--pixel-yellow); font-size: .62rem !important; }
.en-home-steps p,
.en-about-grid p { margin: 0; color: var(--pixel-white); font-size: 1.08rem; line-height: 1.15; }
.en-home-stats { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: .5rem; }
.en-home-stats > div {
  padding: .4rem; text-align: center; color: var(--pixel-dark);
  border: 3px solid #000; background: var(--pixel-cyan);
}
.en-home-stats strong { display: block; font-size: .68rem; }
.en-home-stats span { font-size: 1rem; }
.en-proof-grid { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: .5rem; }
.en-proof-card {
  display: flex; min-width: 0; align-items: center; justify-content: space-between;
  gap: .2rem; padding: .45rem; color: var(--pixel-white);
  border: 3px solid #000; background: var(--pixel-dark); box-shadow: 3px 3px 0 #000;
}
.en-proof-card strong { overflow: hidden; font-size: .62rem; text-overflow: ellipsis; white-space: nowrap; }
.en-proof-card span {
  flex: 0 0 auto; padding: .1rem .25rem; color: var(--pixel-dark);
  font: .48rem "Press Start 2P", monospace; background: var(--pixel-green);
}
.en-proof-card.fail span { background: #ff6b6b; }
.en-about-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .5rem; }
.en-about-grid article { padding: .45rem .6rem; }
.en-about-grid h3 { font-size: .55rem !important; }
.en-about-grid p { font-size: 1.02rem; }
div[data-testid="stTabs"] { min-height: 0; }
div[data-testid="stTabs"] [role="tablist"] {
  min-height: 2.5rem; padding: .2rem; gap: .35rem;
  justify-content: center; align-items: center;
  border: 3px solid #000; background: var(--pixel-pink); box-shadow: 3px 3px 0 #000;
}
div[data-testid="stTabs"] [role="tab"] {
  height: 2.65rem; padding: .35rem .8rem; color: var(--pixel-dark);
  font: .68rem "Press Start 2P", monospace;
}
div[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  color: var(--pixel-yellow); background: var(--pixel-dark);
}
div[data-testid="stTabs"] [role="tabpanel"] { padding: .5rem 0 0; }
div[data-testid="stTabs"] [role="tabpanel"] > [data-testid="stVerticalBlock"] {
  min-height: 0;
}
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
section[data-testid="stSidebar"],
div[data-testid="stSidebarCollapsedControl"] { display: none !important; }
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
body:has(.st-key-main-page) .st-key-main-page input,
body:has(.st-key-main-page) .st-key-main-page textarea,
body:has(.st-key-main-page) .st-key-main-page div[data-baseweb="select"] > div {
  font-size: 1.05rem !important;
}
body:has(.st-key-main-page) .st-key-main-read-panel [data-testid="stImage"] img {
  max-height: 28vh; object-fit: contain;
}
body:has(.st-key-main-page) .st-key-main-read-panel textarea:disabled {
  color: var(--pixel-dark) !important;
  -webkit-text-fill-color: var(--pixel-dark) !important;
  opacity: 1 !important;
}
@media (min-width: 768px) {
  body:has(.st-key-proof-page),
  body:has(.st-key-about-page) {
    overflow: hidden;
  }
  body:has(.st-key-proof-page) .stApp,
  body:has(.st-key-about-page) .stApp,
  body:has(.st-key-proof-page) [data-testid="stAppViewContainer"],
  body:has(.st-key-about-page) [data-testid="stAppViewContainer"] {
    height: 100vh; max-height: 100vh; overflow: hidden;
  }
  body:has(.st-key-proof-page) [data-testid="stMain"],
  body:has(.st-key-about-page) [data-testid="stMain"] {
    flex: 1 1 auto; height: 100vh; min-height: 0; max-height: 100vh;
    overflow-x: hidden; overflow-y: auto;
  }
  body:has(.st-key-proof-page) [data-testid="stMainBlockContainer"],
  body:has(.st-key-about-page) [data-testid="stMainBlockContainer"],
  body:has(.st-key-proof-page) [data-testid="stMain"] .block-container,
  body:has(.st-key-about-page) [data-testid="stMain"] .block-container {
    height: auto; min-height: 100%; max-height: none; overflow: visible;
  }
  body:has(.st-key-proof-page) [data-testid="stMain"] .block-container > [data-testid="stVerticalBlock"],
  body:has(.st-key-about-page) [data-testid="stMain"] .block-container > [data-testid="stVerticalBlock"],
  body:has(.st-key-proof-page) [data-testid="stTabs"],
  body:has(.st-key-about-page) [data-testid="stTabs"],
  body:has(.st-key-proof-page) [data-testid="stTabs"] > div:has([role="tabpanel"]),
  body:has(.st-key-about-page) [data-testid="stTabs"] > div:has([role="tabpanel"]),
  body:has(.st-key-proof-page) [data-testid="stTabs"] [role="tabpanel"],
  body:has(.st-key-about-page) [data-testid="stTabs"] [role="tabpanel"],
  body:has(.st-key-proof-page) [data-testid="stTabs"] [role="tabpanel"] > [data-testid="stVerticalBlock"],
  body:has(.st-key-about-page) [data-testid="stTabs"] [role="tabpanel"] > [data-testid="stVerticalBlock"],
  body:has(.st-key-proof-page) .st-key-proof-page,
  body:has(.st-key-about-page) .st-key-about-page {
    display: block; flex: none; height: auto; max-height: none;
    min-height: 0; overflow: visible;
  }
  body:has(.st-key-proof-page) [data-testid="stMain"] .block-container > [data-testid="stVerticalBlock"],
  body:has(.st-key-about-page) [data-testid="stMain"] .block-container > [data-testid="stVerticalBlock"] {
    height: auto;
  }
}
@media (min-width: 1024px) {
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stHeading"] h1 {
    margin: .05rem 0 .35rem; padding: .2rem .45rem;
    font-size: .72rem; line-height: 1.25 !important;
  }
  body:has(.st-key-proof-page) .st-key-proof-page [data-testid="stHeading"] h1,
  body:has(.st-key-about-page) .st-key-about-page [data-testid="stHeading"] h1 {
    margin: .05rem 0 .35rem; padding: .2rem .45rem;
    font-size: .72rem; line-height: 1.25 !important;
  }
  body:has(.st-key-proof-page) .en-proof-grid { gap: .35rem; }
  body:has(.st-key-proof-page) .en-proof-card { padding: .3rem; }
  body:has(.st-key-about-page) .en-about-grid { gap: .35rem; }
  body:has(.st-key-about-page) .en-about-grid article { padding: .3rem .6rem; }
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stVerticalBlock"] {
    gap: .25rem;
  }
  body:has(.st-key-main-page) .st-key-main-page p,
  body:has(.st-key-main-page) .st-key-main-page label,
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stWidgetLabel"] {
    font-size: 1.05rem; line-height: 1.15;
  }
  body:has(.st-key-main-page) .st-key-main-page h3 {
    margin: 0 0 .2rem; font-size: .62rem !important;
  }
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stVerticalBlockBorderWrapper"] {
    padding: .45rem !important;
  }
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stForm"] {
    padding: .4rem !important;
  }
  body:has(.st-key-main-page) .st-key-main-page textarea {
    height: 80px !important; min-height: 80px !important;
  }
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stFileUploaderDropzone"] {
    min-height: 44px; padding: .1rem .4rem;
  }
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stAlert"] {
    padding: .3rem .45rem !important;
  }
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stCode"] pre,
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stCodeBlock"] pre {
    padding: .35rem .5rem !important;
  }
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stButton"] button,
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stFormSubmitButton"] button {
    min-height: 2.25rem; padding: .25rem .5rem;
  }
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stPopover"] > button {
    min-height: 1.8rem; padding: .15rem .4rem; font-size: .55rem;
  }
}
@media (max-width: 767px) {
  .block-container { max-width: 100%; padding: 4.25rem .8rem 1rem !important; }
  div[data-testid="stTabs"] [role="tablist"] {
    gap: .1rem; overflow-x: auto;
  }
  div[data-testid="stTabs"] [role="tab"] {
    height: 2.2rem; padding: .25rem .4rem; font-size: .48rem;
  }
  .en-home-steps { grid-template-columns: 1fr; }
  .en-home-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .en-proof-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  body:has(.st-key-main-page) .stApp,
  body:has(.st-key-home-page) .stApp,
  body:has(.st-key-proof-page) .stApp,
  body:has(.st-key-about-page) .stApp,
  body:has(.st-key-main-page) [data-testid="stAppViewContainer"] {
    height: auto; min-height: 100vh; overflow: visible;
  }
  body:has(.st-key-home-page) [data-testid="stAppViewContainer"],
  body:has(.st-key-proof-page) [data-testid="stAppViewContainer"],
  body:has(.st-key-about-page) [data-testid="stAppViewContainer"] {
    height: auto; min-height: 100vh; overflow: visible;
  }
  body:has(.st-key-home-page) [data-testid="stMain"],
  body:has(.st-key-proof-page) [data-testid="stMain"],
  body:has(.st-key-about-page) [data-testid="stMain"],
  body:has(.st-key-home-page) [data-testid="stMainBlockContainer"],
  body:has(.st-key-proof-page) [data-testid="stMainBlockContainer"],
  body:has(.st-key-about-page) [data-testid="stMainBlockContainer"],
  body:has(.st-key-home-page) [data-testid="stMain"] .block-container,
  body:has(.st-key-proof-page) [data-testid="stMain"] .block-container,
  body:has(.st-key-about-page) [data-testid="stMain"] .block-container,
  body:has(.st-key-home-page) [data-testid="stTabs"],
  body:has(.st-key-proof-page) [data-testid="stTabs"],
  body:has(.st-key-about-page) [data-testid="stTabs"],
  body:has(.st-key-home-page) [role="tabpanel"],
  body:has(.st-key-proof-page) [role="tabpanel"],
  body:has(.st-key-about-page) [role="tabpanel"],
  body:has(.st-key-home-page) .st-key-home-page,
  body:has(.st-key-proof-page) .st-key-proof-page,
  body:has(.st-key-about-page) .st-key-about-page {
    height: auto; max-height: none; overflow: visible;
  }
  body:has(.st-key-main-page) [data-testid="stMain"],
  body:has(.st-key-home-page) [data-testid="stMain"],
  body:has(.st-key-proof-page) [data-testid="stMain"],
  body:has(.st-key-about-page) [data-testid="stMain"],
  body:has(.st-key-main-page) [data-testid="stMain"],
  body:has(.st-key-main-page) [data-testid="stMainBlockContainer"],
  body:has(.st-key-main-page) .stMainBlockContainer,
  body:has(.st-key-main-page) [data-testid="stMain"] .block-container {
    height: auto; max-height: none; overflow: visible;
  }
  body:has(.st-key-main-page) [data-testid="stMain"] .block-container {
    padding-top: 4.5rem !important; padding-bottom: 2.5rem !important;
  }
  body:has(.st-key-main-page) [data-testid="stMain"] .block-container > [data-testid="stVerticalBlock"],
  body:has(.st-key-main-page) [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"]:has(> .st-key-main-page),
  body:has(.st-key-main-page) .st-key-main-page,
  body:has(.st-key-main-page) .st-key-main-page > [data-testid="stLayoutWrapper"]:has([data-testid="stHorizontalBlock"]) {
    display: block; height: auto; min-height: 0; overflow: visible;
  }
  body:has(.st-key-main-page) .st-key-main-page > [data-testid="stLayoutWrapper"]:has([data-testid="stHorizontalBlock"]) {
    flex: none;
  }
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stHorizontalBlock"] {
    display: flex; flex-direction: column; gap: .75rem;
  }
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stColumn"] {
    display: block; width: 100% !important; min-width: 100% !important;
    height: auto; overflow: visible;
  }
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stColumn"] > [data-testid="stVerticalBlock"],
  body:has(.st-key-main-page) .st-key-main-page [data-testid="stColumn"] > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"] {
    display: block; height: auto; flex: none; overflow: visible;
  }
  body:has(.st-key-main-page) .st-key-main-create-panel,
  body:has(.st-key-main-page) .st-key-main-read-panel {
    height: auto; max-height: 62vh; flex: none; overflow-y: auto;
  }
  body:has(.st-key-main-page) .st-key-main-page textarea {
    height: 80px !important; min-height: 80px !important;
  }
}
@media (max-width: 700px) {
  .block-container { padding: 4.5rem .8rem 2.5rem; }
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
