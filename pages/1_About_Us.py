import streamlit as st

st.set_page_config(
    page_title="About Us",
)

st.write("# About Us 👋")

st.markdown(
    """

## Project Scope

Our Course Recommender app is a proof-of-concept designed to rethink how learners discover courses. Instead of browsing through thousands of listings, users can simply describe in natural language what they want to learn. The system then interprets their intent and provides a curated list of relevant course recommendations.

This prototype currently focuses on a dataset of **1,000 randomly sampled courses** crawled from the **SkillsFuture** platform. The initial scope is intentionally limited for experimentation.

## Objectives

1. **Simplify Course Discovery**
   Enable users to find suitable courses quickly without complex filters and endless scrolling.

2. **Leverage Natural Language Input**
   Allow users to express learning goals freely and translate those descriptions into meaningful recommendations.

## Data Sources

The project uses course information sourced from the **Singapore SkillsFuture** website. From all the listings, we randomly sampled **1,000 courses**, capturing key attributes such as:

* Course titles
* Provider information
* Descriptions and learning outcomes
* Cost before and after subsidy
* Eligibility or requirements

Since this is just a prototype and some time is required to scrape all the courses, we have chosen to randomly select 1000 courses.

## Features

1. **Natural Language Querying**

Users can describe what they want to learn in their own words, e.g., “I want to improve my communication skills” or “courses related to Python for data analysis”, and receive relevant recommendations instantly.

2. **Intelligent Course Matching**

The system uses semantic understanding to interpret user intent, match it to course descriptions, and surface options that closely align with the user’s goals.

3. **Streamlined Recommendation Interface**

Instead of navigating multiple search filters or long lists, users see a concise, ranked selection of courses tailored to their inputs.

## Source Code

Source code can be found [here](https://github.com/amber60/project-folder)

"""
)
