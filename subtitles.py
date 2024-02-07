
import os
import re
import streamlit as st
from pathlib import Path
import moviepy.editor as mp
from datetime import timedelta
from ai import *

# #테스트용 임시 결과물
# def temp():
#     saying = "성공은 노력과 열정을 통해 이루어진다. 실패는 성공의 밑거름이다. 명심해라, 노력하면 성공은 따른다"
#     message = "test " 
#     prompt_tokens = 1000
#     completion_tokens = 300
#     # saying을 텍스트 파일로 저장
#     folder_path = 'txt'
#     # 폴더가 없으면 생성
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)
#     # 텍스트 파일 열기 및 저장    
#     with open(os.path.join(folder_path, 'saying.txt'), 'w', encoding='utf-8') as file:
#         file.write(saying)
#     return {"saying":saying, "message":message, "prompt_tokens":prompt_tokens, "completion_tokens":completion_tokens}

# #명언만들기
# def generate_saying(user_input):    
#     response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a world-class sage."},
#                 {"role": "user", "content": f"{user_input}에 대한 세문장의 명언을 20단어 이내로 한 단락으로 짧게 한글로 만드는데\
#              문장은 마침표로 구분하고 마지막 문장은  '''명심해라, ''' 뒤에 짧게 지시하는 문장을 넣어서 만들어줘,\
#              50자 이내로 만들고 번호, 순서는 넣지마, 해라체로 만들고,'''그리고'''는 넣지마"},                
#             ]
#             )
#     saying = response.choices[0].message.content
#     message = response.choices[0].message   
#     prompt_tokens = response.usage.total_tokens
#     completion_tokens = response.usage.total_tokens 
      # saying을 텍스트 파일로 저장
      # with open('saying.txt', 'w', encoding='utf-8') as file:
      #     file.write(saying)   
#     return {"saying":saying, "message":message, "prompt_tokens":prompt_tokens, "completion_tokens":completion_tokens}
with open(os.path.join('txt', 'saying.txt'), 'r', encoding='utf-8') as file:
        saying = file.read()
#글자수 카운트(공백,부호 포함)
def count_letter(saying):
        # 문장 부호와 공백을 포함한 글자 수 세기
        count_letter = len(saying)
        
        return count_letter

#3문장으로 분리
def saying_sentence(saying):
    # 문장을 .으로 나누기
    sentences = saying.split('. ')
    
    # 마지막 문장의 마침표 제거
    last_sentence = sentences[-1].rstrip('.')
    # 리스트에 저장
    sentences[-1] = last_sentence

    # 문장을 3문장씩 나누기
    chunk_size = 3
    divided_sentences = [sentences[i:i + chunk_size] for i in range(0, len(sentences), chunk_size)]

    # 결과 출력
    for i, chunk in enumerate(divided_sentences):
        print(f"Chunk {i + 1}:")
        for sentence in chunk:
            print(sentence)
    
    # 결과를 텍스트 파일로 저장
    folder_path = 'txt'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    with open(os.path.join(folder_path, 'sentence.txt'), 'w', encoding='utf-8') as file:
        for chunk in divided_sentences:
            file.write('\n'.join(chunk))
            file.write('\n\n')
    
    return divided_sentences

# # 함수 사용 예시
# saying = "성공은 노력과 열정을 통해 이루어진다. 실패는 성공의 밑거름이다. 명심해라, 노력하면 성공은 따른다. 세 번째 문장입니다."
# divided_sentences = saying_sentence(saying)

    
#문장을 단어로 분리
def sentence_word(saying):         
    # 문장 부호 제거
    original_sentences = re.sub(r'[\,\.\?\!\n]', '', saying)            
    # 문장을 공백으로 나누기
    words = original_sentences.split() 
    # 결과 출력
    for word in words:
        print(words)
    # saying을 텍스트 파일로 저장
    folder_path = 'txt'
    # 폴더가 없으면 생성
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # 리스트로 저장
    with open(os.path.join(folder_path, 'words.txt'), 'w', encoding='utf-8') as file:
        file.write('\n'.join(words))
    return words

