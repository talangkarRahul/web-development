
from django.contrib import admin
from django.urls import path

from user.views import signup, login_view
from user.views import home, logout_view
urlpatterns = [
    path('home/', home),
    path('admin/', admin.site.urls),
    path('signup/', signup),
    path('login/', login_view),
    path('logout/', logout_view, name="logout")
]
