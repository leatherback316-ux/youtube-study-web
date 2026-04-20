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

url = st.text_input("유튜브 주소를 입력하세요:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("분석 시작"):
    video_id = extract_video_id(url)
    if video_id:
        cookie_path = "youtube_cookies.txt"
        
        # [디버깅] 파일 존재 여부 및 내용 미리보기
        if os.path.exists(cookie_path):
            with open(cookie_path, "r") as f:
                content = f.read(50) # 첫 50자만 읽어봄
            st.info(f"✅ 쿠키 파일 감지됨: {content[:20]}...")
        else:
            st.error("❌ 쿠키 파일을 찾을 수 없습니다! 깃허브 업로드 상태를 확인하세요.")
            st.stop()

        with st.spinner('보안 우회 중... 잠시만 기다려주세요.'):
            try:
                # 자막 가져오기 시도
                # languages=['en', 'ko'] 순서로 시도
                transcript = YouTubeTranscriptApi.get_transcript(
                    video_id, 
                    languages=['en', 'ko'], 
                    cookies=cookie_path
                )
                
                full_text = " ".join([item['text'] for item in transcript])
                st.success("✅ 드디어 성공했습니다!")
                st.text_area("자막 전체 내용", full_text, height=300)
                
            except Exception as e:
                # 에러 메시지에 따라 원인 분석
                error_msg = str(e)
                if "no element found" in error_msg:
                    st.error("❗ 유튜브가 빈 응답을 보냈습니다 (IP 차단 가능성)")
                    st.warning("방법 1: 다른 유튜브 영상(예: TED 강연) 주소로 시도해보세요.")
                    st.warning("방법 2: 잠시(1~2시간) 후 다시 시도해보세요.")
                else:
                    st.error(f"오류 상세: {error_msg}")
    else:
        st.error("올바른 유튜브 주소를 입력해주세요.")
