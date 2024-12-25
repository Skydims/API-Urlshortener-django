from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ShortenedURL
from .utils import generate_short_code

def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        short_code = generate_short_code()

        # Simpan URL asli dan kode pendek di database
        shortened_url = ShortenedURL.objects.create(original_url=original_url, short_code=short_code)
        shortened_url.save()

        short_url = request.build_absolute_uri('/') + short_code
        return render(request, 'shortener/result.html', {'short_url': short_url})

    return render(request, 'shortener/home.html')

def redirect_url(request, short_code):
    try:
        shortened_url = ShortenedURL.objects.get(short_code=short_code)
        return redirect(shortened_url.original_url)
    except ShortenedURL.DoesNotExist:
        return HttpResponse("URL not found", status=404)
