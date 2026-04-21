import streamlit as st
import streamlit.components.v1 as components
from recommender import CourseRecommender, SKILL_PATHS

st.set_page_config(
    page_title="Learn Anything",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM
# ─────────────────────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Variables ───────────────────────────────────────────────────────────── */
:root {
  --accent:        #4F46E5;
  --accent-light:  #EEF2FF;
  --accent-hover:  #4338CA;
  --bg:            #FFFFFF;
  --bg-muted:      #F9FAFB;
  --border:        #E5E7EB;
  --border-focus:  #4F46E5;
  --text-1:        #111827;
  --text-2:        #374151;
  --text-3:        #6B7280;
  --text-4:        #9CA3AF;
  --shadow-sm:     0 1px 3px 0 rgba(0,0,0,0.08), 0 1px 2px -1px rgba(0,0,0,0.06);
  --shadow-md:     0 4px 16px -2px rgba(0,0,0,0.10), 0 2px 6px -2px rgba(0,0,0,0.06);
  --radius-sm:     6px;
  --radius-md:     10px;
  --radius-lg:     14px;
  --radius-full:   9999px;
  --transition:    150ms ease;
  --font:          'Inter', system-ui, -apple-system, sans-serif;
}
[data-theme="dark"] {
  --bg:        #0F172A;
  --bg-muted:  #1E293B;
  --border:    #334155;
  --text-1:    #F1F5F9;
  --text-2:    #CBD5E1;
  --text-3:    #94A3B8;
  --text-4:    #64748B;
  --shadow-sm: 0 1px 3px 0 rgba(0,0,0,0.3);
  --shadow-md: 0 4px 16px -2px rgba(0,0,0,0.4);
}

/* ── Reset & base ────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"], .stApp {
  font-family: var(--font) !important;
  background: var(--bg) !important;
  color: var(--text-1) !important;
}
.main .block-container {
  max-width: 1080px !important;
  padding: 0 2rem 6rem !important;
  margin: 0 auto !important;
}
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }

/* ── Streamlit element spacing ───────────────────────────────────────────── */
div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"] {
  margin-bottom: 0 !important;
}

/* ── Header ──────────────────────────────────────────────────────────────── */
.la-header {
  padding: 2.5rem 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.la-wordmark {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}
.la-logo-box {
  width: 34px; height: 34px;
  background: var(--accent);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.la-wordmark-text {
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--text-1);
  letter-spacing: -0.02em;
}
.la-tagline {
  font-size: 0.78rem;
  color: var(--text-4);
  font-weight: 400;
  margin-top: 1px;
}
.la-header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.saved-count-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 14px;
  border-radius: var(--radius-full);
  border: 1.5px solid var(--border);
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-2);
  cursor: pointer;
  transition: all var(--transition);
  background: var(--bg);
}
.saved-count-pill:hover { border-color: var(--accent); color: var(--accent); }
.saved-count-pill.active { background: var(--accent-light); border-color: var(--accent); color: var(--accent); }

/* ── Search bar ──────────────────────────────────────────────────────────── */
.search-wrap { margin-bottom: 1.25rem; }
div[data-testid="stTextInput"] {
  margin: 0 !important;
}
div[data-testid="stTextInput"] > label { display: none !important; }
div[data-testid="stTextInput"] > div {
  border: 2px solid var(--border) !important;
  border-radius: var(--radius-full) !important;
  background: var(--bg) !important;
  box-shadow: var(--shadow-sm) !important;
  transition: border-color var(--transition), box-shadow var(--transition) !important;
  padding: 0 !important;
  overflow: hidden;
}
div[data-testid="stTextInput"] > div:focus-within {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(79,70,229,0.12), var(--shadow-sm) !important;
}
div[data-testid="stTextInput"] input {
  font-size: 1rem !important;
  font-family: var(--font) !important;
  padding: 14px 20px !important;
  color: var(--text-1) !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
  line-height: 1.4 !important;
}
div[data-testid="stTextInput"] input::placeholder { color: var(--text-4) !important; }

