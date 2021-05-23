import sys
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def thumbnail_gen(image, ww, hh):
    w, h = image.width, image.height
    if w == ww and h == hh:
        return image

    name = image.name.split('.')[0] + '-thumb'
    image = Image.open(image)
    output = BytesIO()
    ratio = max(ww / w, hh / h)
    image = image.resize((int(w*ratio), int(h*ratio)))

    w, h = image.size
    img = Image.new('RGBA', (ww, hh), (255, 0, 0, 0))
    img.paste(image, (int((ww - w) / 2), int((hh - h) / 2)))

    img.save(output, format='PNG', quality=100)
    output.seek(0)

    return InMemoryUploadedFile(output, 'ImageField', "%s.png" % name, 'image/png', sys.getsizeof(output), None)
