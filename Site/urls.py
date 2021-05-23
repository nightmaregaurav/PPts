from django.urls import path

from .views import search, RankView, get_tournaments, get_matches

app_name = 'Site'
urlpatterns = [
    path('', search, name='home'),
    path('search', search, name='search'),
    path('get-tournaments/<int:host>', get_tournaments, name='get-tournaments'),
    path('get-matches/<int:tournament>', get_matches, name='get-matches'),
    path('<int:tournament_id>/<int:match_number>', RankView.as_view(), name='rank'),
]
