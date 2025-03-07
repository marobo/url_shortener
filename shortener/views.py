from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
import os
from .models import ShortURL
from .forms import URLShortenerForm


def home(request):
    if request.method == 'POST':
        form = URLShortenerForm(request.POST)
        if form.is_valid():
            url = form.save()
            return render(request, 'shortener/result.html', {'url': url})
    else:
        form = URLShortenerForm()
    return render(request, 'shortener/home.html', {'form': form})


def redirect_to_url(request, short_code):
    try:
        short_url = get_object_or_404(ShortURL, short_code=short_code)
        short_url.visits += 1
        short_url.redirect_count += 1
        short_url.save()
        return redirect(short_url.current_url)
    except Http404:
        return render(request, 'shortener/404.html', status=404)


def url_list(request):
    urls = ShortURL.objects.all().order_by('-created_at')
    return render(request, 'shortener/url_list.html', {'urls': urls})


def update_url(request, short_code):
    if request.method == 'POST':
        short_url = get_object_or_404(ShortURL, short_code=short_code)
        new_url = request.POST.get('new_url')
        if new_url:
            short_url.update_url(new_url)
            return redirect('shortener:url_list')
    return render(request, 'shortener/404.html', status=404)


def delete_url(request, short_code):
    if request.method == 'POST':
        short_url = get_object_or_404(ShortURL, short_code=short_code)
        # Delete the QR code image file
        if short_url.qr_code:
            qr_code_path = short_url.qr_code.path
            if os.path.exists(qr_code_path):
                os.remove(qr_code_path)
        # Delete the database record
        short_url.delete()
        return redirect('shortener:url_list')
    return render(request, 'shortener/404.html', status=404)
