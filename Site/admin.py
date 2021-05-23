from django.contrib import admin
from django.db.models import Min

from .forms import SquadForm, TournamentForm, PlacementPointForm, RankForm, ImageForm, PointsTableInfoForm
from .models import Squad, Tournament, Rank, PlacementPoint, Image, PointsTableInfo

admin.site.site_header = "PUBG points table Host Panel"
admin.site.site_title = "PPts Host Panel"
admin.site.index_title = "PPts Host Panel"


@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
    form = SquadForm

    def get_list_filter(self, request):
        if request.user.is_superuser:
            list_filter = ('author',)
        else:
            list_filter = []

        return list_filter

    def get_search_fields(self, request):
        search_fields = ('name', 'display_name')
        return search_fields

    def get_form(self, request, obj=None, change=False, **kwargs):
        model_form = super(SquadAdmin, self).get_form(request, obj, change, **kwargs)

        class ModelFormWithRequest(model_form):
            def __new__(cls, *args, **kwarg):
                kwarg['request'] = request
                return model_form(*args, **kwarg)
        return ModelFormWithRequest

    def get_list_display(self, request):
        if request.user.is_superuser:
            return 'id', 'name', 'display_name', 'author'
        return 'name', 'display_name'

    def get_exclude(self, request, obj=None):
        exclude = super(SquadAdmin, self).get_exclude(request, obj)
        if not exclude:
            exclude = tuple()
        if not request.user.is_superuser:
            exclude += ('author',)
        return exclude

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(SquadAdmin, self).get_queryset(request).order_by('id')
        return super(SquadAdmin, self).get_queryset(request).filter(author=request.user).order_by('display_name')

    def get_readonly_fields(self, request, obj=None):
        prev = super(SquadAdmin, self).get_readonly_fields(request, obj)
        if not prev:
            prev = []
        if obj:
            return prev + ['author', 'display_name']
        return prev

    # noinspection PyBroadException
    def save_model(self, request, obj, form, change):
        try:
            _ = obj.author
        except Exception:
            obj.author = request.user
        obj.save()


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    form = TournamentForm

    def get_list_filter(self, request):
        if request.user.is_superuser:
            list_filter = ('author',)
        else:
            list_filter = []

        return list_filter

    def get_search_fields(self, request):
        search_fields = ('name', 'display_name')
        return search_fields

    def get_form(self, request, obj=None, change=False, **kwargs):
        model_form = super(TournamentAdmin, self).get_form(request, obj, change, **kwargs)

        class ModelFormWithRequest(model_form):
            def __new__(cls, *args, **kwarg):
                kwarg['request'] = request
                return model_form(*args, **kwarg)

        return ModelFormWithRequest

    def get_list_display(self, request):
        if request.user.is_superuser:
            return 'id', 'name', 'display_name', 'author'
        return 'name', 'display_name'

    def get_exclude(self, request, obj=None):
        exclude = super(TournamentAdmin, self).get_exclude(request, obj)
        if not exclude:
            exclude = tuple()
        if not request.user.is_superuser:
            exclude += ('author',)
        return exclude

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(TournamentAdmin, self).get_queryset(request).order_by('id')
        return super(TournamentAdmin, self).get_queryset(request).filter(author=request.user).order_by('display_name')

    def get_readonly_fields(self, request, obj=None):
        prev = super(TournamentAdmin, self).get_readonly_fields(request, obj)
        if not prev:
            prev = []
        if obj:
            return prev + ['author', 'display_name']
        return prev

    # noinspection PyBroadException
    def save_model(self, request, obj, form, change):
        try:
            _ = obj.author
        except Exception:
            obj.author = request.user
        obj.save()


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    form = ImageForm

    def get_list_filter(self, request):
        if request.user.is_superuser:
            list_filter = ('author',)
        else:
            list_filter = []

        return list_filter

    def get_search_fields(self, request):
        search_fields = ('name',)
        return search_fields

    def get_form(self, request, obj=None, change=False, **kwargs):
        model_form = super(ImageAdmin, self).get_form(request, obj, change, **kwargs)

        class ModelFormWithRequest(model_form):
            def __new__(cls, *args, **kwarg):
                kwarg['request'] = request
                return model_form(*args, **kwarg)

        return ModelFormWithRequest

    def get_list_display(self, request):
        if request.user.is_superuser:
            return 'id', 'name', 'author'
        return 'name',

    def get_exclude(self, request, obj=None):
        exclude = super(ImageAdmin, self).get_exclude(request, obj)
        if not exclude:
            exclude = tuple()
        if not request.user.is_superuser:
            exclude += ('author',)
        return exclude

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(ImageAdmin, self).get_queryset(request).order_by('id')
        return super(ImageAdmin, self).get_queryset(request).filter(author=request.user).order_by('name')

    def get_readonly_fields(self, request, obj=None):
        prev = super(ImageAdmin, self).get_readonly_fields(request, obj)
        if not prev:
            prev = []
        if obj:
            return prev + ['author', ]
        return prev

    # noinspection PyBroadException
    def save_model(self, request, obj, form, change):
        try:
            _ = obj.author
        except Exception:
            obj.author = request.user
        obj.save()


