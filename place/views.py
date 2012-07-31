# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from mongoengine.queryset import Q
from place.models import Place, Type
import httplib
import json

def claw(query):    
    conn = httplib.HTTPSConnection("maps.googleapis.com")    
    places = set()
    search = "textsearch"
    if 'search' in query: 
        search = query['search']
    else:
        if 'query' in query:
            search = "textsearch"
        else:
            search = "search"
    para = "/maps/api/place/" + search + "/json?&language=zh-CN&sensor=false&key=AIzaSyDj5SWT2itXCNvgK0z3QZRF7pmi9erViFQ"
    for q in query:
        para += "&" + q + "=" + query[q]
    conn.request("GET", para)
    res = conn.getresponse()
    if res.status == 200:
        data = json.loads(res.read())
        if data.get('status') == "OK" or data.get('status') == "ZERO_RESULTS":
            for rp in data.get('results'):
                place, created = Place.objects.get_or_create(google_place_id=rp.get('id'))
                if created:
                    place.update(set__location=[rp.get('geometry')['location']['lat'], rp.get('geometry')['location']['lng']],
                                                    set__address=rp.get('formatted_address', rp.get('vicinity')),
                                                    set__name=rp.get('name'), set__types=rp.get('types'))
                    place.reload()
                updateType(place)
                places.add(place)
            if data.get('next_page_token'):
                places = places.union(claw({"pagetoken":data.get('next_page_token'), "search":search}))
        else:
            raise Exception('GOOGLE_PLACE_ERROR_' + data.get('status'), para)
    return places

def search(request):
    if request.method == "GET":
        query = request.GET.get("q", "")
        flag = False
        places = Place.objects(Q(name__iexact=query))# | Q(address__icontains=query))
        if places.first() == None:
            places = set(list(Place.objects(Q(name__icontains=query))))
            if len(places) < 20:
                places = places.union(claw({"query":query}))
                flag = True
            
    return render_to_response('search.html', {'places': places, 'flag': flag}, context_instance=RequestContext(request))

def home(request):
    if request.method == "GET":
        place = Place.objects.first()
        updateType(place)
    return render_to_response('place.html', {'place': place}, context_instance=RequestContext(request))
        
    
def profile(request, pid=None):
    if request.method == "GET":
        place = Place.objects.get(id=pid)
        updateType(place)
        places = claw({"location":str(place.location[0]) + "," + str(place.location[1]), "rankby": 'distance', 'types':'establishment'})
    return render_to_response('place.html', {'place': place, 'places':places}, context_instance=RequestContext(request))
        
        
def updateType(place):
    for ty in place.types:
        t, created = Type.objects.get_or_create(name=ty)
