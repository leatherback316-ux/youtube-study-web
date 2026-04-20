import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled, VideoUnavailable

# 페이지 설정
st.set_page_config(page_title="유튜브 영어 학습기", page_icon="📺")

st.title("📺 유튜브 영어 학습 생성기")
st.subheader("AI가 핵심 문장을 정리해드립니다.")

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

# 사용자 입력
url = st.text_input("유튜브 주소를 입력하세요:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("분석 시작"):
    if not url:
        st.warning("주소를 입력해주세요!")
    else:
        video_id = extract_video_id(url)
        
        if not video_id:
            st.error("❌ 유효한 유튜브 주소가 아닙니다.")
        else:
            with st.spinner('자막을 가져오는 중입니다...'):
                try:
                    # 자막 가져오기 시도
                    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                    
                    try:
                        # 영어 자막 우선 탐색
                        transcript = transcript_list.find_transcript(['en'])
                    except NoTranscriptFound:
                        # 영어 없으면 한국어 탐색
                        transcript = transcript_list.find_transcript(['ko'])
                        st.info("ℹ️ 영어 자막이 없어 한국어 자막을 불러왔습니다.")

                    data = transcript.fetch()
                    full_text = " ".join([item['text'] for item in data])

                    # 결과 출력
                    st.success("✅ 자막 추출 성공!")
                    st.text_area("추출된 자막 내용:", full_text, height=300)
                    
                    # 다운로드 버튼
                    st.download_button(
                        label="텍스트 파일로 다운로드",
                        data=full_text,
                        file_name="transcript.txt",
                        mime="text/plain"
                    )

                except TranscriptsDisabled:
                    st.error("❌ 이 영상은 자막 기능이 꺼져 있습니다.")
                except VideoUnavailable:
                    st.error("❌ 영상을 찾을 수 없습니다.")
                except Exception as e:
                    st.error(f"❌ 오류 발생: {str(e)}")
                    st.info("팁: 영상에 자막(CC)이 설정되어 있는지 확인해 주세요!")
