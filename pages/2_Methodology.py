import streamlit as st

st.set_page_config(
    page_title="Methodology",
)

st.write("# Methodology")

st.markdown(
    """

## Implementation Details

1. Data Scraping and Processing
   - Gather the full list of available courses from the source website.
   - Standardise and clean the extracted course details.
   - Randomly select 1000 courses and extract course information from each of the individual webpages.
   - Perform a second round of cleaning to ensure consistency and usability of the dataset.
2. Data Ingestion into the Vector Database
   - Splitting and chunking
   - Store the processed embeddings and metadata in the vector database.
3. Querying
   - RAG Pipeline to interpret user queries and retrieve relevant content.
   - Generate response.
   - Improving Prompt Template.
4. Deploying to Streamlit
   - Deploying Chatbot.
   - Password Protection for controlled access.
   - Multipage App.
   - Deploying.

## Use Cases

### Use Case 1: Course Recommender

#### When to use it:
This mode is designed for users who have a general sense of what they enjoy or what they want to avoid, but do not yet have a concrete idea of which specific courses might suit them.

#### Typical user situation:

- “I’m interested in creative fields… maybe design? But I’m also curious about marketing.”
- “I don’t like coding-heavy courses, but I want something related to technology.”
- “I want to upskill, but I’m not sure what’s out there.”

#### How it works:
The Course Recommender interprets these broad, loosely defined preferences and analyses course descriptions to identify patterns that align with the user’s stated likes or dislikes. Instead of requiring the user to specify precise keywords, it discovers relevant options on their behalf.

#### Value to the user:

- Helps users explore possibilities they may not have considered.
- Surfaces related learning opportunities that match their general interests.
- Ideal for early-stage learners or those seeking inspiration.

### Use Case 2: Course Finder

#### When to use it:
This mode supports users who already know exactly what they want, or at least have a clear understanding of the skill, topic, or certification they’re looking for.

#### Typical user situation:

- “I want a course on Python for data analytics.”
- “Find me a certified cybersecurity fundamentals programme.”
- “I need a WSQ digital marketing course, preferably beginner-friendly.”

#### How it works:
The Course Finder uses the user’s specific intent to perform a targeted search across the course dataset. It filters out irrelevant options and returns only courses that closely match the stated criteria.

#### Value to the user:

- Saves time by eliminating irrelevant content.
- Ensures the user does not need to manually browse courses.
- Ideal for goal-driven learners with defined objectives or deadlines.

"""
)
