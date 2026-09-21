import streamlit as st

def background_color_home():
    st.markdown("""

        <style>
            .stApp{
                background: #5865F2 !important
            }
            
            .stApp div[data-testid="stColumn"]{
                background-color: #E0E3FF !important;
                padding: 2.5rem !important;
                border-radius: 5rem !important;
                width: 300px !important;
                color: #1F2235 !important;
                min-height: 380px !important;
                height: auto !important;
            } 
                
        </style>
""", unsafe_allow_html=True)


def background_color_dashboard():
    st.markdown("""

        <style>
            .stApp{
                background: linear-gradient(135deg,#0F172A,#1E3A8A,#312E81) !important;
            }
        </style>
""", unsafe_allow_html=True)
    

def style_base_layout():
    st.markdown("""

        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&family=Unbounded:wght@200..900&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');
            
            /* to hide top bar of streamlit */
            #MainMenu, footer, header{
                visibility: hidden;
            }
            .block-container{
                padding-top: 1.5rem !important;
            }
                
            h1{
                font-family: 'Unbounded', san-serif !important;
                font-size: 3.5rem !important;
                line-height: 0.9 !important;
                margin-bottom: 0rem !important;
            }
                
            h2{
                font-family:'Unbounded', san-serif !important;
                font-size: 2rem !important;
                line-height: 0.9 !important;
                margin-bottom: 0rem !important;
            }
                
            h3,h4,p{
                font-family: 'Outfit', san-serif !important;
            }
            
            button{
                border-radius: 1.5rem !important;
                background: #5865F2 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                display: inline-block !important;
            }
                
            button[kind='secondary']{
                border-radius: 1.5rem !important;
                background: #EB459E !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }
                
            button[kind='tertiary']{
                border-radius: 1.5rem !important;
                background: black !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                display: inline-block !important;
            }
                
            button:hover{
                transform: scale(1.05)
            }
             
        </style>
""", unsafe_allow_html=True)
