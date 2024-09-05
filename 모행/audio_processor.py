import whisper

# Whisper 모델 로드 (medium 모델로 변경)
model = whisper.load_model("medium")

# 음성 파일 텍스트 변환
result = model.transcribe("녹음 test.m4a")

# 변환된 텍스트 출력

print(result["text"])