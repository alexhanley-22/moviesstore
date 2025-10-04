from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Petition, Vote

def index(request):
    """Display all petitions with vote counts"""
    petitions = Petition.objects.annotate(
        yes_votes=Count('votes', filter=Q(votes__vote_type='yes'))
    ).order_by('-created_at')
    
    template_data = {
        'title': 'Movie Petitions',
        'petitions': petitions
    }
    return render(request, 'petitions/index.html', {'template_data': template_data})

@login_required
def create(request):
    """Create a new petition"""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        movie_title = request.POST.get('movie_title', '').strip()
        movie_year = request.POST.get('movie_year', '').strip()
        
        if not all([title, description, movie_title]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'petitions/create.html', {
                'template_data': {'title': 'Create Petition'}
            })
        
        petition = Petition.objects.create(
            title=title,
            description=description,
            movie_title=movie_title,
            movie_year=int(movie_year) if movie_year else None,
            created_by=request.user
        )
        
        messages.success(request, 'Petition created successfully!')
        return redirect('petitions.index')
    
    template_data = {'title': 'Create Petition'}
    return render(request, 'petitions/create.html', {'template_data': template_data})

@login_required
def vote(request, petition_id):
    """Vote on a petition"""
    petition = get_object_or_404(Petition, id=petition_id)
    vote_type = request.POST.get('vote_type')
    
    if vote_type not in ['yes', 'no']:
        messages.error(request, 'Invalid vote type.')
        return redirect('petitions.index')
    
    # Check if user already voted
    existing_vote = Vote.objects.filter(petition=petition, user=request.user).first()
    
    if existing_vote:
        if existing_vote.vote_type == vote_type:
            messages.info(request, 'You have already voted the same way on this petition.')
        else:
            existing_vote.vote_type = vote_type
            existing_vote.save()
            messages.success(request, f'Your vote has been updated to {vote_type}.')
    else:
        Vote.objects.create(
            petition=petition,
            user=request.user,
            vote_type=vote_type
        )
        messages.success(request, f'Your {vote_type} vote has been recorded.')
    
    return redirect('petitions.index')

@login_required
def detail(request, petition_id):
    """View petition details"""
    petition = get_object_or_404(Petition, id=petition_id)
    user_vote = None
    if request.user.is_authenticated:
        user_vote = Vote.objects.filter(petition=petition, user=request.user).first()
    
    template_data = {
        'title': petition.title,
        'petition': petition,
        'user_vote': user_vote
    }
    return render(request, 'petitions/detail.html', {'template_data': template_data})