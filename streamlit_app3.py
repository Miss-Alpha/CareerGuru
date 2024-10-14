# TODO: 1. Maybe add a checkbox to include the answer or not ✅ 12/09
# TODO: 2. Provide how many questions and answer pairs the user wants (maybe a dropdown or a scale) ✅ 12/09
# TODO: 3. A dropdown fo the general/technical question ✅ 12/09
# TODO: 4. Stream the response - I had problem with markdown ✅> I have added in progress button
# TODO: 5. Change the color of the generate questions button ✅ 12/09
# TODO: 6. Change the main fonts > seems like too much work
# TODO: 7. Read the resume ✅ 16/9
# TODO: 8. Summarize the resume and put it in the place holder ✅ 16/9
# TODO: 9. Put the questions into a placeholder like a table, maybe separate each question ✅ - I think the answers are well presented
# TODO: 10. Extract candidate's name from the resume ✅ - it clutters up my space, pass
# TODO: 11. Give warning with st components like st.warning
# TODO: 12. Remove certainely from the start of the answers ✅ 17/9
# TODO: 13. Add the download button ✅ 17/9
# TODO: 14. Generate a proper pdf with different headers and sections ✅ 18/9
# TODO: 15. Add date and time in generated pdf's name ✅ 17/9
# TODO: 16. Add candidate's name in the pdf file ✅ 25/9
# TODO: 17. Add line breaks in the pdf if possible ✅ 18/9
# TODO: 18. Hide resume summary section in the pdf file if it is not provided > the current design requires a resume
# TODO: 19. Add different steps for the task (stage 1, stage 2, ...) ✅ 19/9
# TODO: 20. Give a similarity score based the job description and uploaded resume ✅ 25/9
# TODO: 21. Add the user name or personal info at the top of the pdf with a different text color - maybe a highlight ✅ 25/9
# TODO: 22. Add a progress bar ✅ 20/9, for sessions 0, 1
# TODO: 23. Handle when the resume is not in proper format
# TODO: 24. Add accept resume summary or regenerate button ✅ 20/9
# TODO: 25. Move provide anwers checkbox in the stage 2 ✅ 23/9
# TODO: 26. Add st.status to show the stages > already added progress expander
# TODO: 27. Add a back button so the user can go to the previous stage ✅ 26/9
# TODO: 28. Make the progress bar seem static when session is restarted ✅ 24/9
# TODO: 29. Move all the pdf functions to a separate file for a cleaner code space  ✅ 25/9
# TODO: 30. Add a helpful tip box in the final pdf ✅ 25/9
# TODO: 31. Extract candidate's name from the uploaded resume ✅ 25/9
# TODO: 31. Add the header of session 3 ✅ 26/9
# TODO: 32. Change the color of sidebar ✅ 26/9
# TODO: 33. Redefine the button names and descriptions ✅ 26/9

import streamlit as st
import texts
import PDF_maker
import resume_handlers

from openai import OpenAI
from dotenv import load_dotenv

from streamlit_extras.stylable_container import stylable_container


#load_dotenv()

# # python -m streamlit run streamlit_app3.py
# #openai.api_key = os.getenv('OPENAI_API_KEY')

# Connect to OpenAI 
#client = OpenAI()

# function for chainging the states
def set_state(i):
    st.session_state.stage = i

def back_button():
    st.session_state.stage -= 1


