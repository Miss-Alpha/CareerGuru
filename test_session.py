# import streamlit as st

# if 'stage' not in st.session_state:
#     st.session_state.stage = 0

# def set_state(i):
#     st.session_state.stage = i

# if st.session_state.stage == 0:
#     st.button('Begin', on_click=set_state, args=[1])

# if st.session_state.stage >= 1:
#     name = st.text_input('Name', on_change=set_state, args=[2])

# if st.session_state.stage >= 2:
#     st.write(f'Hello {name}!')
#     color = st.selectbox(
#         'Pick a Color',
#         [None, 'red', 'orange', 'green', 'blue', 'violet'],
#         on_change=set_state, args=[3]
#     )
#     if color is None:
#         set_state(2)

# if st.session_state.stage >= 3:
#     st.write(f':{color}[Thank you!]')
#     st.button('Start Over', on_click=set_state, args=[0])


import streamlit as st

# Define the content for two pages
content1 = """
**Page 1**

This is page 1
"""

content2 = """
**Page 2**

This is page 2
"""

# Initialize the page state
if "page" not in st.session_state:
    st.session_state.page = "page1"

# Define the back button function
def back_button():
    st.session_state.page = "page1"

# Define the next button function
def next_button():
    st.session_state.page = "page2"

# Create a layout with two columns
cols = st.columns([1, 10])

# Display the content based on the page state
if st.session_state.page == "page1":
    with cols[0].container():
        st.button("→", on_click=next_button)
    cols[1].write(content1)
else:
    with cols[0].container():
        st.button("←", on_click=back_button)
    cols[1].write(content2)