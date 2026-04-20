import streamlit as st
import re
# 임포트 방식을 명확하게 변경
import youtube_transcript_api 
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(page_title="유튜브 영어 학습기", page_icon="📺")
st.title("📺 유튜브 영어 학습 생성기")

def extract_video_id(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:be\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11}).*',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

url = st.text_input("유튜브 주소를 입력하세요:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("분석 시작"):
    if not url:
        st.warning("주소를 입력해주세요!")
    else:
        video_id = extract_video_id(url)
        if not video_id:
            st.error("❌ 유효한 유튜브 주소가 아닙니다.")
        else:
            with st.spinner('자막을 분석 중...'):
                try:
                    # 클래스를 직접 호출하여 자막 리스트 확인
                    # 에러 방지를 위해 명시적으로 호출
                    t_list = YouTubeTranscriptApi.list_transcripts(video_id)
                    
                    try:
                        # 영어 자막 시도
                        transcript = t_list.find_transcript(['en'])
                    except:
                        # 영어 없으면 첫 번째 사용 가능한 자막(자동생성 등) 가져오기
                        transcript = t_list.find_generated_transcript(['en'])
                    
                    data = transcript.fetch()
                    full_text = " ".join([item['text'] for item in data])

                    st.success("✅ 자막 추출 성공!")
                    st.text_area("내용:", full_text, height=300)
                    
                except Exception as e:
                    # 에러가 발생하면 어떤 에러인지 상세히 출력하게 함
                    st.error(f"오류 상세: {e}")
                    st.info("팁: 영상에 자막(CC)이 설정되어 있는지 확인해 주세요!")
