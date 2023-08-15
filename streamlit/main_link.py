import streamlit as st
import webbrowser

if st.button('옴니버스 연결'):
	target_url = 'http://203.250.148.52:8211/streaming/webrtc-client?server=203.250.148.52'
	webbrowser.open_new_tab(target_url)