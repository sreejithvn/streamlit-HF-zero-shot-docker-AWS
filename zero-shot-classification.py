
import streamlit as st
import pandas as pd

# Import for API calls
import requests

# Import for navbar
from streamlit_option_menu import option_menu

# Import for dynamic tagging
from streamlit_tags import st_tags


st.set_page_config(layout='wide', page_title="Zero-Shot Text Classifier", page_icon="🤗")

c1, c2 = st.columns([0.4, 2])

with c1:

    st.image("logo.png", width=110)

with c2:

    st.caption("")
    st.title("Zero-Shot Text Classifier")

with st.sidebar:
    selected = option_menu(
        "",
        ["Demo", "Unlocked Mode"],
        icons=["bi-joystick", "bi-key-fill"],
        menu_icon="",
        default_index=0,
    )


if selected == "Demo":
    # ADD CODE FOR DEMO HERE
    
    API_KEY = st.secrets["API_TOKEN"]

    API_URL = ("https://api-inference.huggingface.co/models/valhalla/distilbart-mnli-12-3")

    headers = {"Authorization": f"Bearer {API_KEY}"}

    with st.form(key="my_form"):

        label_widget = st_tags(
            label="",
            text="Add labels - 3 max",
            value=["Medicine", "Computer Science", "Mathematics"],
            suggestions=[
                "Medicine",
                "Computer Science",
                "Mathematics",
                "Physics",
                "Positive",
                "Negative",
                "Neutral",
            ],
            maxtags=3,
        )

        sample = '''Today, the development of new interfaces and block-programming languages facilitates the teaching of coding and computational thinking starting in kindergarten. However, as new programming languages that are developmentally appropriate emerge, there is a need to explicitly conceptualize pedagogical approaches for teaching computer science in the early years that embrace the maturational stages of children by inviting play and discovery, socialization, and creativity.
This paper is an attempt to summarize the basic elements of the multiset theory. We begin by describing multisets and the operations between them, then we present hybrid sets and their operations. We continue with a categorical approach to multisets, and then we present fuzzy multisets and their operations. Finally, we present partially ordered multisets.
Busy doctors have never had time to read all the journals in their disciplines. There are, for example, about 20 clinical journals in adult internal medicine that report studies of direct importance to clinical practice, and in 1992 these journals included over 6000 articles with abstracts: to keep up the dedicated doctor would need to read about 17 articles a day every day of the year.1 In earlier eras limitations in our understanding of human biology and the absence of powerful clinical research methods meant that major advances were published far less commonly than now. Consequently, clinicians' failure to keep up did not harm patients.
AI is the general term for the science of artificial intelligence. It uses computers to simulate human intelligent behaviors and it trains computers to learn human behaviors such as learning, judgment, and decision-making [94]. AI is a knowledge project that takes knowledge as the object, acquires knowledge, analyzes and studies the expression methods of knowledge, and employs these approaches to achieve the effect of simulating human intellectual activities [19]. AI is a compilation of computer science, logic, biology, psychology, philosophy, and many other disciplines, and it has achieved remarkable results in applications such as speech recognition, image processing, natural language processing, the proving of automatic theorems, and intelligent robots
Machine learning addresses the question of how to build computers that improve automatically through experience. It is one of todays most rapidly growing technical fields, lying at the intersection of computer science and statistics, and at the core of artificial intelligence and data science. Recent progress in machine learning has been driven both by the development of new learning algorithms and theory and by the ongoing explosion in the availability of online data and low-cost computation. The adoption of data-intensive machine-learning methods can be found throughout science, technology and commerce, leading to more evidence-based decision-making across many industries including manufacturing, education, financial modeling, policing, and marketing.
'''


        MAX_LINES = 5
        text = st.text_area(
                    "Enter keyphrase to classify",
                    sample,
                    height=200,
                    key="2",
                    help="At least two keyphrases for the classifier to work, one per line, " + str(MAX_LINES)+ " keyphrases max as part of the demo",
                )
        lines = text.split("\n")  # A list of lines
        linesList = []
        for x in lines:
            linesList.append(x)
        linesList = list(dict.fromkeys(linesList))  # Remove dupes
        linesList = list(filter(None, linesList))  # Remove empty


        if len(linesList) > MAX_LINES:

            st.info(
                f"🚨 Only the first " + str(MAX_LINES) + " keyprases will be reviewed. Unlock that limit by switching to 'Unlocked Mode'"
            )

        submit_button = st.form_submit_button(label="Submit")


    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        # Unhash to check status codes from the API response
        # st.write(response.status_code)
        return response.json()

    if submit_button:

        listToAppend = []

        # st.write(linesList)

        for row in linesList:
            output2 = query(
                        {
                            "inputs": row,
                            "parameters": {"candidate_labels": label_widget},
                            "options": {"wait_for_model": True},
                        }
                    )


            listToAppend.append(output2)

        # st.write(listToAppend)

        df = pd.DataFrame.from_dict(listToAppend)

        st.dataframe(df)



elif selected == "Unlocked Mode":
	# ADD CODE FOR 'Unlocked Mode' HERE
    pass


