import streamlit as st
from src.sourcesync.analyzer.parser import analyze_candidate
from src.sourcesync.scraper.engine import PlaywrightScraper
import os

def get_visa_status_color(visa_status):
    """Return color and styling info for visa status."""
    color_map = {
        "Citizen/GC": {"color": "green", "bg_color": "#d4edda", "border_color": "#c3e6cb"},
        "OPT/CPT": {"color": "blue", "bg_color": "#cce7ff", "border_color": "#b3d9ff"},
        "TN Visa": {"color": "blue", "bg_color": "#cce7ff", "border_color": "#b3d9ff"},
        "F1 Visa": {"color": "orange", "bg_color": "#fff3cd", "border_color": "#ffeaa7"},
        "H4 Visa": {"color": "orange", "bg_color": "#fff3cd", "border_color": "#ffeaa7"},
        "H1B/Sponsorship": {"color": "red", "bg_color": "#f8d7da", "border_color": "#f5c6cb"},
        "Undetermined": {"color": "gray", "bg_color": "#f8f9fa", "border_color": "#dee2e6"}
    }
    return color_map.get(visa_status, color_map["Undetermined"])

st.title("SourceSync: Candidate Analyzer & X-ray Search")

# User Input
bio_input = st.text_area("Paste the candidate's 'About' or 'Experience' section here:", height=200)

if st.button("Quick Analyze"):
    if bio_input:
        results = analyze_candidate(bio_input)

        # Display Results with enhanced visa status visualization
        col1, col2, col3, col4 = st.columns(4)

        # Enhanced Visa Status Display
        with col1:
            visa_info = get_visa_status_color(results["Visa"])
            st.markdown(f"""
            <div style="
                padding: 20px;
                border-radius: 10px;
                border: 2px solid {visa_info['border_color']};
                background-color: {visa_info['bg_color']};
                text-align: center;
                margin-bottom: 10px;
            ">
                <h4 style="color: {visa_info['color']}; margin: 0; font-size: 16px;">Visa Status</h4>
                <p style="color: {visa_info['color']}; margin: 5px 0 0 0; font-size: 18px; font-weight: bold;">{results["Visa"]}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.metric("Job Title", results["Job Title"])
        with col3:
            st.metric("Experience", f"{results['Experience']} Years")
        with col4:
            st.metric("Location", results["Location"])

        st.write("**Top Skills Found:**")
        st.write(", ".join(results["Skills"]) if results["Skills"] else "None detected")

        # Add visa status legend
        st.markdown("""
        **Visa Status Legend:**
        - 🟢 **Green**: Citizen/GC (No sponsorship needed)
        - 🔵 **Blue**: OPT/CPT, TN Visa (Temporary work authorization)
        - 🟡 **Yellow**: F1, H4 Visa (Student/dependent status)
        - 🔴 **Red**: H1B/Sponsorship (Requires sponsorship/transfer)
        - ⚪ **Gray**: Undetermined (Need to verify manually)
        """)
    else:
        st.warning("Please paste some text first!")

# X-ray Search Section
st.header("X-ray Search (DuckDuckGo)")
jd_input = st.text_area("Paste Job Description for X-ray Search:", height=150)

if st.button("Perform X-ray Search"):
    if jd_input:
        # Parse JD first
        parsed_keywords = analyze_candidate(jd_input)
        st.subheader("Parsed Keywords from JD:")
        st.write(f"**Job Title:** {parsed_keywords['Job Title']}")
        st.write(f"**Skills:** {', '.join(parsed_keywords['Skills']) if parsed_keywords['Skills'] else 'None'}")
        st.write(f"**Location:** {parsed_keywords['Location']}")
        st.write(f"**Experience:** {parsed_keywords['Experience']} Years")

        if not (parsed_keywords["Job Title"] != "Undetermined" or parsed_keywords["Skills"] or parsed_keywords["Location"] != "Undetermined" or parsed_keywords["Experience"] != "N/A"):
            st.warning("No usable keywords were detected in the job description. Add job title, skills, location, or experience details to perform X-ray search.")
        else:
            # Perform X-ray search
            with st.spinner("Performing X-ray search on DuckDuckGo..."):
                try:
                    scraper = PlaywrightScraper(headless=True)
                    scraper.launch()
                    search_results = scraper.xray_search(parsed_keywords)
                    scraper.close()

                    if search_results:
                        st.success(f"Found {len(search_results)} potential candidates on DuckDuckGo!")

                        for i, candidate in enumerate(search_results, 1):
                            with st.expander(f"{i}. {candidate['name']}"):
                                st.write(f"**Headline:** {candidate['headline']}")
                                if candidate['profile_url']:
                                    st.write(f"**Profile:** {candidate['profile_url']}")
                                st.write(f"**Source:** {candidate['source']}")
                    else:
                        st.info("No candidates found matching the criteria. If the JD has no detectable skills or search keywords, try adding more details.")

                except Exception as e:
                    st.error(f"Search failed: {str(e)}")
                    st.info("💡 **Troubleshooting tips:**\n"
                           "1. Make sure Firefox is installed: `sudo apt-get install firefox`\n"
                           "2. Try again in a few moments\n"
                           "3. Check your internet connection")
    else:
        st.warning("Please paste a job description first!")