# TODO: 1. Maybe add a checkbox to include the answer or not ✅ 12/09
# TODO: 2. Provide how many questions and answer pairs the user wants (maybe a dropdown or a scale) ✅ 12/09
# TODO: 3. A dropdown fo the general/technical question ✅ 12/09
# TODO: 4. Stream the response - I had problem with markdown 
# TODO: 5. Change the color of the generate questions button
# TODO: 6. Change the main fonts
# TODO: 7. Read the resume ✅ 16/9
# TODO: 8. Summarize the resume and put it in the place holder ✅ 16/9
# TODO: 9. Put the questions into a placeholder like a table, maybe separate each question - I think the answers are well presented
# TODO: 10. Extract candidate's name from the resume - it clutters up my space, pass
# TODO: 11. Give warning with st components like st.warning
# TODO: 12. Remove certainely from the start of the answers ✅ 17/9
# TODO: 13. Add the download button ✅ 17/9
# TODO: 14. Generate a proper pdf with different headers and sections
# TODO: 15. Add date and time in generated pdf's name ✅ 17/9
# TODO: 16. Add candidate's name in the pdf file 
# TODO: 17. Add line breaks if possible 
# TODO: 18. Hide resume summary section in the pdf file if it is not provided
# TODO: 19. Add different steps for the task (stage 1, stage 2, ...)
# TODO: 20. Give a similarity score based the job description and uploaded resume
# TODO: 21. Add the user name or personal info at the top of the pdf with a different text color - maybe a highlight



#import os
#import openai
import re
import streamlit as st
import tempfile
#import markdown2
from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

load_dotenv()

# # python -m streamlit run streamlit_app3.py
# #openai.api_key = os.getenv('OPENAI_API_KEY')

# Connect to OpenAI 
client = OpenAI()
#openai.api_key = os.getenv("OPENAI_API_KEY")
 
# introduce themes
# ms = st.session_state
# if "themes" not in ms: 
#   ms.themes = {"current_theme": "light",
#                     "refreshed": True,
                    
#                     "light": {"theme.base": "dark",
#                               "theme.backgroundColor": "black",
#                               "theme.primaryColor": "#c98bdb",
#                               "theme.secondaryBackgroundColor": "#5591f5",
#                               "theme.textColor": "white",
#                               "button_face": "🌜"},

#                     "dark":  {"theme.base": "light",
#                               "theme.backgroundColor": "white",
#                               "theme.primaryColor": "#5591f5",
#                               "theme.secondaryBackgroundColor": "#82E1D7",
#                               "theme.textColor": "#0a1464",
#                               "button_face": "🌞"},
#                     }


# function for chainging the states
def set_state(i):
    st.session_state.stage = i

if 'stage' not in st.session_state:
    st.session_state.stage = 0


# def ChangeTheme():
#   previous_theme = ms.themes["current_theme"]
#   tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
#   for vkey, vval in tdict.items(): 
#     if vkey.startswith("theme"): st._config.set_option(vkey, vval)


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
    else:
        return ""


