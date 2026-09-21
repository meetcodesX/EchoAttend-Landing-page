# 🎓 EchoAttend - AI Powered Smart Attendance System

<div align="center">
<img src="src/imagesss/home_screen_image.png" width="150">

### 🚀 One Scan. One Voice. One Attendance.
An AI-powered attendance management system that automates classroom attendance using **Face Recognition**, **Voice Recognition**, and **Supabase Cloud Database**.
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E)
![License](https://img.shields.io/badge/License-MIT-green)
</div>
---
# 📌 Overview

Traditional attendance systems are time-consuming and prone to proxy attendance.
**EchoAttend** solves this problem using Artificial Intelligence.
Teachers simply upload classroom photos (or use voice attendance), and the system automatically identifies students and marks attendance.
---

# ✨ Features

## 👨‍🏫 Teacher Portal

- Teacher Registration & Login
- Create Subjects
- Share Subject Join Link
- AI Face Attendance
- AI Voice Attendance
- Attendance History
- Student Management
- Automatic Attendance Reports

---

## 👨‍🎓 Student Portal

- Student Registration
- Face Registration
- Voice Registration
- Join Subjects using Invite Link
- View Attendance
- View Enrolled Subjects

---

## 🤖 AI Features

### Face Recognition

- Detects multiple faces from classroom images
- Generates 128-dimensional facial embeddings using Dlib
- Matches students using Support Vector Machine (SVM)

### Voice Recognition

- Speaker verification using Resemblyzer
- Voice embedding comparison
- AI-assisted attendance verification

---

# 🛠 Tech Stack

### Frontend

- Streamlit

### Backend

- Python

### Database

- Supabase

### Machine Learning

- Dlib
- Face Recognition
- Scikit-learn
- Resemblyzer
- NumPy
- Pandas

### Other Libraries

- Pillow
- Librosa
- Segno
- bcrypt

---
# 🧠 How It Works

## Face Attendance

```
Classroom Photo
        │
        ▼
Face Detection
        │
        ▼
Face Embeddings
        │
        ▼
SVM Classifier
        │
        ▼
Matched Student IDs
        │
        ▼
Attendance Stored in Supabase
```

---

## Voice Attendance

```
Student Voice
      │
      ▼
Audio Processing
      │
      ▼
Voice Embeddings
      │
      ▼
Similarity Matching
      │
      ▼
Attendance Logged
```
---
# 🚀 Future Improvements

- 📱 Mobile App
- 🎥 Live Camera Attendance
- ☁ Cloud Face Embeddings
- 📊 Attendance Analytics Dashboard
- 📧 Email Notifications
- 📍 GPS Based Verification
- 🔐 Multi-factor Authentication
- 📈 AI Attendance Insights

---

# 👨‍💻 Author
## Meet Sahu
B.Tech Computer Science Engineering
AI/ML Enthusiast | Python Developer | Data Science | DSA

GitHub
https://github.com/meetcodesX

LinkedIn
https://linkedin.com/meetsahu
---
# ⭐ If you like this project
Please consider giving this repository a ⭐ on GitHub.
It motivates me to build more AI-powered open-source projects.
