from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("movies:movie_list")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


from django.shortcuts import render

# Create your views here.
