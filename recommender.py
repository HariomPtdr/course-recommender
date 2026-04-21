import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path


SKILL_PATHS = {
    "data scientist": {
        "title": "Data Scientist",
        "icon": "📊",
        "description": "From zero to job-ready data scientist",
        "stages": [
            {"name": "Python Fundamentals", "query": "python programming beginners"},
            {"name": "Statistics & Math", "query": "statistics for data science"},
            {"name": "Data Analysis & Pandas", "query": "pandas numpy data analysis"},
            {"name": "Data Visualization", "query": "matplotlib seaborn data visualization"},
            {"name": "Machine Learning", "query": "machine learning scikit-learn beginners"},
            {"name": "Deep Learning", "query": "deep learning neural networks tensorflow"},
            {"name": "SQL & Databases", "query": "SQL databases data science"},
        ],
    },
    "machine learning engineer": {
        "title": "ML Engineer",
        "icon": "🤖",
        "description": "Build and deploy machine learning systems at scale",
        "stages": [
            {"name": "Python & Programming", "query": "python programming algorithms"},
            {"name": "Machine Learning Fundamentals", "query": "machine learning fundamentals"},
            {"name": "Deep Learning & Neural Networks", "query": "deep learning pytorch tensorflow"},
            {"name": "NLP & Computer Vision", "query": "NLP computer vision transformers"},
            {"name": "MLOps & Deployment", "query": "MLOps model deployment production"},
            {"name": "Cloud ML Platforms", "query": "AWS GCP cloud machine learning"},
        ],
    },
    "web developer": {
        "title": "Full-Stack Web Developer",
        "icon": "🌐",
        "description": "Build modern full-stack web applications",
        "stages": [
            {"name": "HTML & CSS", "query": "HTML CSS web design beginners"},
            {"name": "JavaScript Fundamentals", "query": "javascript programming basics"},
            {"name": "React Frontend", "query": "react javascript frontend"},
            {"name": "Node.js & Backend", "query": "nodejs express backend API"},
            {"name": "Databases", "query": "SQL MongoDB databases web"},
            {"name": "DevOps & Deployment", "query": "docker deployment devops web"},
        ],
    },
    "data engineer": {
        "title": "Data Engineer",
        "icon": "⚙️",
        "description": "Build data pipelines and infrastructure",
        "stages": [
            {"name": "Python & SQL", "query": "python SQL programming"},
            {"name": "Data Warehousing", "query": "SQL databases data warehouse BigQuery"},
            {"name": "Big Data & Spark", "query": "Apache Spark PySpark big data"},
            {"name": "Stream Processing", "query": "Kafka stream processing data"},
            {"name": "Cloud & Pipelines", "query": "data engineering cloud pipelines ETL"},
        ],
    },
    "cybersecurity": {
        "title": "Cybersecurity Analyst",
        "icon": "🔐",
        "description": "Protect systems and networks from threats",
        "stages": [
            {"name": "Networking Fundamentals", "query": "networking TCP/IP fundamentals"},
            {"name": "Linux & Command Line", "query": "linux command line fundamentals"},
            {"name": "Cybersecurity Basics", "query": "cybersecurity fundamentals beginners"},
            {"name": "Ethical Hacking", "query": "ethical hacking penetration testing"},
            {"name": "Security Certifications", "query": "CompTIA Security+ certification"},
        ],
    },
    "mobile developer": {
        "title": "Mobile Developer",
        "icon": "📱",
        "description": "Build iOS and Android mobile applications",
        "stages": [
            {"name": "Programming Basics", "query": "python javascript programming fundamentals"},
            {"name": "Mobile UI Fundamentals", "query": "UI design mobile fundamentals"},
            {"name": "Flutter or React Native", "query": "flutter dart cross-platform mobile"},
            {"name": "Backend & APIs", "query": "REST API backend mobile"},
            {"name": "App Store Deployment", "query": "iOS Android app deployment store"},
        ],
    },
    "cloud architect": {
        "title": "Cloud Architect",
        "icon": "☁️",
        "description": "Design and manage cloud infrastructure",
        "stages": [
            {"name": "Networking Fundamentals", "query": "networking fundamentals computer"},
            {"name": "Linux & DevOps Basics", "query": "linux command line devops"},
            {"name": "Docker & Containers", "query": "docker containers beginners"},
            {"name": "Kubernetes", "query": "kubernetes orchestration deployment"},
            {"name": "AWS/GCP/Azure", "query": "AWS cloud solutions architect certification"},
            {"name": "Infrastructure as Code", "query": "terraform ansible infrastructure code"},
        ],
    },
    "guitar player": {
        "title": "Guitar Player",
        "icon": "🎸",
        "description": "From absolute beginner to advanced guitarist",
        "stages": [
            {"name": "Guitar Basics & Chords", "query": "guitar lessons beginners chords"},
            {"name": "Music Theory", "query": "music theory guitar scales"},
            {"name": "Strumming & Rhythm", "query": "guitar strumming rhythm patterns"},
            {"name": "Fingerstyle Technique", "query": "guitar fingerstyle fingerpicking"},
            {"name": "Scales & Improvisation", "query": "guitar scales improvisation blues"},
        ],
    },
    "spanish speaker": {
        "title": "Spanish Speaker",
        "icon": "🇪🇸",
        "description": "From zero to conversational Spanish",
        "stages": [
            {"name": "Spanish Basics", "query": "spanish beginners basics vocabulary"},
            {"name": "Grammar Fundamentals", "query": "spanish grammar fundamentals"},
            {"name": "Conversation Practice", "query": "spanish conversation practice phrases"},
            {"name": "Intermediate Spanish", "query": "spanish intermediate fluency"},
        ],
    },
    "photographer": {
        "title": "Photographer",
        "icon": "📸",
        "description": "Master photography from basics to professional",
        "stages": [
            {"name": "Camera Basics", "query": "photography camera basics beginners"},
            {"name": "Composition & Lighting", "query": "photography composition lighting"},
            {"name": "Photo Editing", "query": "lightroom photo editing"},
            {"name": "Advanced Photography", "query": "photography portrait landscape advanced"},
        ],
    },
}

