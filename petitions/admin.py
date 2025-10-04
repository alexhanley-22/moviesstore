from django.contrib import admin
from .models import Petition, Vote

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie_title', 'movie_year', 'created_by', 'created_at', 'vote_count', 'is_approved')
    list_filter = ('created_at', 'is_approved', 'movie_year')
    search_fields = ('title', 'movie_title', 'description')
    readonly_fields = ('created_at', 'vote_count', 'total_votes')
    
    def vote_count(self, obj):
        return obj.vote_count
    vote_count.short_description = 'Yes Votes'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'petition', 'vote_type', 'created_at')
    list_filter = ('vote_type', 'created_at')
    search_fields = ('user__username', 'petition__title')