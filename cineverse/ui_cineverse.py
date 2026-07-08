from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from pydantic import BaseModel
from typing import List, Optional

# -------------------- LLM --------------------

model = ChatMistralAI(model="mistral-small-2506")


class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str


parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a professional Movie Information Extraction Assistant.

Extract movie information from the user's paragraph.

{format_instructions}
"""
        ),
        ("human", "{paragraph}")
    ]
)

# -------------------- Streamlit --------------------

st.set_page_config(
    page_title="🎬 CineVerse",
    page_icon="🎥",
    layout="wide",
)

st.title("🎬 CineVerse")
st.caption("AI Powered Movie Information Extractor")

st.divider()

sample_movies = {
    "✏️ Write Your Own": "",

    "🌌 Interstellar":
    """Interstellar is a visually stunning science fiction epic directed by Christopher Nolan. Released in 2014, the film stars Matthew McConaughey, Anne Hathaway, Jessica Chastain, and Michael Caine. The story revolves around a group of astronauts who travel through a wormhole near Saturn in search of a new home for humanity as Earth faces environmental collapse. The movie was widely appreciated for its emotional depth, scientific accuracy, Hans Zimmer's powerful soundtrack. It holds a rating of 8.6 on IMDb and is often considered one of the greatest sci-fi films of the 21st century.""",

    "🌀 Inception":
    """Inception is a 2010 science fiction action film directed by Christopher Nolan. It stars Leonardo DiCaprio as Dom Cobb, a skilled thief who enters people's dreams to steal secrets. Cobb is offered the chance to erase his criminal history by planting an idea into someone's subconscious. The film is celebrated for its stunning visuals, layered storytelling, and an IMDb rating of 8.8.""",

    "🦇 The Dark Knight":
    """The Dark Knight is a 2008 superhero film directed by Christopher Nolan starring Christian Bale and Heath Ledger. Set in Gotham City, Batman faces the Joker, whose chaotic crimes push the city into fear and moral conflict. Heath Ledger's performance won a posthumous Academy Award, and the film holds an IMDb rating of 9.0.""",

    "🚢 Titanic":
    """Titanic is a 1997 romantic disaster film directed by James Cameron. It stars Leonardo DiCaprio and Kate Winslet as Jack and Rose, two young lovers from different social classes who meet aboard the RMS Titanic. Their romance unfolds during the ship's tragic maiden voyage. The movie won 11 Academy Awards and has an IMDb rating of 7.9.""",

    "🧙 Harry Potter":
    """Harry Potter and the Philosopher's Stone is a 2001 fantasy film directed by Chris Columbus. It stars Daniel Radcliffe, Emma Watson, and Rupert Grint. The story follows Harry Potter as he discovers he is a wizard and begins studying at Hogwarts School of Witchcraft and Wizardry. The film became one of the highest-grossing movies of its time."""
}

selected = st.selectbox(
    "Choose a sample paragraph",
    sample_movies.keys()
)

paragraph = st.text_area(
    "Movie Paragraph",
    value=sample_movies[selected],
    height=250,
)

if st.button("🎬 Extract Information", use_container_width=True):

    if paragraph.strip() == "":
        st.warning("Please enter a movie paragraph.")
        st.stop()

    final_prompt = prompt.invoke(
        {
            "paragraph": paragraph,
            "format_instructions": parser.get_format_instructions(),
        }
    )

    with st.spinner("Analyzing movie..."):

        response = model.invoke(final_prompt)
        movie = parser.parse(response.content)

    st.success("Extraction Complete!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎥 Movie Details")
        st.write(f"**Title:** {movie.title}")
        st.write(f"**Release Year:** {movie.release_year}")
        st.write(f"**Director:** {movie.director}")
        st.write(f"**IMDb Rating:** {movie.rating}")

    with col2:
        st.subheader("🎭 Genre & Cast")
        st.write("**Genres**")
        st.write(", ".join(movie.genre))

        st.write("**Main Cast**")
        st.write(", ".join(movie.cast))

    st.divider()

    st.subheader("📝 Summary")
    st.info(movie.summary)

    with st.expander("📦 View Parsed JSON"):
        st.json(movie.model_dump())