from django.http import HttpResponse, HttpRequest


def show_headers(request: HttpRequest):
    headers = [f'<br>&emsp;{key}: {value}'for key, value in request.headers.items()]
    return HttpResponse(f'Hello from my first view<br>Headers in from your request: {"".join(headers)}')
