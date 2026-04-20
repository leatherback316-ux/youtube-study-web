import streamlit as st
import re
import os
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(page_title="유튜브 영어 학습기", page_icon="📺")
st.title("📺 유튜브 영어 학습 생성기")

def extract_video_id(url):
    patterns = [r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', r'(?:be\/)([0-9A-Za-z_-]{11}).*']
    for p in patterns:
        match = re.search(p, url)
        if match: return match.group(1)
    return None

url = st.text_input("유튜브 주소를 입력하세요:")

if st.button("분석 시작"):
    video_id = extract_video_id(url)
    if video_id:
        with st.spinner('보안 우회 중... 자막을 가져오고 있습니다.'):
            try:
                # 깃허브에 올린 쿠키 파일 이름과 똑같아야 해!
                cookie_path = "youtube_cookies.txt"
                
                if os.path.exists(cookie_path):
                    # 쿠키를 들고 유튜브에 입장!
                    transcript = YouTubeTranscriptApi.get_transcript(
                        video_id, 
                        languages=['en', 'ko'], 
                        cookies=cookie_path
                    )
                    
                    full_text = " ".join([item['text'] for item in transcript])
                    st.success("✅ 보안을 뚫고 자막을 가져왔습니다!")
                    st.text_area("자막 내용", full_text, height=300)
                else:
                    st.error("❌ 쿠키 파일을 찾을 수 없습니다. 깃허브에 올렸는지 확인해주세요.")
                
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
                st.info("팁: 쿠키가 만료되었을 수 있습니다. 다시 추출해서 올려보세요!")
    else:
        st.error("올바른 유튜브 주소를 입력해주세요.")
