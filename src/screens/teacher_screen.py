import streamlit as st
from src.UI.base_layout import background_color_dashboard
from src.components.header import header_dashboard
from src.UI.base_layout import style_base_layout 
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists,create_teacher,login_teacher,get_teacher_subject,get_attendance_for_teacher
from src.components.dialog_create_sub import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_sub import share_subject_dialog
from src.components.add_photos_dialog import add_photos_dialog
from src.pipelines.face_pipepline import predict_attendance
import numpy as np
import pandas as pd
from src.database.config import supabase
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from collections import defaultdict
from src.utils.time_utils import to_ist

def teacher_screen():
    if "teacher_login_type" not in st.session_state:
        st.session_state.teacher_login_type = "login"
    # Safety check
    if (st.session_state.teacher_login_type == "teacher_data"and "teacher_data" not in st.session_state):
        st.session_state.teacher_login_type = "login"
        st.session_state.login_type = None
        st.rerun()
        return 

    background_color_dashboard()
    style_base_layout()

    if st.session_state.teacher_login_type == "teacher_data":
        teacher_dashboard()
    elif st.session_state.teacher_login_type == "login":
        teacher_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_signup()

def teacher_dashboard():
    if "teacher_data" not in st.session_state:
        st.session_state.teacher_login_type = "login"
        st.rerun()
        return

    teacher_data = st.session_state.teacher_data

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"""Welcome, {teacher_data['name']} """)
        if st.button("Logout",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
           
            if "teacher_data" in st.session_state:
                del st.session_state.teacher_data
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else 'tertiary'
        if st.button('Take Attendance',type=type1,width='stretch',icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else 'tertiary'
        if st.button('Manage Subjects',type=type2,width='stretch',icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendence_records' else 'tertiary'
        if st.button('Attendence Record',type=type3,width='stretch',icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendence_records'
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendence_records":
        teacher_tab_attendance_records()

    footer_dashboard()

def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header("Take AI Attendance")

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subject(teacher_id)

    if not subjects:
        st.warning("You haven't created any subjects yet! Please create one to begin!")
        return

    subject_options = {
        f"{s['sub_name']} - {s['sub_code']}": s["subject_id"]
        for s in subjects
    }

    col1, col2 = st.columns([3, 1],vertical_alignment="bottom")

    with col1:
        selected_subject_label = st.selectbox("Select Subject",options=list(subject_options.keys()))
    with col2:
        if st.button("Add Photos",type="primary",icon=":material/photo_prints:",width="stretch"):
            if st.session_state.attendance_images:
                st.caption(f"📷 {len(st.session_state.attendance_images)} photo(s) ready for analysis")
            else:
                st.caption("No photos added yet")
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    has_photos = bool(st.session_state.attendance_images)

    if has_photos:
        st.subheader("Added Photos")
        thumb_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with thumb_cols[idx % 4]:
                st.image(img, use_container_width=True)
                st.caption(f"Photo {idx + 1}")
        st.divider()
    else:
        st.caption("No photos added yet")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🗑 Clear all photos",type="secondary", use_container_width=True,disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()
    with col2:
        if st.button("🧠 Run Face Analysis",type="primary",use_container_width=True,disabled=not has_photos):
            results = []
            attendance_to_log = []
            with st.spinner("Scanning classroom photos..."):
                all_detected_ids = defaultdict(list)

                for idx,img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert("RGB"))
                    detected ,_, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids[student_id].append(f"Photo {idx+1}")

                enrolled_res = supabase.table("subject_student").select("*,students(*)").eq("subject_id",selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:
                    results, attendance_to_log = [], []
                    current_timestamp = datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()

                    for node in enrolled_students:
                        student = node["students"]
                        sources = all_detected_ids.get(int(student["student_id"]), [])
                        is_present = len(sources) > 0

                        # Result table
                        results.append({
                            "Name": student["name"],
                            "ID": student["student_id"],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        # Save into database
                        attendance_to_log.append({
                            "student_id": student["student_id"],
                            "subject_id": selected_subject_id,
                            "timestamp": current_timestamp,
                            "is_present": bool(is_present)
                        })
                    attendance_result_dialog(pd.DataFrame(results),attendance_to_log)

    with col3:
        if st.button("🎤 Use Voice Attendance",type="primary",use_container_width=True):
            voice_attendance_dialog(selected_subject_id)

def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)

    with col1:
        st.header("Manage Subjects")

    with col2:
        if st.button("Create new subject +", width="stretch"):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subject(teacher_id)

    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub["total_students"]),
                ("🕧", "Classes", sub["total_classes"])
            ]
            def share_button(sub=sub):
                if st.button(f"Share Code : {sub['sub_name']}",key=f"share_{sub['sub_code']}",icon=":material/share:"):
                    share_subject_dialog(sub["sub_name"],sub["sub_code"])
                st.space()

            subject_card(
                name=sub["sub_name"],
                code=sub["sub_code"],
                section=sub["section"],
                stats=stats,
                footer_callback=share_button
            )

    else:
        st.info("No Subjects Found!")

def teacher_tab_attendance_records():
    st.header("Attendence Records")
    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        return
    
    data = []
    for r in records:
        ts = r.get("timestamp")
        if ts:
            dt = to_ist(ts)
            display_time = dt.strftime("%Y-%m-%d %I:%M %p")
        else:
            display_time = "N/A"


        data.append({
            'ts_group' : ts.split('*')[0] if ts else None,
            'Time' : display_time,
            'Subject' : r['subjects']['sub_name'],
            'Subject Code' : r['subjects']['sub_code'],
            'is_present' : bool(r.get('is_present',False))
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        )
        .reset_index()
    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + "/"
        + summary['Total_Count'].astype(str) + " Students"
    )

    display_df = (
        summary.sort_values(by='ts_group', ascending=False)
            [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
    )

    st.dataframe(display_df, hide_index=True, width="stretch")


def login_into_teacher(username,password):
    if not username or not password:
        return False

    teacher = login_teacher(username,password)

    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        st.session_state.teacher_login_type = "teacher_data"
        return True
    
    
    return False

def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_confirm_pass):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "This username is already taken"
    if teacher_pass != teacher_confirm_pass:
        return False, "Password doesnt match"
    
    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True, "Successfully created! Login Now"
    except Exception as e:
        return False, "Unexpected error"

def teacher_login():
    c1,c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard();
    with c2:
        if st.button("Go Back to Home",type='secondary',key='signinbackbutton',shortcut='control+enter'):
            st.session_state['login_type'] = None
            st.rerun()
    
    st.header("Login using your Credentials.",text_alignment='center')
    st.space()
    st.space()

    teacher_username = st.text_input("Enter your Username",placeholder='Ex. Rahulshah123')
    teacher_pass = st.text_input("Enter your Password",type='password',placeholder="Enter Password")
    st.divider()

    bnt1,bnt2 = st.columns(2)
    with bnt1:
        if st.button("Sign In",icon=":material/passkey:",shortcut="Enter",width='stretch'):
            if login_into_teacher(teacher_username,teacher_pass):
                st.toast(f"Welcome back! {teacher_username}")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password")
    with bnt2:
        if st.button("Don't have an account? Sign Up",icon=":material/passkey:",width='stretch',type='primary'):
            st.session_state.teacher_login_type = 'register'
            st.rerun()

    footer_dashboard()


def teacher_signup():
    c1,c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard();
    with c2:
        if st.button("Go Back to Home",type='secondary',key='signupbackbutton',shortcut='control+enter'):
            st.session_state['login_type'] = None
            st.rerun()
    
    st.header("Register Your Profile")
    st.space()
    st.space()

    teacher_username = st.text_input("Enter your Username",placeholder='Ex. Rahulshah123')
    teacher_name = st.text_input("Enter Name", placeholder='Rahul shah')
    teacher_pass = st.text_input("Enter your Password",type='password',placeholder="Enter Password")
    teacher_confirm_pass = st.text_input("Confirm your Password",type='password',placeholder="Confirm Password")
    st.divider()

    bnt1,bnt2 = st.columns(2)
    with bnt1:
        if st.button("Sign Up",icon=":material/passkey:",shortcut="control+a",width='stretch'):
            success,message = register_teacher(teacher_username,teacher_name,teacher_pass,teacher_confirm_pass)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)
    
    with bnt2:
        if st.button("Already have an account? Sign In",icon=":material/passkey:",width='stretch',type='primary'):
            st.session_state.teacher_login_type = 'login'
        
    footer_dashboard()