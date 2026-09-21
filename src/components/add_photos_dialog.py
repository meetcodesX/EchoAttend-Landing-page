from PIL import Image
import streamlit as st


@st.dialog("Capture or upload photos")
def add_photos_dialog():
    st.write("Add classroom photos to scan for attendance")
    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"
    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []
    if "uploaded_hashes" not in st.session_state:
        st.session_state.uploaded_hashes = set()

    uploaded_files = []

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Camera",type="primary" if st.session_state.photo_tab == "camera" else "secondary",use_container_width=True):
            st.session_state.photo_tab = "camera"
    with col2:
        if st.button("Upload Photos",type="primary" if st.session_state.photo_tab == "upload" else "secondary", use_container_width=True):
            st.session_state.photo_tab = "upload"


    if st.session_state.photo_tab == "camera":
        cam_photo = st.camera_input("Take Snapshot", key="dialog_cam")
        if cam_photo:
            img = Image.open(cam_photo).convert("RGB")
            file_bytes = cam_photo.getvalue()
            if file_bytes not in st.session_state.uploaded_hashes:
                st.session_state.attendance_images.append(img)
                st.session_state.uploaded_hashes.add(file_bytes)
                st.toast("Photo Added Successfully")

    if st.session_state.photo_tab == "upload":
        uploaded_files = st.file_uploader("Upload Classroom Photos",type=["png", "jpg", "jpeg"],accept_multiple_files=True,key="upload_dialog")
    st.divider()

    if st.button("Done", type="primary", use_container_width=True):
        if st.session_state.photo_tab == "upload":
            for file in uploaded_files:
                file_bytes = file.getvalue()
                if file_bytes not in st.session_state.uploaded_hashes:
                    img = Image.open(file).convert("RGB")
                    st.session_state.attendance_images.append(img)
                    st.session_state.uploaded_hashes.add(file_bytes)

        st.toast(f"{len(st.session_state.attendance_images)} photo(s) ready for attendance.")
        st.session_state.photo_tab = "camera"
        st.toast(f"{len(st.session_state.attendance_images)} photo(s) ready for attendance.")
        st.rerun()