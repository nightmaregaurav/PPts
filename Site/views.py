import json

from django.contrib.auth.models import User
from django.db.models import Max, Min
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from .forms import RankForm
from .models import Rank, Tournament

app_name = 'Site'
app_url = app_name + '/'


def search(request):
    hosts = User.objects.filter(is_superuser=False, is_active=True, is_staff=True)

    context = {
        'title': 'Search Rank table',
        'hosts': hosts,
    }
    return render(request, app_url + 'search.html', context=context)


def get_tournaments(request, host):
    if not request.is_ajax():
        raise Http404('Not found')

    tournaments = Tournament.objects.filter(author_id=host)
    t_list = []
    for tournament in tournaments:
        t_list.append({'id': tournament.id, 'display': tournament.display_name, 'full': tournament.name})
    t_dic = {
        'tournaments': t_list,
    }
    return HttpResponse(json.dumps(t_dic), content_type='application/json')


def get_matches(request, tournament):
    if not request.is_ajax():
        raise Http404('Not found')

    match_list = [match for match in Rank.objects.filter(tournament_id=tournament).values_list('match_number', flat=True).distinct().order_by('-match_number')]

    ret = {
        'match_list': match_list,
    }
    return HttpResponse(json.dumps(ret), content_type='application/json')


class RankView(ListView):
    extra_context = dict()
    extra_context['title'] = 'Rank table'
    template_name = app_url + 'rank.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(RankView, self).get_context_data(**kwargs)
        try:
            tournament = Tournament.objects.get(id=self.kwargs["tournament_id"])
        except Exception:
            raise Http404("This page is unavailable")

        context['tournament'] = tournament
        if Rank.objects.filter(tournament_id=self.kwargs["tournament_id"],
                               match_number__lt=self.kwargs['match_number']).count() > 0:
            have_prev_match = True
            context['prev_match_no'] = Rank.objects.filter(tournament_id=self.kwargs["tournament_id"],
                                                           match_number__lt=self.kwargs['match_number']).aggregate(
                                                            Max('match_number'))['match_number__max']
        else:
            have_prev_match = False
        if Rank.objects.filter(tournament_id=self.kwargs["tournament_id"],
                               match_number__gt=self.kwargs['match_number']).count() > 0:
            have_next_match = True
            context['next_match_no'] = Rank.objects.filter(tournament_id=self.kwargs["tournament_id"],
                                                           match_number__gt=self.kwargs['match_number']).aggregate(
                                                            Min('match_number'))['match_number__min']
        else:
            have_next_match = False
        if have_prev_match or have_next_match:
            have_other_match = True
        else:
            have_other_match = False

        max_match_no = Rank.objects.filter(tournament_id=self.kwargs["tournament_id"]).values_list('tournament', 'match_number').distinct().aggregate(Max('match_number'))['match_number__max']

        context['match_number_max'] = max_match_no
        context['match_number'] = self.kwargs['match_number']
        context['have_prev_match'] = have_prev_match
        context['have_next_match'] = have_next_match
        context['have_other_match'] = have_other_match
        return context

    def get_queryset(self):
        actual_rank_qs = Rank.objects.filter(tournament_id=self.kwargs['tournament_id'], match_number=self.kwargs['match_number']).order_by('-gross_total_pts')

        return actual_rank_qs
