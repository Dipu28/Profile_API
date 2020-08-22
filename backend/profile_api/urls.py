from django.urls import path, include
from rest_framework.routers import DefaultRouter

from profile_api import views

# To use routers we have to assign it to variable:
router = DefaultRouter()
router.register('hello-viewset',views.HelloViewSet,basename='hello-viewset')
# We don't have to asign the basename beacuse the queryset will do the work(we can override it by using base)
router.register('profile',views.UserProfileViewSet)
router.register('feed',views.UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/',views.HelloApiView.as_view(),name="hello_view"),
    path('login/',views.UserLoginApiView.as_view(),name="login"),
    path('',include(router.urls)),
]
