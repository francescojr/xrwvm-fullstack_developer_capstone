from django.urls import path
from . import views

from django.views.generic import TemplateView

app_name = 'djangoapp'

urlpatterns = [
    # Página principal
    path('', views.get_dealerships, name='index'),
    
    # API de autenticação
    path('login/', views.login_user, name='login_api'),
    path('logout/', views.logout_request, name='logout_api'),
    path('register/', views.registration, name='register_api'),  # ✅ Rota de registro
    path('get_current_user/', views.get_current_user, name='get_current_user'),
    path(route='get_cars', view=views.get_cars, name ='getcars'),
    path('populate/', views.populate_database, name='populate_database'),
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),
    path(route='add_review', view=views.add_review, name='add_review'),
    path(route='get_dealers/', view=views.get_dealerships, name='get_dealers'),
    # path('register/', TemplateView.as_view(template_name="index.html")),
    
    # Outras rotas (implementar depois)
    # path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    # path('dealer/<int:dealer_id>/reviews/', views.get_dealer_reviews, name='dealer_reviews'),
    # path('add_review/', views.add_review, name='add_review'),
]
