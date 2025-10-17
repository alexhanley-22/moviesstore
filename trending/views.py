from django.shortcuts import render

def us_trending_map(request):
    """Display US map with location services"""
    
    template_data = {
        'title': 'US Movie Trends Map'
    }
    
    return render(request, 'trending/us_map.html', {'template_data': template_data})