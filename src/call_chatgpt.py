from call_whisper import whisper

audio_file = "test.mp3"

content  = whisper(audio_file)

print(content)