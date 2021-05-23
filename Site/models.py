import random
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Max, Min


class Squad(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    display_name = models.CharField(max_length=10, null=False, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)

    class Meta:
        unique_together = ('display_name', 'author')

    def __str__(self):
        return self.display_name


class Tournament(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    display_name = models.CharField(max_length=10, null=False, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)

    class Meta:
        unique_together = ('display_name', 'author')

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    image = models.ImageField(null=False, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)

    class Meta:
        unique_together = ('name', 'author')

    def __str__(self):
        return self.name

    def clean(self):
        super(Image, self).clean()

        errors = dict()

        try:
            if hasattr(self, 'image'):
                if self.image is not None:
                    if self.image.size > 5 * 1024 * 1024:
                        raise ValidationError("Image file too large (>5mb)")
        except ValidationError as e:
            errors['image'] = e.error_list

        if errors:
            raise ValidationError(errors)


class PointsTableInfo(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=False, blank=False)
    match_number = models.PositiveIntegerField(null=False, blank=False)
    bottom_left_text = models.CharField(max_length=25, null=True, blank=True)
    bottom_center_text = models.CharField(max_length=25, null=True, blank=True)
    bottom_right_text = models.CharField(max_length=25, null=True, blank=True)
    background_image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, related_name='background_pt_set')
    top_left_image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, related_name='top_left_pt_set')
    top_right_image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, related_name='top_right_pt_set')
    bottom_left_images = models.ManyToManyField(Image, blank=True, related_name='btm_lt_set')
    bottom_center_images = models.ManyToManyField(Image, blank=True, related_name='btm_cn_set')
    bottom_right_images = models.ManyToManyField(Image, blank=True, related_name='btm_rt_set')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)

    class Meta:
        unique_together = ('tournament', 'match_number', 'author')

    def __str__(self):
        return str(self.tournament) + ' -> Match: ' + str(self.match_number)

    def clean(self):
        super(PointsTableInfo, self).clean()

        errors = dict()

        if errors:
            raise ValidationError(errors)


class PlacementPoint(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=False, blank=False)
    match_number = models.PositiveIntegerField(null=False, blank=False)
    placement = models.IntegerField(null=False, blank=False)
    point = models.IntegerField(null=False, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)

    class Meta:
        unique_together = ('tournament', 'match_number', 'placement', 'author')

    def __str__(self):
        return str(self.tournament) + ' -> Match: ' + str(self.match_number) + ' -> Placement: ' + str(self.placement)

    def clean(self):
        super(PlacementPoint, self).clean()

        errors = dict()

        try:
            if hasattr(self, 'placement') and hasattr(self, 'tournament') and hasattr(self, 'match_number'):
                if (self.placement is not None) and (self.match_number is not None) and (self.tournament is not None):
                    if self.placement < -1:
                        raise ValidationError("Placement must be greater than or equal to -1")
        except ValidationError as e:
            errors['placement'] = e.error_list

        if errors:
            raise ValidationError(errors)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(PlacementPoint, self).save(force_insert, force_update, using, update_fields)

        infected_tournament = self.tournament
        infected_match = self.match_number

        if infected_match == 0:
            m = [match_number for match_number in
                 PlacementPoint.objects.filter(tournament=infected_tournament).values_list('match_number',
                                                                                           flat=True).distinct()]
            infected_ranks = Rank.objects.filter(tournament=infected_tournament).exclude(match_number__in=m)
        else:
            infected_ranks = Rank.objects.filter(tournament=infected_tournament, match_number=infected_match)

        if infected_ranks.count() != 0:
            infected_squads = [squad for squad in infected_ranks.values_list('squad', flat=True).distinct()]
            for infected_squad in infected_squads:
                if infected_match == 0:
                    infected_match = Rank.objects.filter(tournament=infected_tournament, squad=infected_squad).values_list('match_number').distinct().aggregate(Min('match_number'))['match_number__min']

                infection_center = Rank.objects.get(tournament=infected_tournament, match_number=infected_match, squad=infected_squad)
                infection_center.save()


