from enum import StrEnum


# --<> ChatAction Enum
class ChatAction(StrEnum):
    typing = "typing"
    photo = "upload_photo"
    video = "upload_video"
    audio = "upload_voice"
    document = "upload_document"
    # --</>