#@st.cache_resource
def generate_questions(interview_type, question_count, input_contents, provide_answers, resume_summary):
    if provide_answers:
    #    if len(resume_summary)>0:
            prompt_text = f"""
            You are an experienced interview assistant helping managers prepare tailored interview questions. 
            The manager will provide you with a job title and a description, and you will create a list of relevant questions to guide the interview process.
            
            Please generate a set of {question_count} high-quality questions for a {interview_type} interview with their respective answers.
            
            The position and desription being interviewed for is: {input_contents} and the candidate summary is: {resume_summary}.

            Ensure the questions are thoughtful, focus on key competencies for the role, and maintain a professional tone throughout.
            Do not start the responses with sure or certainly.
            """

    else:
        prompt_text = f"""
        You are an experienced interview assistant helping managers prepare tailored interview questions. 
        The manager will provide you with a job title and a description, and you will create a list of relevant questions to guide the interview process.
        
        Please generate a set of {question_count} high-quality questions for a {interview_type} interview. 
        
        The position and desription being interviewed for is: {input_contents} and the candidate summary is: {resume_summary}.

        Ensure the questions are thoughtful, focus on key competencies for the role, and maintain a professional tone throughout.
        Do not start the responses with sure or certainly.
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

# def stream_response(response): # this was never used
#     for chunk in response.split():
#         yield chunk + " "
#         time.sleep(0.05)

# Create PDF Functions

def create_header_style(level):
    """Create and return a header style based on the level."""
    styles = getSampleStyleSheet()
    if level == 1:
        return ParagraphStyle(
            'Header1Style',
            parent=styles['Heading1'],
            fontSize=20,
            fontName='Helvetica-Bold',
            spaceAfter=20,
            spaceBefore=10  
        )
    elif level == 2:
        return ParagraphStyle(
            'Header2Style',
            parent=styles['Heading2'],
            fontSize=14,
            fontName='Helvetica-Bold',
            spaceAfter=18,  
            spaceBefore=8 
        )
    return styles['Normal']

def create_paragraph_style():
    """Create and return a normal paragraph style with more line spacing."""
    return ParagraphStyle(
        'Normal',
        fontName='Helvetica',
        fontSize=12,
        spaceBefore=12,  
        spaceAfter=12,   
        leading=15       
    )


def format_text(text):
    """Format text to replace '---' with a line break and '**' for bold, '##' for headers."""
    # Replace line breaks
    text = text.replace('---', '<br />')

    # Handle line breaks for specific patterns
    text = re.sub(r'(Question \d+:|Answer: )', r'<br/>\1', text, flags=re.IGNORECASE)
    
    # Handle bold text
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    
    # Handle headers
    text = re.sub(r'## (.*?)\n', lambda match: f"<font size=16><b>{match.group(1)}</b></font>\n", text)
    
    return text

def add_section(content, header_text, paragraph_text, header_style, paragraph_style):
    """Add a section with a header and paragraph to the content list."""
    header = Paragraph(header_text, header_style)
    formatted_paragraph_text = format_text(paragraph_text)
    paragraph = Paragraph(formatted_paragraph_text, paragraph_style)
    content.extend([header, paragraph])


def generate_filename(base_name):
    """Generate a filename with the current date and time."""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.pdf"


def create_pdf(pdf_filename, sections):
    """Create a PDF with the given sections."""
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    content = []
    
    for header_text, paragraph_text in sections:
        header_level = 1 if header_text.startswith("## ") else 2
        header_style = create_header_style(header_level)
        paragraph_style = create_paragraph_style()
        add_section(content, header_text, paragraph_text, header_style, paragraph_style)
    
    doc.build(content)



def create_main_frame():
    
    if 'stage' not in st.session_state:
        st.session_state.stage = 0


    if st.session_state.stage == 0:
        # Open the video file
        # video_file = open('get_started.mp4', 'rb')

        # # Read the video file
        # video_bytes = video_file.read()

        # # Display the video
        # st.video(video_bytes)


        st.markdown('\n')
        st.markdown('\n')
        st.markdown('\n')
        st.markdown('# AI-Powered features from the future.')
        st.markdown('\n')
        st.markdown('\n')
        st.markdown('##### Hirevision is utilized by numerous businesses, institutions, and recruiters to significantly enhance their screening and recruitment procedures.')
        st.markdown('\n')
        st.markdown('\n')
        st.markdown('\n')
        st.markdown('\n')

        #font-family: 'Poppins', sans-serif;

        # to put the button in the middle
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.markdown(' ')
        with col2:
            st.button('Get Started', on_click=set_state, args=[1])
        with col3:
            st.markdown(' ')


    if st.session_state.stage >= 1:
        with st.sidebar:
            st.sidebar.markdown('<p style="color:#012a4a; font-size:70px; font-family:Helvetica" > <b> HireWise </b> </p>', unsafe_allow_html=True)
            #st.subheader("Job Information")

            st.html(
            """
            <style>
            [data-testid="stSidebarContent"] {
                color: white;
                width:380px;
            }
            [data-testid="stSidebar"] {
                color: white;
                width:400px;
            }
            </style>
            """
            )

            # Job Title Text Box
            job_title = st.text_input('Enter the role the candidates are applying for:', 'Data Scientist')

            # Job Description Text Box
            job_description = st.text_area("Enter the description of the role:", 'We are seeking a skilled and motivated Data Scientist to join our team. As a mid-level Data Scientist, you will work on developing and implementing data models, performing data analysis, and contributing to data-driven decision-making. You’ll collaborate with cross-functional teams to turn raw data into valuable insights that help drive our business forward.', height=210)

            # Upload Resume
            uploaded_file = st.file_uploader("Upload Resume", type="pdf")
                


        #st.image('img/TailorQ_banner.png')  # TITLE and Creator information
        #st.markdown("Prepare for interviews like a pro! Our app instantly creates tailored interview questions based on the job title and description, helping you focus on key skills and make smarter hiring decisions.")
        #st.markdown("No more stress—just easy, effective interview prep!")
        #st.write('\n')  # add spacing

        st.subheader('\nWhat role are you hiring for?\n')
        
        # with st.expander("Role Description - Expand for Customization", expanded=False):
        #     job_title = st.text_input('Enter the role the candidates are applying for', 'Data Scientist')
        #     job_desc = st.text_area("Enter the description of the role", 'We are seeking a skilled and motivated Data Scientist to join our team. As a mid-level Data Scientist, you will work on developing and implementing data models, performing data analysis, and contributing to data-driven decision-making. You’ll collaborate with cross-functional teams to turn raw data into valuable insights that help drive our business forward.', height=20)

        #     uploaded_cv = st.file_uploader("Upload the candidate's CV", type=['pdf', 'docx'])

        interview_questions = ""
        resume_summary = ""


        col1, col2= st.columns([1, 1])

        with col1:
            interview_type = st.selectbox('Interview Type',
                                        ('General', 'Technical'),
                                        index=0)
        with col2:
            #question_count = st.text_input('Question Count', '2')
            #question_count = str(st.slider('Question Count', 2, 10))
            question_count = st.selectbox('Question Count', ('2', '3', '4', '5', '6', '7', '8', '9', '10'), index=0)

        resume_summary = summarise_resume(uploaded_file)
        st.text_area("Resume Summary", resume_summary, height=200)

        # with col3:
        provide_answers = st.checkbox('Provide Sample Answers')

        # with col4:
            #st.write("\n")  # add spacing
            #st.write("\n")  # add spacing
        if st.button('Generate Questions'):
            with st.spinner():

                input_contents = []  # let the user input all the data
                if (job_title != ""):
                    input_contents.append(str(job_title))
                if (job_description != ""):
                    input_contents.append(str(job_description))
                if (len(input_contents) == 0):  # remind user to provide data
                    st.write('Please fill in some contents for your message!')


                if (len(input_contents) >= 1):  # initiate llm
                    if (len(interview_type) != 0) and (len(question_count) != 0):
                        interview_questions = generate_questions(interview_type, 
                                                                question_count, 
                                                                input_contents, 
                                                                provide_answers,
                                                                resume_summary)
                
                    
        if interview_questions != "":
            with st.expander("Interview Questions", expanded=True):
                st.markdown(interview_questions)

                pdf_sections = [
                        ("Resume Summary", resume_summary),
                        ("List of Questions", interview_questions)
                    ]
                
                filename = generate_filename('HireWise')
                create_pdf(filename, pdf_sections)

                with open(filename, 'rb') as download_file:
                    st.download_button('Download', data=download_file, file_name=filename)


if __name__ == '__main__': 
    # call main function
    create_main_frame()