def create_main_frame():
    
    if 'stage' not in st.session_state:
        st.session_state.stage = 0

    # Initialize the progress bar
    progress_bar = st.progress(0)
     # progress bar color
    st.markdown(
            """
            <style>
                .stProgress > div > div > div > div {
                    background-color: #ff5400;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
    
    # color of the sidebar
    st.html(
    """
    <style>
    [data-testid="stSidebarContent"] {
        color: white;
        background-color: #83c5be;
    }
    </style>
    """
    )

    st.markdown("""
    <style>
        button {
            font-size: 14px !important;
            font-weight: bold !important;
        }
    </style>
    """, unsafe_allow_html=True)

     
    if st.session_state.stage == 0:
        progress_bar.progress((st.session_state.stage+1)*15)

        # Initialze Session Variables
        # if 'candidate_name' not in st.session_state:
        #     st.session_state.candidate_name = ' '

        # if 'job_title' not in st.session_state:
        #     st.session_state.job_title = ' '
        
        # if 'job_description' not in st.session_state:
        #     st.session_state.job_description = ' '

        # if 'resume_summary' not in st.session_state:
        #     st.session_state.resume_summary = ' '

        # if 'interview_questions' not in st.session_state:
        #     st.session_state.interview_questions = ' '


        col011, col012, col013 = st.columns([1, 1, 1])
        with col011: 
            st.markdown('')
        with col012: 
            st.image('img/logo.gif') 
        with col013: 
            st.markdown(' ')


        #st.markdown("<p style='color:#0a1128; text-align: center; font-size:50px; font-family:'Pacifito', cursive;' > <b> AI-Powered features from the future. </b> </p>", unsafe_allow_html=True)
        #st.markdown('# AI-Powered features from the future.')
        st.markdown("<p style='color:#00072d; text-align: center; font-size:50px; font-family:'Pacifito', cursive;' > <b> Connecting Candidates to Their Dream Jobs </b> </p>", unsafe_allow_html=True)
        st.markdown("<p style='color:#00072d; text-align: center; font-size:20px; font-family:'Pacifito', cursive;' > <b> Find the perfect job match for your candidates with AI-powered interview preparation. </b> </p>", unsafe_allow_html=True)
        #st.markdown('\n')
        #st.header('Connecting candidates to their dream jobs')
        #st.subheader("Find the perfect job match for your candidates with AI-powered interview preparation.")

        with st.sidebar:
            # candidate_name = st.text_input('Candidate\'s Name', key='candidate name')
            # st.session_state['candidate_name'] = candidate_name

            job_title2 = st.text_input('Job Title', 'Data Scientist')
            st.session_state['job_title'] = job_title2
        
            job_desc = st.text_area('Job Description' , texts.job_description , height = 340)
            st.session_state['job_description'] = job_desc

            for _ in range(29):
                st.markdown('\n')

            st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/Miss-Alpha/CareerGuru)")

            
        # to put the button in the middle
        col021, col022, col023 = st.columns([2, 1, 2])
        with col021:
            st.markdown(' ')
        with col022:
            with stylable_container(
                "green",
                css_styles="""
                button {
                    background-color: #FFFFFF;
                    color: #ff5400;
                }
                button:hover {
                    background-color: #ff5400;
                    color: #ff5400;
                }
                """,
            ):
                st.button(f"Get Started", key="button", on_click=set_state, args=[1], use_container_width=True)

        with col023:
            st.markdown(' ') 

        
    if st.session_state.stage == 1:
        progress_bar.progress((st.session_state.stage+1)*15)

        # Create a layout with two columns for back button
        cols = st.columns([1, 7])

        # Display back button
        with cols[0].container():
                st.button("← Back", on_click=back_button, use_container_width=True)
        
        # for i in range(35):
        #     # Update the progress bar with each iteration.
        #     progress_bar.progress(i + 1)
            #time.sleep(0.1)
        #with st.sidebar:
            # st.sidebar.markdown('<p style="color:#012a4a; font-size:70px; font-family:Helvetica" > <b> HireWise </b> </p>', unsafe_allow_html=True)
            #st.subheader("Job Information")

            # st.html(
            # """
            # <style>
            # [data-testid="stSidebarContent"] {
            #     color: white;
            #     width:380px;
            # }
            # [data-testid="stSidebar"] {
            #     color: white;
            #     width:400px;
            # }
            # </style>
            # """
            # )

            # # Job Title Text Box
            # job_title = st.text_input('Enter the role the candidates are applying for:', 'Data Scientist')

            # # Job Description Text Box
            # job_description = st.text_area("Enter the description of the role:", 'We are seeking a skilled and motivated Data Scientist to join our team. As a mid-level Data Scientist, you will work on developing and implementing data models, performing data analysis, and contributing to data-driven decision-making. You’ll collaborate with cross-functional teams to turn raw data into valuable insights that help drive our business forward.', height=210)

            # # Upload Resume
            # uploaded_file = st.file_uploader("Upload Resume", type="pdf")


        st.header('Step 1: Upload Candidate Resume...')

        st.markdown('Provide the candidate\'s resume, and we\'ll summarize it for a quick review.')

        resume_summary = ""

        st.info('To ensure the best results, please upload resumes in a standard format (PDF, DOCX) with clear sections like Work Experience, Skills, and Education. This helps our system generate an accurate summary and relevant interview questions.')

        col1, col2= st.columns([1, 1])

        # with col1:
        #     interview_type = st.selectbox('Interview Type',
        #                                 ('General', 'Technical'),
        #                                 index=0)
        # with col2:
        #     question_count = st.selectbox('Question Count', ('2', '3', '4', '5', '6', '7', '8', '9', '10'), index=0)

        with st.sidebar:
        
            uploaded_file = st.file_uploader("Upload Resume", type=['pdf', 'docx'])

        if uploaded_file:
            with st.expander('Resume Summary', expanded=True):
                st.success('Your resume is successfully uploaded!')
                with st.spinner():
                    full_resume = resume_handlers.read_resume(uploaded_file)
                    resume_summary = resume_handlers.summarise_resume(full_resume)
                    st.session_state['candidate_name'] = resume_handlers.extract_candidate_name(full_resume)
                    
                    
                    # col111, col112 = st.columns([1, 1])
                    # with col111:
                    st.button('Confirm the Summary', key="button", on_click=set_state, args=[2], use_container_width=True)
                    # with col112:
                    #     if st.button('Regenerate Summary', use_container_width=True):
                    #         resume_summary = summarise_resume(full_resume) # this part is giving me errors that it cannot upload an empty file
                    #         st.text_area("Resume Summary", resume_summary, height=200)
                            
                                        
                    st.text_area("Resume Summary", resume_summary, height=200)
                    st.session_state['resume_summary'] = resume_summary


    if st.session_state.stage == 2:
        progress_bar.progress((st.session_state.stage+1)*15)
        
        st.sidebar.write(" ")

        # Create a layout with two columns for back button
        cols = st.columns([1, 7])

        # Display back button
        with cols[0].container():
            st.button("← Back", on_click=back_button, use_container_width=True)

        st.header("Step 2: Let's Review Candidate Information")
        st.markdown("Here’s what you’ve provided so far. Make sure everything is correct.")

        # Initialize session state if not already done
        if 'candidate_name' not in st.session_state:
            st.session_state['candidate_name'] = ""
        if 'job_title' not in st.session_state:
            st.session_state['job_title'] = ""
        if 'job_description' not in st.session_state:
            st.session_state['job_description'] = ""



        st.button('Proceed to Interview Preparation', key='proceed_button', on_click=set_state, args=[3], use_container_width=True)

        # col221, col222= st.columns([1, 1])

        # with col221:
        #     st.button('Proceed to Interview Preparation', key='proceed_button', on_click=set_state, args=[3], use_container_width=True)
        # with col222:
        #     if st.button('Submit Changes', key="submit_changes", on_click=set_state, args=[3], use_container_width=True)

        st.subheader("General Information")

        col211, col212= st.columns([1, 1])
        with col211:
            candidate_name_text_input = st.text_input('Candidate Name', value = st.session_state['candidate_name'])
        with col212:
            job_title_text_input = st.text_input('Job Title', value = st.session_state['job_title'])
        job_description_text_area = st.text_area('Job Description', value = st.session_state['job_description'], height=150)
            
        
        # Draw a horizontal line
        st.divider()

        st.subheader("Resume")
        st.text_area('Resume Summary', value = st.session_state['resume_summary'], height=200)
        

    if st.session_state.stage == 3:

        progress_bar.progress((st.session_state.stage+2)*15)

        st.sidebar.write(" ")

        # Create a layout with two columns for back button
        cols = st.columns([1, 7])

        # Display back button
        with cols[0].container():
            st.button("← Back", on_click=back_button, use_container_width=True)

        st.header("Step 3 - Finalize it...")
        st.markdown("Choose the number of questions and interview type. Get question-answer pairs and a similarity score between the job description and resume.")

        st.session_state.interview_questions = ''
        st.session_state.similarity_score = ''

        st.markdown(f"{st.session_state['candidate_name']}")

        col311, col312 = st.columns([1, 1])

        with col311: 
            interview_type = st.selectbox('Interview Type',
                                        ('General', 'Technical'),
                                        index=0)
        with col312:
            question_count = st.selectbox('Question Count', ('2', '3', '4', '5', '6', '7', '8', '9', '10'), index=0)

        provide_answers = st.checkbox('Provide Sample Answers')

        # st.markdown(f'Job title: {st.session_state.job_title}')
        # st.markdown(f'Job description: {st.session_state.job_description}')

        if st.button('Generate Questions and Evaluate', use_container_width=True):
            with st.spinner():

                input_contents = []  # let the user input all the data
                if (st.session_state.job_title != ""):
                    #st.markdown('job title provided')
                    input_contents.append(str(st.session_state.job_title))
                if (st.session_state.job_description != ""):
                    #st.markdown('job description provided')
                    input_contents.append(str(st.session_state.job_description))
                    #st.markdown(input_contents)
                if (len(input_contents) == 0):  # remind user to provide data
                    st.write('Please fill in some contents for your message!')


                if (len(input_contents) >= 1):  # initiate llm
                    if (len(interview_type) != 0) and (len(question_count) != 0):
                        #st.markdown(f'Function Inputs: {interview_type}, {question_count}, {input_contents}, {provide_answers}, {st.session_state.resume_summary}')
                        st.session_state.interview_questions = resume_handlers.generate_questions(interview_type, 
                                                                question_count, 
                                                                input_contents, 
                                                                provide_answers,
                                                                st.session_state.resume_summary)
                        st.session_state.similarity_score = resume_handlers.compute_similarity(st.session_state.job_description, st.session_state.resume_summary)
                                                                            
                    
        if st.session_state.interview_questions != "":
            with st.expander("Interview Questions", expanded=True):
                st.markdown(st.session_state.similarity_score) 
                st.markdown(st.session_state.interview_questions)
                  
                pdf_sections = [
                        ("Resume Summary",  st.session_state.resume_summary),
                        ("List of Questions", st.session_state.interview_questions),
                        ("Similarity Score", st.session_state.similarity_score)
                    ]
                
                filename = PDF_maker.generate_filename('HireWiser')
                PDF_maker.create_pdf(filename, pdf_sections, candidate_name=st.session_state['candidate_name'])

                with open(filename, 'rb') as download_file:
                    st.download_button('Download Full Report', data=download_file, file_name=filename, use_container_width=True)


if __name__ == '__main__': 
    # call main function
    create_main_frame()
