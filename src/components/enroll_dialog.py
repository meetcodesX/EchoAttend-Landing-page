import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time

@st.dialog("Enroll in Subject")
def enroll_dialog():

    st.write("Enter the subject code provided by your teacher to enroll")

    join_code = st.text_input("Subject Code",placeholder="Eg. CS101",key="join_code")
    if "join_code" not in st.session_state:
        st.session_state.join_code = ""

    if st.button("Enroll now", type="primary", width="stretch"):
        if not join_code:
            st.warning("Please enter a subject code")
            return

        res = (supabase.table("subjects").select("subject_id, sub_name, sub_code").eq("sub_code", join_code).execute())

        if not res.data:
            st.error("Invalid Subject Code")
            return

        subject = res.data[0]

        student_id = st.session_state.student_data["student_id"]

        check = (supabase.table("subject_student").select("*").eq("subject_id", subject["subject_id"]).eq("student_id", student_id).execute())

        if check.data:
            st.warning("You are already enrolled.")
            return

        try:
            enroll_student_to_subject(student_id, subject["subject_id"])
            st.success("Successfully enrolled!")
            time.sleep(1)
            st.rerun()

        except Exception as e:
            st.error(str(e))