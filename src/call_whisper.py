from transformers import pipeline

def whisper(audio_file):
    # Whisper 모델 로드
    whisper_medium = pipeline(task="automatic-speech-recognition", model="openai/whisper-medium")

    # 오디오 파일 경로

    # 음성 인식 실행
    result = whisper_medium(audio_file)

    # 결과 출력
    return result['text']

