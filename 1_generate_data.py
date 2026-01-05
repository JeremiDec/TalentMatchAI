"""
GraphRAG Data Generation - Single Integrated Module (Full Logic + BI Enhancements)
==================================================================================

Generates realistic programmer profiles and PDF CVs for GraphRAG educational demonstration.
Uses LLM to create unique, unstructured CVs in markdown format, then converts to PDF.

ENHANCEMENTS:
- Includes strict Business Intelligence metadata (Rates, GPA, Soft Skills).
- Real-time project dates logic (Historical vs Active).
- Preserves complex assignment algorithms (Skill matching, Availability checks).

CRITICAL: No fallbacks, no mock data. All dependencies must be available.
"""

from dotenv import load_dotenv
load_dotenv(override=True)

import os
import json
import random
import toml
from datetime import date, datetime, timedelta
from faker import Faker
from typing import List, Dict, Any
from langchain_openai import AzureChatOpenAI
import markdown
from weasyprint import HTML, CSS

fake = Faker()


class GraphRAGDataGenerator:
    """Integrated generator for programmer profiles and realistic PDF CVs."""

    def __init__(self, config_path: str = "utils/config.toml"):
        """Initialize with required dependencies - fail fast if missing."""
        # Load configuration
        self.config = self._load_config(config_path)

        # --- ZMIANA 1: Walidacja pod Azure ---
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        if not api_key:
            # Fallback: sprawdź czy może jednak jest stary klucz, jeśli nie, rzuć błąd
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("AZURE_OPENAI_API_KEY environment variable is required")

        # Initialize LLM
        # Wersja dla Azure
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),  # Nazwa wdrożenia z .env
            openai_api_version=os.getenv("OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0.7
        )

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from TOML file."""
        if not os.path.exists(config_path):
            raise ValueError(f"Configuration file not found: {config_path}")

        with open(config_path, 'r') as f:
            config = toml.load(f)

        return config

    def _generate_education(self, total_exp: int) -> dict:
        """Generate detailed education data with Ranking and GPA (New Helper)."""
        universities = [
            {"name": "Massachusetts Institute of Technology (MIT)", "location": "Cambridge, MA", "ranking": 1},
            {"name": "Stanford University", "location": "Stanford, CA", "ranking": 2},
            {"name": "University of California, Berkeley", "location": "Berkeley, CA", "ranking": 4},
            {"name": "University of Oxford", "location": "Oxford, UK", "ranking": 5},
            {"name": "ETH Zurich", "location": "Zurich, CH", "ranking": 9},
            {"name": "Georgia Institute of Technology", "location": "Atlanta, GA", "ranking": 15},
            {"name": "Warsaw University of Technology", "location": "Warsaw, PL", "ranking": 50},
            {"name": "Technical University of Munich", "location": "Munich, DE", "ranking": 20}
        ]
        
        univ = random.choice(universities)
        current_year = datetime.now().year
        # Logic: Graduation year based on experience to make sense
        grad_year = current_year - total_exp - random.randint(0, 2)
        
        return {
            "university_name": univ["name"],
            "university_location": univ["location"],
            "university_ranking": univ["ranking"],
            "degree": random.choice(["B.Sc. in Computer Science", "M.Sc. in Software Engineering", "PhD in Artificial Intelligence"]),
            "graduation_year": grad_year,
            "gpa": round(random.uniform(3.2, 4.0), 2)
        }

    def _generate_soft_skills(self) -> List[dict]:
        """Generate soft skills for team composition analysis (New Helper)."""
        skills = [
            "Team Leadership", "Agile Methodology", "Scrum", "Mentoring",
            "Public Speaking", "Problem Solving", "Strategic Planning",
            "Cross-functional Communication", "Conflict Resolution", "Adaptability"
        ]
        selected = random.sample(skills, random.randint(3, 5))
        return [{"name": s} for s in selected]

    def _generate_languages(self) -> List[dict]:
        """Generate spoken languages (New Helper)."""
        langs = [
            {"name": "English", "levels": ["C1", "C2", "Native"]},
            {"name": "Spanish", "levels": ["B1", "B2", "C1"]},
            {"name": "German", "levels": ["B1", "B2"]},
            {"name": "French", "levels": ["B1", "B2"]},
            {"name": "Polish", "levels": ["Native", "C2"]}
        ]
        # Always include English
        my_langs = [{"name": "English", "level": random.choice(["C1", "C2", "Native"])}]
        # Add 0-2 others
        other_langs = random.sample(langs[1:], random.randint(0, 2))
        for lang in other_langs:
            my_langs.append({"name": lang["name"], "level": random.choice(lang["levels"])})
        return my_langs

    def generate_programmer_profiles(self, num_profiles: int) -> List[dict]:
        """Generate realistic programmer profiles with RICH METADATA."""
        if num_profiles <= 0:
            raise ValueError("Number of profiles must be positive")

        profiles = []
        for i in range(num_profiles):
            total_exp = random.randint(2, 15)
            
            profile = {
                "id": i + 1,
                "name": fake.name(),
                "email": fake.email(),
                "phone": fake.phone_number(), # Added
                "location": fake.city(),
                "total_years_experience": total_exp, # Added
                "hourly_rate": random.randint(45, 160), # Added
                "currency": "USD", # Added
                "education": self._generate_education(total_exp), # Added
                "soft_skills": self._generate_soft_skills(), # Added
                "languages": self._generate_languages(), # Added
                "skills": self._generate_skills(total_exp), # Enhanced
                "projects": self._generate_project_names_context(), # Renamed helper
                "certifications": self._generate_certifications(), # Enhanced
            }
            profiles.append(profile)

        return profiles

    def _generate_skills(self, total_exp: int) -> List[dict]:
        """Generate realistic programming skills with categories and years."""
        # Expanded Catalog
        skill_catalog = {
            "Backend": ["Python", "Java", "C++", "Go", "Rust", "Node.js", "Django", "Spring Boot"],
            "Frontend": ["JavaScript", "TypeScript", "React", "Vue.js", "Angular", "Next.js"],
            "Data/AI": ["Machine Learning", "Data Science", "PostgreSQL", "MongoDB", "Redis", "PyTorch"],
            "DevOps": ["AWS", "Docker", "Kubernetes", "Jenkins", "Git", "Terraform", "Azure"]
        }

        proficiency_levels = ["Beginner", "Intermediate", "Advanced", "Expert"]
        selected_skills = []

        # Logic: Ensure distribution across categories
        for category, skills in skill_catalog.items():
            # 70% chance to have skills in a category
            if random.random() < 0.7:
                num_picks = random.randint(1, 3)
                picks = random.sample(skills, min(num_picks, len(skills)))
                
                for skill_name in picks:
                    # Years based on total exp
                    years = random.randint(1, total_exp)
                    
                    # Proficiency mapping
                    if years < 2: prof = "Beginner"
                    elif years < 4: prof = "Intermediate"
                    elif years < 7: prof = "Advanced"
                    else: prof = "Expert"
                    
                    # Weight from config logic preserved via random choice refinement if needed
                    # but calculating from years is more consistent for BI
                    
                    selected_skills.append({
                        "name": skill_name,
                        "category": category, # Added
                        "proficiency": prof,
                        "years_experience": years # Added
                    })

        return selected_skills

    def _generate_project_names_context(self) -> List[str]:
        """Generate realistic project names for CV context only."""
        project_types = [
            "E-commerce Platform", "Data Analytics Dashboard", "Mobile App",
            "API Gateway", "Machine Learning Pipeline", "Web Application",
            "Microservices Architecture", "Real-time Chat System",
            "Content Management System", "Payment Processing System"
        ]
        num_projects = random.randint(2, 5)
        return random.sample(project_types, num_projects)

    def _generate_certifications(self) -> List[dict]:
        """Generate realistic certifications with details."""
        cert_db = [
            {"name": "AWS Certified Solutions Architect", "provider": "Amazon"},
            {"name": "Google Cloud Professional", "provider": "Google"},
            {"name": "Certified Kubernetes Administrator", "provider": "Linux Foundation"},
            {"name": "Microsoft Azure Developer", "provider": "Microsoft"},
            {"name": "Scrum Master Certification", "provider": "Scrum.org"},
            {"name": "Docker Certified Associate", "provider": "Docker"}
        ]
        
        num_certs = random.randint(0, 3)
        if num_certs == 0: return []
        
        selected = random.sample(cert_db, num_certs)
        results = []
        for c in selected:
            date_earned = fake.date_between(start_date='-3y', end_date='today')
            results.append({
                "name": c["name"],
                "provider": c["provider"],
                "date_earned": date_earned.isoformat(),
                "expiry_date": (date_earned + timedelta(days=365*3)).isoformat(), # Added
                "score": random.randint(700, 1000) # Added
            })
        return results

    # ==========================================
    # 2. PROJECTS GENERATION (Logic Fixes)
    # ==========================================

    def generate_projects(self, num_projects: int = 20, programmer_profiles: List[dict] = None) -> List[dict]:
        """Generate realistic project data with STRICT Historical/Active split."""
        if num_projects <= 0:
            raise ValueError("Number of projects must be positive")

        project_types = [
            "E-commerce Platform", "Data Analytics Dashboard", "Mobile App Development",
            "API Gateway Implementation", "Machine Learning Pipeline", "Web Application",
            "Microservices Architecture", "Real-time Chat System", "Content Management System",
            "Payment Processing System", "DevOps Automation", "Cloud Migration",
            "Security Audit System", "Inventory Management", "Customer Portal"
        ]

        clients = [
            "TechCorp", "DataSystems Inc", "CloudNative Solutions", "FinTech Innovations",
            "HealthTech Partners", "RetailMax", "LogisticsPro", "EduTech Solutions",
            "MediaStream", "GreenEnergy Co", "SmartCity Initiative", "BioTech Labs"
        ]

        projects = []
        now = datetime.now()

        # Build skill pool for requirements
        if programmer_profiles:
            available_skills = set()
            for profile in programmer_profiles:
                for skill in profile['skills']:
                    available_skills.add(skill['name'])
            skill_names = list(available_skills)
        else:
            skill_names = ["Python", "Java", "JavaScript", "React", "AWS", "Docker"]

        # --- LOGIC SPLIT: 2/3 Historical, 1/3 Active ---
        num_historical = int(num_projects * 0.67)
        num_active = num_projects - num_historical

        # Helper to create project
        def create_project_structure(status, idx):
            p_type = random.choice(project_types)
            client = random.choice(clients)
            duration_months = random.randint(3, 18)
            
            # --- DATE LOGIC FIX ---
            if status == "completed":
                # Must end in the past
                days_ago_ended = random.randint(30, 700)
                end_date_obj = now - timedelta(days=days_ago_ended)
                start_date_obj = end_date_obj - timedelta(days=duration_months * 30)
                start_date = start_date_obj.isoformat()
                end_date = end_date_obj.isoformat()
            elif status == "active":
                # Must span "now" (start in past, end in future)
                months_passed = random.randint(1, duration_months - 1) if duration_months > 1 else 0
                start_date_obj = now - timedelta(days=months_passed * 30)
                end_date_obj = start_date_obj + timedelta(days=duration_months * 30)
                start_date = start_date_obj.isoformat()
                end_date = end_date_obj.isoformat()
            else:
                # Fallback
                start_date = now.isoformat()
                end_date = None

            # Requirements generation (Enhanced with Preferred Level)
            requirements = []
            num_reqs = random.randint(3, 8)
            req_skills = random.sample(skill_names, min(len(skill_names), num_reqs))
            
            levels = ["Beginner", "Intermediate", "Advanced", "Expert"]

            for skill in req_skills:
                min_idx = random.randint(0, 2)
                requirements.append({
                    "skill_name": skill,
                    "min_proficiency": levels[min_idx],
                    "preferred_proficiency": levels[min(3, min_idx + 1)], # Added
                    "is_mandatory": random.choice([True, True, False])
                })

            return {
                "id": f"PRJ-{idx:03d}",
                "name": f"{p_type} for {client}",
                "client": client,
                "description": f"Development of {p_type.lower()} focusing on scalability.",
                "start_date": start_date,
                "end_date": end_date,
                "estimated_duration_months": duration_months,
                "budget": random.randint(50000, 500000), # Never None
                "status": status,
                "team_size": random.randint(2, 8),
                "requirements": requirements,
                "assigned_programmers": []
            }

        # Generate lists
        for i in range(num_historical):
            projects.append(create_project_structure("completed", i + 1))
        
        for i in range(num_active):
            projects.append(create_project_structure("active", num_historical + i + 1))

        # Assign programmers to projects if profiles provided
        if programmer_profiles:
            projects = self._assign_programmers_to_projects(projects, programmer_profiles)

        return projects

    def _assign_programmers_to_projects(self, projects: List[dict], programmer_profiles: List[dict]) -> List[dict]:
        """Assign programmers to projects based on skill matching (COMPLEX LOGIC PRESERVED)."""

        # Create a list to track programmer availability periods
        programmer_assignments = {p['id']: [] for p in programmer_profiles}

        # Helper function to check if programmer has required skill at minimum proficiency
        def has_skill_requirement(programmer, skill_name, min_proficiency):
            proficiency_levels = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Expert": 4}
            min_level = proficiency_levels[min_proficiency]

            for skill in programmer['skills']:
                if skill['name'] == skill_name:
                    programmer_level = proficiency_levels[skill['proficiency']]
                    return programmer_level >= min_level
            return False

        # Helper function to check if programmer is available during project period
        def is_available(programmer_id, start_date, end_date):
            assignments = programmer_assignments[programmer_id]
            project_start = datetime.fromisoformat(start_date).date()
            project_end = datetime.fromisoformat(end_date).date() if end_date else None

            for assignment in assignments:
                assign_start = datetime.fromisoformat(assignment['assignment_start_date']).date()
                assign_end = datetime.fromisoformat(assignment['assignment_end_date']).date() if assignment['assignment_end_date'] else None

                # Check for overlap
                if assign_end is None:  # Ongoing assignment
                    if project_end is None or project_start <= assign_start:
                        return False
                elif project_end is None:  # Ongoing project
                    if assign_end >= project_start:
                        return False
                else:  # Both have end dates
                    if not (project_end < assign_start or project_start > assign_end):
                        return False
            return True

        # Process projects for assignments
        # Note: We process all provided projects (historical + active)
        
        assignment_probability = self.config['assignment']['assignment_probability']

        for project in projects:
            if random.random() > assignment_probability:
                continue  # Skip this project to leave programmers available

            assigned_count = 0
            max_assignments = min(project['team_size'], len(programmer_profiles))

            # Get mandatory requirements
            mandatory_requirements = [req for req in project['requirements'] if req['is_mandatory']]

            # Try to find programmers matching mandatory skills
            eligible_programmers = []
            for programmer in programmer_profiles:
                matches_mandatory = True
                for req in mandatory_requirements:
                    if not has_skill_requirement(programmer, req['skill_name'], req['min_proficiency']):
                        matches_mandatory = False
                        break

                # We preserve the strict date check logic
                if matches_mandatory and is_available(programmer['id'], project['start_date'], project['end_date']):
                    eligible_programmers.append(programmer)

            # Randomly select from eligible programmers
            selected_programmers = random.sample(
                eligible_programmers,
                min(max_assignments, len(eligible_programmers))
            )

            # Create assignments
            for programmer in selected_programmers:
                assignment_start = project['start_date']
                
                # Logic for assignment dates matching project dates
                if project['end_date']:
                    assignment_end = project['end_date']
                else:
                    # Active project estimation
                    p_start = datetime.fromisoformat(project['start_date']).date()
                    est_end = p_start + timedelta(days=project['estimated_duration_months']*30)
                    assignment_end = est_end.isoformat()

                # --- ENHANCEMENT: ADD BI METADATA TO ASSIGNMENT ---
                
                # Role Logic
                roles = ["Backend Dev", "Frontend Dev", "Fullstack Dev", "Tech Lead", "Architect", "DevOps Eng"]
                role = random.choice(roles)
                
                # Allocation Logic (Active projects can have partial allocation)
                allocation = 100
                if project['status'] == 'active':
                    allocation = random.choice([50, 100])
                    
                # Performance Logic
                rating = random.choices([3, 4, 5], weights=[10, 40, 50])[0]
                outcome = "Successfully delivered" if rating >= 4 else "Completed with challenges"

                assignment = {
                    "programmer_name": programmer['name'],
                    "programmer_id": programmer['id'],
                    "assignment_start_date": assignment_start,
                    "assignment_end_date": assignment_end,
                    "role_in_project": role, # Added
                    "allocation_percent": allocation, # Added
                    "performance_rating": rating, # Added
                    "project_outcome": outcome # Added
                }

                project['assigned_programmers'].append(assignment)
                programmer_assignments[programmer['id']].append(assignment)
                assigned_count += 1

        return projects

    # ==========================================
    # 3. RFP GENERATION
    # ==========================================

    def generate_rfps(self, num_rfps: int = 3) -> List[dict]:
        """Generate realistic RFP data with counts and deadlines."""
        if num_rfps <= 0:
            raise ValueError("Number of RFPs must be positive")

        rfp_types = [
            "Enterprise Web Application", "Mobile App Development", "Data Analytics Platform",
            "Cloud Migration Project", "E-commerce Modernization", "API Integration Platform"
        ]

        clients = ["Global Finance Corp", "MedTech Industries", "Retail Solutions Ltd", "Manufacturing Plus"]
        budget_ranges = ["$100K - $250K", "$250K - $500K", "$500K - $1M", "$1M - $2M"]
        
        # Skill pool
        skill_names = ["Python", "JavaScript", "Java", "React", "Angular", "Node.js", "AWS", "Docker", "Kubernetes"]

        rfps = []
        for i in range(num_rfps):
            start_date_obj = fake.date_between(start_date='+1m', end_date='+6m')
            duration_months = random.randint(6, 24)
            
            # --- POPRAWKA 1: Obliczanie Deadline ---
            # Zakładamy miesiąc = 30 dni
            deadline_obj = start_date_obj + timedelta(days=duration_months * 30)
            
            team_size = random.randint(3, 12)
            
            # Generate skill requirements with Counts
            requirements = []
            # Wybieramy losowe skille
            selected_skills = random.sample(skill_names, random.randint(3, 6))
            
            # --- POPRAWKA 2: Rozdzielanie Team Size na skille ---
            # Prosta logika: rozdajemy wakaty po skillach
            slots_left = team_size
            for idx, skill in enumerate(selected_skills):
                # Jeśli to ostatni skill, daj mu resztę (chyba że 0)
                if idx == len(selected_skills) - 1:
                    count = max(1, slots_left)
                else:
                    # Losujemy od 1 do (slots_left - reszta skilli)
                    max_alloc = max(1, slots_left - (len(selected_skills) - idx - 1))
                    count = random.randint(1, min(3, max_alloc)) # max 3 per skill żeby było różnorodnie
                
                slots_left -= count
                
                requirements.append({
                    "skill_name": skill,
                    "min_proficiency": "Advanced",
                    "preferred_proficiency": "Expert",
                    "is_mandatory": True,
                    "required_count": count, # <--- TUTAJ JEST BRAKUJĄCE POLE
                    "preferred_certifications": []
                })

            rfp = {
                "id": f"RFP-{i+1:03d}",
                "title": f"{random.choice(rfp_types)}",
                "client": random.choice(clients),
                "description": f"Strategic initiative for {random.choice(rfp_types)}.",
                "project_type": "Software Development",
                "duration_months": duration_months,
                "team_size": team_size, 
                "budget_range": random.choice(budget_ranges),
                "start_date": start_date_obj.isoformat(),
                "deadline": deadline_obj.isoformat(), # <--- TUTAJ JEST BRAKUJĄCE POLE
                "requirements": requirements,
                "location": fake.city(),
                "remote_allowed": True
            }
            rfps.append(rfp)

        return rfps

    def generate_rfp_markdown(self, rfp: dict) -> str:
        """Generate RFP document with STRICT HEADERS for parsing."""

        # Format requirements text
        requirements_text = []
        for req in rfp['requirements']:
            requirements_text.append(f"- {req['skill_name']}: Required {req['min_proficiency']} (Preferred: {req.get('preferred_proficiency')})")

        prompt = f"""
