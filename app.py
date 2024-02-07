import streamlit as st
import time
from ai import *
from img_video import *
from subtitles import *
# from ai import generate_saying

def main(): 
    # 사이드바
    with st.sidebar:        
        # 스트림릿 앱 제목 설정
        st.title("OpenAI TTS Voice Generator")

        # 사이드바에 API 키 입력 필드 추가
        api_key = st.sidebar.text_input("OpenAI API 키", "")

        with st.form("side_form"):            
            size = st.selectbox("Size", ["1024x1792", "1024x1024", "1792x1024"])
             # 사이드바에 성우 선택
            selected_voice = st.selectbox("성우 선택", ["onyx", "nova", "shimmer", "echo", "fable", "alloy"])
            # 사이드바에 스타일 선택
            selected_style = st.selectbox("스타일 선택", ["clear", "concise", "conversational"])
            submit = st.form_submit_button("Submit") 
    
    # 메인
    st.header(':blue[SAYIN]:red[G]:blue[RAM]  :clapper:', divider='rainbow')
    with st.form("top_form"):
            user_input = st.text_input("명언을 만들 주제를 입력해 주세요")           
            submit = st.form_submit_button("Submit") 
    if submit and user_input:
        st.write(user_input + '에 대한 명언을 만들겠습니다')
        with st.spinner('Wait for it...'):
            # saying = temp()["saying"]
            # prompt_tokens = temp()["prompt_tokens"]
            # completion_tokens = temp()["completion_tokens"]   
            saying = generate_saying(user_input)["saying"]
            # prompt_tokens = generate_saying(user_input)["prompt_tokens"]
            # completion_tokens = generate_saying(user_input)["completion_tokens"]         
            print("봇:", saying)

            dollar = 1280    
            # input_price = prompt_tokens*0.00005
            # output_price = completion_tokens*0.0015
            # total_price = input_price + output_price
            # price = int(total_price*dollar)
            
            st.write(saying)
            # st.write(saying_sentence(saying))
            # st.write(sentence_word(saying))
            saying_sentence(saying)
            sentence_word(saying)
            saying_speech(saying,selected_voice)           
            subtitles_txt()
            subtitles_srt()
            generate_image(user_input, size)
            img_size()
            img_video()
            video_audio()
            
            st.write(str(count_letter(saying))+"글자")
            st.subheader(':blue[*Price*]  :credit_card:', divider='rainbow')
            # st.caption('input_tokens:' +str(prompt_tokens))
            # st.caption('output_tokens:' +str(completion_tokens))           
            # st.subheader(str(price) + '원')

if __name__ == "__main__":
    main()