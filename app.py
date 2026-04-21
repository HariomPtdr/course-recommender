import streamlit as st
from recommender import CourseRecommender, SKILL_PATHS

st.set_page_config(
    page_title="Learn Anything — Course Recommender",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

*, body, .stApp { font-family: 'Inter', sans-serif; }
.main .block-container { padding-top: 1rem; max-width: 1200px; }
.stTabs [data-baseweb="tab-list"] { gap: 8px; background: #f8faff; padding: 6px; border-radius: 12px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px; padding: 6px 18px; font-weight: 600; }
.stTabs [aria-selected="true"] { background: white !important; box-shadow: 0 2px 8px rgba(102,126,234,0.2); }

/* Hero */
.hero { background: linear-gradient(135deg,#667eea 0%,#764ba2 100%); border-radius:16px; padding:32px 36px; color:white; margin-bottom:24px; }
.hero h1 { font-size:2.4rem; font-weight:800; margin:0 0 8px 0; }
.hero p  { font-size:1.05rem; opacity:0.9; margin:0; }

/* Stats bar */
.stats-bar { display:flex; gap:24px; background:#f8faff; border-radius:12px; padding:14px 20px; margin-bottom:20px; flex-wrap:wrap; }
.stat-item { text-align:center; }
.stat-num { font-size:1.4rem; font-weight:800; color:#667eea; display:block; }
.stat-label { font-size:0.75rem; color:#6b7280; font-weight:500; }

/* Search bar */
div[data-testid="stTextInput"] input {
    font-size: 1.05rem !important;
    padding: 14px 18px !important;
    border-radius: 12px !important;
    border: 2px solid #e5e7eb !important;
    transition: border 0.2s;
}
div[data-testid="stTextInput"] input:focus { border-color: #667eea !important; box-shadow: 0 0 0 3px rgba(102,126,234,0.15) !important; }

/* Quick filter chips */
.chip-row { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:12px; }
.chip { display:inline-block; padding:5px 14px; border-radius:20px; font-size:0.8rem; font-weight:600; cursor:pointer; border:2px solid transparent; transition:all 0.15s; }
.chip-active { background:#667eea; color:white; border-color:#667eea; }
.chip-inactive { background:white; color:#6b7280; border-color:#e5e7eb; }
.chip-inactive:hover { border-color:#667eea; color:#667eea; }

/* Course card */
.course-card {
    border:1px solid #e5e7eb; border-radius:14px; padding:18px 20px;
    margin-bottom:12px; background:white; position:relative; overflow:hidden;
    transition: transform 0.15s, box-shadow 0.15s;
}
.course-card:hover { transform:translateY(-2px); box-shadow:0 8px 30px rgba(0,0,0,0.1); }
.card-accent { position:absolute; top:0; left:0; width:4px; height:100%; border-radius:4px 0 0 4px; }
.accent-coursera { background:#0056d2; }
.accent-udemy    { background:#a435f0; }
.accent-youtube  { background:#ff0000; }

.course-title { font-size:1rem; font-weight:700; color:#111827; margin:0 0 3px 0; }
.course-instructor { font-size:0.8rem; color:#9ca3af; margin-bottom:8px; }
.course-desc { font-size:0.85rem; color:#374151; line-height:1.55; margin-bottom:10px; }
.meta-row { display:flex; gap:6px; flex-wrap:wrap; align-items:center; }

/* Badges */
.badge { display:inline-block; padding:2px 10px; border-radius:20px; font-size:0.72rem; font-weight:700; }
.badge-coursera  { background:#dbeafe; color:#1e40af; }
.badge-udemy     { background:#f3e8ff; color:#6b21a8; }
.badge-youtube   { background:#fee2e2; color:#991b1b; }
.badge-beginner  { background:#d1fae5; color:#065f46; }
.badge-intermediate { background:#fef3c7; color:#92400e; }
.badge-advanced  { background:#fee2e2; color:#991b1b; }
.badge-free      { background:#ecfdf5; color:#059669; border:1px solid #6ee7b7; }
.badge-paid      { background:#f5f3ff; color:#7c3aed; }
.badge-saved     { background:#fef3c7; color:#92400e; }

/* Tag pills */
.tag { display:inline-block; background:#f3f4f6; color:#374151; padding:2px 8px; border-radius:6px; font-size:0.72rem; margin:2px; }

/* Stars */
.stars { color:#f59e0b; font-size:0.9rem; }

/* Match bar */
.match-wrap { display:flex; align-items:center; gap:6px; }
.match-track { background:#e5e7eb; border-radius:4px; height:5px; width:70px; }
.match-fill  { background:linear-gradient(90deg,#667eea,#764ba2); border-radius:4px; height:5px; }

/* Category grid */
.cat-card {
    background:white; border:2px solid #e5e7eb; border-radius:12px; padding:20px;
    text-align:center; cursor:pointer; transition:all 0.15s;
}
.cat-card:hover, .cat-card.selected { border-color:#667eea; background:#f5f3ff; }
.cat-icon { font-size:2rem; margin-bottom:6px; }
.cat-name { font-size:0.85rem; font-weight:700; color:#374151; }
.cat-count { font-size:0.75rem; color:#9ca3af; }

/* Skill path */
.path-banner {
    background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
    color:white; border-radius:14px; padding:22px 26px; margin-bottom:20px;
}
.path-banner h2 { margin:0 0 4px 0; font-size:1.4rem; }
.path-banner p  { margin:0; opacity:0.85; font-size:0.9rem; }

.stage-card {
    background:white; border:2px solid #e5e7eb; border-radius:12px;
    padding:16px 18px; margin-bottom:10px; cursor:pointer; transition:all 0.15s;
}
.stage-card:hover, .stage-card.active { border-color:#667eea; background:#fafbff; }
.stage-num-pill {
    background:linear-gradient(135deg,#667eea,#764ba2);
    color:white; width:30px; height:30px; border-radius:50%;
    display:inline-flex; align-items:center; justify-content:center;
    font-weight:800; font-size:0.8rem; margin-right:12px; vertical-align:middle;
}
.stage-title { font-size:0.92rem; font-weight:700; color:#111827; }
.stage-sub   { font-size:0.8rem; color:#6b7280; margin-top:2px; }

/* Comparison table */
.compare-header { background:#667eea; color:white; padding:10px; text-align:center; border-radius:8px 8px 0 0; font-weight:700; }
.compare-cell   { padding:10px; border-bottom:1px solid #f3f4f6; font-size:0.85rem; }
.compare-label  { color:#9ca3af; font-size:0.75rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em; }

/* Saved empty */
.empty-state { text-align:center; padding:60px 20px; color:#9ca3af; }
.empty-state .e-icon { font-size:3rem; margin-bottom:12px; }
.empty-state h3 { color:#374151; margin:0 0 6px 0; }

/* Search history pill */
.hist-pill { display:inline-block; background:#f3f4f6; border:1px solid #e5e7eb; color:#374151; padding:3px 12px; border-radius:20px; font-size:0.78rem; cursor:pointer; margin:2px; }
.hist-pill:hover { background:#ede9fe; border-color:#c4b5fd; color:#7c3aed; }

/* Notification */
.notif { background:#d1fae5; border:1px solid #6ee7b7; color:#065f46; border-radius:8px; padding:8px 14px; font-size:0.85rem; margin-bottom:10px; }
</style>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
def _init():
    defaults = {
        "bookmarks": set(),
        "search_history": [],
        "compare_list": [],
        "selected_path_key": None,
        "selected_stage_idx": None,
        "selected_category": None,
        "view_mode": "grid",
        "active_tab": 0,
        "last_notif": "",
        "query": "",
        "level_filter": ["beginner", "intermediate", "advanced"],
        "platform_filter": ["Coursera", "Udemy", "YouTube"],
        "price_filter": "All",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()


# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading recommendation engine…")
def load_recommender():
    return CourseRecommender("data/courses.json")

recommender = load_recommender()
all_courses  = recommender.courses
categories   = sorted(set(c.get("category", "Other") for c in all_courses))

CATEGORY_ICONS = {
    "Machine Learning": "🤖", "Deep Learning": "🧠", "Data Science": "📊",
    "Python": "🐍", "JavaScript": "⚡", "Web Development": "🌐",
    "Frontend Development": "🎨", "Backend Development": "⚙️", "Mobile Development": "📱",
    "Databases": "🗄️", "DevOps": "🔧", "Cloud Computing": "☁️",
    "Cybersecurity": "🔐", "Statistics & Math": "📐", "Data Engineering": "🔩",
    "AI": "✨", "Languages": "🗣️", "Music": "🎵", "Photography": "📸",
    "Finance": "💰", "Design": "🖌️", "Marketing": "📢", "Programming": "💻",
    "Computer Science": "🖥️", "Business": "💼", "Project Management": "📋",
    "Blockchain": "⛓️", "Health & Fitness": "🏃", "Cooking": "🍳", "Art": "🎨",
}


# ── Helpers ────────────────────────────────────────────────────────────────────
def notify(msg):
    st.session_state.last_notif = msg

def platform_badge(p):
    icons = {"Coursera": "🎓", "Udemy": "🎯", "YouTube": "▶️"}
    return f'<span class="badge badge-{p.lower()}">{icons.get(p,"")} {p}</span>'

def level_badge(l):
    return f'<span class="badge badge-{l}">{l.capitalize()}</span>'

def price_badge(price):
    is_free = price in ("Free", "Free to audit")
    cls = "badge-free" if is_free else "badge-paid"
    label = "Free to audit" if price == "Free to audit" else ("Free" if is_free else "Paid")
    return f'<span class="badge {cls}">{label}</span>'

def stars_html(rating):
    filled = int(round(rating))
    return f'<span class="stars">{"★"*filled}{"☆"*(5-filled)}</span> <strong style="font-size:0.85rem">{rating}</strong>'

def match_bar(score):
    pct = int(score * 100)
    w = max(4, min(70, int(score * 130)))
    return f'<div class="match-wrap"><span style="font-size:0.73rem;color:#9ca3af">Match {pct}%</span><div class="match-track"><div class="match-fill" style="width:{w}px"></div></div></div>'

def accent_class(platform):
    return f"accent-{platform.lower()}"

def toggle_bookmark(course_id):
    if course_id in st.session_state.bookmarks:
        st.session_state.bookmarks.discard(course_id)
        notify("Removed from saved courses")
    else:
        st.session_state.bookmarks.add(course_id)
        notify("✅ Course saved!")

def toggle_compare(course_id):
    if course_id in st.session_state.compare_list:
        st.session_state.compare_list.remove(course_id)
    else:
        if len(st.session_state.compare_list) < 3:
            st.session_state.compare_list.append(course_id)
        else:
            notify("⚠️ Compare limit is 3 courses. Remove one first.")

def get_course_by_id(cid):
    return next((c for c in all_courses if c["id"] == cid), None)


# ── Card renderer ──────────────────────────────────────────────────────────────
def render_card(course, show_score=True, compact=False, key_prefix="card"):
    cid  = course["id"]
    saved = cid in st.session_state.bookmarks
    in_compare = cid in st.session_state.compare_list
    score_html = match_bar(course["score"]) if show_score and "score" in course else ""
    tags_html = " ".join(f'<span class="tag">{t}</span>' for t in course.get("tags", [])[:5])
    desc = course["description"]
    short_desc = desc[:180] + "…" if len(desc) > 180 else desc

    st.markdown(f"""
    <div class="course-card">
        <div class="card-accent {accent_class(course['platform'])}"></div>
        <div class="course-title">{course['title']}</div>
        <div class="course-instructor">by {course.get('instructor','—')} &nbsp;·&nbsp; {course.get('duration','N/A')}</div>
        <div class="course-desc">{short_desc}</div>
        <div class="meta-row">
            {platform_badge(course['platform'])}
            {level_badge(course['level'])}
            {price_badge(course.get('price','Paid'))}
            {stars_html(course['rating'])}
            {score_html}
        </div>
        <div style="margin-top:8px">{tags_html}</div>
    </div>
    """, unsafe_allow_html=True)

    b1, b2, b3 = st.columns([2, 1.4, 1.4])
    with b1:
        st.link_button("→ View Course", course["url"], use_container_width=True)
    with b2:
        save_label = "❤️ Saved" if saved else "🤍 Save"
        if st.button(save_label, key=f"{key_prefix}_save_{cid}", use_container_width=True):
            toggle_bookmark(cid)
            st.rerun()
    with b3:
        comp_label = "✅ Added" if in_compare else "⚖️ Compare"
        if st.button(comp_label, key=f"{key_prefix}_cmp_{cid}", use_container_width=True):
            toggle_compare(cid)
            st.rerun()


def render_cards_grid(courses, key_prefix="grid", cols=2):
    if not courses:
        st.info("No courses match your current filters.")
        return
    if st.session_state.view_mode == "grid" and len(courses) > 1:
        col_list = st.columns(cols)
        for i, c in enumerate(courses):
            with col_list[i % cols]:
                render_card(c, key_prefix=f"{key_prefix}_{i}")
    else:
        for i, c in enumerate(courses):
            render_card(c, key_prefix=f"{key_prefix}_{i}")


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Filters")

    new_platforms = st.multiselect(
        "Platform", ["Coursera", "Udemy", "YouTube"],
        default=st.session_state.platform_filter,
    )
    new_levels = st.multiselect(
        "Level", ["beginner", "intermediate", "advanced"],
        default=st.session_state.level_filter,
        format_func=str.capitalize,
    )
    new_price = st.radio("Price", ["All", "Free only", "Paid only"], horizontal=True,
                         index=["All", "Free only", "Paid only"].index(st.session_state.price_filter))

    if (new_platforms != st.session_state.platform_filter or
        new_levels != st.session_state.level_filter or
        new_price != st.session_state.price_filter):
        st.session_state.platform_filter = new_platforms
        st.session_state.level_filter    = new_levels
        st.session_state.price_filter    = new_price
        st.rerun()

    top_k = st.slider("Results", 4, 24, 10, step=2)

    st.divider()

    # View toggle
    st.markdown("### 🖼️ View")
    vc1, vc2 = st.columns(2)
    with vc1:
        if st.button("⊞ Grid", use_container_width=True,
                     type="primary" if st.session_state.view_mode == "grid" else "secondary"):
            st.session_state.view_mode = "grid"; st.rerun()
    with vc2:
        if st.button("☰ List", use_container_width=True,
                     type="primary" if st.session_state.view_mode == "list" else "secondary"):
            st.session_state.view_mode = "list"; st.rerun()

    st.divider()

    # Compare tray
    if st.session_state.compare_list:
        st.markdown(f"### ⚖️ Compare ({len(st.session_state.compare_list)}/3)")
        for cid in st.session_state.compare_list:
            c = get_course_by_id(cid)
            if c:
                col_a, col_b = st.columns([4, 1])
                col_a.caption(c["title"][:38] + ("…" if len(c["title"]) > 38 else ""))
                if col_b.button("✕", key=f"rm_cmp_{cid}"):
                    st.session_state.compare_list.remove(cid); st.rerun()
        if st.button("Clear compare", use_container_width=True):
            st.session_state.compare_list = []; st.rerun()
        st.divider()

    # Bookmarks count
    n_saved = len(st.session_state.bookmarks)
    if n_saved:
        st.markdown(f"### ❤️ Saved ({n_saved})")
        st.caption("Switch to the **Saved** tab to view them.")
        st.divider()

    # Search history
    if st.session_state.search_history:
        st.markdown("### 🕐 Recent Searches")
        for h in st.session_state.search_history[-5:][::-1]:
            if st.button(h, key=f"hist_{h}", use_container_width=True):
                st.session_state.query = h; st.rerun()
        if st.button("Clear history", use_container_width=True):
            st.session_state.search_history = []; st.rerun()

    st.divider()
    st.markdown("### 💡 Try these")
    examples = [
        "machine learning beginners",
        "guitar fingerstyle",
        "Spanish for travel",
        "become a data scientist",
        "web developer career",
        "deep learning pytorch",
        "photography basics",
    ]
    for ex in examples:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state.query = ex
            st.rerun()


# ── Notification bar ───────────────────────────────────────────────────────────
if st.session_state.last_notif:
    st.markdown(f'<div class="notif">{st.session_state.last_notif}</div>', unsafe_allow_html=True)
    st.session_state.last_notif = ""


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🎓 Learn Anything</h1>
  <p>Semantic course search across Coursera, Udemy &amp; YouTube — find the perfect course in seconds</p>
</div>
""", unsafe_allow_html=True)

# Stats bar
free_count = sum(1 for c in all_courses if c.get("price") in ("Free", "Free to audit"))
st.markdown(f"""
<div class="stats-bar">
  <div class="stat-item"><span class="stat-num">{len(all_courses)}</span><span class="stat-label">Courses</span></div>
  <div class="stat-item"><span class="stat-num">{len(categories)}</span><span class="stat-label">Categories</span></div>
  <div class="stat-item"><span class="stat-num">{free_count}</span><span class="stat-label">Free Courses</span></div>
  <div class="stat-item"><span class="stat-num">3</span><span class="stat-label">Platforms</span></div>
  <div class="stat-item"><span class="stat-num">{len(SKILL_PATHS)}</span><span class="stat-label">Skill Paths</span></div>
</div>
""", unsafe_allow_html=True)


# ── Compare overlay ────────────────────────────────────────────────────────────
if len(st.session_state.compare_list) >= 2:
    with st.expander(f"⚖️ Compare {len(st.session_state.compare_list)} courses", expanded=True):
        compare_courses = [get_course_by_id(cid) for cid in st.session_state.compare_list if get_course_by_id(cid)]
        cols = st.columns(len(compare_courses))
        fields = [("Platform", "platform"), ("Level", "level"), ("Rating", "rating"),
                  ("Duration", "duration"), ("Price", "price"), ("Instructor", "instructor")]
        for i, course in enumerate(compare_courses):
            with cols[i]:
                st.markdown(f'<div class="compare-header">{course["title"][:45]}</div>', unsafe_allow_html=True)
                for label, key in fields:
                    st.markdown(f'<div class="compare-cell"><div class="compare-label">{label}</div>{course.get(key,"—")}</div>', unsafe_allow_html=True)
                st.link_button("Open Course →", course["url"], use_container_width=True)


# ── Main tabs ─────────────────────────────────────────────────────────────────
tabs = st.tabs(["🔍 Search", "🗂️ Browse", "🗺️ Skill Paths", "❤️ Saved"])

filters = {
    "platforms": st.session_state.platform_filter,
    "levels":    st.session_state.level_filter,
    "price":     st.session_state.price_filter,
}

# ═══════════════════════════════════════════════════
# TAB 1 — SEARCH
# ═══════════════════════════════════════════════════
with tabs[0]:
    query = st.text_input(
        "search",
        value=st.session_state.query,
        placeholder='What do you want to learn? e.g. "machine learning for beginners", "guitar fingerstyle"…',
        label_visibility="collapsed",
        key="main_search",
    )

    # Update session query
    if query != st.session_state.query:
        st.session_state.query = query
        if query and (not st.session_state.search_history or st.session_state.search_history[-1] != query):
            st.session_state.search_history.append(query)

    if query:
        # Skill path detection
        skill_path = recommender.detect_skill_path(query)
        if skill_path:
            st.markdown(f"""
            <div class="path-banner">
                <h2>{skill_path['icon']} {skill_path['title']} Learning Path detected!</h2>
                <p>{skill_path['description']} — scroll down for courses, or visit the <strong>Skill Paths</strong> tab for the full roadmap.</p>
            </div>
            """, unsafe_allow_html=True)

        # Result header
        st.markdown(f"**Results for:** *{query}*")
        rc1, rc2 = st.columns([6, 1])

        with st.spinner("Finding best matches…"):
            results = recommender.search(query, top_k=top_k, filters=filters)

        if not results:
            st.warning("No courses match your filters. Try adjusting platform or level.")
        else:
            with rc2:
                st.caption(f"{len(results)} found")

            # Quick level chips (display only — filter is in sidebar)
            counts = {}
            for r in results:
                counts[r["level"]] = counts.get(r["level"], 0) + 1
            chips = " ".join(
                f'<span class="chip chip-active">{lvl.capitalize()} ({n})</span>'
                for lvl, n in sorted(counts.items())
            )
            st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)

            render_cards_grid(results, key_prefix="search", cols=2)
    else:
        # Landing — trending
        st.markdown("### 🔥 Trending Right Now")
        trending = []
        for q in ["machine learning beginners", "react javascript", "data science python", "guitar beginners"]:
            r = recommender.search(q, top_k=1)
            if r: trending.append(r[0])
        render_cards_grid(trending, key_prefix="trend", cols=2)


# ═══════════════════════════════════════════════════
# TAB 2 — BROWSE BY CATEGORY
# ═══════════════════════════════════════════════════
with tabs[1]:
    st.markdown("### 🗂️ Browse by Category")

    # Category grid
    cat_cols = st.columns(5)
    for i, cat in enumerate(categories):
        icon = CATEGORY_ICONS.get(cat, "📚")
        count = sum(1 for c in all_courses if c.get("category") == cat)
        with cat_cols[i % 5]:
            selected = st.session_state.selected_category == cat
            btn_type = "primary" if selected else "secondary"
            if st.button(f"{icon}\n{cat}\n({count})", key=f"cat_{cat}",
                         use_container_width=True, type=btn_type):
                st.session_state.selected_category = None if selected else cat
                st.rerun()

    st.divider()

    if st.session_state.selected_category:
        cat = st.session_state.selected_category
        icon = CATEGORY_ICONS.get(cat, "📚")
        st.markdown(f"### {icon} {cat}")

        cat_courses = [c for c in all_courses if c.get("category") == cat]
        # Apply filters
        if filters["platforms"]:
            cat_courses = [c for c in cat_courses if c["platform"] in filters["platforms"]]
        if filters["levels"]:
            cat_courses = [c for c in cat_courses if c["level"] in filters["levels"]]

        # Sort by rating
        cat_courses = sorted(cat_courses, key=lambda x: x["rating"], reverse=True)
        st.caption(f"{len(cat_courses)} courses in this category")

        for c in cat_courses:
            c_scored = {**c, "score": c["rating"] / 5.0}
        render_cards_grid([{**c, "score": c["rating"]/5.0} for c in cat_courses],
                          key_prefix="browse", cols=2)
    else:
        st.info("👆 Click any category above to explore its courses.")

        # Show all categories with a quick top course
        st.markdown("### 🌟 Top Pick per Category")
        top_picks = []
        for cat in categories[:8]:
            cat_c = sorted([c for c in all_courses if c.get("category") == cat],
                           key=lambda x: x["rating"], reverse=True)
            if cat_c:
                top_picks.append({**cat_c[0], "score": cat_c[0]["rating"]/5.0})
        render_cards_grid(top_picks, key_prefix="top_pick", cols=2)


# ═══════════════════════════════════════════════════
# TAB 3 — SKILL PATHS
# ═══════════════════════════════════════════════════
with tabs[2]:
    st.markdown("### 🗺️ Skill Paths — Structured Learning Journeys")
    st.caption("Click a path to see your step-by-step course roadmap from beginner to advanced.")

    # Path selector grid
    path_keys = list(SKILL_PATHS.keys())
    path_cols = st.columns(5)
    for i, pk in enumerate(path_keys):
        pdata = SKILL_PATHS[pk]
        with path_cols[i % 5]:
            selected = st.session_state.selected_path_key == pk
            label = f"{pdata['icon']}\n{pdata['title']}"
            if st.button(label, key=f"path_sel_{pk}", use_container_width=True,
                         type="primary" if selected else "secondary"):
                st.session_state.selected_path_key = None if selected else pk
                st.session_state.selected_stage_idx = None
                st.rerun()

    st.divider()

    if st.session_state.selected_path_key:
        pk     = st.session_state.selected_path_key
        pdata  = SKILL_PATHS[pk]
        stages = pdata["stages"]

        st.markdown(f"""
        <div class="path-banner">
            <h2>{pdata['icon']} {pdata['title']}</h2>
            <p>{pdata['description']} &nbsp;·&nbsp; {len(stages)} stages</p>
        </div>
        """, unsafe_allow_html=True)

        # Progress indicator
        done_stages = st.session_state.get("done_stages", set())
        progress = len([s for s in range(len(stages)) if f"{pk}_{s}" in done_stages])
        st.progress(progress / len(stages), text=f"Progress: {progress}/{len(stages)} stages")

        for i, stage in enumerate(stages):
            stage_id = f"{pk}_{i}"
            is_active = st.session_state.selected_stage_idx == i
            is_done   = stage_id in done_stages

            done_mark = "✅ " if is_done else ""
            st.markdown(f"""
            <div class="stage-card {'active' if is_active else ''}">
                <span class="stage-num-pill">{i+1}</span>
                <strong class="stage-title">{done_mark}{stage['name']}</strong>
            </div>
            """, unsafe_allow_html=True)

            sc1, sc2, sc3 = st.columns([2, 1.5, 1.5])
            with sc1:
                if st.button(
                    "▼ Show course" if not is_active else "▲ Hide",
                    key=f"stage_btn_{pk}_{i}", use_container_width=True
                ):
                    st.session_state.selected_stage_idx = None if is_active else i
                    st.rerun()
            with sc2:
                mark_label = "↩ Undo" if is_done else "✅ Mark done"
                if st.button(mark_label, key=f"stage_done_{pk}_{i}", use_container_width=True):
                    if "done_stages" not in st.session_state:
                        st.session_state.done_stages = set()
                    if is_done:
                        st.session_state.done_stages.discard(stage_id)
                    else:
                        st.session_state.done_stages.add(stage_id)
                    st.rerun()
            with sc3:
                if st.button("🔄 Alternatives", key=f"stage_alt_{pk}_{i}", use_container_width=True):
                    st.session_state.selected_stage_idx = i
                    st.rerun()

            # Expanded stage: show recommended + alternatives
            if is_active:
                with st.container():
                    st.markdown(f"**Best match for *{stage['name']}*:**")
                    alts = recommender.search(stage["query"], top_k=3, filters=None)
                    if alts:
                        render_cards_grid(alts, key_prefix=f"path_{pk}_{i}", cols=2 if len(alts) > 1 else 1)

    else:
        st.info("👆 Select a skill path above to begin your learning journey.")


# ═══════════════════════════════════════════════════
# TAB 4 — SAVED COURSES
# ═══════════════════════════════════════════════════
with tabs[3]:
    saved_ids = list(st.session_state.bookmarks)
    saved_courses = [get_course_by_id(cid) for cid in saved_ids if get_course_by_id(cid)]

    if not saved_courses:
        st.markdown("""
        <div class="empty-state">
            <div class="e-icon">🤍</div>
            <h3>No saved courses yet</h3>
            <p>Click <strong>Save</strong> on any course to bookmark it here.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"### ❤️ Saved Courses ({len(saved_courses)})")

        col_a, col_b = st.columns([6, 2])
        with col_b:
            if st.button("🗑️ Clear all saved", use_container_width=True):
                st.session_state.bookmarks = set(); st.rerun()

        # Group by platform
        by_platform = {}
        for c in saved_courses:
            by_platform.setdefault(c["platform"], []).append(c)

        for platform, courses in by_platform.items():
            st.markdown(f"**{platform}** ({len(courses)})")
            render_cards_grid(
                [{**c, "score": c["rating"]/5.0} for c in courses],
                key_prefix=f"saved_{platform}", cols=2
            )

        st.divider()
        # Export as text
        with st.expander("📋 Export saved courses list"):
            lines = []
            for c in saved_courses:
                lines.append(f"- [{c['title']}]({c['url']}) — {c['platform']} | {c['level']} | ⭐{c['rating']}")
            st.code("\n".join(lines), language="markdown")
            st.download_button(
                "⬇️ Download as Markdown",
                "\n".join(lines),
                file_name="my_courses.md",
                mime="text/markdown",
            )
