from django.shortcuts import render
from django.http import JsonResponse
from cart.models import Order, Item
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from movies.models import Movie
from collections import defaultdict, Counter

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

    user = request.user if request.user.is_authenticated else None
    recent_purchases = []
    if user:
        orders_qs = Order.objects.filter(user = user).order_by('-date')[:5]
        for o in orders_qs:
            items = Item.objects.filter(order = o).select_related('movie')
            recent_purchases.append({
                'order': o,
                'items': items
            })
    

    other_users = User.objects.none()
    selected_other_user = None
    other_user_purchases = []
    if user and user.is_authenticated:
        other_users = User.objects.exclude(id = user.id).order_by('username')[:50]
        other_user_id = request.GET.get('other_user')
        if other_user_id:
            try:
                selected_other_user = User.objects.get(id = int(other_user_id))
                orders_qs = Order.objects.filter(user = selected_other_user).order_by('-date')[:5]
                for o in orders_qs:
                    items = Item.objects.filter(order = o).select_related('movie')
                    other_user_purchases.append({
                        'order': o,
                        'items': items
                    })
            except (User.DoesNotExist, ValueError):
                selected_other_user = None


    selected_region = request.GET.get('region')
    region_trending = []
    region_states = {}
    for rname, rdata in regions.items():
        states = []
        for sub in rdata.get('subregions', {}).values():
            states.extend(sub)
        region_states[rname] = states
        
    if selected_region and selected_region in region_states:
        states = region_states[selected_region]
        items_qs = Item.objects.filter(order__state__in=states).select_related('movie')
        movie_counter = Counter()
        for it in items_qs:
            if it.movie:
                movie_counter[it.movie.id] += it.quantity or 1
    
        top = movie_counter.most_common(10)
        movie_ids = [m_id for m_id, _ in top]
        movies = Movie.objects.filter(id__in = movie_ids)

        movies_by_id = {m.id: m for m in movies}
        for m_id, count in top:
            m = movies_by_id.get(m_id)
            if m:
                region_trending.append({
                    'movie': m,
                    'count': count
                })
    
    template_data = {
        'title': 'US Movie Trends Map',
        'regions': regions,
        'recent_purchases': recent_purchases,
        'other_users': other_users,
        'selected_other_user': selected_other_user,
        'other_user_purchases': other_user_purchases,
        'selected_region': selected_region,
        'region_trending': region_trending,
        'region_states': region_states,
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