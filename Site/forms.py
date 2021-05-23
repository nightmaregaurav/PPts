from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Tournament, Squad, Rank, PlacementPoint, Image, PointsTableInfo


class SquadForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(SquadForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Squad
        exclude = ()

    def clean(self):
        cleaned_data = super(SquadForm, self).clean()

        errors = dict()

        if not (cleaned_data.get('author', False) is not False):
            cleaned_data['author'] = self.request.user

        try:
            if cleaned_data.get('display_name', False) is not False:
                if Squad.objects.filter(display_name=cleaned_data.get('display_name'), author=cleaned_data.get('author')).exists():
                    raise ValidationError("A squad with same display name already exists.")
        except ValidationError as e:
            errors['display_name'] = e.error_list

        if errors:
            raise ValidationError(errors)
        else:
            return cleaned_data


class TournamentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(TournamentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Tournament
        exclude = ()

    def clean(self):
        cleaned_data = super(TournamentForm, self).clean()

        errors = dict()

        if not (cleaned_data.get('author', False) is not False):
            cleaned_data['author'] = self.request.user

        try:
            if cleaned_data.get('display_name', False) is not False:
                if Tournament.objects.filter(display_name=cleaned_data.get('display_name'), author=cleaned_data.get('author')).exists():
                    raise ValidationError("A Tournament with same display name already exists.")
        except ValidationError as e:
            errors['display_name'] = e.error_list

        if errors:
            raise ValidationError(errors)
        else:
            return cleaned_data


class ImageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ImageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Image
        exclude = ()

    def clean(self):
        cleaned_data = super(ImageForm, self).clean()

        errors = dict()

        if not (cleaned_data.get('author', False) is not False):
            cleaned_data['author'] = self.request.user

        try:
            if cleaned_data.get('name', False) is not False:
                if Image.objects.filter(name=cleaned_data.get('name'), author=cleaned_data.get('author')).exists():
                    raise ValidationError("An Image with same name already exists.")
        except ValidationError as e:
            errors['name'] = e.error_list

        if errors:
            raise ValidationError(errors)
        else:
            return cleaned_data


class PointsTableInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(PointsTableInfoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PointsTableInfo
        exclude = ()

    def clean(self):
        cleaned_data = super(PointsTableInfoForm, self).clean()

        errors = dict()

        if not (cleaned_data.get('author', False) is not False):
            cleaned_data['author'] = self.request.user

        try:
            if (cleaned_data.get('tournament', False) is not False) and (cleaned_data.get('match_number', False) is not False):
                if cleaned_data.get('match_number') < 0:
                    raise ValidationError("Match number must be greater than or equal to 0")
                if PointsTableInfo.objects.filter(tournament=cleaned_data.get('tournament'), match_number=cleaned_data.get('match_number')).exists():
                    raise ValidationError("Points table info for same tournament's same match already exists.")
        except ValidationError as e:
            errors['match_number'] = e.error_list

        if errors:
            raise ValidationError(errors)
        else:
            return cleaned_data


class PlacementPointForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(PlacementPointForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PlacementPoint
        exclude = ()

    def clean(self):
        cleaned_data = super(PlacementPointForm, self).clean()

        errors = dict()

        if not (cleaned_data.get('author', False) is not False):
            cleaned_data['author'] = self.request.user

        try:
            if (cleaned_data.get('tournament', False) is not False) and (cleaned_data.get('match_number', False) is not False):
                if cleaned_data.get('match_number') < 0:
                    raise ValidationError("Match number must be greater than or equal to 0")
        except ValidationError as e:
            errors['match_number'] = e.error_list

        try:
            if (cleaned_data.get('tournament', False) is not False) and (cleaned_data.get('match_number', False) is not False) and (cleaned_data.get('placement', False) is not False):
                if PlacementPoint.objects.filter(tournament=cleaned_data.get('tournament'), match_number=cleaned_data.get('match_number'), placement=cleaned_data.get('placement')).exists():
                    raise ValidationError("A Placement Point for same place, match and tournament already exists.")
        except ValidationError as e:
            errors['placement'] = e.error_list

        if errors:
            raise ValidationError(errors)
        else:
            return cleaned_data


class RankForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(RankForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Rank
        exclude = ()

    def clean(self):
        cleaned_data = super(RankForm, self).clean()

        errors = dict()

        if not cleaned_data.get('author', False):
            cleaned_data['author'] = self.request.user

        try:
            if (cleaned_data.get('tournament', False) is not False) and (cleaned_data.get('match_number', False) is not False):
                if cleaned_data.get('match_number') <= 0:
                    raise ValidationError("Match number must be greater than 0")
        except ValidationError as e:
            errors['match_number'] = e.error_list

        try:
            if (cleaned_data.get('tournament', False) is not False) and (cleaned_data.get('match_number', False) is not False) and (cleaned_data.get('squad', False) is not False):
                if Rank.objects.filter(tournament=cleaned_data.get('tournament'), match_number=cleaned_data.get('match_number'), squad=cleaned_data.get('squad')).exists():
                    raise ValidationError("A Rank for same squad on same match and tournament already exists.")
        except ValidationError as e:
            errors['squad'] = e.error_list

        try:
            if (cleaned_data.get('tournament', False) is not False) and (cleaned_data.get('match_number', False) is not False) and (cleaned_data.get('placement', False) is not False):
                if cleaned_data.get('placement') != -1:
                    if Rank.objects.filter(tournament=cleaned_data.get('tournament'), match_number=cleaned_data.get('match_number'), placement=cleaned_data.get('placement')).exists():
                        raise ValidationError("You already have this position reserved for this tournament and match")
        except ValidationError as e:
            errors['placement'] = e.error_list

        if errors:
            raise ValidationError(errors)
        else:
            return cleaned_data