/* ── Filter bar ──────────────────────────────────────────────────────────── */
.filter-label {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--text-4);
  margin-bottom: 6px;
}
.filter-divider {
  width: 1px;
  background: var(--border);
  height: 36px;
  margin: auto 0;
}
/* Chip buttons - override Streamlit */
div[data-testid="stButton"] > button {
  font-family: var(--font) !important;
  font-size: 0.8rem !important;
  font-weight: 500 !important;
  border-radius: var(--radius-full) !important;
  padding: 6px 14px !important;
  line-height: 1.4 !important;
  transition: all var(--transition) !important;
  cursor: pointer !important;
  white-space: nowrap !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
  background: var(--accent) !important;
  color: white !important;
  border: 1.5px solid var(--accent) !important;
  box-shadow: none !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
  background: var(--accent-hover) !important;
  border-color: var(--accent-hover) !important;
}
div[data-testid="stButton"] > button[kind="secondary"] {
  background: var(--bg) !important;
  color: var(--text-2) !important;
  border: 1.5px solid var(--border) !important;
  box-shadow: none !important;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover {
  border-color: var(--accent) !important;
  color: var(--accent) !important;
  background: var(--accent-light) !important;
}
div[data-testid="stButton"] > button:focus-visible {
  outline: 2px solid var(--accent) !important;
  outline-offset: 2px !important;
}

/* ── Link button ─────────────────────────────────────────────────────────── */
div.stLinkButton > a {
  font-family: var(--font) !important;
  font-size: 0.82rem !important;
  font-weight: 600 !important;
  border-radius: var(--radius-md) !important;
  padding: 8px 16px !important;
  background: var(--accent) !important;
  color: white !important;
  border: none !important;
  text-decoration: none !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 100% !important;
  transition: background var(--transition) !important;
  box-shadow: none !important;
}
div.stLinkButton > a:hover {
  background: var(--accent-hover) !important;
  color: white !important;
}

/* ── Result header ───────────────────────────────────────────────────────── */
.result-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin: 1.5rem 0 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}
.result-count {
  font-size: 0.92rem;
  font-weight: 600;
  color: var(--text-1);
}
.result-count em { font-style: normal; color: var(--accent); }
.result-meta { font-size: 0.78rem; color: var(--text-4); }

