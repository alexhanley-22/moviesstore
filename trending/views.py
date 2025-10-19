from django.shortcuts import render
from django.http import JsonResponse
from cart.models import Order
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from cart.models import Order  # adjust if your Order model is elsewhere
from collections import defaultdict

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



@login_required
@login_required
def order_locations_api(request):
    user = request.user
    orders = Order.objects.filter(user=user)  # only show the logged-in user's orders

    location_groups = {}
    for o in orders:
        if o.latitude and o.longitude:  # ✅ correct field names
            key = (round(o.latitude, 3), round(o.longitude, 3), o.state)
            if key not in location_groups:
                location_groups[key] = []
            location_groups[key].append({
                'total': float(o.total),
                'date': o.date.strftime('%Y-%m-%d %H:%M')
            })

    data = []
    for (lat, lng, state), order_list in location_groups.items():
        data.append({
            'lat': lat,
            'lng': lng,
            'state': state,
            'count': len(order_list),
            'orders': order_list
        })

    return JsonResponse(data, safe=False)