# Keywords to detect skill path intent
SKILL_PATH_KEYWORDS = {
    "data scientist": ["data scientist", "data science career", "become a data scientist"],
    "machine learning engineer": ["ml engineer", "machine learning engineer", "ai engineer"],
    "web developer": ["web developer", "web development", "fullstack developer", "frontend developer", "backend developer"],
    "data engineer": ["data engineer", "data engineering", "build data pipelines"],
    "cybersecurity": ["cybersecurity", "cyber security", "security analyst", "ethical hacker", "penetration tester"],
    "mobile developer": ["mobile developer", "app developer", "mobile development", "ios developer", "android developer"],
    "cloud architect": ["cloud architect", "cloud engineer", "devops engineer"],
    "guitar player": ["learn guitar", "become guitarist", "play guitar", "guitar player", "guitar fingerstyle", "guitar beginners", "acoustic guitar"],
    "spanish speaker": ["learn spanish", "speak spanish", "spanish fluency", "spanish for travel", "spanish language", "spanish beginners"],
    "photographer": ["learn photography", "become photographer", "photography skills"],
}


class CourseRecommender:
    def __init__(self, courses_path: str = "data/courses.json"):
        self.courses = self._load_courses(courses_path)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embeddings = self._compute_embeddings()

    def _load_courses(self, path: str):
        with open(Path(path), "r") as f:
            return json.load(f)

    def _compute_embeddings(self):
        texts = []
        for c in self.courses:
            tags = " ".join(c.get("tags", []))
            text = f"{c['title']} {c['description']} {tags} {c.get('category', '')} {c.get('level', '')}"
            texts.append(text)
        return self.model.encode(texts, show_progress_bar=False, batch_size=32)

    def search(self, query: str, top_k: int = 12, filters: dict = None) -> list:
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]

        results = []
        for idx, sim in enumerate(similarities):
            course = self.courses[idx]
            if filters:
                if filters.get("platforms") and course["platform"] not in filters["platforms"]:
                    continue
                if filters.get("levels") and course["level"] not in filters["levels"]:
                    continue
                if filters.get("price") and filters["price"] != "All":
                    is_free = course["price"] in ("Free", "Free to audit")
                    if filters["price"] == "Free only" and not is_free:
                        continue
                    if filters["price"] == "Paid only" and is_free:
                        continue
            results.append({**course, "score": float(sim)})

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def detect_skill_path(self, query: str) -> dict | None:
        query_lower = query.lower().strip()
        for path_key, keywords in SKILL_PATH_KEYWORDS.items():
            for kw in keywords:
                if kw in query_lower:
                    return self._build_skill_path(path_key)
        return None

    def _build_skill_path(self, path_key: str) -> dict:
        path_def = SKILL_PATHS[path_key]
        stages_with_courses = []
        for stage in path_def["stages"]:
            results = self.search(stage["query"], top_k=1, filters=None)
            stages_with_courses.append({
                "stage_name": stage["name"],
                "course": results[0] if results else None,
            })
        return {
            "title": path_def["title"],
            "icon": path_def["icon"],
            "description": path_def["description"],
            "stages": stages_with_courses,
        }

    def get_categories(self) -> list[str]:
        return sorted(set(c.get("category", "Other") for c in self.courses))
