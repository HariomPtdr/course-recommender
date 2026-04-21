import streamlit as st
from recommender import CourseRecommender, SKILL_PATHS

st.set_page_config(
    page_title="Learn Anything",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main .block-container { padding: 2rem 3rem 4rem; max-width: 1100px; margin: 0 auto; }
[data-testid="collapsedControl"] { display: none; }

/* Hero */
.hero { text-align: center; padding: 3rem 1rem 1.5rem; }
.hero-title {
    font-size: 3rem; font-weight: 800; margin: 0 0 8px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub { font-size: 1.1rem; color: #6b7280; margin: 0; }

/* Search input */
div[data-testid="stTextInput"] input {
    font-size: 1.1rem !important;
    padding: 16px 20px !important;
    border-radius: 50px !important;
    border: 2px solid #e5e7eb !important;
    box-shadow: 0 4px 20px rgba(102,126,234,.12) !important;
    transition: all .2s !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #667eea !important;
    box-shadow: 0 4px 30px rgba(102,126,234,.25) !important;
    outline: none !important;
}

/* Filter chips */
div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button {
    border-radius: 50px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 6px 18px !important;
    transition: all .15s !important;
}

/* Result count badge */
.result-info {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0 4px; margin-bottom: 8px;
}
.result-count { font-size: 0.85rem; color: #9ca3af; font-weight: 500; }

/* Course card */
.card {
    background: white;
    border: 1px solid #f0f0f0;
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,.04);
    transition: transform .18s ease, box-shadow .18s ease;
    animation: fadeUp .35s ease both;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(102,126,234,.15);
}
@keyframes fadeUp {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0);    }
}
.card-bar { position:absolute; top:0; left:0; right:0; height:3px; border-radius:16px 16px 0 0; }
.bar-coursera { background: linear-gradient(90deg,#0056d2,#3b82f6); }
.bar-udemy    { background: linear-gradient(90deg,#a435f0,#c084fc); }
.bar-youtube  { background: linear-gradient(90deg,#ff0000,#f97316); }

.card-platform { font-size:.72rem; font-weight:700; letter-spacing:.04em; text-transform:uppercase; margin-bottom:8px; }
.plat-coursera { color:#0056d2; } .plat-udemy { color:#a435f0; } .plat-youtube { color:#dc2626; }
.card-title { font-size:1.05rem; font-weight:700; color:#111827; margin:0 0 3px; line-height:1.3; }
.card-meta  { font-size:.8rem; color:#9ca3af; margin-bottom:10px; }
.card-desc  { font-size:.85rem; color:#4b5563; line-height:1.6; margin-bottom:12px; }
.card-footer { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; }
.card-badges { display:flex; gap:6px; flex-wrap:wrap; }
.badge {
    display:inline-block; padding:3px 10px; border-radius:20px;
    font-size:.72rem; font-weight:600;
}
.b-beg  { background:#d1fae5; color:#065f46; }
.b-int  { background:#fef3c7; color:#92400e; }
.b-adv  { background:#fee2e2; color:#991b1b; }
.b-free { background:#ecfdf5; color:#059669; border:1px solid #a7f3d0; }
.b-paid { background:#f5f3ff; color:#7c3aed; }
.rating { font-size:.88rem; font-weight:700; color:#f59e0b; }

/* Tags */
.tags { display:flex; flex-wrap:wrap; gap:5px; margin-top:10px; }
.tag  { background:#f3f4f6; color:#374151; padding:2px 9px; border-radius:6px; font-size:.72rem; }

/* Skill path banner */
.path-box {
    background: linear-gradient(135deg,#667eea,#764ba2);
    border-radius:16px; padding:22px 26px; margin-bottom:24px; color:white;
    animation: fadeUp .4s ease both;
}
.path-box h3 { margin:0 0 4px; font-size:1.25rem; }
.path-box p  { margin:0 0 18px; opacity:.88; font-size:.9rem; }
.path-steps  { display:flex; gap:0; flex-wrap:wrap; }
.path-step {
    display:flex; align-items:center; gap:8px;
    background:rgba(255,255,255,.15); border-radius:10px;
    padding:8px 14px; margin:4px;
    font-size:.82rem; font-weight:600; white-space:nowrap;
}
.step-num {
    background:rgba(255,255,255,.3); border-radius:50%;
    width:22px; height:22px; display:flex; align-items:center;
    justify-content:center; font-weight:800; font-size:.75rem; flex-shrink:0;
}

/* Saved heart */
.saved-bar { background:#fff7ed; border:1px solid #fed7aa; border-radius:12px; padding:12px 16px; margin-bottom:16px; font-size:.88rem; color:#92400e; }

/* Empty state */
.empty { text-align:center; padding:4rem 2rem; color:#9ca3af; }
.empty-icon { font-size:3rem; margin-bottom:12px; }

/* Section header */
.sec-header { font-size:1.1rem; font-weight:700; color:#111827; margin:20px 0 12px; padding-bottom:8px; border-bottom:2px solid #f3f4f6; }
</style>
""", unsafe_allow_html=True)


# ── Init ───────────────────────────────────────────────────────────────────────
for k, v in {
    "saved": set(), "query": "",
    "plat": ["Coursera", "Udemy", "YouTube"],
    "lvl":  ["beginner", "intermediate", "advanced"],
    "free": False, "show_saved": False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


@st.cache_resource(show_spinner="Loading…")
def load():
    return CourseRecommender("data/courses.json")

rec = load()


# ── Helpers ────────────────────────────────────────────────────────────────────
PLAT_ICON = {"Coursera": "🎓", "Udemy": "🎯", "YouTube": "▶️"}

def rating_str(r):   return "★" * int(round(r)) + "☆" * (5 - int(round(r)))
def level_cls(l):    return {"beginner": "b-beg", "intermediate": "b-int", "advanced": "b-adv"}.get(l, "b-beg")
def is_free(c):      return c.get("price") in ("Free", "Free to audit")

def render_card(c, idx=0):
    plat   = c["platform"]
    bar    = plat.lower()
    p_cls  = f"plat-{bar}"
    tags   = "".join(f'<span class="tag">{t}</span>' for t in c.get("tags", [])[:4])
    free_b = '<span class="badge b-free">Free</span>' if is_free(c) else '<span class="badge b-paid">Paid</span>'
    lvl_b  = f'<span class="badge {level_cls(c["level"])}">{c["level"].capitalize()}</span>'
    score  = f'<span style="font-size:.75rem;color:#c4b5fd;margin-left:auto">Match {int(c.get("score",0)*100)}%</span>' if "score" in c else ""

    st.markdown(f"""
    <div class="card" style="animation-delay:{idx*0.05:.2f}s">
        <div class="card-bar bar-{bar}"></div>
        <div class="card-platform {p_cls}">{PLAT_ICON.get(plat,'')} {plat}</div>
        <div class="card-title">{c['title']}</div>
        <div class="card-meta">by {c.get('instructor','—')} &nbsp;·&nbsp; {c.get('duration','N/A')}</div>
        <div class="card-desc">{c['description'][:190]}{'…' if len(c['description'])>190 else ''}</div>
        <div class="card-footer">
            <div class="card-badges">{lvl_b} {free_b} <span class="rating">{rating_str(c['rating'])} {c['rating']}</span></div>
            {score}
        </div>
        <div class="tags">{tags}</div>
    </div>
    """, unsafe_allow_html=True)

    ca, cb = st.columns([2, 1])
    with ca:
        st.link_button("View Course →", c["url"], use_container_width=True)
    with cb:
        saved = c["id"] in st.session_state.saved
        label = "❤️ Saved" if saved else "🤍 Save"
        if st.button(label, key=f"save_{c['id']}_{idx}", use_container_width=True):
            if saved:
                st.session_state.saved.discard(c["id"])
            else:
                st.session_state.saved.add(c["id"])
            st.rerun()


def render_grid(courses, key="g"):
    if not courses:
        st.markdown('<div class="empty"><div class="empty-icon">🔍</div><p>No courses match. Try different filters.</p></div>', unsafe_allow_html=True)
        return
    col1, col2 = st.columns(2, gap="medium")
    for i, c in enumerate(courses):
        with (col1 if i % 2 == 0 else col2):
            render_card(c, idx=i)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">🎓 Learn Anything</div>
  <p class="hero-sub">Search 100+ curated courses from Coursera, Udemy &amp; YouTube</p>
</div>
""", unsafe_allow_html=True)

# Search box
query = st.text_input("", placeholder="What do you want to learn?  e.g. machine learning, guitar, Spanish for travel…",
                      value=st.session_state.query, label_visibility="collapsed")
if query != st.session_state.query:
    st.session_state.query = query

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Inline filters ─────────────────────────────────────────────────────────────
fc1, _sp, fc2, _sp2, fc3 = st.columns([3.5, 0.2, 3.5, 0.2, 2])

with fc1:
    st.caption("Platform")
    pc = st.columns(3)
    for i, p in enumerate(["Coursera", "Udemy", "YouTube"]):
        with pc[i]:
            active = p in st.session_state.plat
            if st.button(
                f"{PLAT_ICON[p]} {p}",
                key=f"p_{p}",
                type="primary" if active else "secondary",
                use_container_width=True,
            ):
                if active:
                    if len(st.session_state.plat) > 1:
                        st.session_state.plat = [x for x in st.session_state.plat if x != p]
                else:
                    st.session_state.plat = st.session_state.plat + [p]
                st.rerun()

with fc2:
    st.caption("Level")
    lc = st.columns(3)
    for i, (l, label) in enumerate([("beginner","Beginner"),("intermediate","Inter."),("advanced","Advanced")]):
        with lc[i]:
            active = l in st.session_state.lvl
            if st.button(label, key=f"l_{l}", type="primary" if active else "secondary", use_container_width=True):
                if active:
                    if len(st.session_state.lvl) > 1:
                        st.session_state.lvl = [x for x in st.session_state.lvl if x != l]
                else:
                    st.session_state.lvl = st.session_state.lvl + [l]
                st.rerun()

with fc3:
    st.caption("Price")
    oc1, oc2 = st.columns(2)
    with oc1:
        if st.button("🆓 Free", key="free_tog",
                     type="primary" if st.session_state.free else "secondary",
                     use_container_width=True):
            st.session_state.free = not st.session_state.free
            st.rerun()
    with oc2:
        n_saved = len(st.session_state.saved)
        if st.button(f"❤️ {n_saved}" if n_saved else "❤️ 0", key="saved_tog",
                     type="primary" if st.session_state.show_saved else "secondary",
                     use_container_width=True):
            st.session_state.show_saved = not st.session_state.show_saved
            st.rerun()

st.markdown("<hr style='border:none;border-top:1px solid #f3f4f6;margin:18px 0 12px'>", unsafe_allow_html=True)

# ── Saved view ─────────────────────────────────────────────────────────────────
if st.session_state.show_saved:
    if not st.session_state.saved:
        st.markdown('<div class="empty"><div class="empty-icon">🤍</div><h3 style="color:#374151">No saved courses yet</h3><p>Click Save on any course.</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sec-header">❤️ Saved Courses</div>', unsafe_allow_html=True)
        saved_list = [{**c, "score": c["rating"]/5} for c in rec.courses if c["id"] in st.session_state.saved]
        render_grid(saved_list, key="saved")

        sa, sb = st.columns(2)
        with sa:
            lines = [f"- [{c['title']}]({c['url']}) — {c['platform']} ⭐{c['rating']}" for c in saved_list]
            st.download_button("⬇️ Download list (.md)", "\n".join(lines), "my_courses.md", "text/markdown", use_container_width=True)
        with sb:
            if st.button("🗑️ Clear all saved", use_container_width=True):
                st.session_state.saved = set(); st.rerun()

# ── Main results ───────────────────────────────────────────────────────────────
elif st.session_state.query:
    q = st.session_state.query
    filters = {
        "platforms": st.session_state.plat,
        "levels":    st.session_state.lvl,
        "price":     "Free only" if st.session_state.free else "All",
    }

    # Skill path detection
    path = rec.detect_skill_path(q)
    if path:
        steps_html = "".join(
            f'<div class="path-step"><div class="step-num">{i+1}</div>{s["stage_name"]}</div>'
            for i, s in enumerate(path["stages"])
        )
        st.markdown(f"""
        <div class="path-box">
            <h3>{path['icon']} {path['title']} — Learning Path</h3>
            <p>{path['description']}</p>
            <div class="path-steps">{steps_html}</div>
        </div>
        """, unsafe_allow_html=True)

    results = rec.search(q, top_k=12, filters=filters)

    if results:
        plat_counts = {}
        for r in results: plat_counts[r["platform"]] = plat_counts.get(r["platform"], 0) + 1
        breakdown = "  ·  ".join(f"{PLAT_ICON.get(p,p)} {p} {n}" for p, n in sorted(plat_counts.items()))
        st.markdown(f'<div class="result-info"><span style="font-weight:700;color:#111">{len(results)} courses for <em>"{q}"</em></span><span class="result-count">{breakdown}</span></div>', unsafe_allow_html=True)

    render_grid(results, key="results")

# ── Landing ────────────────────────────────────────────────────────────────────
else:
    # Quick topic pills
    st.markdown('<div class="sec-header">✨ Popular Topics</div>', unsafe_allow_html=True)
    topics = [
        ("🤖","Machine Learning"),("🧠","Deep Learning"),("🐍","Python"),
        ("🌐","Web Development"),("📊","Data Science"),("🎸","Guitar"),
        ("🗣️","Spanish"),("📸","Photography"),("💰","Finance"),("☁️","Cloud"),
    ]
    rows = [topics[:5], topics[5:]]
    for row in rows:
        cols = st.columns(5)
        for i, (icon, topic) in enumerate(row):
            with cols[i]:
                if st.button(f"{icon} {topic}", key=f"topic_{topic}", use_container_width=True):
                    st.session_state.query = topic.lower()
                    st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Skill paths
    st.markdown('<div class="sec-header">🗺️ Career Paths</div>', unsafe_allow_html=True)
    path_items = list(SKILL_PATHS.items())
    pcols = st.columns(5)
    for i, (pk, pd) in enumerate(path_items[:10]):
        with pcols[i % 5]:
            if st.button(f"{pd['icon']}\n{pd['title']}", key=f"lp_{pk}", use_container_width=True):
                st.session_state.query = pk
                st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Trending courses
    st.markdown('<div class="sec-header">🔥 Trending Courses</div>', unsafe_allow_html=True)
    trending = []
    for tq in ["machine learning beginners", "javascript react", "data science python", "guitar beginners"]:
        r = rec.search(tq, top_k=1)
        if r: trending.append({**r[0], "score": r[0]["score"]})
    render_grid(trending, key="trend")