class Rank(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=False, blank=False)
    match_number = models.PositiveIntegerField(null=False, blank=False)
    squad = models.ForeignKey(Squad, on_delete=models.CASCADE, null=False, blank=False)
    placement = models.IntegerField(null=False, blank=False)
    placement_pts = models.IntegerField(default=0, null=False, blank=True)
    gross_placement_pts = models.IntegerField(default=0, null=False, blank=True)
    kill_pts = models.IntegerField(null=False, blank=False)
    gross_kill_pts = models.IntegerField(default=0, null=False, blank=True)
    total_pts = models.IntegerField(default=0, null=False, blank=True)
    gross_total_pts = models.IntegerField(default=0, null=False, blank=True)
    chicken_dinner = models.IntegerField(default=0, null=False, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)

    class Meta:
        unique_together = ('tournament', 'match_number', 'squad', 'author')

    def __str__(self):
        return self.tournament.display_name + " -> Match: " + str(self.match_number) + ' -> Squad: ' + self.squad.display_name

    @property
    def have_dinner(self):
        return self.chicken_dinner > 0

    @property
    def gradient_color(self):
        gradient_color_choices = ['red', 'gold', 'pink', 'purple', 'orange', 'blue', 'green', 'magenta', 'teal',
                                  '#802a00', '#800070', '#00803c', '#646629', '#293a66', '#28915e', '#914b28', '#c35f5f'
                                  ]
        return random.choice(gradient_color_choices)

    @property
    def rank(self):
        score = self.gross_total_pts
        return Rank.objects.filter(match_number=self.match_number,
                                   gross_total_pts__gt=score,
                                   tournament=self.tournament,
                                   author=self.author).values_list('gross_total_pts', flat=True).distinct().count() + 1

    @property
    def rank_tag(self):
        if self.match_number == 1:
            return 'fa-arrow-up text-success'
        else:
            qs = Rank.objects.filter(match_number__lt=self.match_number, tournament=self.tournament, squad=self.squad,
                                     author=self.author)
            if qs.count() == 0:
                return 'fa-arrow-up text-success'
            else:
                temp = qs.aggregate(Max('match_number'))['match_number__max']
                prev_rank = Rank.objects.get(match_number=temp, tournament=self.tournament, squad=self.squad,
                                             author=self.author).rank
                current_rank = self.rank

                if current_rank < prev_rank:
                    return 'fa-arrow-up text-success'
                elif current_rank == prev_rank:
                    return 'fa-minus text-warning'
                else:
                    return 'fa-arrow-down text-danger'

    def clean(self):
        super(Rank, self).clean()

        errors = dict()

        try:
            if hasattr(self, 'placement') and hasattr(self, 'match_number') and hasattr(self, 'tournament'):
                if (self.placement is not None) and (self.match_number is not None) and (self.tournament is not None):
                    if self.placement == 0 or self.placement < -1:
                        raise ValidationError("Placement must be greater than 0 (it can be -1 if squad did not participate)")
        except ValidationError as e:
            errors['placement'] = e.error_list

        try:
            if hasattr(self, 'kill_pts'):
                if self.kill_pts is not None:
                    if self.kill_pts < 0:
                        raise ValidationError("Kill point must be greater or equal to 0")
                    if hasattr(self, 'placement'):
                        if self.placement is not None:
                            if self.placement == -1 and self.kill_pts > 0:
                                raise ValidationError("Kill point must be 0 while placement is -1")
        except ValidationError as e:
            errors['kill_pts'] = e.error_list

        if errors:
            raise ValidationError(errors)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        pts_qs = PlacementPoint.objects.filter(tournament=self.tournament, match_number=self.match_number)
        if pts_qs.exists():
            pts_qs_qs = pts_qs.filter(placement=self.placement)
            if pts_qs_qs.exists():
                self.placement_pts = pts_qs_qs[0].point
            else:
                pts_qs_qs = pts_qs.filter(placement=0)
                if pts_qs_qs.exists():
                    self.placement_pts = pts_qs_qs[0].point
                else:
                    self.placement_pts = 0
        else:
            pts_qs = PlacementPoint.objects.filter(tournament=self.tournament, match_number=0)
            pts_qs_qs = pts_qs.filter(placement=self.placement)
            if pts_qs_qs.exists():
                self.placement_pts = pts_qs_qs[0].point
            else:
                pts_qs_qs = pts_qs.filter(placement=0)
                if pts_qs_qs.exists():
                    self.placement_pts = pts_qs_qs[0].point
                else:
                    self.placement_pts = 0

        self.total_pts = self.placement_pts + self.kill_pts

        qs = Rank.objects.filter(match_number__lt=self.match_number, tournament=self.tournament, squad=self.squad)
        if qs.count() == 0:
            self.gross_placement_pts = self.placement_pts
            self.gross_kill_pts = self.kill_pts
            cd_prev = 0
            self.gross_total_pts = self.total_pts
        else:
            max_match_num_lt_current = qs.aggregate(Max('match_number'))['match_number__max']
            prev_rank = Rank.objects.get(match_number=max_match_num_lt_current, tournament=self.tournament, squad=self.squad)

            self.gross_placement_pts = prev_rank.gross_placement_pts + self.placement_pts
            self.gross_kill_pts = prev_rank.gross_kill_pts + self.kill_pts
            cd_prev = prev_rank.chicken_dinner
            self.gross_total_pts = prev_rank.gross_total_pts + self.total_pts

        add_cd = 1 if self.placement == 1 else 0
        self.chicken_dinner = cd_prev + add_cd

        super(Rank, self).save(force_insert, force_update, using, update_fields)

        tournament = self.tournament
        match = self.match_number
        squad = self.squad
        infected_ranks = Rank.objects.filter(tournament=tournament, match_number__gt=match, squad=squad)
        if infected_ranks.exists():
            infected_ranks = infected_ranks.order_by('match_number')
            infected_ranks[0].placement_pts = 0
            infected_ranks[0].save()
