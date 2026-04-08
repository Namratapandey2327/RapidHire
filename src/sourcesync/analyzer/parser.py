import re

def analyze_candidate(text):
    """
    Analyzes a candidate's bio for key recruitment parameters.
    """
    # 1. Job Title Detection
    job_title_patterns = [
        r"\b(?:senior|lead|principal|staff|junior|associate)?\s*(?:qa|software|devops|data|cloud|full.?stack|backend|frontend|mobile|ios|android|machine learning|ml|ai)\s+(?:engineer|developer|architect|analyst|specialist|consultant|administrator|manager|tester)\b",
        r"\b(?:qa|software|devops|data|cloud|full.?stack|backend|frontend|mobile|ios|android|machine learning|ml|ai)\s+(?:engineer|developer|architect|analyst|specialist|consultant|administrator|manager|tester)\b",
        r"(?:position|role|title)\s*[:\-]\s*([^\n\r]{5,60})",
        r"^([^\n\r]{5,40}?)(?:\s*[-–]\s*|\s*@\s*|\s*at\s*|\s*in\s*|\s*\|\s*)"
    ]
    
    found_job_title = "Undetermined"
    for pattern in job_title_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            title = match.group(1) if match.groups() else match.group(0)
            title = title.strip()
            # Clean up the title
            title = re.sub(r'^[^\w]*|[^\w]*$', '', title)  # Remove leading/trailing non-word chars
            # Only take reasonable length titles
            if 5 <= len(title) <= 60:
                # Capitalize words properly
                found_job_title = ' '.join(word.capitalize() for word in title.split())
                break

    # 2. Visa Status Detection - Enhanced with more robust patterns
    visa_patterns = {
        "H1B/Sponsorship": r"\bh1-?b\b|h-1b|visa.*sponsor|sponsor.*visa|transfer.*visa|visa.*transfer|seeking.*transfer|transfer.*seeking|needs.*sponsor|sponsor.*needed|work.*permit|employment.*authorization",
        "OPT/CPT": r"\bopt\b|\bcpt\b|\bead\b|stem.?opt|practical.?training|curricular.?practical",
        "H4 Visa": r"\bh4\b|h-4.?visa|dependent.?visa",
        "TN Visa": r"\btn\b|tn.?visa|nafta.?professional",
        "F1 Visa": r"\bf1\b|f-1.?visa|student.?visa",
        "Citizen/GC": r"\bcitizen\b|green.?card|gc.?holder|permanent.?resident|usc|us.?citizen|authorized.*work.*permanently|work.*authorized.*permanently"
    }
    
    found_visa = "Undetermined"
    for status, pattern in visa_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            found_visa = status
            break

    # 3. Location Detection - UAE focused
    location_patterns = {
        "Offshore": r"\boffshore\b",
        "Remote": r"\bremote\b",
        "Abu Dhabi UAE": r"\babu dhabi(?:[,.\s]*(?:uae|united arab emirates)|\s*-\s*(?:uae|united arab emirates))\b|(?:uae|united arab emirates)(?:\s*-\s*|\s*,\s*|\s+)abu dhabi\b",
        "Dubai UAE": r"\bdubai(?:[,.\s]*(?:uae|united arab emirates)|\s*-\s*(?:uae|united arab emirates))\b|(?:uae|united arab emirates)(?:\s*-\s*|\s*,\s*|\s+)dubai\b",
        "Sharjah UAE": r"\bsharjah(?:[,.\s]*(?:uae|united arab emirates)|\s*-\s*(?:uae|united arab emirates))\b|(?:uae|united arab emirates)(?:\s*-\s*|\s*,\s*|\s+)sharjah\b",
        "UAE": r"\b(?:uae|united arab emirates)\b(?!(?:\s*[-]\s*|\s*,\s*|\s+)(?:abu dhabi|dubai|sharjah))",
    }

    found_location = "Undetermined"
    for location, pattern in location_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            found_location = location
            break

    # 3. Tech Stack Detection
    #    Automatically detect common technologies from pasted text or JD/resume snippets.
    tech_keywords = [
        "MuleSoft", "OpenShift", "RTF", "AKS", "CI/CD", "GitHub",
        "Unix", "Azure", "Nexus", "Elasticsearch", "ActiveMQ",
        "SonarQube", "Datadog", "Grafana", "DB Cache",
        "Python", "Flask", "Django", "FastAPI", "React", "AWS", "SQL",
        "Docker", "Kubernetes", "Terraform", "Jenkins", "Linux",
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Kafka",
        "Java", "JavaScript", "TypeScript", "Node.js", "Angular", "Vue",
        "C#", "Go", "Ruby", "Swift", "Kotlin", "PowerShell"
    ]

    def _split_skill_terms(skill_text):
        return [term.strip().strip('"\'.,;()[]{}') for term in re.split(r"\b(?:and|or)\b|[,/|&]+", skill_text) if term.strip()]

    def _extract_skills_from_sections(text):
        skill_phrases = []
        patterns = [
            r"(?:skills|technologies|tech stack|tools)\s*[:\-]\s*([^\n\r]+)",
            r"(?:experience with|experienced in|proficient in|familiar with|expert in)\s*([^\.\;\n\r]+)",
            r"(?:knowledge of|working knowledge of|hands[- ]on experience with)\s*([^\.\;\n\r]+)"
        ]
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                skill_phrases.append(match.group(1))

        found = []
        for phrase in skill_phrases:
            if not re.search(r"[,/|&]|\band\b|\bor\b", phrase, re.IGNORECASE):
                continue
            for term in _split_skill_terms(phrase):
                normalized_term = term.strip()
                if not normalized_term:
                    continue
                for tech in tech_keywords:
                    if normalized_term.lower() == tech.lower():
                        found.append(tech)
                        break
                else:
                    if len(normalized_term) > 2 and re.search(r"[A-Za-z0-9]", normalized_term):
                        found.append(normalized_term)
        return list(dict.fromkeys(found))

    text_lower = text.lower()
    found_tech = _extract_skills_from_sections(text)
    if not found_tech:
        found_tech = [tech for tech in tech_keywords if tech.lower() in text_lower]

    # 4. Experience Estimation
    exp_match = re.search(r"(\d+)\+?\s*(years|yrs)", text, re.IGNORECASE)
    years = exp_match.group(1) if exp_match else "N/A"

    return {
        "Job Title": found_job_title,
        "Visa": found_visa,
        "Location": found_location,
        "Skills": found_tech,
        "Experience": years
    }