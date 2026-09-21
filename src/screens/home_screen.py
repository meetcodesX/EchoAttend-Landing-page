import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.UI.base_layout import background_color_home,style_base_layout

def home_screen():
    header_home()
    background_color_home()
    style_base_layout()

    teacher_img = "src/imagesss/Professor-amico.png"
    student_img = "src/imagesss/student.png"

    col1,col2 = st.columns(2,gap='large')

    with col1:
        st.header("I'm Student")
        st.image(student_img,width=180)
        if st.button('Student Portal',type='primary',icon=':material/arrow_outward:',icon_position='right'):
            st.session_state['login_type'] = 'student'
            st.rerun()
        
    with col2:
        st.header("I'm Teacher")
        st.image(teacher_img,width=180)
        if st.button('Teacher Portal',type='primary',icon=':material/arrow_outward:',icon_position='right'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home();