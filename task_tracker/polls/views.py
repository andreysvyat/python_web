from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest):
    headers = [f'<p>{key}: {value}</p>'for key, value in request.headers.items()]
    return HttpResponse(f'Hello from my first view<br></br>your headers: {"".join(headers)}')
