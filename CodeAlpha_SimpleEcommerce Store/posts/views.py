from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from users.models import UserProfile
from datetime import datetime

# --------------------------------------------------
# HOME VIEW
# --------------------------------------------------

@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')

    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    context = {
        'posts': posts,
        'profile': profile,
    }
    return render(request, 'posts/home.html', context)


# --------------------------------------------------
# CREATE POST
# --------------------------------------------------

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if content or image:
            Post.objects.create(
                author=request.user,
                content=content,
                image=image
            )
            messages.success(request, 'Post créé avec succès!')
            return redirect('home')
        else:
            messages.error(request, 'Veuillez remplir au moins le texte ou l\'image.')

    return render(request, 'posts/create_post.html')


# --------------------------------------------------
# LIKE POST
# --------------------------------------------------

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return redirect('home')


# --------------------------------------------------
# POST DETAIL
# --------------------------------------------------

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})


# --------------------------------------------------
# ADD COMMENT
# --------------------------------------------------

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
            messages.success(request, 'Commentaire ajouté!')
        else:
            messages.error(request, 'Le commentaire ne peut pas être vide.')

    return redirect('home')


# --------------------------------------------------
# POST LIST
# --------------------------------------------------

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/post_list.html', {'posts': posts})


# --------------------------------------------------
# PROFILE SETTINGS
# --------------------------------------------------

@login_required
def profile_settings(request):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        profile.bio = request.POST.get('bio', profile.bio)
        profile.location = request.POST.get('location', profile.location)
        profile.website = request.POST.get('website', profile.website)
        profile.birth_date = request.POST.get('birth_date', profile.birth_date)
        profile.gender = request.POST.get('gender', profile.gender)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        user.save()
        profile.save()
        messages.success(request, 'Profil mis à jour avec succès!')
        return redirect('profile_settings')

    context = {
        'user': user,
        'profile': profile,
        'birthdate': profile.birth_date.strftime('%Y-%m-%d') if profile.birth_date else ''
    }
    return render(request, 'posts/parametre.html', context)


# --------------------------------------------------
# PROFILE VIEW
# --------------------------------------------------

@login_required
def profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        profile.bio = request.POST.get('bio', profile.bio)
        profile.location = request.POST.get('location', profile.location)
        profile.website = request.POST.get('website', profile.website)
        profile.gender = request.POST.get('gender', profile.gender)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)

        birthdate_str = request.POST.get('birth_date')
        if birthdate_str:
            try:
                profile.birth_date = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Date de naissance invalide.')

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        user.save()
        profile.save()
        messages.success(request, 'Profil mis à jour avec succès!')

        return redirect('profile')

    birthdate_value = profile.birth_date
    if isinstance(birthdate_value, str):
        birthdate_for_input = birthdate_value
    elif birthdate_value:
        birthdate_for_input = birthdate_value.strftime('%Y-%m-%d')
    else:
        birthdate_for_input = ''

    context = {
        'user': user,
        'profile': profile,
        'birthdate': birthdate_for_input
    }
    return render(request, 'posts/profile.html', context)
