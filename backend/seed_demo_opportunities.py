from __future__ import annotations

from datetime import datetime, timedelta

from app.core.database import Base, SessionLocal, engine
from app.models.category import Category
from app.models.opportunity import Opportunity, OpportunityStatus
from app.models.opportunity_eligibility import OpportunityEligibility
from app.models.opportunity_skill import OpportunitySkill
from app.models.skill import Skill
from app.models.source import Source


SEED_DATA = [
    {
        "title": "AI Builders Sprint",
        "organization": "OpenAI for Good",
        "description": "Build a meaningful AI prototype and present your idea to mentors in Bengaluru.",
        "category": "Hackathons",
        "location": "Bengaluru",
        "mode": "hybrid",
        "deadline": datetime.utcnow() + timedelta(days=10),
        "skills": ["Python", "Machine Learning", "FastAPI"],
        "eligible_degrees": "B.Tech, B.E., M.Tech",
        "eligible_branches": "Computer Science, IT, Electronics",
        "eligible_years": "2nd Year, 3rd Year, 4th Year",
        "benefits": "Mentorship, travel support, internship referrals",
    },
    {
        "title": "Cloud Native Hack Weekend",
        "organization": "Google Cloud Community",
        "description": "Create cloud-native solutions using modern infrastructure patterns and developer tooling.",
        "category": "Hackathons",
        "location": "Hyderabad",
        "mode": "offline",
        "deadline": datetime.utcnow() + timedelta(days=15),
        "skills": ["Python", "Cloud", "Docker"],
        "eligible_degrees": "B.Tech, B.E.",
        "eligible_branches": "Computer Science, Information Technology",
        "eligible_years": "1st Year, 2nd Year, 3rd Year",
        "benefits": "Swag, certificates, cloud credits",
    },
    {
        "title": "Product Fellowship",
        "organization": "Product School India",
        "description": "Work with startup mentors and build a strong product strategy portfolio.",
        "category": "Internships",
        "location": "Remote",
        "mode": "online",
        "deadline": datetime.utcnow() + timedelta(days=25),
        "skills": ["Product Management", "Research", "Communication"],
        "eligible_degrees": "B.Tech, B.A., B.Com",
        "eligible_branches": "Any",
        "eligible_years": "2nd Year, 3rd Year, 4th Year",
        "benefits": "Stipend, mentorship, portfolio review",
    },
    {
        "title": "Summer Research Internship",
        "organization": "NIT Research Cell",
        "description": "Join a faculty-led research team exploring AI and signal processing applications.",
        "category": "Internships",
        "location": "Trichy",
        "mode": "offline",
        "deadline": datetime.utcnow() + timedelta(days=18),
        "skills": ["Python", "Research", "Machine Learning"],
        "eligible_degrees": "B.Tech, M.Tech",
        "eligible_branches": "Computer Science, Electronics, Electrical",
        "eligible_years": "2nd Year, 3rd Year, 4th Year",
        "benefits": "Research stipend, certificate",
    },
    {
        "title": "MSME Innovation Grant",
        "organization": "Startup India",
        "description": "Pitch a practical innovation idea with support from local incubators and domain experts.",
        "category": "Scholarships",
        "location": "Delhi",
        "mode": "hybrid",
        "deadline": datetime.utcnow() + timedelta(days=32),
        "skills": ["Business Strategy", "Presentation", "Research"],
        "eligible_degrees": "B.Tech, B.E., B.A., B.Com",
        "eligible_branches": "Any",
        "eligible_years": "1st Year, 2nd Year, 3rd Year, 4th Year",
        "benefits": "Grant, incubation support",
    },
    {
        "title": "Cybersecurity Capture the Flag",
        "organization": "Indian Cyber Security Club",
        "description": "Participate in a team-based security challenge and sharpen practical red-team skills.",
        "category": "Hackathons",
        "location": "Pune",
        "mode": "offline",
        "deadline": datetime.utcnow() + timedelta(days=21),
        "skills": ["Linux", "Networking", "Cybersecurity"],
        "eligible_degrees": "B.Tech, B.E.",
        "eligible_branches": "Computer Science, IT, Cybersecurity",
        "eligible_years": "2nd Year, 3rd Year, 4th Year",
        "benefits": "Cash prize, certificates",
    },
    {
        "title": "Frontend Fellowship",
        "organization": "Design and Build Labs",
        "description": "Build polished interfaces and ship real-world design sprints with product designers.",
        "category": "Internships",
        "location": "Remote",
        "mode": "online",
        "deadline": datetime.utcnow() + timedelta(days=12),
        "skills": ["JavaScript", "React", "UI/UX"],
        "eligible_degrees": "B.Tech, B.Des, B.A.",
        "eligible_branches": "Computer Science, Design, IT",
        "eligible_years": "1st Year, 2nd Year, 3rd Year",
        "benefits": "Remote stipend, design toolkit",
    },
    {
        "title": "Women in STEM Scholarship",
        "organization": "STEM Future Foundation",
        "description": "Support exceptional female students in STEM with mentoring and financial aid.",
        "category": "Scholarships",
        "location": "Bengaluru",
        "mode": "online",
        "deadline": datetime.utcnow() + timedelta(days=40),
        "skills": ["Leadership", "Communication", "Research"],
        "eligible_degrees": "B.Tech, B.E., M.Tech",
        "eligible_branches": "Computer Science, Electronics, Mechanical",
        "eligible_years": "2nd Year, 3rd Year, 4th Year",
        "benefits": "Scholarship and mentorship",
    },
    {
        "title": "Sustainable Energy Challenge",
        "organization": "Climate Action Lab",
        "description": "Prototype solutions in clean energy and sustainable urban systems.",
        "category": "Hackathons",
        "location": "Ahmedabad",
        "mode": "hybrid",
        "deadline": datetime.utcnow() + timedelta(days=27),
        "skills": ["Python", "Analytics", "Research"],
        "eligible_degrees": "B.Tech, B.E.",
        "eligible_branches": "Mechanical, Civil, Computer Science",
        "eligible_years": "2nd Year, 3rd Year, 4th Year",
        "benefits": "Prize money, prototyping support",
    },
    {
        "title": "Data Science Bootcamp",
        "organization": "Analytics Hub",
        "description": "Build practical machine learning projects with experts in data product design.",
        "category": "Bootcamp",
        "location": "Remote",
        "mode": "online",
        "deadline": datetime.utcnow() + timedelta(days=7),
        "skills": ["Python", "Machine Learning", "Statistics"],
        "eligible_degrees": "B.Tech, B.Sc, B.Com",
        "eligible_branches": "Any",
        "eligible_years": "1st Year, 2nd Year, 3rd Year, 4th Year",
        "benefits": "Certificate, GPU credits",
    },
    {
        "title": "Campus Innovation Grant",
        "organization": "Atal Incubation Centre",
        "description": "Get early support to validate, prototype, and pitch a campus startup idea.",
        "category": "Scholarships",
        "location": "Chennai",
        "mode": "offline",
        "deadline": datetime.utcnow() + timedelta(days=50),
        "skills": ["Business Strategy", "Presentation", "Research"],
        "eligible_degrees": "B.Tech, B.E.",
        "eligible_branches": "Any",
        "eligible_years": "2nd Year, 3rd Year, 4th Year",
        "benefits": "Seed funding, mentorship",
    },
    {
        "title": "Applied AI Internship",
        "organization": "VisionWorks Labs",
        "description": "Work with ML engineers on real product usage, evaluation, and efficient deployment pipelines.",
        "category": "Internships",
        "location": "Remote",
        "mode": "hybrid",
        "deadline": datetime.utcnow() + timedelta(days=19),
        "skills": ["Python", "Machine Learning", "FastAPI"],
        "eligible_degrees": "B.Tech, B.E.",
        "eligible_branches": "Computer Science, Electronics, IT",
        "eligible_years": "2nd Year, 3rd Year, 4th Year",
        "benefits": "Paid internship, letter of recommendation",
    },
    {
        "title": "Blockchain Builder Weekend",
        "organization": "Web3 India Community",
        "description": "Explore blockchain use cases and build prototypes for the next generation of dApps.",
        "category": "Hackathons",
        "location": "Mumbai",
        "mode": "offline",
        "deadline": datetime.utcnow() + timedelta(days=6),
        "skills": ["Solidity", "JavaScript", "Blockchain"],
        "eligible_degrees": "B.Tech, B.E., B.Sc",
        "eligible_branches": "Computer Science, IT, Mathematics",
        "eligible_years": "2nd Year, 3rd Year, 4th Year",
        "benefits": "Hackathon prize pool",
    },
    {
        "title": "Global Youth Summit",
        "organization": "Future Leaders Forum",
        "description": "Join a global youth summit exploring entrepreneurship, innovation, and civic engagement.",
        "category": "Events",
        "location": "Online",
        "mode": "online",
        "deadline": datetime.utcnow() + timedelta(days=14),
        "skills": ["Communication", "Leadership", "Research"],
        "eligible_degrees": "Any",
        "eligible_branches": "Any",
        "eligible_years": "1st Year, 2nd Year, 3rd Year, 4th Year",
        "benefits": "Networking, certificates, travel support",
    },
]


