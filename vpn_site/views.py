from django.http import HttpResponse, HttpResponseNotFound
from django.db.models import F
from bs4 import BeautifulSoup
import requests
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .utils import *


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')  
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
  

def register_view(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('profile')  
    else:
        form = CustomRegistrationForm()
    return render(request, 'register.html', {'form': form})


def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileUpdateForm(instance=user)
    return render(request, 'profile/edit_profile.html', {'user': user, 'form': form})


def sites_view(request):
    if request.method == 'POST':
        form = CreateWebsiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('statistics')
    form = CreateWebsiteForm()
    return render(request, 'sites.html', {'form': form})


def stats_view(request):
    sites = Website.objects.filter(user=request.user)
    return render(request, 'profile/statistics.html', {'sites': sites})


def update_user_statistics(request, website, route, data_sent, data_downloaded):
    user = request.user
    statistics, created = VPNUserStatistics.objects.get_or_create(user=user, site=website)

    VPNUserStatistics.objects.filter(pk=statistics.pk).update(
        pages_count=F('pages_count') + 1,
        size_data_sent=F('size_data_sent') + data_sent,
        size_data_downloaded=F('size_data_downloaded') + data_downloaded
    )


def proxy_view(request, site_name, route):
    try:
        website = Website.objects.get(site_name=site_name)
    except Website.DoesNotExist:
        return HttpResponseNotFound("Website not found")

    url = website.site_link + route

    http_proxy = "http://localhost:8000"
    proxies = {
        "http": http_proxy,
    }

    s = requests.Session()
    s.proxies = proxies
    r = s.get(url)

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')

        data_sent = len(str(soup))
        data_downloaded = r.headers.get('Content-Length', 0)

        update_user_statistics(request, website, route, data_sent, data_downloaded)

        for link in soup.find_all('a', href=True):
            link_website = extract_website_name(link['href']) 
            domain_index = link['href'].find(link_website)
            link['href'] = f"http://localhost/{site_name}{link['href'][domain_index + len(link_website):]}"

        return HttpResponse(str(soup), content_type=r.headers['Content-Type'])
    return HttpResponse(f"Error: {r.status_code}", status=r.status_code)