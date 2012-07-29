from django import forms
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from feed.views import getAllFeeds
from mongoengine.django.auth import User

class EmailAuthBackend(object):
    """
    Authenticate using email and password with mongoengine.django.auth.User.
    """

    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, email=None, password=None):
        user = User.objects(email=email).first()
        if user:
            if password and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        return User.objects.with_id(user_id)


class UserSignupForm(forms.Form):

    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    email = forms.EmailField(label=_("Email"),
        widget=forms.TextInput(attrs={'placeholder':'Email', 'data-mini':'true'}))
    username = forms.CharField(label=_("Username"), max_length=30,
        help_text=_("Required. 30 characters or fewer."),
        widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'placeholder':'Password confirmation'}),
        help_text=_("Enter the same password as above, for verification."))

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self):
        user = User.create_user(username=self.cleaned_data["username"], email=self.cleaned_data["email"], password=self.cleaned_data["password1"])
        
        return user

class UserLoginForm(forms.Form):

    error_messages = {
        'invalid_email': _("A user with that email does not exists."),
        'invalid_password': _("email and password are invalid."),
    }
    user = None
    email = forms.EmailField(label=_("Email"), 
        widget=forms.TextInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={'placeholder':'password'}))

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(self.error_messages['invalid_email'])
        return email
        
    
    def clean_password(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data.get("email", "")
        password = self.cleaned_data["password"]
        self.user = auth.authenticate(email=email, password=password)
        if self.user is not None and self.user.is_active:
            return password
        raise forms.ValidationError(self.error_messages['invalid_password'])


def home(request):
    try:
        return getAllFeeds(request)
    except:
        return render_to_response('home.html', context_instance=RequestContext(request))

def signup(request):    
    if request.method == 'POST':
        form = UserSignupForm(request.POST, auto_id="form_signup_%s")
        if form.is_valid():
            user = form.save()
            user = auth.authenticate(username=user.username, password=request.POST.get('password1'))
            auth.login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = UserSignupForm(auto_id="form_signup_%s")
    
    return render_to_response("signup.html", {
        'form': form,
    }, context_instance=RequestContext(request))

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST, auto_id="form_login_%s")
        if form.is_valid():
            auth.login(request, form.user)
            return HttpResponseRedirect("/")
    else:
        form = UserLoginForm(auto_id="form_login_%s")
    
    return render_to_response("login.html", {
        'form': form,
    }, context_instance=RequestContext(request))
