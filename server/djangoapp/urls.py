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
    # path('register/', TemplateView.as_view(template_name="index.html")),
    
    # Outras rotas (implementar depois)
    # path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    # path('dealer/<int:dealer_id>/reviews/', views.get_dealer_reviews, name='dealer_reviews'),
    # path('add_review/', views.add_review, name='add_review'),
]
