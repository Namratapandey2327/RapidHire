from src.sourcesync.analyzer.parser import analyze_candidate

def test_analyze_candidate_detects_visa_and_skills():
    text = "5 years experience with Python, AWS, and React. H1B sponsorship available."
    result = analyze_candidate(text)

    assert result["Visa"] == "H1B/Sponsorship"
    assert "Python" in result["Skills"]
    assert result["Experience"] == "5"

def test_analyze_candidate_detects_skills_from_pasted_section():
    text = "Skills: Python, Docker, Kubernetes, Terraform, Jenkins\nExperience with cloud-native development."
    result = analyze_candidate(text)

    assert "Python" in result["Skills"]
    assert "Docker" in result["Skills"]
    assert "Kubernetes" in result["Skills"]
    assert "Terraform" in result["Skills"]
    assert "Jenkins" in result["Skills"]


def test_analyze_candidate_returns_undetermined_when_missing_info():
    text = "Entry-level developer with no explicit visa or years listed."
    result = analyze_candidate(text)

    assert result["Visa"] == "Undetermined"
    assert result["Skills"] == []
    assert result["Experience"] == "N/A"

def test_analyze_candidate_detects_mulesoft_and_openshift_from_jd():
    text = (
        "10+ years of IT experience with MuleSoft, OpenShift, RTF, AKS, CI/CD, GitHub, "
        "Unix, Azure, Nexus, Elasticsearch, ActiveMQ, SonarQube, Datadog, Grafana"
    )
    result = analyze_candidate(text)

    assert "MuleSoft" in result["Skills"]
    assert "OpenShift" in result["Skills"]
    assert "ActiveMQ" in result["Skills"]
    assert result["Experience"] == "10"
    assert result["Location"] == "Undetermined"

def test_analyze_candidate_detects_remote_location():
    text = "Software Engineer Offshore Remote role with MuleSoft and OpenShift"
    result = analyze_candidate(text)

    assert result["Location"] == "Offshore"

def test_analyze_candidate_detects_uae_location():
    text = "Location: Abu Dhabi, UAE - Senior Developer with 5 years experience"
    result = analyze_candidate(text)

    assert result["Location"] == "Abu Dhabi UAE"
    assert result["Experience"] == "5"

def test_analyze_candidate_detects_enhanced_visa_patterns():
    # Test H1B variations
    text1 = "Experienced QA with 4 years in payments, currently on H1-B seeking transfer"
    result1 = analyze_candidate(text1)
    assert result1["Visa"] == "H1B/Sponsorship"

    # Test Citizen variations
    text2 = "US Citizen with green card holder status"
    result2 = analyze_candidate(text2)
    assert result2["Visa"] == "Citizen/GC"

    # Test OPT variations
    text3 = "F1 student on OPT with STEM extension"
    result3 = analyze_candidate(text3)
    assert result3["Visa"] == "OPT/CPT"

    # Test TN Visa
    text4 = "TN visa holder working as software engineer"
    result4 = analyze_candidate(text4)
    assert result4["Visa"] == "TN Visa"

    # Test sponsorship needs
    text5 = "Needs visa sponsorship for H1B transfer"
    result5 = analyze_candidate(text5)
    assert result5["Visa"] == "H1B/Sponsorship"

def test_analyze_candidate_detects_job_title():
    # Test QA Engineer title
    text1 = "QA Engineer – Payment Domain with 5 years experience"
    result1 = analyze_candidate(text1)
    assert result1["Job Title"] == "Qa Engineer"

    # Test Senior Developer title
    text2 = "Senior Software Developer at Tech Corp"
    result2 = analyze_candidate(text2)
    assert result2["Job Title"] == "Senior Software Developer"

    # Test title with dash
    text3 = "Lead QA Engineer - Automation"
    result3 = analyze_candidate(text3)
    assert result3["Job Title"] == "Lead Qa Engineer"

    # Test title in position field
    text4 = "Position: DevOps Engineer"
    result4 = analyze_candidate(text4)
    assert result4["Job Title"] == "Devops Engineer"