Create a professional RFP (Request for Proposal) document in markdown format.

CRITICAL INSTRUCTION: You MUST use EXACTLY the following headers in this order:
# Executive Summary
# Project Scope
# Technical Requirements
# Team Structure & Budget
# Timeline
# Submission Guidelines

DETAILS TO INCLUDE:
Project: {rfp['title']}
Client: {rfp['client']}
Budget: {rfp['budget_range']}
Start Date: {rfp['start_date']}
Duration: {rfp['duration_months']} months

Technical Requirements List:
{chr(10).join(requirements_text)}

Make it sound professional and business-oriented. Return ONLY the RFP content in markdown.
"""

        response = self.llm.invoke(prompt)
        content = response.content.replace("```markdown", "").replace("```", "").strip()
        if not content: raise ValueError(f"LLM returned empty content for RFP {rfp['id']}")
        return content

    # ==========================================
    # 4. CV DOCUMENT GENERATION
    # ==========================================

    def generate_cv_markdown(self, profile: dict) -> str:
        """Generate realistic CV in markdown using LLM with ALL BI METADATA."""

        # Format rich metadata for prompt
        skills_text = []
        for skill in profile['skills']:
            skills_text.append(f"{skill['name']} ({skill['proficiency']}, {skill['years_experience']} yrs)")
            
        soft_text = ", ".join([s['name'] for s in profile['soft_skills']])
        langs_text = ", ".join([f"{l['name']} ({l['level']})" for l in profile['languages']])
        
        certs_text = []
        for c in profile['certifications']:
            certs_text.append(f"{c['name']} (Score: {c['score']}, Exp: {c['expiry_date']})")
            
        edu = profile['education']
        edu_text = f"{edu['degree']} at {edu['university_name']} (Rank: #{edu['university_ranking']}, GPA: {edu['gpa']})"

        prompt = f"""
