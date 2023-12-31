# -*- coding: utf-8 -*-
'''
Streamlit Web App with Picture Upload using Tesseract-OCR
'''

import os
from os.path import join, dirname
#import sys

from dotenv import load_dotenv

from PIL import Image

import streamlit as st
from streamlit_chat import message

import pytesseract

class TessApp:
    def __init__(self):
        '''
        Init the app, set params via env
        '''
        dotenv_path = join(dirname(__file__), 'config/.env')
        load_dotenv(dotenv_path)
        self.tesseract_page_segmentation_mode = os.environ.get('TESSERACT_PAGE_SEGMENTATION_MODE')
        self.tesseract_ocr_engine_mode = os.environ.get('TESSERACT_OCR_ENGINE_MODE')
        
        st.set_page_config(layout='wide')
        
        self.sidebar = st.sidebar
        self.upform = st.form
        
        self.prompted_filename = None
        self.ocr_output = None
        
    #https://github.com/katanaml/sparrow/blob/main/sparrow-ui/donut/views/data_annotation.py#L356
    def store_file(self, uploaded_file):
        '''
        Save uploaded file 
        '''
        if uploaded_file is not None:
            if os.path.exists(os.path.join('./data', uploaded_file.name)):
                st.write("File already exists")
                return False

            if len(uploaded_file.name) > 100:
                st.write("File name too long")
                return False
            
            with open(os.path.join('./data', uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            st.success("File uploaded successfully")
            return True
            
    def do_ocr(self, uploaded_file):
        ''' 
        Perform OCR for uploaded file
        '''
        img_file = Image.open(os.path.join("./data", uploaded_file.name))
        
        file_name_base = uploaded_file.name.split('.')[0]
        
        #custom_config = r'--oem 3 --psm 3' #default: ocr-engine-mode, page-segmentation-mode
        custom_config = f'--oem {self.tesseract_ocr_engine_mode} --psm {self.tesseract_page_segmentation_mode}'
        
        text = pytesseract.image_to_string(img_file, lang = 'por', config = custom_config)
        
        self.prompted_filename = uploaded_file.name
        self.ocr_output = text
        
        with open(f'output/{file_name_base}.txt','w') as f:
            f.write(text)
            
        st.success("Picture OCR done")
    
    def window(self):
        '''
        File upload, processing, showing results in a chat form 
        '''
        self.prompted_filename = None
        self.ocr_output = None
        
        with self.sidebar:
            st.header('Instructions')
            st.info(
            '''
            The application allows to upload
            a picture file of type png, jpg/jpeg, perform OCR of
            the text in the picture and save the results
            '''
            )
            
            with self.upform('upload-form',clear_on_submit=True):
                uploaded_file = st.file_uploader('file-uploader',
                                                 type=['png','jpg','jpeg'], 
                                                 accept_multiple_files=False
                )
                submitted = st.form_submit_button('OK')
                if submitted and uploaded_file is not None:
                    ret = self.store_file(uploaded_file)
                    if ret is not False:
                        self.do_ocr(uploaded_file)

        st.title("OCR Results")
        
        #storing results in a form of a chat
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []
            
        if 'past' not in st.session_state:
            st.session_state['past'] = []

        if self.ocr_output is not None:
            st.session_state['past'].append(self.prompted_filename)
            st.session_state['generated'].append(self.ocr_output)
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])-1, -1, -1):
                message(st.session_state["generated"][i], key=str(i))
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_file')

if __name__ == '__main__':
    app = TessApp()
    app.window()
