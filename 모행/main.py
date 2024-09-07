# 1. 사용자에게 파일을 업로드 받아 음성을 녹음 및 저장
# 2. whisper 모델을 사용하여 음성르 텍스트로 변환
# 3. 변환된 텍스트를 반환

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import speech_recognition as sr
import whisper
from playsound import playsound
import os

app = FastAPI()

# 사용자 정보 사전
user_dict = {"donggun": "dongguri", "modeep": "modeep", "ai": "whisper"}

# Whisper 모델 로드 (medium 모델)
model = whisper.load_model("medium")

# Recognizer 객체 생성
r = sr.Recognizer()

# 마이크를 오디오 소스로 사용
mic = sr.Microphone()

# 음성 녹음 함수
def record_audio():
    with mic as source:
        print("녹음 시작...")
        audio_data = r.listen(source, timeout=10, phrase_time_limit=10)
        print("---------")
        print("녹음 완료!")
        return audio_data

# 오디오 파일 저장 함수
def save_audio(file_name: str, audio_data):
    with open(file_name, "wb") as f:
        f.write(audio_data.get_wav_data())

# 오디오 파일 재생 함수
def play_audio(file_name: str):
    playsound(file_name)

# 사용자 입력받아 음성 파일을 녹음하는 엔드포인트
@app.post("/record/")
async def record(user_id: str = Form(...)):
    if user_id not in user_dict:
        raise HTTPException(status_code=404, detail="User not found")

    # 파일 이름 설정
    file_name = f"{user_dict[user_id]}.mp3"
    
    # 음성 녹음
    audio_data = record_audio()
    
    # 오디오 파일로 저장
    save_audio(file_name, audio_data)
    
    return {"message": f"Audio saved as {file_name}"}

# 파일을 업로드하고 Whisper로 텍스트 변환하는 엔드포인트
@app.post("/transcribe/")
async def transcribe(user_id: str = Form(...)):
    if user_id not in user_dict:
        raise HTTPException(status_code=404, detail="User not found")

    file_name = f"{user_dict[user_id]}.mp3"
    
    # 음성 파일이 존재하는지 확인
    if not os.path.exists(file_name):
        raise HTTPException(status_code=404, detail="Audio file not found")

    # Whisper로 음성 텍스트 변환
    result = model.transcribe(file_name)
    
    # 변환된 텍스트 반환
    return {"transcribed_text": result["text"]}

# 오디오 파일을 업로드해서 Whisper로 변환하는 엔드포인트
@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_name = file.filename

    # 파일 저장
    with open(file_name, "wb") as f:
        f.write(await file.read())

    # Whisper로 음성 텍스트 변환
    result = model.transcribe(file_name)
    
    # 변환된 텍스트 반환
    return {"transcribed_text": result["text"]}

# 오디오 파일 재생 엔드포인트
@app.post("/play/")
async def play(user_id: str = Form(...)):
    if user_id not in user_dict:
        raise HTTPException(status_code=404, detail="User not found")
    
    file_name = f"{user_dict[user_id]}.mp3"
    
    # 파일이 존재하는지 확인
    if not os.path.exists(file_name):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    # 오디오 파일 재생
    play_audio(file_name)
    
    return {"message": f"Playing audio {file_name}"}
