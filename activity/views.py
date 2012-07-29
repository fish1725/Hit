from activity.models import Activity
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from feed.models import Feed
from mongoengine.django.auth import User

@login_required
def plan(request):
    act = Activity()
    act.participants = selectUser(request.user)
    act.num_participants = 2
    act.save()
    for u in act.participants:
        feed = Feed(user=u, content=act)
        feed.save()
    return HttpResponse("ok")
    
    
def selectUser(founder=None):
    users = list(User.objects(username="1"))
    if founder and founder.username != "1":
        users.append(founder)
    return users
