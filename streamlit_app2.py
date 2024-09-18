import os
import openai
import io
import time
import tempfile
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

#from pypdf import PdfReader
#from tika import parser


load_dotenv()

# python -m streamlit run streamlit_app2.py

## Rather than a tool for individuals to prepare for interviews, what if it was used by recruiters to support candidates? So a recruiter will have a role definition from an organisation and then may plan to put forward several candidates for an interview. The recruiter supplies the job description and company profile and for each CV/applicant profile can request the LLM to prepare a document that gives sample questions/answers, and perhaps some general advice on what topics to prepare for. What do you think?

# Connect to OpenAI 
client = OpenAI()
#openai.api_key = os.getenv("OPENAI_API_KEY")


title = 'TailorQ'
#st.set_page_config(page_title=title, page_icon="img/careerguru_logo.png",)
st.set_page_config(page_title=title, page_icon="img/TailorQ_logo.png",)
#st.title(title)

# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -300rem;}</style>''',
    unsafe_allow_html=True)

# Design change hyperlink href link color
st.markdown('''<style>.css-znku1x a {color: #9d03fc;}</style>''',
    unsafe_allow_html=True)  # darkmode

# Design change hyperlink href link color
st.markdown('''<style>.css-znku1x a {color: #9d03fc;}</style>''',
    unsafe_allow_html=True)  # darkmode

# Design change height of text input fields headers
st.markdown('''<style>.css-qrbaxs {min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)

# Design change spinner color to primary color
st.markdown('''<style>.stSpinner > div > div {border-top-color: #9d03fc;}</style>''',
    unsafe_allow_html=True)

# Design change min height of text input box
st.markdown('''<style>.css-15tx938{min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)

# Design hide top header line
hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

# Design hide "made with streamlit" footer menu area
hide_streamlit_footer = """<style>#MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

@st.cache_resource
def generate_questions(interview_type, question_count, input_contents, answers):
    if answers:
        prompt_text = f"""
        You are an experienced interview assistant helping managers prepare tailored interview questions. 
        The manager will provide you with a job title and a description, and you will create a list of relevant questions to guide the interview process.
        
        Please generate a set of {question_count} high-quality questions for a {interview_type} interview with their respective answers.
        
        The position and desription being interviewed for is: {input_contents}.

        Ensure the questions are thoughtful, focus on key competencies for the role, and maintain a professional tone throughout.
        """
    
    else:
        prompt_text = f"""
        You are an experienced interview assistant helping managers prepare tailored interview questions. 
        The manager will provide you with a job title and a description, and you will create a list of relevant questions to guide the interview process.
        
        Please generate a set of {question_count} high-quality questions for a {interview_type} interview. 
        
        The position and desription being interviewed for is: {input_contents}.

        Ensure the questions are thoughtful, focus on key competencies for the role, and maintain a professional tone throughout.
        """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt_text},
            #{"role": "user", "content": "I'm applying for senior data scientist"},
        ]
        )
    message = response.choices[0].message.content
    # for word in response.split():
    #     yield word + " "
    #     time.sleep(0.05)
    return message
    #return 'successfully done'


def summarise_resume(uploaded_cv):
    if uploaded_cv is not None:

        #st.write("File uploaded successfully!")


        # Save the uploaded file as a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_cv.read())  # Write the uploaded PDF content to a temp file
            temp_file_path = tmp_file.name
        
        # Use PyPDFLoader to read the content of the PDF from the temporary file path
        loader = PyPDFLoader(temp_file_path)
        documents = loader.load()

        # Combine all documents into a single text
        full_text = "\n".join([doc.page_content for doc in documents])

        summary_prompt = f"Summarize the following resume into one concise paragraph, highlighting the candidate's key skills, experience, and qualifications: \n\n{full_text}."

        resume_summary = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": summary_prompt},
            ] 
        )
        summary = resume_summary.choices[0].message.content
        return summary


def stream_response(response): # this was never used
    for chunk in response.split():
        yield chunk + " "
        time.sleep(0.05)


def create_main_frame():
    st.image('img/TailorQ_banner.png')  # TITLE and Creator information
    st.markdown("Prepare for interviews like a pro! Our app instantly creates tailored interview questions based on the job title and description, helping you focus on key skills and make smarter hiring decisions.")
    st.markdown("No more stress—just easy, effective interview prep!")
    st.write('\n')  # add spacing

    st.subheader('\nWhat role are you hiring for?\n')
    
    with st.expander("Role Description - Expand for Customization", expanded=False):
        job_title = st.text_input('Enter the role the candidates are applying for', 'Data Scientist')
        job_desc = st.text_area("Enter the description of the role", 'We are seeking a skilled and motivated Data Scientist to join our team. As a mid-level Data Scientist, you will work on developing and implementing data models, performing data analysis, and contributing to data-driven decision-making. You’ll collaborate with cross-functional teams to turn raw data into valuable insights that help drive our business forward.', height=20)

        uploaded_cv = st.file_uploader("Upload the candidate's CV", type=['pdf', 'docx'])

        interview_questions = ""


    col1, col2, col3, col4 = st.columns([3, 3, 3, 3])

    with col1:
        interview_type = st.selectbox('Interview Type',
                                    ('General', 'Technical'),
                                    index=0)
    with col2:
        #question_count = st.text_input('Question Count', '2')
        #question_count = str(st.slider('Question Count', 2, 10))
        question_count = st.selectbox('Question Count', ('2', '3', '4', '5', '6', '7', '8', '9', '10'), index=0)
    with col3:
        answers = st.checkbox('Provide Sample Answers')

    with col4:
        st.write("\n")  # add spacing
        st.write("\n")  # add spacing
        if st.button('Generate Questions'):
            with st.spinner():

                input_contents = []  # let the user input all the data
                if (job_title != ""):# and (input_c1 != 'topic 1'):
                    input_contents.append(str(job_title))
                if (job_desc != ""):# and (input_c2 != 'topic 2 (optional)'):
                    input_contents.append(str(job_desc))

                if (len(input_contents) == 0):  # remind user to provide data
                    st.write('Please fill in some contents for your message!')
                # if (len(input_sender) == 0) or (len(input_recipient) == 0):
                #     st.write('Sender and Recipient names can not be empty!')


                if (len(input_contents) >= 1):  # initiate llm
                    if (len(interview_type) != 0) and (len(question_count) != 0):
                        # email_text = gen_mail_format(input_sender,
                        #                                 input_recipient,
                        #                                 input_style,
                        #                                 input_contents)
                        interview_questions = generate_questions(interview_type, question_count, input_contents, answers)


    if interview_questions != "":
        with st.expander("Interview Questions", expanded=True):
            st.markdown(interview_questions)
            # with st.chat_message("assistant"):
            #     response = st.write(stream_response(interview_questions))


    if uploaded_cv is not None:

        st.text_area("Resume Summary", summarise_resume(uploaded_cv), height=200)

        # st.write("File uploaded successfully!")

        # # Save the uploaded file as a temporary file
        # with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        #     tmp_file.write(uploaded_cv.read())  # Write the uploaded PDF content to a temp file
        #     temp_file_path = tmp_file.name
        
        # # Use PyPDFLoader to read the content of the PDF from the temporary file path
        # loader = PyPDFLoader(temp_file_path)
        # documents = loader.load()

        # # Display the PDF content
        # for page, doc in enumerate(documents):
        #     st.write(f"### Page {page + 1}:") 
        #     st.write(doc.page_content)
        #     #st.write(f'Page {page} read successfully.')



if __name__ == '__main__': 
    # call main function
    create_main_frame()


