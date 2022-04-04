from django.urls import path

from .views import ImageFormView, ImageDetail

urlpatterns = [
    path('image/add/', ImageFormView.as_view(), name='add'),
    path('image/<slug:lbry_id>/', ImageDetail.as_view(), name='detail'),
]