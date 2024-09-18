import os
import openai
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

import pandas as pd

load_dotenv()

# python -m streamlit run streamlit_app.py

# Connect to OpenAI 
client = OpenAI()
#openai.api_key = os.getenv("OPENAI_API_KEY")


title = 'CareerGuru'
st.set_page_config(page_title=title, page_icon="img/careerguru_logo.png",)
st.title(title)


def generate_question():
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant that help people prepare for their interviews. For each role provode at least two questions and answer pairs. Be a cheerleader and keep your tone motivational."},
    #         {"role": "user", "content": "I'm applying for senior data scientist"},
    #     ]
    #     )
    # message = response.choices[0].message.content
    # print(message)
    return 'successfully done'


def create_main_frame():
    #st.image('img/image_banner.png')  # TITLE and Creator information
    st.markdown('Generate professional sounding emails based on your direct comments - powered by Artificial Intelligence (OpenAI GPT-3) Implemented by '
        '[stefanrmmr](https://www.linkedin.com/in/stefanrmmr/) - '
        'view project source code on '
        '[GitHub](https://github.com/stefanrmmr/gpt3_email_generator)')
    st.write('\n')  # add spacing

    st.subheader('\nWhat role are you applying for?\n')
    with st.expander("SECTION - Email Input", expanded=True):
        user_role = st.text_input('Enter the role you are applying for!', 'Your role')
        company_name = st.text_input("Enter the company's name you're applying for.", 'Company name')

        interview_questions = ""

    col1, col2, col3, space, col4 = st.columns([5, 5, 5, 0.5, 5])

    with col1:
        input_sender = st.text_input('Sender Name', '[rephraise]')
    with col2:
        input_recipient = st.text_input('Recipient Name', '[recipient]')
    with col3:
        input_style = st.selectbox('Writing Style',
                                    ('formal', 'motivated', 'concerned', 'disappointed'),
                                    index=0)

    with col4:
        st.write("\n")  # add spacing
        st.write("\n")  # add spacing
        if st.button('Generate Questions'):
            with st.spinner():

                input_contents = []  # let the user input all the data
                if (user_role != ""):# and (input_c1 != 'topic 1'):
                    input_contents.append(str(user_role))
                if (company_name != ""):# and (input_c2 != 'topic 2 (optional)'):
                    input_contents.append(str(company_name))

                if (len(input_contents) == 0):  # remind user to provide data
                    st.write('Please fill in some contents for your message!')
                # if (len(input_sender) == 0) or (len(input_recipient) == 0):
                #     st.write('Sender and Recipient names can not be empty!')

                if (len(input_contents) >= 1):  # initiate llm
                    if (len(input_sender) != 0) and (len(input_recipient) != 0):
                        # email_text = gen_mail_format(input_sender,
                        #                                 input_recipient,
                        #                                 input_style,
                        #                                 input_contents)
                        generate_question()
    if interview_questions != "":
        with st.expander("Section - Interview Questions Outpit", expanded=True):
            st.markdown(interview_questions)






if __name__ == '__main__': 
    # call main function
    generate_question()