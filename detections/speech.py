import whisper
import json
import requests

with open("config.json", "r") as fp:
    data = json.load(fp)


def get_audio(message=None, direct_url: str = None, filename: str = "audio.ogg") -> bool:
    url = None

    if direct_url is None:
        for attachment in message.attachments:
            if attachment.filename.endswith(".ogg"):
                url = attachment.url
                break
    else:
        url = direct_url

    if url is None:
        return False

    response = requests.get(url)

    with open(filename, "wb") as file:
        file.write(response.content)

    return True


def to_text(filename: str = "audio.ogg") -> whisper.DecodingResult:
    model = whisper.load_model("base")

    audio = whisper.load_audio(filename)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    if data["language"] == "auto":
        _, probs = model.detect_language(mel)
        options = whisper.DecodingOptions(fp16=False)
    else:
        options = whisper.DecodingOptions(fp16=False, language=data["language"])

    result = whisper.decode(model, mel, options)

    return result
