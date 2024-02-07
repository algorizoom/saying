import os
import requests
import openai
from openai import OpenAI
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()
# client = OpenAI(
#     api_key = st.secrets["api_key"]
# )

#명언만들기
def generate_saying(user_input):    
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a world-class sage."},
                {"role": "user", "content": f"Please write a quote about{user_input}in Korean\
                  using 50 characters or less and 15 words or less.\
                  {user_input}에 대한 세문장의 명언을 15단어 이하,50글자 이하로\
                  한 단락으로 순서, 번호 없이 짧게 한글로 만드는데 문장은 마침표로 구분하고\
                  마지막 문장은  '''명심해라, ''' 뒤에 짧게 지시하는 문장을 넣어서 만들어줘,\
                  50자 이내로 만들고 번호, 순서는 넣지마, 해라체로 만들고,'''그리고'''는 넣지마,\
                  briefly in about 15 words, max_lenth:30,writingstyle:jurnalistic,temperature:5, "}    
            # max_tokens = 500,
            # temperature = 5,         
            ],
            # max_tokens=500,
            # temperature=5  
            )
    saying = response.choices[0].message.content
    message = response.choices[0].message   
    prompt_tokens = response.usage.total_tokens
    completion_tokens = response.usage.total_tokens 

    # 저장할 폴더 경로
    txt_folder = 'txt'    
    # 폴더가 없으면 생성
    if not os.path.exists(txt_folder):
        os.makedirs(txt_folder)
    # 저장할 파일 경로
    output_file_path = os.path.join(txt_folder, 'saying.txt')
    #saying을 텍스트 파일로 저장
    # 파일 저장
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(saying)

    print(f'{output_file_path} 파일에 내용이 저장되었습니다.')  
    return {"saying":saying, "message":message, "prompt_tokens":prompt_tokens, "completion_tokens":completion_tokens}

#음성으로 변환
def saying_speech(saying,selected_voice):
    # 보이스 폴더 경로 설정
    speech_folder = Path(__file__).parent / "output_speech"
    # MP3 파일 경로 설정
    speech_file_path = speech_folder / "speech.mp3"
     # 보이스 폴더가 없으면 생성
    if not os.path.exists(speech_folder):
        os.makedirs(speech_folder)
    # MP3 생성 및 저장
    speech = openai.audio.speech.create(
        model="tts-1",
        voice=selected_voice,
        input=saying
    )
    # 보이스 폴더에 MP3 파일 저장
    speech.write_to_file(speech_file_path)  
# 함수 사용 예시
# saying = "성공은 노력과 열정을 통해 이루어진다. 실패는 성공의 밑거름이다. 명심해라, 노력하면 성공은 따른다"
# selected_voice = "voice1"
# saying_speech(saying, selected_voice) 

def generate_image(user_input,size):

    gpt_prompt = [{
        "role": "system",
        # "content": "Imagine the detail appeareance of the input. Response it shortly around 30 words \
        #     in hyper-realistic, city, portraits, Medium aevum"
        "content": "입력의 상세한 모양을 상상해보십시오.\
        최고의 현실적 사진, 세밀한 묘사,도시적, 암벽등반, 스포츠, 어둡고 강렬한, 풍경에서 30 단어 내외로 간략하게 응답하세요.\
        회전된 사진은 만들지 마"
    }]

    gpt_prompt.append({
        "role": "user",
        "content": user_input
    })
   
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=gpt_prompt
    )                    

    prompt = completion.choices[0].message.content
    st.write(prompt)

    with st.spinner("Waiting for DALL-E..."):
        dalle_response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size=size
        )      
    image_url = dalle_response.data[0].url
    
    # webbrowser.open(image_url)
     # 이미지 저장 폴더 설정
    output_folder = 'input_images'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 이미지 다운로드 및 저장
    image_data = requests.get(image_url).content
    image_filename = f"{output_folder}/generated_image.png"
    with open(image_filename, 'wb') as image_file:
        image_file.write(image_data)

    # #이미지 보여주기
    # st.image(image_url)
    # st.caption(f"Image saved at {image_filename}")

# # 사용 예시
# user_input = "Generate an image of a futuristic cityscape with flying cars."
# size = "256x256"  # 이미지 크기 설정
# generate_image(user_input, size)
    
   