import streamlit as st
import re
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
        with st.spinner('유튜브에서 자막을 찾는 중...'):
            try:
                # [핵심 변경] 언어 설정을 en(영어)과 ko(한국어)를 동시에 시도
                # 자동 생성된 자막(generated)까지 포함해서 가져오게 함
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'ko'])
                
                full_text = " ".join([item['text'] for item in transcript])
                st.success("✅ 자막을 성공적으로 가져왔습니다!")
                st.text_area("자막 내용", full_text, height=300)
                
            except Exception as e:
                st.error("자막을 가져올 수 없습니다.")
                st.warning("이유 1: 유튜브가 보안상 클라우드 서버의 접근을 막았을 수 있습니다.")
                st.warning("이유 2: 해당 영상에 사용 가능한 자막(CC)이 없습니다.")
                st.info("💡 팁: 다른 유튜브 영상 주소로 다시 시도해보세요!")
    else:
        st.error("올바른 유튜브 주소를 입력해주세요.")
