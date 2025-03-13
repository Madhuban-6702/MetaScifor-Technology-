from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator


def landing(request):
    return render(request, 'landing.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')
        password2 = request.POST.get('confirm_password')

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        # Create user
        user = CustomUser.objects.create_user(
            username=username, 
            email=email, 
            password=password, 
            full_name=full_name,
            phone_number=phone_number
        )
        login(request, user)
        return redirect('login')  

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')  # Redirect to profile page after login
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def main(request):
    query = request.GET.get('q', '')
    
    if query:
        animes = Anime.objects.filter(
            Q(name__icontains=query) |
            Q(genres__icontains=query) |
            Q(type__icontains=query)
        )
    else:
        animes = Anime.objects.all()

    for anime in animes:  # Optimized this loop
        print(f"Anime ID: {anime.anime_id}, Name: {anime.name}")
    paginator = Paginator(animes, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'main.html', {
        'page_obj': page_obj,
        'query': query
    })



@login_required
def anime_detail(request, anime_id):
    anime = get_object_or_404(Anime, anime_id=anime_id)

    # Split genres into a list
    genres_list = anime.genres.split(',') if anime.genres else []

    return render(request, 'details.html', {
        'anime': anime,
        'genres_list': genres_list,  # Pass the split genres
    })
    
    
@login_required
def add_to_watchlist(request, anime_id):
    anime = Anime.objects.get(anime_id=anime_id)
    user_watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    if anime not in user_watchlist.animes.all():
        user_watchlist.animes.add(anime)
        messages.success(request, f'"{anime.name}" has been added to your watchlist!')
    else:
        messages.info(request, f'"{anime.name}" is already in your watchlist.')
    return redirect('main')


@login_required
def watchlist_page(request):
    user = request.user
    watchlist = Anime.objects.filter(watchlist__user=user)
    return render(request, 'watchlist.html', {'watchlist': watchlist})


@login_required
def remove_from_watchlist(request, anime_id):
    anime = Anime.objects.get(anime_id=anime_id)  # Fixed field name
    user_watchlist, created = Watchlist.objects.get_or_create(user=request.user)

    if anime in user_watchlist.animes.all():
        user_watchlist.animes.remove(anime)
        messages.success(request, f'"{anime.name}" has been removed from your watchlist.')
    else:
        messages.info(request, f'"{anime.name}" is not in your watchlist.')
    return redirect('main')


@login_required
def recommendation_page(request):
    if request.method == 'POST':
        genre = request.POST.get('genre', '').strip()  # Ensure genre is not None
        rating = request.POST.get('rating', '').strip()  # Ensure rating is not None
        num_recommendations = request.POST.get('num_recommendations', 5)

        try:
            num_recommendations = int(num_recommendations)  # Convert safely
        except ValueError:
            num_recommendations = 5  # Default if invalid input

        # Initialize query
        query = Anime.objects.filter(genres__icontains=genre) if genre else Anime.objects.all()

        # Apply rating filter if rating is provided and valid
        if rating:
            try:
                rating = float(rating)
                query = query.filter(score__gte=rating)  # Use score instead of rating
            except ValueError:
                rating = None  # Ignore rating if conversion fails

        # Order by 'members' and limit results
        recommended_animes = query.order_by('-members')[:num_recommendations]

        return render(request, 'recommendations.html', {
            'recommended_animes': recommended_animes,
            'genre': genre,
            'rating': rating,
            'num_recommendations': num_recommendations
        })

    return render(request, 'recommendations_form.html')


@login_required
def profile(request):
    # This is where we fetch the user data to display in the profile page
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST['username']
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone_number = request.POST['phone']

        # Check if the new username already exists (excluding the current user)
        if CustomUser.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, "Username is already taken. Please choose another.")
            return redirect('profile')

        # Check if the new email already exists (excluding the current user)
        if CustomUser.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, "Email is already registered. Please use another.")
            return redirect('profile')

        # Split full_name into first_name and last_name safely
        name_parts = full_name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Update user details
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone = phone_number  # Ensure your CustomUser model has a `phone` field

        try:
            user.save()
            messages.success(request, "Profile updated successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('profile')

    return render(request, 'profile.html')