import re

def analyze_candidate(text):
    """
    Analyzes a candidate's bio for key recruitment parameters.
    """
    # 1. Visa Status Detection
    visa_patterns = {
        "H1B/Sponsorship": r"h1b|h-1b|sponsorship|visa|transfer",
        "Citizen/GC": r"citizen|green card|gc holder|permanent resident",
        "OPT/CPT": r"opt|cpt|ead|stem opt"
    }
    
    found_visa = "Undetermined"
    for status, pattern in visa_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            found_visa = status
            break

    # 2. Tech Stack Detection (Customize this for your current roles!)
    tech_keywords = ["Python", "Flask", "Django", "FastAPI", "React", "AWS", "SQL"]
    found_tech = [tech for tech in tech_keywords if tech.lower() in text.lower()]

    # 3. Experience Estimation
    exp_match = re.search(r"(\d+)\+?\s*(years|yrs)", text, re.IGNORECASE)
    years = exp_match.group(1) if exp_match else "N/A"

    return {
        "Visa": found_visa,
        "Skills": found_tech,
        "Experience": years
    }