Create a professional CV in markdown format for a programmer.

VITAL DATA TO INCLUDE (Do not hallucinate different values):
Name: {profile['name']}
Email: {profile['email']} | Phone: {profile['phone']}
Location: {profile['location']}
Hourly Rate: ${profile['hourly_rate']}/hr
Total Experience: {profile['total_years_experience']} years

EDUCATION:
{edu_text}

SKILLS:
{', '.join(skills_text)}

SOFT SKILLS:
{soft_text}

LANGUAGES:
{langs_text}

CERTIFICATIONS:
{', '.join(certs_text)}

PROJECT CONTEXT (Mention these names in Experience):
{', '.join(profile['projects'])}

Requirements:
1. Use proper markdown formatting.
2. **Explicitly mention** the Hourly Rate, University Ranking, GPA, and Exam Scores in the text.
3. In the Experience section, invent 2-3 detailed roles. For each role, mention the **Company Industry** (e.g. FinTech) and **Size** (Startup/Enterprise).
4. Use the specific years of experience provided for skills.
5. Create a Summary section highlighting total years and soft skills.

IMPORTANT: Return ONLY the CV content in markdown format.
"""

        response = self.llm.invoke(prompt)
        content = response.content.replace("```markdown", "").replace("```", "").strip()
        if not content: raise ValueError(f"LLM returned empty content for {profile['name']}")
        return content

    def save_cv_as_pdf(self, markdown_content: str, filename: str, output_dir: str) -> str:
        """Convert markdown CV to PDF."""
        os.makedirs(output_dir, exist_ok=True)
        html_content = markdown.markdown(markdown_content)

        css_content = """
        body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 20px; }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; }
        h2 { color: #34495e; margin-top: 30px; border-bottom: 1px solid #eee; }
        h3 { color: #7f8c8d; }
        strong { color: #2c3e50; }
        ul { margin-left: 20px; }
        .meta { color: #666; font-size: 0.9em; }
        """

        pdf_path = os.path.join(output_dir, f"{filename}.pdf")
        HTML(string=html_content).write_pdf(
            pdf_path,
            stylesheets=[CSS(string=css_content)]
        )
        return pdf_path

    # ==========================================
    # 5. ORCHESTRATION
    # ==========================================

    def generate_all_data(self, num_programmers: int = 10, num_projects: int = 20, num_rfps: int = 3) -> dict:
        """Generate all data: profiles, CVs, projects, and RFPs."""
        if num_programmers <= 0: raise ValueError("Number of programmers must be positive")

        print(f"Generating {num_programmers} programmer profiles with RICH METADATA...")

        # Create output directories
        programmers_dir = self.config['output']['programmers_dir']
        rfps_dir = self.config['output']['rfps_dir']
        projects_dir = self.config['output']['projects_dir']

        for d in [programmers_dir, rfps_dir, projects_dir]:
            os.makedirs(d, exist_ok=True)

        # Generate programmer profiles
        profiles = self.generate_programmer_profiles(num_programmers)

        # Generate CVs
        generated_cv_files = []
        for i, profile in enumerate(profiles, 1):
            print(f"Generating CV {i}/{num_programmers}: {profile['name']} (${profile['hourly_rate']}/hr, GPA: {profile['education']['gpa']})")
            
            cv_markdown = self.generate_cv_markdown(profile)
            safe_name = profile['name'].replace(" ", "_").replace(".", "")
            filename = f"cv_{profile['id']:03d}_{safe_name}"
            file_path = self.save_cv_as_pdf(cv_markdown, filename, programmers_dir)
            generated_cv_files.append(file_path)

        # Generate projects (Historical + Active split inside)
        print(f"Generating {num_projects} projects (Historical/Active logic)...")
        projects = self.generate_projects(num_projects, profiles)

        # Generate RFPs
        print(f"Generating {num_rfps} RFPs (Standardized)...")
        rfps = self.generate_rfps(num_rfps)

        generated_rfp_files = []
        for i, rfp in enumerate(rfps, 1):
            print(f"Generating RFP PDF {i}/{num_rfps}: {rfp['title']}")
            rfp_markdown = self.generate_rfp_markdown(rfp)
            safe_title = rfp['title'].replace(" ", "_").replace(".", "").replace("/", "_")
            filename = f"rfp_{rfp['id']}_{safe_title}"
            file_path = self.save_cv_as_pdf(rfp_markdown, filename, rfps_dir)
            generated_rfp_files.append(file_path)

        # Save JSONs
        profiles_path = os.path.join(programmers_dir, "programmer_profiles.json")
        with open(profiles_path, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, indent=2, default=str)

        projects_path = os.path.join(projects_dir, "projects.json")
        with open(projects_path, 'w', encoding='utf-8') as f:
            json.dump(projects, f, indent=2, default=str)

        rfps_path = os.path.join(rfps_dir, "rfps.json")
        with open(rfps_path, 'w', encoding='utf-8') as f:
            json.dump(rfps, f, indent=2, default=str)

        print(f"✅ Data generation complete.")
        print(f"   CVs: {len(generated_cv_files)}")
        print(f"   Projects: {len(projects)}")
        print(f"   RFPs: {len(generated_rfp_files)}")

        return {
            "profiles": profiles,
            "projects": projects,
            "rfps": rfps,
            "cv_files": generated_cv_files,
            "rfp_files": generated_rfp_files,
            "profiles_file": profiles_path,
            "projects_file": projects_path,
            "rfps_file": rfps_path
        }


def main():
    """Generate data for GraphRAG demonstration."""
    try:
        generator = GraphRAGDataGenerator()
        config = generator.config['generation']
        # Note: config should ideally set num_projects to 150 to see full historical/active split effect
        result = generator.generate_all_data(
            config['num_programmers'],
            config['num_projects'],
            config['num_rfps']
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Ensure OPENAI_API_KEY is set and dependencies are installed.")
        raise


if __name__ == "__main__":
    main()