@admin.register(PointsTableInfo)
class PointsTableInfoAdmin(admin.ModelAdmin):
    form = PointsTableInfoForm

    def get_list_filter(self, request):
        if request.user.is_superuser:
            list_filter = ('tournament', 'match_number', 'author')
        else:
            list_filter = ('tournament', 'match_number')

        return list_filter

    def get_search_fields(self, request):
        search_fields = ('tournament__name', 'tournament__display_name', 'bottom_left_text', 'bottom_center_text', 'bottom_right_text')
        return search_fields

    def get_form(self, request, obj=None, change=False, **kwargs):
        model_form = super(PointsTableInfoAdmin, self).get_form(request, obj, change, **kwargs)

        class ModelFormWithRequest(model_form):
            def __new__(cls, *args, **kwarg):
                kwarg['request'] = request
                return model_form(*args, **kwarg)

        return ModelFormWithRequest

    def get_list_display(self, request):
        if request.user.is_superuser:
            return 'id', 'tournament', 'match_number', 'bottom_left_text', 'bottom_center_text', 'bottom_right_text', 'background_image', 'top_left_image', 'top_right_image', 'bottom_left_images', 'bottom_center_images', 'bottom_right_images', 'author'
        return 'tournament', 'match_number', 'bottom_left_text', 'bottom_center_text', 'bottom_right_text', 'background_image', 'top_left_image', 'top_right_image', 'bottom_left_images', 'bottom_center_images', 'bottom_right_images'

    def get_exclude(self, request, obj=None):
        exclude = super(PointsTableInfoAdmin, self).get_exclude(request, obj)
        if not exclude:
            exclude = tuple()
        if not request.user.is_superuser:
            exclude += ('author',)
        return exclude

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(PointsTableInfoAdmin, self).get_queryset(request).order_by('-tournament__id', '-match_number')
        return super(PointsTableInfoAdmin, self).get_queryset(request).filter(author=request.user).order_by('-tournament__id', '-match_number')

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'tournament':
                kwargs["queryset"] = Tournament.objects.filter(author=request.user)
            elif db_field.name in ['background_image', 'top_left_image', 'top_right_image', 'bottom_left_images', 'bottom_center_images', 'bottom_right_images']:
                kwargs["queryset"] = Image.objects.filter(author=request.user)
            else:
                pass

        return super(PointsTableInfoAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'tournament':
                kwargs["queryset"] = Tournament.objects.filter(author=request.user)
            elif db_field.name in ['background_image', 'top_left_image', 'top_right_image', 'bottom_left_images', 'bottom_center_images', 'bottom_right_images']:
                kwargs["queryset"] = Image.objects.filter(author=request.user)
            else:
                pass

        return super(PointsTableInfoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'tournament':
                kwargs["queryset"] = Tournament.objects.filter(author=request.user)
            elif db_field.name in ['background_image', 'top_left_image', 'top_right_image', 'bottom_left_images', 'bottom_center_images', 'bottom_right_images']:
                kwargs["queryset"] = Image.objects.filter(author=request.user)
            else:
                pass

        return super(PointsTableInfoAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        prev = super(PointsTableInfoAdmin, self).get_readonly_fields(request, obj)
        if not prev:
            prev = []
        if obj:
            return prev + ['tournament', 'match_number', 'author']
        return prev

    # noinspection PyBroadException
    def save_model(self, request, obj, form, change):
        try:
            _ = obj.author
        except Exception:
            obj.author = request.user
        obj.save()


@admin.register(PlacementPoint)
class PlacementPointAdmin(admin.ModelAdmin):
    form = PlacementPointForm

    def get_list_filter(self, request):
        if request.user.is_superuser:
            list_filter = ('tournament', 'match_number', 'author')
        else:
            list_filter = ('tournament', 'match_number')

        return list_filter

    def get_search_fields(self, request):
        search_fields = ('tournament__name', 'tournament__display_name')
        return search_fields

    def get_form(self, request, obj=None, change=False, **kwargs):
        model_form = super(PlacementPointAdmin, self).get_form(request, obj, change, **kwargs)

        class ModelFormWithRequest(model_form):
            def __new__(cls, *args, **kwarg):
                kwarg['request'] = request
                return model_form(*args, **kwarg)

        return ModelFormWithRequest

    def get_list_display(self, request):
        if request.user.is_superuser:
            return 'id', 'tournament', 'match_number', 'placement', 'point', 'author'
        return 'tournament', 'match_number', 'placement', 'point'

    def get_exclude(self, request, obj=None):
        exclude = super(PlacementPointAdmin, self).get_exclude(request, obj)
        if not exclude:
            exclude = tuple()
        if not request.user.is_superuser:
            exclude += ('author',)
        return exclude

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(PlacementPointAdmin, self).get_queryset(request).order_by('-tournament__id', '-match_number', 'placement')
        return super(PlacementPointAdmin, self).get_queryset(request).filter(author=request.user).order_by('-tournament__id', '-match_number', 'placement')

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'tournament':
                kwargs["queryset"] = Tournament.objects.filter(author=request.user)
            else:
                pass

        return super(PlacementPointAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'tournament':
                kwargs["queryset"] = Tournament.objects.filter(author=request.user)
            else:
                pass

        return super(PlacementPointAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'tournament':
                kwargs["queryset"] = Tournament.objects.filter(author=request.user)
            else:
                pass

        return super(PlacementPointAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def delete_model(self, request, obj):
        infected_tournament = obj.tournament
        infected_match = obj.match_number

        obj.delete()

        if infected_match == 0:
            m = [match_number for match_number in
                 PlacementPoint.objects.filter(tournament=infected_tournament).values_list('match_number', flat=True).distinct()]
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

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            infected_tournament = obj.tournament
            infected_match = obj.match_number

            obj.delete()

            if infected_match == 0:
                m = [match_number for match_number in PlacementPoint.objects.filter(tournament=infected_tournament).values_list('match_number', flat=True).distinct()]
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

    def get_readonly_fields(self, request, obj=None):
        prev = super(PlacementPointAdmin, self).get_readonly_fields(request, obj)
        if not prev:
            prev = []
        if obj:
            return prev + ['tournament', 'match_number', 'placement', 'author']
        return prev

    # noinspection PyBroadException
    def save_model(self, request, obj, form, change):
        try:
            _ = obj.author
        except Exception:
            obj.author = request.user
        obj.save()


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    form = RankForm

    def get_list_filter(self, request):
        if request.user.is_superuser:
            list_filter = ('tournament', 'match_number', 'author')
        else:
            list_filter = ('tournament', 'match_number')

        return list_filter

    def get_search_fields(self, request):
        search_fields = ('tournament__name', 'tournament__display_name', 'squad__name', 'squad__display_name')
        return search_fields

    def get_form(self, request, obj=None, change=False, **kwargs):
        model_form = super(RankAdmin, self).get_form(request, obj, change, **kwargs)

        class ModelFormWithRequest(model_form):
            def __new__(cls, *args, **kwarg):
                kwarg['request'] = request
                return model_form(*args, **kwarg)

        return ModelFormWithRequest

    def get_list_display(self, request):
        list_display = ('tournament', 'match_number', 'squad', 'placement', 'placement_pts',
                        'gross_placement_pts', 'kill_pts', 'gross_kill_pts', 'total_pts', 'gross_total_pts', 'rank',
                        'chicken_dinner')
        if request.user.is_superuser:
            return list_display + ('author', 'id')
        return list_display

    def get_exclude(self, request, obj=None):
        exclude = super(RankAdmin, self).get_exclude(request, obj)
        if not exclude:
            exclude = tuple()
        if not request.user.is_superuser:
            exclude += ('author',)
        return exclude

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(RankAdmin, self).get_queryset(request)\
                .order_by('-tournament__id', '-match_number', '-gross_total_pts')
        return super(RankAdmin, self).get_queryset(request).filter(author=request.user)\
            .order_by('-tournament__id', '-match_number', '-gross_total_pts')

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'squad':
                kwargs["queryset"] = Squad.objects.filter(author=request.user)
            elif db_field.name == 'tournament':
                kwargs["queryset"] = Tournament.objects.filter(author=request.user)
            else:
                pass

        return super(RankAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'squad':
                kwargs["queryset"] = Squad.objects.filter(author=request.user)
            elif db_field.name == 'tournament':
                kwargs["queryset"] = Tournament.objects.filter(author=request.user)
            else:
                pass

        return super(RankAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'squad':
                kwargs["queryset"] = Squad.objects.filter(author=request.user)
            elif db_field.name == 'tournament':
                kwargs["queryset"] = Tournament.objects.filter(author=request.user)
            else:
                pass

        return super(RankAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def delete_model(self, request, obj):
        infected_tournament = obj.tournament
        infected_match = obj.match_number
        infected_squad = obj.squad

        obj.delete()

        infected_ranks = Rank.objects.filter(tournament=infected_tournament, match_number__gt=infected_match, squad=infected_squad)
        if infected_ranks.exists():
            infected_ranks = infected_ranks.order_by('match_number')
            infected_ranks[0].placement_pts = 0
            infected_ranks[0].save()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            infected_tournament = obj.tournament
            infected_match = obj.match_number
            infected_squad = obj.squad

            obj.delete()

            infected_ranks = Rank.objects.filter(tournament=infected_tournament, match_number__gt=infected_match,
                                                 squad=infected_squad)
            if infected_ranks.exists():
                infected_ranks = infected_ranks.order_by('match_number')
                infected_ranks[0].placement_pts = 0
                infected_ranks[0].save()

    def get_readonly_fields(self, request, obj=None):
        prev = super(RankAdmin, self).get_readonly_fields(request, obj)
        if not prev:
            prev = []
        prev += ['placement_pts', 'gross_placement_pts', 'gross_kill_pts', 'total_pts', 'gross_total_pts',
                 'chicken_dinner']
        if obj:
            return prev + ['tournament', 'match_number', 'squad', 'author', 'placement']
        return prev

    # noinspection PyBroadException
    def save_model(self, request, obj, form, change):
        try:
            _ = obj.author
        except Exception:
            obj.author = request.user
        obj.save()
