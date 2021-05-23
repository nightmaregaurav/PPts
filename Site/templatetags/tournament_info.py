from django import template

from Site.models import PointsTableInfo

register = template.Library()


@register.filter()
def get_details(value1, value2):
    info = PointsTableInfo.objects.filter(tournament=value1, match_number=value2)
    if info.exists():
        info = info[0]

        bottom_left_text_status = True if info.bottom_left_text else False
        bottom_left_text = info.bottom_left_text.title() if info.bottom_left_text else None
        bottom_center_text_status = True if info.bottom_center_text else False
        bottom_center_text = info.bottom_center_text.title() if info.bottom_center_text else None
        bottom_right_text_status = True if info.bottom_right_text else False
        bottom_right_text = info.bottom_right_text.title() if info.bottom_right_text else None
        background_image_status = True if info.background_image else False
        background_image = info.background_image.image if info.background_image else None
        top_left_image_status = True if info.top_left_image else False
        top_left_image = info.top_left_image.image if info.top_left_image else None
        top_right_image_status = True if info.top_right_image else False
        top_right_image = info.top_right_image.image if info.top_right_image else None
        bottom_left_images_status = True if info.bottom_left_images.count() > 0 else False
        bottom_left_images = info.bottom_left_images.all() if info.bottom_left_images.count() > 0 else None
        bottom_center_images_status = True if info.bottom_center_images.count() > 0 else False
        bottom_center_images = info.bottom_center_images.all() if info.bottom_center_images.count() > 0 else None
        bottom_right_images_status = True if info.bottom_right_images.count() > 0 else False
        bottom_right_images = info.bottom_right_images.all() if info.bottom_right_images.count() > 0 else None
    else:
        info = PointsTableInfo.objects.filter(tournament=value1, match_number=0)
        if info.exists():
            info = info[0]

            bottom_left_text_status = True if info.bottom_left_text else False
            bottom_left_text = info.bottom_left_text.title() if info.bottom_left_text else None
            bottom_center_text_status = True if info.bottom_center_text else False
            bottom_center_text = info.bottom_center_text.title() if info.bottom_center_text else None
            bottom_right_text_status = True if info.bottom_right_text else False
            bottom_right_text = info.bottom_right_text.title() if info.bottom_right_text else None
            background_image_status = True if info.background_image else False
            background_image = info.background_image.image if info.background_image else None
            top_left_image_status = True if info.top_left_image else False
            top_left_image = info.top_left_image.image if info.top_left_image else None
            top_right_image_status = True if info.top_right_image else False
            top_right_image = info.top_right_image.image if info.top_right_image else None
            bottom_left_images_status = True if info.bottom_left_images.count() > 0 else False
            bottom_left_images = info.bottom_left_images.all() if info.bottom_left_images.count() > 0 else None
            bottom_center_images_status = True if info.bottom_center_images.count() > 0 else False
            bottom_center_images = info.bottom_center_images.all() if info.bottom_center_images.count() > 0 else None
            bottom_right_images_status = True if info.bottom_right_images.count() > 0 else False
            bottom_right_images = info.bottom_right_images.all() if info.bottom_right_images.count() > 0 else None
        else:
            bottom_left_text_status = False
            bottom_left_text = None
            bottom_center_text_status = False
            bottom_center_text = None
            bottom_right_text_status = False
            bottom_right_text = None
            background_image_status = False
            background_image = None
            top_left_image_status = False
            top_left_image = None
            top_right_image_status = False
            top_right_image = None
            bottom_left_images_status = False
            bottom_left_images = None
            bottom_center_images_status = False
            bottom_center_images = None
            bottom_right_images_status = False
            bottom_right_images = None

    return {
        'bottom_left_text': {
            'exists': bottom_left_text_status,
            'data': bottom_left_text,
        },
        'bottom_center_text': {
            'exists': bottom_center_text_status,
            'data': bottom_center_text,
        },
        'bottom_right_text': {
            'exists': bottom_right_text_status,
            'data': bottom_right_text,
        },
        'background_image': {
            'exists': background_image_status,
            'data': background_image,
        },
        'top_left_image': {
            'exists': top_left_image_status,
            'data': top_left_image,
        },
        'top_right_image': {
            'exists': top_right_image_status,
            'data': top_right_image,
        },
        'bottom_left_images': {
            'exists': bottom_left_images_status,
            'data': bottom_left_images,
        },
        'bottom_center_images': {
            'exists': bottom_center_images_status,
            'data': bottom_center_images,
        },
        'bottom_right_images': {
            'exists': bottom_right_images_status,
            'data': bottom_right_images,
        },
    }
