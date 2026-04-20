import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import spacy
from collections import Counter

# 페이지 설정
st.set_page_config(page_title="YouTube English Study", page_icon="📺")
st.title("📺 유튜브 영어 학습 생성기")
st.write("유튜브 주소를 넣으면 AI가 핵심 문장과 단어를 정리해줍니다.")

# 모델 로드
@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")

nlp = load_nlp()

url = st.text_input("유튜브 주소를 입력하세요:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("분석 시작!"):
    if url:
        try:
            v_id = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1]
            with st.spinner('자막을 가져와 분석 중입니다...'):
                transcript = YouTubeTranscriptApi.get_transcript(v_id)
                full_text = " ".join([t['text'] for t in transcript])
                doc = nlp(full_text)
                
                # 문장 및 단어 분석
                sents = [s.text.strip() for s in doc.sents if 10 < len(s.text.split()) < 18]
                words = [t.lemma_.lower() for t in doc if not t.is_stop and not t.is_punct and t.pos_ in ["NOUN", "VERB"]]
                top_words = Counter(words).most_common(5)

                st.success("분석 완료!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("🎯 추천 학습 문장")
                    for i, s in enumerate(sents[:5], 1):
                        st.write(f"{i}. {s}")
                
                with col2:
                    st.subheader("🔑 핵심 단어 TOP 5")
                    for word, count in top_words:
                        st.write(f"- **{word}** ({count}회)")
        except Exception as e:
            st.error(f"에러가 발생했습니다: {e}")
    else:
        st.warning("주소를 입력해주세요!")
