import os 
# import cv2
import time
from PIL import Image
import streamlit as st
from moviepy.editor import AudioFileClip, VideoFileClip,TextClip,CompositeVideoClip, concatenate_videoclips
from moviepy.video.tools.subtitles import SubtitlesClip
import pysrt
import imageio


def img_size():
    # 이미지 파일이 저장된 디렉토리 경로
    input_images = 'input_images'

    # 조정된 이미지를 저장할 디렉토리 경로
    output_images = 'output_images'    
    # 출력 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(output_images):
        os.makedirs(output_images)    
    # 새로운 이미지 크기 설정 (가로 x 세로)
    new_width = 1080
    new_height = 1920

    # 입력 디렉토리에서 모든 이미지 파일 가져오기
    image_files = [f for f in os.listdir(input_images) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

    # 이미지 크기 조정 및 저장
    for image_file in image_files:
        input_image_path = os.path.join(input_images, image_file)
        output_image_path = os.path.join(output_images, image_file)

        # 이미지 열기
        image = Image.open(input_image_path)

        # 이미지 크기 조정
        resized_image = image.resize((new_width, new_height))

        # 조정된 이미지 저장
        resized_image.save(output_image_path)

        # 이미지 객체 닫기
        image.close()

#cv2 안쓰고 구현 
def img_video():
    video_folder = 'output_video'
    # 출력 디렉토리가 존재하지 않으면 생성    
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)        
    # 이미지 파일이 저장된 디렉토리 경로
    image_dir = 'output_images'
    # 이미지 파일의 확장자 (일반적으로 .jpg, .png 등)
    image_extension = ('.jpg', '.png')
    # 동영상 파일명
    video_filename = 'output_video.mp4'
    # 동영상 프레임 속도 (fps)
    frame_rate = 0.5
    # 프레임 간 딜레이 설정 (초)
    frame_delay = 0.1  # 0.1초 (100 밀리초) 딜레이
    # 이미지 파일을 정렬하여 가져오기
    image_files = [f for f in os.listdir(image_dir) if f.endswith(image_extension)]
    image_files.sort()

    # 첫 번째 이미지를 기반으로 동영상 크기 설정
    first_image = imageio.imread(os.path.join(image_dir, image_files[0]))
    frame_width, frame_height = first_image.shape[1], first_image.shape[0]

    # 동영상 작성자 생성
    video_path = os.path.join(video_folder, video_filename)
    writer = imageio.get_writer(video_path, fps=frame_rate)

    # 이미지를 프레임으로 추가하여 동영상 생성
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        frame = imageio.imread(image_path)
        writer.append_data(frame)
        
        # 프레임 간 딜레이 추가
        writer.append_data(frame)
        time.sleep(frame_delay)

    # 동영상 작성 종료
    writer.close()
    # 이미지 파일 삭제
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        os.remove(image_path)

##cv2써서 구현
# def img_video():
#     video_folder = 'output_video'
#     # 출력 디렉토리가 존재하지 않으면 생성    
#     if not os.path.exists(video_folder):
#         os.makedirs(video_folder)        
#     # 이미지 파일이 저장된 디렉토리 경로
#     image_dir = 'output_images'
#     # 이미지 파일의 확장자 (일반적으로 .jpg, .png 등)
#     image_extension = ('.jpg', '.png')
#     # 동영상 파일명
#     video_filename = 'output_video.mp4'
#     # 동영상 프레임 속도 (fps)
#     frame_rate = 0.5
#     # 프레임 간 딜레이 설정 (초)
#     frame_delay = 0.1  # 0.1초 (100 밀리초) 딜레이
#     # 이미지 파일을 정렬하여 가져오기
#     image_files = [f for f in os.listdir(image_dir) if f.endswith(image_extension)]
#     image_files.sort()

#     # 첫 번째 이미지를 기반으로 동영상 크기 설정
#     first_image = cv2.imread(os.path.join(image_dir, image_files[0]))
#     frame_width, frame_height = first_image.shape[1], first_image.shape[0]

#     # 동영상 작성자 생성
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     video_path = os.path.join(video_folder, video_filename)
#     out = cv2.VideoWriter(video_path, fourcc, frame_rate, (frame_width, frame_height))

#     # 이미지를 프레임으로 추가하여 동영상 생성
#     for image_file in image_files:
#         image_path = os.path.join(image_dir, image_file)
#         frame = cv2.imread(image_path)
#         out.write(frame)
        
#         # 프레임 간 딜레이 추가
#         time.sleep(frame_delay)

#     # 동영상 작성 종료
#     out.release()
#     # 이미지 파일 삭제
#     for image_file in image_files:
#         image_path = os.path.join(image_dir, image_file)
#         os.remove(image_path)
# # # 사용 예시
# # image_dir = 'output_images'  # 이미지 파일이 저장된 디렉토리 경로
# # image_extension = ('.jpg', '.png')  # 이미지 파일의 확장자 (jpg, png 등)
# # video_filename = 'output_video.mp4'  # 동영상 파일명
# # img_video(image_dir, image_extension, video_filename)