def seed_demo_opportunities() -> int:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(Opportunity).count()
        if existing >= len(SEED_DATA):
            return existing

        source = db.query(Source).filter(Source.name == "OpportunityHub Demo").first()
        if source is None:
            source = Source(name="OpportunityHub Demo", url="https://example.com")
            db.add(source)
            db.flush()

        for item in SEED_DATA:
            category = db.query(Category).filter(Category.name == item["category"]).first()
            if category is None:
                category = Category(name=item["category"])
                db.add(category)
                db.flush()

            opportunity = Opportunity(
                title=item["title"],
                organization=item["organization"],
                description=item["description"],
                category_id=category.id,
                location=item["location"],
                mode=item["mode"],
                deadline=item["deadline"],
                status=OpportunityStatus.PUBLISHED,
                benefits=item["benefits"],
                application_url="https://example.com/opportunity",
                source_id=source.id,
            )
            db.add(opportunity)
            db.flush()

            for skill_name in item["skills"]:
                skill = db.query(Skill).filter(Skill.name == skill_name).first()
                if skill is None:
                    skill = Skill(name=skill_name)
                    db.add(skill)
                    db.flush()
                db.add(OpportunitySkill(opportunity_id=opportunity.id, skill_id=skill.id))

            db.add(
                OpportunityEligibility(
                    opportunity_id=opportunity.id,
                    eligible_degrees=item["eligible_degrees"],
                    eligible_branches=item["eligible_branches"],
                    eligible_years=item["eligible_years"],
                    notes="Open to eligible students from the listed streams.",
                )
            )

        db.commit()
        return db.query(Opportunity).count()
    finally:
        db.close()


if __name__ == "__main__":
    count = seed_demo_opportunities()
    print(f"Seeded {count} demo opportunities.")
