import streamlit as st
from recommender import CourseRecommender

st.set_page_config(
    page_title="Learn Anything — Course Recommender",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styles ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Global */
.main .block-container { padding-top: 1.5rem; max-width: 1200px; }

/* Search hero */
.hero-title {
    font-size: 2.6rem; font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}
.hero-sub { font-size: 1.1rem; color: #6b7280; margin-top: 0.2rem; margin-bottom: 1.5rem; }

/* Course card */
.course-card {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
    background: white;
    transition: box-shadow 0.2s;
}
.course-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
.course-title { font-size: 1.05rem; font-weight: 700; color: #111827; margin: 0 0 4px 0; }
.course-instructor { font-size: 0.82rem; color: #6b7280; margin-bottom: 6px; }
.course-desc { font-size: 0.87rem; color: #374151; line-height: 1.5; margin-bottom: 10px; }
.meta-row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }

/* Badges */
.badge {
    display: inline-block; padding: 2px 9px; border-radius: 20px;
    font-size: 0.75rem; font-weight: 600;
}
.badge-coursera  { background: #0056d2; color: white; }
.badge-udemy     { background: #a435f0; color: white; }
.badge-youtube   { background: #ff0000; color: white; }
.badge-beginner  { background: #d1fae5; color: #065f46; }
.badge-intermediate { background: #fef3c7; color: #92400e; }
.badge-advanced  { background: #fee2e2; color: #991b1b; }
.badge-free      { background: #ecfdf5; color: #059669; border: 1px solid #6ee7b7; }
.badge-paid      { background: #f5f3ff; color: #7c3aed; border: 1px solid #c4b5fd; }

/* Stars */
.stars { color: #f59e0b; font-size: 0.85rem; }
.rating-count { color: #9ca3af; font-size: 0.75rem; }

/* Skill path */
.path-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; border-radius: 12px; padding: 18px 22px; margin-bottom: 16px;
}
.path-header h3 { margin: 0; font-size: 1.3rem; }
.path-header p  { margin: 4px 0 0 0; opacity: 0.9; font-size: 0.9rem; }

.stage-row {
    display: flex; align-items: flex-start; gap: 14px;
    margin-bottom: 12px; padding: 14px 16px;
    background: #f9fafb; border-radius: 10px; border-left: 4px solid #667eea;
}
.stage-num {
    background: #667eea; color: white;
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.8rem; flex-shrink: 0;
}
.stage-content { flex: 1; min-width: 0; }
.stage-name { font-weight: 700; font-size: 0.88rem; color: #4c1d95; margin-bottom: 3px; }
.stage-course-title { font-size: 0.92rem; font-weight: 600; color: #111827; }
.stage-meta { font-size: 0.78rem; color: #6b7280; margin-top: 2px; }

/* Score bar */
.score-bar-outer { background: #e5e7eb; border-radius: 4px; height: 4px; width: 60px; display: inline-block; vertical-align: middle; }
.score-bar-inner { background: #667eea; border-radius: 4px; height: 4px; }

/* Tip box */
.tip-box {
    background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px;
    padding: 10px 14px; font-size: 0.85rem; color: #1e40af; margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)


# ── Data loading ────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading recommendation engine…")
def load_recommender():
    return CourseRecommender("data/courses.json")


recommender = load_recommender()


# ── Helpers ─────────────────────────────────────────────────────────────────────
def platform_badge(platform: str) -> str:
    cls = f"badge-{platform.lower()}"
    icons = {"Coursera": "🎓", "Udemy": "🎯", "YouTube": "▶️"}
    icon = icons.get(platform, "🔗")
    return f'<span class="badge {cls}">{icon} {platform}</span>'


def level_badge(level: str) -> str:
    return f'<span class="badge badge-{level}">{level.capitalize()}</span>'


def price_badge(price: str) -> str:
    is_free = price in ("Free", "Free to audit")
    cls = "badge-free" if is_free else "badge-paid"
    label = "Free" if price == "Free" else ("Free to audit" if price == "Free to audit" else "Paid")
    return f'<span class="badge {cls}">{label}</span>'


def rating_stars(rating: float, num_ratings: int) -> str:
    filled = int(round(rating))
    stars = "★" * filled + "☆" * (5 - filled)
    count = f"{num_ratings:,}" if num_ratings >= 1000 else str(num_ratings)
    # Show as views for YouTube
    label = "views" if num_ratings > 500_000 else "ratings"
    return f'<span class="stars">{stars}</span> <span style="font-size:0.85rem;color:#374151;font-weight:600">{rating}</span> <span class="rating-count">({count} {label})</span>'


def match_score_bar(score: float) -> str:
    pct = int(score * 100)
    width = max(5, min(100, int(score * 180)))
    return f'<span style="font-size:0.75rem;color:#6b7280;">Match: {pct}%</span> <span class="score-bar-outer"><span class="score-bar-inner" style="width:{width}px"></span></span>'


def render_course_card(course: dict, show_score: bool = True):
    score_html = match_score_bar(course["score"]) if show_score and "score" in course else ""
    st.markdown(f"""
    <div class="course-card">
        <div class="course-title">{course['title']}</div>
        <div class="course-instructor">by {course.get('instructor','Unknown')} &nbsp;·&nbsp; {course.get('duration','N/A')}</div>
        <div class="course-desc">{course['description'][:220]}{'…' if len(course['description']) > 220 else ''}</div>
        <div class="meta-row">
            {platform_badge(course['platform'])}
            {level_badge(course['level'])}
            {price_badge(course.get('price','Paid'))}
            {rating_stars(course['rating'], course.get('num_ratings', 0))}
            {score_html}
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("→ View Course", course["url"], use_container_width=False)


def render_skill_path(path: dict):
    st.markdown(f"""
    <div class="path-header">
        <h3>{path['icon']} {path['title']} Learning Path</h3>
        <p>{path['description']}</p>
    </div>
    """, unsafe_allow_html=True)

    for i, stage in enumerate(path["stages"], 1):
        course = stage["course"]
        if not course:
            continue
        plat_badge = platform_badge(course["platform"])
        st.markdown(f"""
        <div class="stage-row">
            <div class="stage-num">{i}</div>
            <div class="stage-content">
                <div class="stage-name">{stage['stage_name']}</div>
                <div class="stage-course-title">{course['title']}</div>
                <div class="stage-meta">{plat_badge}&nbsp; ★ {course['rating']} &nbsp;·&nbsp; {course.get('duration','N/A')} &nbsp;·&nbsp; {course.get('price','Paid')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.link_button(f"Open: {course['title'][:55]}{'…' if len(course['title']) > 55 else ''}", course["url"], key=f"path_{i}_{course['id']}")


# ── Sidebar ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Filters")

    platforms = st.multiselect(
        "Platform",
        ["Coursera", "Udemy", "YouTube"],
        default=["Coursera", "Udemy", "YouTube"],
    )
    levels = st.multiselect(
        "Level",
        ["beginner", "intermediate", "advanced"],
        default=["beginner", "intermediate", "advanced"],
        format_func=str.capitalize,
    )
    price_filter = st.radio("Price", ["All", "Free only", "Paid only"], horizontal=True)
    top_k = st.slider("Number of results", 4, 20, 9, step=1)

    st.divider()
    st.markdown("### 💡 Example queries")
    examples = [
        "machine learning for beginners",
        "guitar fingerstyle",
        "Spanish for travel",
        "become a data scientist",
        "web developer career path",
        "deep learning with PyTorch",
        "SQL for data analysis",
        "photography basics",
        "personal finance investing",
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True, key=f"ex_{ex}"):
            st.session_state["search_query"] = ex

    st.divider()
    st.markdown(
        "<small>🔍 Powered by sentence-transformers + semantic search over 100 curated courses</small>",
        unsafe_allow_html=True,
    )


# ── Main content ──────────────────────────────────────────────────────────────────
st.markdown('<p class="hero-title">🎓 Learn Anything</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Enter what you want to learn — get the best courses from Coursera, Udemy & YouTube instantly</p>',
    unsafe_allow_html=True,
)

# Search bar
query = st.text_input(
    "What do you want to learn?",
    value=st.session_state.get("search_query", ""),
    placeholder='Try "machine learning for beginners", "guitar fingerstyle", "Spanish for travel", or "become a data scientist"…',
    label_visibility="collapsed",
)

col_btn, col_tip = st.columns([1, 5])
with col_btn:
    search = st.button("🔍 Find Courses", type="primary", use_container_width=True)

if query:
    filters = {"platforms": platforms, "levels": levels, "price": price_filter}

    # ── Skill path detection ──────────────────────────────────────────────────
    skill_path = recommender.detect_skill_path(query)
    if skill_path:
        st.divider()
        st.markdown("## 🗺️ Skill Path Detected")
        st.markdown(
            '<div class="tip-box">✨ We detected a <strong>career goal</strong> in your query — here\'s a curated step-by-step learning path for you!</div>',
            unsafe_allow_html=True,
        )
        render_skill_path(skill_path)

    # ── Course results ────────────────────────────────────────────────────────
    st.divider()
    st.markdown(f"## 📚 Recommended Courses for *\"{query}\"*")

    with st.spinner("Finding the best courses…"):
        results = recommender.search(query, top_k=top_k, filters=filters)

    if not results:
        st.warning("No courses matched your filters. Try adjusting the platform or level filters.")
    else:
        st.caption(f"Showing {len(results)} courses · sorted by relevance")

        # Platform breakdown
        platforms_found = {}
        for r in results:
            platforms_found[r["platform"]] = platforms_found.get(r["platform"], 0) + 1
        breakdown = "  ·  ".join(f"{p}: {n}" for p, n in sorted(platforms_found.items()))
        st.caption(f"Platforms: {breakdown}")

        st.markdown("")
        for course in results:
            render_course_card(course)

else:
    # Landing state
    st.divider()
    st.markdown("### 🚀 Popular Skill Paths")
    cols = st.columns(3)
    featured_paths = [
        ("📊", "Data Scientist", "Python → Stats → ML → Deep Learning → Deploy"),
        ("🌐", "Web Developer", "HTML → JS → React → Node → Databases → DevOps"),
        ("🤖", "ML Engineer", "Python → ML → Deep Learning → MLOps → Cloud"),
        ("☁️", "Cloud Architect", "Linux → Docker → K8s → AWS → Terraform"),
        ("🔐", "Cybersecurity", "Networking → Linux → Security → Ethical Hacking"),
        ("🎸", "Guitarist", "Basics → Chords → Music Theory → Fingerstyle"),
    ]
    for i, (icon, title, desc) in enumerate(featured_paths):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {icon} {title}")
                st.caption(desc)

    st.divider()
    st.markdown("### 🔥 Trending Courses")
    trending_queries = [
        "generative AI LLMs",
        "machine learning beginners",
        "react javascript",
        "data science python",
        "guitar beginners",
    ]
    trend_results = []
    for q in trending_queries:
        r = recommender.search(q, top_k=1, filters=None)
        if r:
            trend_results.append(r[0])

    cols2 = st.columns(2)
    for i, course in enumerate(trend_results[:4]):
        with cols2[i % 2]:
            render_course_card(course, show_score=False)
