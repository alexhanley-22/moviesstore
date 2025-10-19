from django.shortcuts import render
from django.http import JsonResponse
from cart.models import Order

def us_trending_map(request):
    """Display US map with location services and regional data"""
    
    # US Regions with their states
    regions = {
        'Northeast': {
            'color': '#FF6B6B',
            'subregions': {
                'New England': ['Maine', 'New Hampshire', 'Vermont', 'Massachusetts', 'Rhode Island', 'Connecticut'],
                'Middle Atlantic': ['New York', 'New Jersey', 'Pennsylvania']
            }
        },
        'Midwest': {
            'color': '#4ECDC4',
            'subregions': {
                'East North Central': ['Ohio', 'Indiana', 'Illinois', 'Michigan', 'Wisconsin'],
                'West North Central': ['Minnesota', 'Iowa', 'Missouri', 'North Dakota', 'South Dakota', 'Nebraska', 'Kansas']
            }
        },
        'South': {
            'color': '#45B7D1',
            'subregions': {
                'South Atlantic': ['Delaware', 'Maryland', 'District of Columbia', 'Virginia', 'West Virginia', 'North Carolina', 'South Carolina', 'Georgia', 'Florida'],
                'East South Central': ['Kentucky', 'Tennessee', 'Mississippi', 'Alabama'],
                'West South Central': ['Oklahoma', 'Texas', 'Arkansas', 'Louisiana']
            }
        },
        'West': {
            'color': '#96CEB4',
            'subregions': {
                'Mountain': ['Montana', 'Idaho', 'Wyoming', 'Nevada', 'Utah', 'Colorado', 'Arizona', 'New Mexico'],
                'Pacific': ['Alaska', 'Washington', 'Oregon', 'California', 'Hawaii']
            }
        }
    }
    
    template_data = {
        'title': 'US Movie Trends Map',
        'regions': regions
    }
    
    return render(request, 'trending/us_map.html', {'template_data': template_data})



def order_locations_api(request):
    """Return recent orders with location data for map plotting"""
    orders = Order.objects.exclude(latitude=None).order_by('-date')[:100]
    data = [
        {
            'lat': o.latitude,
            'lng': o.longitude,
            'state': o.state,
            'user': o.user.username,
            'total': o.total,
            'date': o.date.strftime('%Y-%m-%d %H:%M')
        }
        for o in orders
    ]
    return JsonResponse(data, safe=False)