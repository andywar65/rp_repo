from django.urls import path
from .views import (FrontLoginView, FrontLogoutView, FrontPasswordResetView,
    TemplateResetView, FrontPasswordResetConfirmView, TemplateResetDoneView,
    TemplateAccountView, FrontPasswordChangeView, FrontPasswordChangeDoneView,
    ProfileChangeView, ProfileDeleteView, TemplateDeletedView,
    ProfileChangeRegistryView, ProfileChangeAddressView, ProfileChangeCourseView,
    ProfileChangeNoCourseView, ProfileAddChildView, )

#namespace is '/accounts/'
urlpatterns = [
    path('profile/', TemplateAccountView.as_view(),
        name='profile'),
    path('profile/<int:pk>/change/', ProfileChangeView.as_view(),
        name='profile_change'),
    path('profile/<int:pk>/change/registry', ProfileChangeRegistryView.as_view(),
        name='profile_change_registry'),
    path('profile/<int:pk>/change/address', ProfileChangeAddressView.as_view(),
        name='profile_change_address'),
    path('profile/<int:pk>/change/course', ProfileChangeCourseView.as_view(),
        name='profile_change_course'),
    path('profile/<int:pk>/change/no_course', ProfileChangeNoCourseView.as_view(),
        name='profile_change_no_course'),
    path('profile/add_child', ProfileAddChildView.as_view(),
        name='profile_add_child'),
    path('profile/<int:pk>/delete', ProfileDeleteView.as_view(),
        name='profile_delete'),
    path('profile/deleted', TemplateDeletedView.as_view(),
        name='profile_deleted'),
    path('login/', FrontLoginView.as_view(),
        name='front_login'),
    path('logout/', FrontLogoutView.as_view(),
        name='front_logout'),
    path('password_reset/', FrontPasswordResetView.as_view(),
        name='front_password_reset'),
    path('password_reset/done/', TemplateResetView.as_view(),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', FrontPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path('reset/done/', TemplateResetDoneView.as_view(),
        name='password_reset_complete'),
    path('password_change/', FrontPasswordChangeView.as_view(),
        name='password_change'),
    path('password_change_done/', FrontPasswordChangeDoneView.as_view(),
        name='password_change_done'),
    ]