# #음성으로 변환
# def saying_speech(saying,selected_voice):
#     # 보이스 폴더 경로 설정
#     speech_folder = Path(__file__).parent / "output_speech"
#     # MP3 파일 경로 설정
#     speech_file_path = speech_folder / "speech.mp3"
#      # 보이스 폴더가 없으면 생성
#     if not os.path.exists(speech_folder):
#         os.makedirs(speech_folder)
#     # MP3 생성 및 저장
#     speech = openai.audio.speech.create(
#         model="tts-1",
#         voice=selected_voice,
#         input=saying
#     )
#     # 보이스 폴더에 MP3 파일 저장
#     speech.write_to_file(speech_file_path)  
# # 함수 사용 예시
# # saying = "성공은 노력과 열정을 통해 이루어진다. 실패는 성공의 밑거름이다. 명심해라, 노력하면 성공은 따른다"
# # selected_voice = "voice1"
# # saying_speech(saying, selected_voice)  

# 한글자당 오디오 재생시간 계산
def speech_duration():
    # 오디오 파일 경로
    audio_path = './output_speech/speech.mp3'
    # 오디오 클립 열기
    audio_clip = mp.AudioFileClip(audio_path)
    # 오디오 길이 가져오기 (단위: 초)
    audio_duration = audio_clip.duration
    # "saying.txt" 파일 열기
    with open(os.path.join('txt', 'saying.txt'), 'r', encoding='utf-8') as file:
        saying = file.read()
    # # 자막 간격 계산 (오디오 길이를 글자수로 나눔)
    subtitle_duration = audio_duration / len(saying)
    return subtitle_duration
# # 함수 사용 예시
# # 한 글자당 오디오 재생 시간 계산
# subtitle_duration = speech_duration()
# # 계산된 값을 출력
# print(f'한 글자당 오디오 재생 시간: {subtitle_duration} 초')

def format_timestamp(seconds):
    ms = int((seconds - int(seconds)) * 1000)
    formatted_time = str(timedelta(seconds=int(seconds)))

    if formatted_time.startswith("0:"):
        formatted_time = "0" + formatted_time  # 시간이 한 자리 숫자인 경우 앞에 0 추가

    # 시간 부분을 00으로 설정 (예: 00:23:45.678)
    if not formatted_time.startswith("00:"):
        formatted_time = "00:" + formatted_time

    return f"{formatted_time},{ms:03d}"
# # 함수 사용 예시
# seconds = 37750  # 시간(초)
# formatted = format_timestamp(seconds)
# print(f'포맷된 시간: {formatted}')


def subtitles_txt():
    # words.txt 파일의 경로
    words_file_path = './txt/words.txt'

    # 자막 파일의 경로 (txt 폴더 내에 저장)
    subtitles_file_path = './txt/subtitles.txt'

    # 음성 재생시간
    subtitle_duration = speech_duration()

    # 'txt' 폴더가 없으면 생성
    folder_path = 'txt'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 'words.txt' 파일을 'txt' 폴더 내에서 열기
    with open(words_file_path, 'r', encoding='utf-8') as words_file:
        subtitles = words_file.readlines()

    # 'subtitles.txt' 파일을 'txt' 폴더 내에서 생성
    with open(subtitles_file_path, 'w', encoding='utf-8') as subtitle_file:
        for i, subtitle in enumerate(subtitles):
            start_time = format_timestamp(i * subtitle_duration)
            end_time = format_timestamp((i + 1) * subtitle_duration)
            subtitle_file.write(f"{i + 1}\n")
            subtitle_file.write(f"{start_time} --> {end_time}\n")
            subtitle_file.write(subtitle.strip() + "\n\n")

    print(f'자막이 {subtitles_file_path} 파일로 저장되었습니다.')
# # 함수 호출
# subtitles_txt()

def subtitles_srt():
    # words.txt 파일의 경로
    words_file_path = './txt/words.txt'

    # 자막 파일의 경로 (txt 폴더 내에 저장)
    subtitles_file_path = './txt/subtitles.srt'

    # 음성 재생시간
    subtitle_duration = speech_duration()

    # 'txt' 폴더가 없으면 생성
    folder_path = 'txt'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 'words.txt' 파일을 'txt' 폴더 내에서 열기
    with open(words_file_path, 'r', encoding='utf-8') as words_file:
        subtitles = words_file.readlines()

    # 'subtitles.txt' 파일을 'txt' 폴더 내에서 생성
    with open(subtitles_file_path, 'w', encoding='utf-8') as subtitle_file:
        for i, subtitle in enumerate(subtitles):
            start_time = format_timestamp(i * subtitle_duration)
            end_time = format_timestamp((i + 1) * subtitle_duration)
            subtitle_file.write(f"{i + 1}\n")
            subtitle_file.write(f"{start_time} --> {end_time}\n")
            subtitle_file.write(subtitle.strip() + "\n\n")

    print(f'자막이 {subtitles_file_path} 파일로 저장되었습니다.')
# # 함수 호출
# subtitles_srt()
