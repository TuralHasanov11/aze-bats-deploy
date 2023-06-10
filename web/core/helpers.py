import uuid

from django.template.defaultfilters import slugify


def generateSlug(value):
    return slugify(value) + f"{uuid.uuid4()}"


class UploadImageStrategy:
    directory: str = None

    def __init__(self, directory: str) -> None:
        self.directory = directory

    def uploadTo(self, instance, filename: str) -> str:
        return f'{self.directory}/{slugify(str(instance))}-{uuid.uuid4()}-{filename}'
