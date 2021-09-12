from django.shortcuts import redirect, render


def user_handle(request):
    if request.user.user_type == "staff":
        return render(request, "")
