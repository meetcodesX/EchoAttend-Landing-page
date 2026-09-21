import streamlit as st
from src.UI.base_layout import background_color_dashboard
from src.components.header import header_dashboard
from src.UI.base_layout import style_base_layout
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists,create_teacher,login_teacher
from PIL import Image
import numpy as np
from src.pipelines.face_pipepline import predict_attendance,get_face_embeddings,train_classifier,verify_student
from src.database.db import get_all_students,create_student,get_student_subject,get_student_attendance,unenroll_student_to_subject
import time
from src.pipelines.voice_pipeline import get_voice_embeddings
from src.components.enroll_dialog import enroll_dialog 
from src.components.subject_card import subject_card
from src.components.dialog_auto_enroll import auto_enroll_dialog

def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    join_code = st.query_params.get("join-code")
    if (join_code and st.session_state.get("is_logged_in") and not st.session_state.get("auto_dialog_opened", False)):
        st.session_state.auto_dialog_opened = True
        auto_enroll_dialog(join_code)
        return 


    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"""Welcome, {student_data['name']} """)
        if st.button("Logout",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()

    st.space()
    c1,c2 = st.columns(2)
    with c1:
        st.header("Your Enrolled Subject")
    with c2:
        if st.button("Enroll in Subject",type='primary',width='stretch'):
            enroll_dialog()

    st.divider()
    with st.spinner("Loading Your enrolled subjects..."):
        subjects = get_student_subject(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total": 0,"attended": 0}

        stats_map[sid]["total"] += 1

        if log.get("is_present"):
            stats_map[sid]["attended"] += 1


    cols = st.columns(2)

    for i, sub_node in enumerate(subjects):
        sub = sub_node["subjects"]
        sid = sub["subject_id"]

        stats = stats_map.get(sid,{"total": 0,"attended": 0})
        def unenroll_btn():
            if st.button("Unenroll from this course",type="tertiary",width="stretch",key=f'unenroll_{sid}'):
                unenroll_student_to_subject(student_id,sid)
                st.toast(f"Unenroll from {sub['sub_name']} Successfully")
                st.rerun()
        
        with cols[i % 2]:

            subject_card(
                name=sub["sub_name"],
                code=sub["sub_code"],
                section=sub["section"],
                stats=[
                    ("📚", "Total", stats["total"]),
                    ("✅", "Attended", stats["attended"]),
                ],
                footer_callback = unenroll_btn
            )

    footer_dashboard()

def student_screen():

    background_color_dashboard() 
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return 
    

    st.header("student screen")
    c1,c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard();
    with c2:
        if st.button("Go Back to Home",type='secondary',key='signinbackbutton',shortcut='control+enter'):
            st.session_state['login_type'] = None
            st.rerun()
    

    st.header("Login with your FaceID",text_alignment='center')
    st.space()
    st.space()

    show_registration = False
    photo_source = st.camera_input("Position your face into the camera")
    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning..."):
            student = verify_student(img)

            if student == "MULTIPLE":
                st.warning("Multiple faces detected.")
            elif student:

                st.session_state.is_logged_in = True
                st.session_state.user_role = "student"
                st.session_state.student_data = student

                st.toast(f"Welcome Back {student['name']}")
                time.sleep(1)
                st.rerun()
            else:
                st.info("Face not recognized! You might be a new student!")
                show_registration = True

    if show_registration:
        with st.container(border=True):
            st.header('Register new Profile')
            new_name = st.text_input(
                "Enter your name",
                placeholder='E.g. Rahul Shah'
            )

            st.subheader('Optional : Voice Enrollment')
            st.info("Enroll for voice only attendence")

            audio_data = None

            try:
                audio_data = st.audio_input(
                    'Record a short phrase like I am present, My name is Akash.'
                )
            except Exception:
                st.error('Audio Data failed!')

            if st.button('Create Account', type='primary'):
                if new_name:
                    with st.spinner('Creating profile..'):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()
                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embeddings(audio_data.read())

                            response_data = create_student(new_name,face_embedding=face_emb,voice_embedding=voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile created! Hi {new_name}")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("couldn't capture your face! sorry")

                else:
                    st.warning('Please enter your name!')
        
    footer_dashboard()