import whisper
from user import *

# Whisper 모델 로드 (medium 모델로 변경)
model = whisper.load_model("medium")

print("한글로 변환하고 싶은 유저 오디오의 이름은?")
id = input()
if id in user.keys():
    id = user[id]
else:
    print("error, 유저 없음")
    exit(0)
file_name = f"{id}.mp3"


# 음성 파일 텍스트 변환
result = model.transcribe(file_name)

# 변환된 텍스트 출력

print(result["text"])