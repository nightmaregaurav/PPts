from django.core.exceptions import ValidationError
from django.db import models


class SiteSetting(models.Model):
    key = models.CharField(unique=True, max_length=20)
    value_string = models.CharField(max_length=1000, null=True, blank=True)
    value_image = models.ImageField(null=True, blank=True)

    @property
    def value(self):
        return self.value_image if self.value_image else self.value_string

    def clean(self):
        errors = dict()

        try:
            if not self.value_string and not self.value_image:
                raise ValidationError("Fill one value type.")
            if self.value_string and self.value_image:
                raise ValidationError("Fill only one value type.")
        except ValidationError as e:
            errors['value_string'] = e.error_list
            errors['value_image'] = e.error_list

        super(SiteSetting, self).clean()

        if errors:
            raise ValidationError(errors)
