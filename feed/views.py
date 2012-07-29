# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from feed.models import Feed

@login_required
def getAllFeeds(request):
    feeds = Feed.objects(user=request.user)
    #data = serializers.serialize("json", feeds)
    return render_to_response('home.html', {'feeds': feeds}, context_instance=RequestContext(request))
    