
from django.contrib import admin
from django.urls import path, include

from user.views import signup, login_view
from user.views import home, logout_view
urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('signup/', signup, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('user/', include('user.urls'))
]
