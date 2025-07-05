from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Follow
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # connexion automatique après inscription
            return redirect('home')  # redirige vers la page principale
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def follow_user(request, user_id):
    target = get_object_or_404(User, id=user_id)

    if request.user == target:
        messages.error(request, "Tu ne peux pas t'abonner à toi-même.")
    else:
        Follow.objects.get_or_create(follower=request.user, following=target)
        messages.success(request, f"Tu t'es abonné à {target.username}.")

    return redirect('home')



@login_required
def unfollow_user(request, user_id):
    if request.method == 'POST':
        to_unfollow = get_object_or_404(User, id=user_id)
        request.user.following.filter(following=to_unfollow).delete()
        # Redirection après l'action
        return redirect('home')  # Ou autre URL valide
    else:
        # Si la méthode n'est pas POST, rediriger aussi (ou gérer autrement)
        return redirect('home')
    
@login_required
def profile_view(request):
    user = request.user
    followers_count = user.followers.count()
    following_count = user.following.count()
    posts_count = user.posts.count()  # si tu as la relation définie dans Post

    context = {
        'user': user,
        'followers_count': followers_count,
        'following_count': following_count,
        'posts_count': posts_count,
        # autres variables
    }
    return render(request, 'posts/profile.html', context)
