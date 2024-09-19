job_description =  """- Advanced degree in Computer Science, Statistics, Mathematics, or a related field. 
- 5+ years of experience as a Data Scientist.
- Strong proficiency in Python, R, or other relevant programming languages.
- Expertise in machine learning algorithms (e.g., regression, classification, clustering).
- Experience with data visualization tools (e.g., Matplotlib, Seaborn).
- Knowledge of cloud platforms (e.g., AWS, GCP, Azure) is a plus.
- Excellent problem-solving and analytical skills.
- Strong communication and teamwork abilities."""

prompt_text_with_answers = """
You are an experienced interview assistant helping managers prepare tailored interview questions. 
The manager will provide you with a job title and a description, and you will create a list of relevant questions to guide the interview process.

Please generate a set of {question_count} high-quality questions for a {interview_type} interview with their respective answers.

The position and desription being interviewed for is: {input_contents} and the candidate summary is: {resume_summary}.

Ensure the questions are thoughtful, focus on key competencies for the role, and maintain a professional tone throughout.
Do not start the responses with sure or certainly.
"""

prompt_text_without_answers = """
You are an experienced interview assistant helping managers prepare tailored interview questions. 
The manager will provide you with a job title and a description, and you will create a list of relevant questions to guide the interview process.

Please generate a set of {question_count} high-quality questions for a {interview_type} interview. 

The position and desription being interviewed for is: {input_contents} and the candidate summary is: {resume_summary}.

Ensure the questions are thoughtful, focus on key competencies for the role, and maintain a professional tone throughout.
Do not start the responses with sure or certainly.
"""