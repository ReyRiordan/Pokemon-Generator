import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO
import audio
import image


st.title("Generate Experimental Stimuli")

client = OpenAI()

st.session_state['word'] = st.text_input("Word:")


if st.session_state['word']:
    st.divider()

    if st.columns(3)[1].button("Generate Audio", type="primary", use_container_width=True) and st.session_state['word']:
        st.session_state['audio'] = audio.generate_openai(st.session_state['word'], client)
    
    if 'audio' in st.session_state:
        audio_layout = st.columns(4)

        audio_layout[1].button(label="Play",
                on_click=audio.play,
                args=[st.session_state['audio']],
                use_container_width=True)
        
        audio_layout[2].download_button(label="Download",
                        data=st.session_state['audio'],
                        file_name=st.session_state['word']+".mp3",
                        mime="audio/mpeg",
                        use_container_width=True)
        
    st.divider()

    num_images = st.select_slider(label="Number of images:", options=[i+1 for i in range(10)])

    if st.columns(3)[1].button("Generate Image(s)", type="primary", use_container_width=True):
        st.session_state['images'] = image.edit_openai(st.session_state['word'], num_images, client)

    if 'images' in st.session_state:
        for index, img in enumerate(st.session_state['images']):
            image_layout = st.columns([3, 1, 1, 1])

            image_layout[0].image(image=img,
                    output_format="PNG")
            
            for i in range(4):
                image_layout[2].markdown("#")
            image_layout[2].download_button(label="Download",
                            data=img,
                            file_name=st.session_state['word']+".png",
                            mime="image/png",
                            key=index)