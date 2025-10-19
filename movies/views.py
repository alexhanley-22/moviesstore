from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})
def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)

    template_data = {
        'title': movie.name,
        'movie': movie,
        'reviews': reviews,
        # ✅ Include average rating
        'average_rating': movie.average_rating(),
    }

    return render(request, 'movies/show.html', {'template_data': template_data})
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '': 
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def create_review(request, id):
    movie = get_object_or_404(Movie, id=id)

    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()
        rating = request.POST.get('rating', 0)

        if not comment:
            messages.warning(request, "Please enter a comment before submitting.")
            return redirect('movies.show', id=id)

        # ✅ Check if user already has a review for this movie
        existing_review = Review.objects.filter(movie=movie, user=request.user).first()

        if existing_review:
            # Update the existing review instead of inserting duplicate
            existing_review.comment = comment
            existing_review.rating = rating
            existing_review.save()
            messages.success(request, "Your review has been updated!")
        else:
            # Create a new review
            Review.objects.create(
                comment=comment,
                rating=rating,
                movie=movie,
                user=request.user
            )
            messages.success(request, "Your review has been added!")

    return redirect('movies.show', id=id)
def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')