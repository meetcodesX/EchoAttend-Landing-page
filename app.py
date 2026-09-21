<<<<<<< HEAD
import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

def main():
    st.set_page_config(
        page_title="EchoAttend - Making Attendance Faster using AI",
        page_icon= "src/imagesss/home_screen_image.png"
    )

    if "login_type" not in st.session_state:
        st.session_state.login_type = None

    if st.query_params.get("join-code") and st.session_state.login_type is None:
            st.session_state.login_type = "student"

    if st.session_state.login_type == "teacher":
        teacher_screen()

    elif st.session_state.login_type == "student":
        student_screen()

    else:
        home_screen()


if __name__ == "__main__":
    main()
=======
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
>>>>>>> 497e0e1 (Add EchoAttend Landing page)