/* ── Course card ─────────────────────────────────────────────────────────── */
.crd {
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  background: var(--bg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition), box-shadow var(--transition);
  animation: fadeUp 0.3s ease both;
  margin-bottom: 4px;
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0);    }
}
.crd:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
/* Thumbnail */
.crd-thumb {
  position: relative;
  height: 148px;
  overflow: hidden;
  flex-shrink: 0;
}
.crd-thumb-inner {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
}
.crd-thumb-text {
  font-size: 1.1rem;
  font-weight: 700;
  color: rgba(255,255,255,0.55);
  text-align: center;
  padding: 0 20px;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.thumb-coursera { background: #0056D2; }
.thumb-udemy    { background: #7B2FBE; }
.thumb-youtube  { background: #C0392B; }
.thumb-edx      { background: #1A1A2E; }
.thumb-default  { background: #374151; }
/* Overlay badges */
.thumb-badges {
  position: absolute; bottom: 0; left: 0; right: 0;
  padding: 8px 12px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  background: linear-gradient(to top, rgba(0,0,0,0.45) 0%, transparent 100%);
}
.plat-pill {
  font-size: 0.68rem;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: var(--radius-full);
  letter-spacing: 0.03em;
  backdrop-filter: blur(6px);
}
.plat-coursera { background: rgba(219,234,254,0.92); color: #1E40AF; }
.plat-udemy    { background: rgba(243,232,255,0.92); color: #6B21A8; }
.plat-youtube  { background: rgba(254,226,226,0.92); color: #991B1B; }
.plat-edx      { background: rgba(243,244,246,0.92); color: #1F2937; }
.plat-default  { background: rgba(255,255,255,0.20); color: white; }
.match-pill {
  font-size: 0.68rem;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: var(--radius-full);
  background: rgba(79,70,229,0.88);
  color: white;
  backdrop-filter: blur(6px);
}
/* Card body */
.crd-body { padding: 16px 18px 14px; }
.crd-title {
  font-size: 0.97rem;
  font-weight: 700;
  color: var(--text-1);
  line-height: 1.38;
  margin: 0 0 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.crd-instructor {
  font-size: 0.78rem;
  color: var(--text-4);
  margin: 0 0 10px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.crd-tags { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 11px; }
.crd-tag {
  font-size: 0.7rem;
  font-weight: 500;
  color: var(--text-3);
  background: var(--bg-muted);
  padding: 2px 8px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border);
  white-space: nowrap;
}
.crd-meta {
  display: flex;
  align-items: center;
  gap: 7px;
  flex-wrap: wrap;
}
/* Partial star */
.stars-wrap {
  position: relative;
  display: inline-block;
  font-size: 12px;
  line-height: 1;
}
.stars-base { color: #E5E7EB; letter-spacing: 1px; }
.stars-fill {
  position: absolute; top: 0; left: 0;
  overflow: hidden;
  color: #F59E0B;
  white-space: nowrap;
  letter-spacing: 1px;
}
.stars-num { font-size: 0.78rem; font-weight: 600; color: var(--text-2); }
.meta-dot { width: 3px; height: 3px; border-radius: 50%; background: var(--border); display: inline-block; }
.level-pill {
  font-size: 0.68rem; font-weight: 600;
  padding: 2px 8px; border-radius: var(--radius-full);
}
.lp-beg { background: #D1FAE5; color: #065F46; }
.lp-int { background: #FEF3C7; color: #92400E; }
.lp-adv { background: #FEE2E2; color: #991B1B; }
.price-free { font-size: 0.78rem; font-weight: 600; color: #059669; }
.price-paid { font-size: 0.78rem; font-weight: 600; color: #7C3AED; }
/* Card view link (anchor inside HTML) */
.crd-view {
  display: block;
  margin: 12px 0 0;
  padding: 9px 0;
  text-align: center;
  background: var(--accent);
  color: white !important;
  font-size: 0.82rem;
  font-weight: 600;
  border-radius: var(--radius-md);
  text-decoration: none;
  transition: background var(--transition);
}
.crd-view:hover { background: var(--accent-hover); }
/* Save button — small ghost below card */
.save-row { margin-bottom: 20px; }
.save-row div[data-testid="stButton"] > button {
  background: var(--bg) !important;
  border: 1px solid var(--border) !important;
  color: var(--text-3) !important;
  border-radius: 0 0 var(--radius-lg) var(--radius-lg) !important;
  font-size: 0.78rem !important;
  padding: 6px 12px !important;
  width: 100% !important;
  border-top: none !important;
}
.save-row div[data-testid="stButton"] > button:hover {
  color: #DC2626 !important;
  border-color: #DC2626 !important;
  background: #FFF1F2 !important;
}
.save-row-saved div[data-testid="stButton"] > button {
  color: #DC2626 !important;
  background: #FFF1F2 !important;
  border-color: #FCA5A5 !important;
}

/* ── Skill path banner ───────────────────────────────────────────────────── */
.path-banner {
  border: 1px solid #C7D2FE;
  border-radius: var(--radius-lg);
  background: var(--accent-light);
  padding: 20px 24px;
  margin-bottom: 20px;
  animation: fadeUp 0.3s ease both;
}
.path-banner-title {
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--accent);
  margin: 0 0 6px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.path-banner-name {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text-1);
  margin: 0 0 4px;
}
.path-banner-desc {
  font-size: 0.82rem;
  color: var(--text-3);
  margin: 0 0 14px;
}
.path-steps-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.path-step-chip {
  display: inline-flex; align-items: center; gap: 7px;
  background: white;
  border: 1px solid #C7D2FE;
  border-radius: var(--radius-full);
  padding: 5px 12px;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--accent);
}
.step-n {
  background: var(--accent);
  color: white;
  border-radius: 50%;
  width: 18px; height: 18px;
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 0.65rem; font-weight: 800;
  flex-shrink: 0;
}

/* ── Section headers ─────────────────────────────────────────────────────── */
.sec-hd {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-1);
  margin: 2rem 0 0.9rem;
}

/* ── Popular topic chips ─────────────────────────────────────────────────── */
.topic-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 8px; }
.topic-chip {
  font-family: var(--font);
  font-size: 0.82rem; font-weight: 500;
  padding: 7px 16px;
  border-radius: var(--radius-full);
  border: 1.5px solid var(--border);
  background: var(--bg);
  color: var(--text-2);
  cursor: pointer;
  transition: all var(--transition);
  text-decoration: none;
  display: inline-block;
}
.topic-chip:hover { border-color: var(--accent); color: var(--accent); background: var(--accent-light); }

/* ── Category grid ───────────────────────────────────────────────────────── */
.cat-card {
  border: 1.5px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px 16px;
  text-align: center;
  background: var(--bg);
  cursor: pointer;
  transition: all var(--transition);
  box-shadow: var(--shadow-sm);
}
.cat-card:hover { border-color: var(--accent); background: var(--accent-light); box-shadow: var(--shadow-md); }
.cat-card.active { border-color: var(--accent); background: var(--accent-light); }
.cat-icon { font-size: 1.5rem; margin-bottom: 8px; }
.cat-label { font-size: 0.8rem; font-weight: 600; color: var(--text-2); }
.cat-count { font-size: 0.7rem; color: var(--text-4); margin-top: 2px; }

/* ── Saved drawer ────────────────────────────────────────────────────────── */
.drawer-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}
.drawer-title { font-size: 1rem; font-weight: 700; color: var(--text-1); }
.saved-compact-card {
  display: flex; gap: 12px; align-items: flex-start;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
  animation: fadeUp 0.25s ease both;
}
.scc-thumb {
  width: 56px; height: 44px;
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}
.scc-title { font-size: 0.85rem; font-weight: 600; color: var(--text-1); line-height: 1.35; margin-bottom: 3px; }
.scc-meta  { font-size: 0.73rem; color: var(--text-4); }

/* ── Empty state ─────────────────────────────────────────────────────────── */
.empty-state {
  text-align: center; padding: 4rem 2rem;
  animation: fadeUp 0.3s ease both;
}
.empty-icon { font-size: 2.5rem; margin-bottom: 14px; opacity: 0.4; }
.empty-title { font-size: 1rem; font-weight: 600; color: var(--text-1); margin-bottom: 6px; }
.empty-sub   { font-size: 0.85rem; color: var(--text-4); }

/* ── Dark mode toggle ────────────────────────────────────────────────────── */
.dm-btn {
  padding: 7px 13px;
  border-radius: var(--radius-full);
  border: 1.5px solid var(--border);
  background: var(--bg);
  color: var(--text-3);
  font-size: 0.82rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition);
  font-family: var(--font);
}
.dm-btn:hover { border-color: var(--accent); color: var(--accent); }

/* ── Keyboard hint ───────────────────────────────────────────────────────── */
.search-hint {
  display: flex; align-items: center; gap: 8px;
  padding: 0 20px;
  font-size: 0.72rem; color: var(--text-4);
  margin-top: 6px;
}
.kbd {
  display: inline-flex; align-items: center; justify-content: center;
  background: var(--bg-muted); border: 1px solid var(--border);
  border-radius: 4px; padding: 1px 5px;
  font-size: 0.68rem; font-weight: 600; color: var(--text-3);
  font-family: monospace;
}

/* ── Columns gap ─────────────────────────────────────────────────────────── */
div[data-testid="stHorizontalBlock"] { gap: 16px !important; align-items: start !important; }
div[data-testid="column"] { padding: 0 !important; }

/* ── Skeleton loader ─────────────────────────────────────────────────────── */
.skeleton {
  background: linear-gradient(90deg, var(--bg-muted) 25%, var(--border) 50%, var(--bg-muted) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
  border-radius: var(--radius-sm);
}
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
.sk-card { height: 300px; border-radius: var(--radius-lg); margin-bottom: 4px; }
.sk-btn  { height: 36px;  border-radius: var(--radius-md); margin-bottom: 20px; }

/* ── Reduced motion ──────────────────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}

/* ── Focus rings ─────────────────────────────────────────────────────────── */
a:focus-visible, button:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
"""

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# KEYBOARD SHORTCUT + DARK MODE JS
# ─────────────────────────────────────────────────────────────────────────────
components.html(f"""
<script>
(function() {{
  // Apply dark mode from session state on every render
  const dark = {'true' if st.session_state.dark else 'false'};
  const root = window.parent.document.documentElement;
  root.setAttribute('data-theme', dark ? 'dark' : 'light');
  // Cmd/Ctrl+K → focus search
  window.parent.document.addEventListener('keydown', function(e) {{
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {{
      e.preventDefault();
      const inp = window.parent.document.querySelector('input[type="text"]');
      if (inp) inp.focus();
    }}
  }});
}})();
</script>
""", height=0)


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
_defaults = dict(
    saved=set(), query="", dark=False,
    show_saved=False, selected_cat=None,
    plat=["Coursera","Udemy","YouTube"],
    lvl=["beginner","intermediate","advanced"],
    free_only=False,
    sort="match",
)
for k, v in _defaults.items():
    if k not in st.session_state: st.session_state[k] = v


# ─────────────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading…")
def load_rec(): return CourseRecommender("data/courses.json")
rec = load_rec()
courses = rec.courses

PLAT_CFG = {
    "Coursera": {"cls": "plat-coursera", "thumb": "thumb-coursera"},
    "Udemy":    {"cls": "plat-udemy",    "thumb": "thumb-udemy"},
    "YouTube":  {"cls": "plat-youtube",  "thumb": "thumb-youtube"},
    "edX":      {"cls": "plat-edx",      "thumb": "thumb-edx"},
}
LEVEL_CFG = {
    "beginner":     ("Beginner",     "lp-beg"),
    "intermediate": ("Intermediate", "lp-int"),
    "advanced":     ("Advanced",     "lp-adv"),
}
CAT_ICONS = {
    "Machine Learning":"🤖","Deep Learning":"🧠","Data Science":"📊","Python":"🐍",
    "JavaScript":"⚡","Web Development":"🌐","Frontend Development":"🎨",
    "Backend Development":"⚙️","Mobile Development":"📱","Databases":"🗄️",
    "DevOps":"🔧","Cloud Computing":"☁️","Cybersecurity":"🔐",
    "Statistics & Math":"📐","Data Engineering":"🔩","AI":"✦",
    "Languages":"💬","Music":"🎵","Photography":"📸","Finance":"💰",
    "Design":"✏️","Marketing":"📣","Programming":"💻","Computer Science":"🖥️",
    "Health & Fitness":"🏃","Cooking":"🍳","Art":"🎨","Business":"💼",
}
TOPICS = [
    "Machine Learning","Data Science","Python","Web Development","AI",
    "JavaScript","SQL","Deep Learning","Design","Finance",
]
SORT_OPTIONS = {"match": "Best match", "rating": "Highest rated", "free": "Free first"}


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def stars_html(rating: float) -> str:
    pct = (rating / 5) * 100
    return (
        f'<span class="stars-wrap">'
        f'<span class="stars-base">★★★★★</span>'
        f'<span class="stars-fill" style="width:{pct}%">★★★★★</span>'
        f'</span>'
    )

def render_card(c: dict, idx: int = 0):
    cid   = c["id"]
    plat  = c["platform"]
    pc    = PLAT_CFG.get(plat, {"cls":"plat-default","thumb":"thumb-default"})
    score = int(c.get("score", c["rating"]/5) * 100)
    tags  = c.get("tags", [])[:3]
    lname, lcls = LEVEL_CFG.get(c["level"], ("Beginner","lp-beg"))
    free  = c.get("price") in ("Free", "Free to audit")
    saved = cid in st.session_state.saved

    tags_html = "".join(f'<span class="crd-tag">{t}</span>' for t in tags)
    score_html = f'<span class="match-pill">{score}%</span>' if score > 0 else ""

    delay = f"animation-delay:{idx*0.04:.2f}s"

    st.markdown(f"""
    <div class="crd" style="{delay}">
      <div class="crd-thumb">
        <div class="crd-thumb-inner {pc['thumb']}">
          <span class="crd-thumb-text">{c['title']}</span>
        </div>
        <div class="thumb-badges">
          <span class="{pc['cls']} plat-pill">{plat}</span>
          {score_html}
        </div>
      </div>
      <div class="crd-body">
        <h3 class="crd-title">{c['title']}</h3>
        <p class="crd-instructor">{c.get('instructor','—')} · {c.get('duration','N/A')}</p>
        <div class="crd-tags">{tags_html}</div>
        <div class="crd-meta">
          {stars_html(c['rating'])}
          <span class="stars-num">{c['rating']}</span>
          <span class="meta-dot"></span>
          <span class="level-pill {lcls}">{lname}</span>
          <span class="meta-dot"></span>
          <span class="{'price-free' if free else 'price-paid'}">{'Free' if free else 'Paid'}</span>
        </div>
        <a href="{c['url']}" class="crd-view" target="_blank" rel="noopener">View Course →</a>
      </div>
    </div>
    """, unsafe_allow_html=True)

    save_lbl = "♥  Saved" if saved else "♡  Save"
    st.markdown(f'<div class="save-row {"save-row-saved" if saved else ""}">', unsafe_allow_html=True)
    if st.button(save_lbl, key=f"sv_{cid}_{idx}", use_container_width=True):
        if saved: st.session_state.saved.discard(cid)
        else:     st.session_state.saved.add(cid)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def render_grid(items: list, prefix: str = "g", delay_start: int = 0):
    if not items:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">◎</div>
          <div class="empty-title">No courses found</div>
          <div class="empty-sub">Try different keywords or adjust your filters</div>
        </div>""", unsafe_allow_html=True)
        return
    col_a, col_b = st.columns(2, gap="medium")
    for i, c in enumerate(items):
        with (col_a if i % 2 == 0 else col_b):
            render_card(c, idx=delay_start + i)


def active_filters() -> dict:
    return {
        "platforms": st.session_state.plat,
        "levels":    st.session_state.lvl,
        "price":     "Free only" if st.session_state.free_only else "All",
    }

def apply_sort(results: list) -> list:
    s = st.session_state.sort
    if s == "rating": return sorted(results, key=lambda x: x["rating"], reverse=True)
    if s == "free":   return sorted(results, key=lambda x: x.get("price","Paid") not in ("Free","Free to audit"))
    return results  # match (default, already sorted by score)


# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
logo_svg = """<svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M9 2L2 6l7 4 7-4-7-4z" fill="white"/>
  <path d="M2 10l7 4 7-4" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M2 13l7 4 7-4" stroke="rgba(255,255,255,0.55)" stroke-width="1.5" stroke-linecap="round"/>
</svg>"""

n_saved = len(st.session_state.saved)
saved_active = "active" if st.session_state.show_saved else ""

h1, h2 = st.columns([1, 1])
with h1:
    st.markdown(f"""
    <div class="la-header">
      <div class="la-wordmark">
        <div class="la-logo-box">{logo_svg}</div>
        <div>
          <div class="la-wordmark-text">Learn Anything</div>
          <div class="la-tagline">Semantic course search · Coursera, Udemy, YouTube</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

with h2:
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    hc1, hc2 = st.columns([3, 2], gap="small")
    with hc1:
        if st.button(
            f"{'♥' if n_saved else '♡'}  {n_saved} saved",
            key="toggle_saved",
            type="primary" if st.session_state.show_saved else "secondary",
        ):
            st.session_state.show_saved = not st.session_state.show_saved
            st.rerun()
    with hc2:
        dm_label = "☀  Light" if st.session_state.dark else "◑  Dark"
        if st.button(dm_label, key="dm_toggle", type="secondary"):
            st.session_state.dark = not st.session_state.dark
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# SEARCH BAR
# ─────────────────────────────────────────────────────────────────────────────
query = st.text_input(
    "search",
    value=st.session_state.query,
    placeholder="Find a course — try 'machine learning for beginners'",
    label_visibility="collapsed",
    key="main_q",
)
if query != st.session_state.query:
    st.session_state.query = query
    st.session_state.show_saved = False
    st.session_state.selected_cat = None

st.markdown(
    '<div class="search-hint">'
    '<span class="kbd">⌘</span><span class="kbd">K</span>'
    '<span>to focus search</span></div>',
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# FILTER BAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
f1, _d1, f2, _d2, f3, _d3, f4 = st.columns([3.5, 0.08, 3.2, 0.08, 2.2, 0.08, 2.0])

with f1:
    st.markdown('<div class="filter-label">Platform</div>', unsafe_allow_html=True)
    pc1, pc2, pc3 = st.columns(3, gap="small")
    for col, plat in zip([pc1, pc2, pc3], ["Coursera", "Udemy", "YouTube"]):
        with col:
            active = plat in st.session_state.plat
            label = f"{plat} ×" if active else plat
            if st.button(label, key=f"pf_{plat}",
                         type="primary" if active else "secondary",
                         use_container_width=True):
                if active and len(st.session_state.plat) > 1:
                    st.session_state.plat = [p for p in st.session_state.plat if p != plat]
                elif not active:
                    st.session_state.plat = st.session_state.plat + [plat]
                st.rerun()

with _d1:
    st.markdown('<div class="filter-divider" style="margin-top:30px"></div>', unsafe_allow_html=True)

with f2:
    st.markdown('<div class="filter-label">Level</div>', unsafe_allow_html=True)
    lc1, lc2, lc3 = st.columns(3, gap="small")
    levels = [("beginner","Beginner"), ("intermediate","Inter."), ("advanced","Advanced")]
    for col, (lv, lb) in zip([lc1, lc2, lc3], levels):
        with col:
            active = lv in st.session_state.lvl
            label = f"{lb} ×" if active else lb
            if st.button(label, key=f"lf_{lv}",
                         type="primary" if active else "secondary",
                         use_container_width=True):
                if active and len(st.session_state.lvl) > 1:
                    st.session_state.lvl = [l for l in st.session_state.lvl if l != lv]
                elif not active:
                    st.session_state.lvl = st.session_state.lvl + [lv]
                st.rerun()

with _d2:
    st.markdown('<div class="filter-divider" style="margin-top:30px"></div>', unsafe_allow_html=True)

with f3:
    st.markdown('<div class="filter-label">Price</div>', unsafe_allow_html=True)
    if st.button(
        "Free only ×" if st.session_state.free_only else "Free only",
        key="ff_free",
        type="primary" if st.session_state.free_only else "secondary",
        use_container_width=True,
    ):
        st.session_state.free_only = not st.session_state.free_only
        st.rerun()

with _d3:
    st.markdown('<div class="filter-divider" style="margin-top:30px"></div>', unsafe_allow_html=True)

with f4:
    st.markdown('<div class="filter-label">Sort</div>', unsafe_allow_html=True)
    opts = list(SORT_OPTIONS.keys())
    labels = [SORT_OPTIONS[o] for o in opts]
    cur_idx = opts.index(st.session_state.sort)
    choice = st.selectbox("sort", labels, index=cur_idx, label_visibility="collapsed", key="sort_sel")
    new_sort = opts[labels.index(choice)]
    if new_sort != st.session_state.sort:
        st.session_state.sort = new_sort
        st.rerun()

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SAVED COURSES VIEW
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.show_saved:
    saved_courses = [c for c in courses if c["id"] in st.session_state.saved]
    st.markdown('<div class="result-header"><span class="result-count">Saved courses</span></div>', unsafe_allow_html=True)

    if not saved_courses:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">♡</div>
          <div class="empty-title">No saved courses yet</div>
          <div class="empty-sub">Click "Save" on any course card to bookmark it here</div>
        </div>""", unsafe_allow_html=True)
    else:
        ca, cb = st.columns([5, 2])
        with cb:
            lines = [f"- [{c['title']}]({c['url']}) — {c['platform']} ⭐{c['rating']}" for c in saved_courses]
            st.download_button("Export as Markdown", "\n".join(lines), "courses.md", "text/markdown", use_container_width=True)
        render_grid([{**c,"score": c["rating"]/5} for c in saved_courses], prefix="saved")

# ─────────────────────────────────────────────────────────────────────────────
# SEARCH RESULTS
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.query:
    q = st.session_state.query

    # Skill path banner
    path = rec.detect_skill_path(q)
    if path:
        steps = "".join(
            f'<span class="path-step-chip"><span class="step-n">{i+1}</span>{s["stage_name"]}</span>'
            for i, s in enumerate(path["stages"])
        )
        st.markdown(f"""
        <div class="path-banner">
          <div class="path-banner-title">Learning path detected</div>
          <div class="path-banner-name">{path['icon']} {path['title']}</div>
          <div class="path-banner-desc">{path['description']}</div>
          <div class="path-steps-row">{steps}</div>
        </div>""", unsafe_allow_html=True)

    # Fetch + sort
    with st.spinner(""):
        results = rec.search(q, top_k=12, filters=active_filters())
    results = apply_sort(results)

    # Result header
    if results:
        plat_counts = {}
        for r in results: plat_counts[r["platform"]] = plat_counts.get(r["platform"], 0) + 1
        breakdown = " · ".join(f"{p} {n}" for p, n in sorted(plat_counts.items()))
        st.markdown(f"""
        <div class="result-header">
          <span class="result-count">{len(results)} results for <em>"{q}"</em></span>
          <span class="result-meta">{breakdown}</span>
        </div>""", unsafe_allow_html=True)

    render_grid(results, prefix="res")

# ─────────────────────────────────────────────────────────────────────────────
# LANDING STATE
# ─────────────────────────────────────────────────────────────────────────────
else:
    # Popular topics
    st.markdown('<div class="sec-hd">Popular topics</div>', unsafe_allow_html=True)
    cols_t = st.columns(len(TOPICS), gap="small")
    for i, topic in enumerate(TOPICS):
        with cols_t[i]:
            if st.button(topic, key=f"tp_{topic}", use_container_width=True, type="secondary"):
                st.session_state.query = topic.lower()
                st.rerun()

    # Career paths
    st.markdown('<div class="sec-hd">Career paths</div>', unsafe_allow_html=True)
    path_keys = list(SKILL_PATHS.keys())
    path_cols = st.columns(5, gap="small")
    for i, pk in enumerate(path_keys[:10]):
        pd = SKILL_PATHS[pk]
        with path_cols[i % 5]:
            if st.button(f"{pd['icon']}  {pd['title']}", key=f"lp_{pk}", use_container_width=True, type="secondary"):
                st.session_state.query = pk
                st.rerun()

    # Trending picks
    st.markdown('<div class="sec-hd">Trending now</div>', unsafe_allow_html=True)
    trending = []
    for tq in ["machine learning beginners","react javascript","data science","guitar beginners"]:
        r = rec.search(tq, top_k=1)
        if r: trending.append(r[0])
    render_grid(trending, prefix="trend")
