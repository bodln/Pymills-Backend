from django.urls import path
from pymills.views import OK, maps_list, get_move

urlpatterns = [
    path('', OK),
    path('maps/', maps_list, name='maps'),
    path('calculatemove/', get_move, name='calculatemove')
]
