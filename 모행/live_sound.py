# import pyaudio
# import numpy as np
# import whisper
# import wave 
# import time

# #위스퍼 모델 로드
# model = whisper.load_model("medium")

# #마이크 입력 초기화 
# FORMAT = pyaudio.paInt16 #오디오 포멧
# CHANNELS = 1 #모노
# RATE = 16000 #샘플링 레이트 (whisper은 16khz를 권장)
# CHUNK = 1024 #오디오 청크 크기

# #pyAudio 객체 생성
# audio = pyaudio.PyAudio()


# #마이크 스트림 열기
# stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,frames_per_buffer=CHUNK)

# print(bool(stream))

# print("실시간 음성 입력을 시작합니다. Ctrl+c로 종료하세요.")

# try:
#     while True:
#         #실시간으로 입력받은 음성 데이터 읽기
#         audio_data = stream.read(CHUNK)

#         #입력받은 데이터를 float형으로 반환하여 numpy 배열로 저장
#         audio_np = np.frombuffer(audio_data, np.int16).astype(np.float32)

#         #whisper는 음성 파일을 필요로 하므로, 데이터를 파일로 저장하거나 가상 파일로 처리해야함
#         #여기서는 간단히 temp파일로 저장하고 처리하는 방법을 사용
#         wf = wave.open("temp.wav", 'wb')
#         wf.setnchannels(CHANNELS)
#         wf.setsampwidth(audio.get_sample_size(FORMAT))
#         wf.setframerate(RATE)
#         wf.writeframes(audio_data)
#         wf.close()

#         #whisper로 음성 파일을 텍스트로 변환
#         result = model.transcribe("temp.wav")

#         #변환된 텍스트 출력
#         print("변환된 텍스트:",result['text'])

#         time.sleep(0.1)

# except Exception as e:
#     print("------------", str(e))
# # except KeyboardInterrupt:
# #     print("실시간 음성 입력을 종료합니다.")
    
# #스트림 닫기
# stream.stop_stream()
# stream.close()
# audio.terminate()

# 아직 모르겠음



# 필요한 라이브러리 import
import speech_recognition as sr
import ffmpeg
from user import user
from playsound import playsound

# Recognizer 객체 생성
r = sr.Recognizer()

# 마이크를 오디오 소스로 사용
mic = sr.Microphone()

# 저장할 오디오 파일의 이름
# file_name = "recorded_audio.mp3"
print("이름를 입력하세요.")
id = input()
if id in user.keys():
    id = user[id]
else:
    print("error, 유저 없음")
    exit(0)
file_name = f"{id}.mp3"

# 음성 녹음 함수
def record_audio():
    with mic as source:
        print("녹음 시작...")
        audio_data = r.listen(source, timeout=10, phrase_time_limit=10)
        print("---------")
        print("녹음 완료!")
        return audio_data

# 오디오 파일 녹음 및 재생 함수
def play_audio():
    playsound(file_name)

if __name__ == "__main__":
    # 음성 녹음
    audio_data = record_audio()

    # 오디오 파일로 저장
    with open(file_name, "wb") as f:
        f.write(audio_data.get_wav_data())

    # 오디오 파일 재생
    # play_audio()


    #live_sound 에서 사용자 이름을 입력받는 다음 그에 맞는 파일이름으로 음성녹음을 한다
    #그리고 audio_processor로 파일을 보내준다
    # 사용자마다 파일 이름을 정해주는 이유는 사람들이 같이 음성녹음을 진행하면 마지막에 녹음한 사람의 것으로 파일 녹음이 된다 그러하여 각각의 파일 이름을 정해준다
    