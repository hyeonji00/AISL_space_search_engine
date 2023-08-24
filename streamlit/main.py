import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from datetime import datetime
import os
import webbrowser

menu = ['이미지 업로드', 'ridar 업로드']
choice = st.sidebar.selectbox('메뉴', menu)

if choice == '이미지 업로드':
	st.subheader('이미지 업로드')
	img_file = st.file_uploader('',type=['png', 'jpg', 'jpeg'])

	if img_file is not None:

		# 이미지명이 고유하도록 시간을 활용하여 변경
		current_time = datetime.now()
		filename = current_time.isoformat().replace(":", "_")
		img_file.name = filename + '.jpg'

		# 실제로 저장
		if not os.path.exists('image'):
			os.makedirs('image')
			
		with open(os.path.join('image', img_file.name), 'wb') as f:
			f.write(img_file.getbuffer())

		#st.success('파일 업로드 성공! 변경된 고유한 파일명 : ' + img_file.name)


		# 경로로 이미지 출력
		st.subheader('업로드한 이미지')
		img = Image.open('image/'+img_file.name)
		st.image(img)

elif choice == 'ridar 업로드':
	st.subheader('ridar 업로드')
	img_file = st.file_uploader('',type=['pcd', 'bin'])

if st.button('옴니버스 연결'):
	#target_url = 'http://203.250.148.52:20516/streaming/client/' # 52
	target_url = 'http://192.168.0.31:8211/streaming/webrtc-client?server=192.168.0.31'
	webbrowser.open_new_tab(target_url)
