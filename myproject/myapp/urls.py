from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home_page'),
    path('home2/', home2, name='home2_page'),
    path('home3/', home3, name='home3_page'),
    path('aboutus/', aboutUs, name='about_page'),
    path('contact/', contact, name='contact_page'),
    path('addinfo/', addInfo, name='addinfo_page'),
    path('showcontact/', showContact, name='showcontact_page'),
    path("register/", userRegister, name='register_page'),
    path("profile/", userProfile, name="profile_page"),
    path('editprofile/', editProfile, name="editprofile_page"),
    path('action/<int:cid>/', actionPage, name="action_page"),
    path('gamedetail/<str:type>/<int:cid>/', gameDetailPage, name="gamedetail_page"),
    path('crud/', CrudView.as_view(), name='crud_ajax'),
    path('ajax/crud/create/', CreateCrudUser.as_view(), name='crud_ajax_create'),
    path('ajax/crud/delete/', DeleteCrudUser.as_view(), name='crud_ajax_delete'),
    path('ajax/crud/update/', UpdateCrudUser.as_view(), name='crud_ajax_update'),

]