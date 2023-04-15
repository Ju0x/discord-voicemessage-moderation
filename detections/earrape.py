# Simple detection for earrapes.
# max_DBFS returns the relative value to the max possible volume in DB.
# Most of the voicemessages are at -10 to -15

from pydub import AudioSegment


def is_earrape(filename: str = "audio.ogg") -> bool:
    audio = AudioSegment.from_ogg(filename)

    if audio.max_dBFS > -2.5:
        return True
    return False
