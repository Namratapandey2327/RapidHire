import streamlit as st
from src.sourcesync.analyzer.parser import analyze_candidate

st.title("SourceSync: Candidate Analyzer")

# User Input
bio_input = st.text_area("Paste the candidate's 'About' or 'Experience' section here:", height=200)

if st.button("Quick Analyze"):
    if bio_input:
        results = analyze_candidate(bio_input)
        
        # Display Results in nice columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Visa Status", results["Visa"])
        with col2:
            st.metric("Experience", f"{results['Experience']} Years")
        with col3:
            st.write("**Top Skills Found:**")
            st.write(", ".join(results["Skills"]) if results["Skills"] else "None detected")
    else:
        st.warning("Please paste some text first!")