#비디오 오디오 병합
def video_audio():
             # 비디오 오디오 병합
    audio = AudioFileClip("./output_speech/speech.mp3")
    video = VideoFileClip("./output_video/output_video.mp4")
    output_folder = "output_video"
    # 비디오 길이를 오디오 길이에 맞추기
    if video.duration > audio.duration:
        # 비디오가 더 길면 오디오 길이에 맞춰 자르기
        video = video.subclip(0, audio.duration)
    elif video.duration < audio.duration:
        # 비디오가 더 짧으면 반복하거나 무음 장면으로 채우기
        repeats = int(audio.duration // video.duration) + 1
        video = concatenate_videoclips([video] * repeats)
        video = video.subclip(0, audio.duration)   
   
    final_clip = video.set_audio(audio)
    output_file_path = os.path.join(output_folder, "video_audio.mp4")
    # final_clip.write_videofile("output.mp4")
    final_clip.write_videofile(output_file_path, fps=30)

    # 비디오를 스트림릿으로 보여주기
    st.video(output_file_path)    

def video_subtitles():
    # 파일 경로 지정
    video_path = './output_video/video_audio.mp4'  # 비디오 파일 경로
    subtitle_path = './txt/subtitles.srt'  # 자막 파일 경로
    output_folder = 'output_video'  # 출력 폴더 경로

    # 비디오 클립 로드
    video = VideoFileClip(video_path)

    # 자막 파일 로드
    subs = pysrt.open(subtitle_path)

    # 자막 클립 생성 및 추가
    clips = [video]  # 최종 비디오 클립 리스트
    for sub in subs:
        # subtitle = TextClip(sub.text, font='Arial', fontsize=48, color='white')
        subtitle = TextClip(sub.text, fontsize=24, font='Arial', color='white', stroke_color='black', stroke_width=0.5)
        # subtitle = subtitle.set_position(('center', 'bottom')).set_duration(sub.duration.total_seconds()).set_start(sub.start.ordinal / 1000)
        subtitle = subtitle.set_position(('center', 'center')).set_duration(sub.duration.seconds).set_start(sub.start.ordinal / 1000)

        clips.append(subtitle)

    # 자막이 추가된 비디오 생성
    final_video = concatenate_videoclips(clips)

    # 결과 저장할 폴더 생성 (없을 경우)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, "video_with_subtitles.mp4")
    final_video.write_videofile(output_path, fps=video.fps)

    # 스트림릿으로 비디오 보여주기
    st.video(output_path)

# # 함수 실행
# video_subtitles()
    
import subprocess

def merge_video_subtitle():
    # 파일 경로를 함수 내부에서 직접 정의
    video_path = './output_video/output_video.mp4'  # 비디오 파일 경로
    subtitle_path = './txt/subtitles.srt'  # 자막 파일 경로
    output_path = './output_video/video_subtitles.mp4'  # 출력 파일 경로

    # FFmpeg 명령 구성
    command = [
        'ffmpeg',
        '-i', video_path,         # 입력 비디오 파일
        '-i', subtitle_path,      # 입력 자막 파일
        '-c', 'copy',
        '-c:s', 'mov_text',       # 자막 코덱 설정
        output_path               # 출력 파일 경로
    ]

    # FFmpeg 명령 실행
    subprocess.run(command, shell=True)

# # 함수 실행
# merge_video_subtitle()
    

def make_textclip(txt, fontsize=24, font='Arial', color='white', stroke_color='black', stroke_width=0.5):
    # TextClip을 생성하는 사용자 정의 함수
    return TextClip(txt, fontsize=fontsize, font=font, color=color, stroke_color=stroke_color, stroke_width=stroke_width)    


def video_subtitle():
    # 자막 파일을 UTF-8로 읽기
    with open("subtitles.srt", encoding='utf-8') as f:
        subtitles = f.read()
    
    # 동영상 파일 경로
    video_file = "./output_video/output_video.mp4"
    # 자막 파일 경로
    subtitles_file = "./txt/subtitles.srt"

    # 동영상 클립 생성
    video_clip = VideoFileClip(video_file)
    # 자막 클립 생성
    subtitles_clip = SubtitlesClip("subtitles.srt", make_textclip=make_textclip)

    # 자막이 보일 위치 설정
    subtitles_clip = CompositeVideoClip([video_clip, subtitles_clip.set_position(('bottom'))])
    # subtitles_clip = subtitles_clip.set_position(('center', 'bottom')).set_duration(video_clip.duration)

    # 동영상과 자막을 합치기 위한 CompositeVideoClip 생성
    video_clip.write_videofile("output_with_subtitles.mp4")
    # final_clip = CompositeVideoClip([video_clip, subtitles_clip])

    # 합쳐진 동영상 파일로 저장
    


# # 비디오 로드
# video = VideoFileClip("example.mp4")

# # SubtitlesClip 생성, 사용자 정의 함수 사용
# subtitles_clip = SubtitlesClip("subtitles.srt", make_textclip=make_textclip)

# # 자막 클립을 비디오에 오버레이
# video = CompositeVideoClip([video, subtitles_clip.set_position(('bottom'))])

# # 결과 출력
# video.write_videofile("output_with_subtitles.mp4")
    
# # 결과 출력
# video_with_subtitles.write_videofile("output_with_subtitles.mp4")