from enum import Enum


class AssistantName(Enum):
    GPT = 'gpt'
    CLOUD = 'cloud'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.title()) for key in cls]

