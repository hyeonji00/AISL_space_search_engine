import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from datetime import datetime
import os
import webbrowser

## streamlit run main.py --server.port 20519

st.subheader('텍스트 업로드')
text = st.text_input('') 

if st.button("검색"):
	con = st.container()
	con.write(f"{str(text)} 검색 !")

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

	st.success('파일 업로드 성공! 변경된 고유한 파일명 : ' + img_file.name)


	# 경로로 이미지 출력
	st.subheader('업로드한 이미지')
	img = Image.open('image/'+img_file.name)
	st.image(img)


st.subheader('LiDAR 업로드')
LiDAR_file = st.file_uploader('',type=['pcd', 'bin'])

#if st.button('옴니버스 연결'):
	#target_url = 'http://203.250.148.52:20516/streaming/client/' # 52
	#target_url = 'http://192.168.0.31:8211/streaming/webrtc-client?server=192.168.0.31' # local
	#webbrowser.open_new_tab(target_url)

target_url1 = 'http://203.250.148.52:20516/streaming/client/'
link = '[search in Omniverse]('+target_url1+')'
st.markdown(link, unsafe_allow_html=True)

#if st.button('옴니버스 연결'):
	#target_url1 = 'http://203.250.148.52:20516/streaming/client/'
	#link = '[search in Omniverse]('+target_url1+')'
	#st.markdown(link, unsafe_allow_html=True)

#target_url2 = 'https://www.3dcitydb.org/3dcitydb-web-map/1.7/3dwebclient/index.html?title=Berlin_Demo&batchSize=1&latitude='+'52.517479728958044'+'&longitude='+'13.411141287558161'+'&height=534.3099172951087&heading=345.2992773976952&pitch=-44.26228062802528&roll=359.933888621294&layer_0=url%3Dhttps%253A%252F%252Fwww.3dcitydb.org%252F3dcitydb%252Ffileadmin%252Fmydata%252FBerlin_Demo%252FBerlin_Buildings_rgbTexture_ScaleFactor_0.3%252FBerlin_Buildings_rgbTexture_collada_MasterJSON.json%26name%3DBrlin_Buildings_rgbTexture%26active%3Dtrue%26spreadsheetUrl%3Dhttps%253A%252F%252Fwww.google.com%252Ffusiontables%252FDataSource%253Fdocid%253D19cuclDgIHMqrRQyBwLEztMLeGzP83IBWfEtKQA3B%2526pli%253D1%2523rows%253Aid%253D1%26cityobjectsJsonUrl%3D%26minLodPixels%3D100%26maxLodPixels%3D1.7976931348623157e%252B308%26maxSizeOfCachedTiles%3D200%26maxCountOfVisibleTiles%3D200'
#ink = '[search in 3DCityDb]('+target_url2+')'
#st.markdown(link, unsafe_allow_html=True)