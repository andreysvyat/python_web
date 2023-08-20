from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import now


def autoescape(req):
    return HttpResponse(render(req, 'autoescape.html',
                               context={"value": "<h1>Html header with signs &lt; &gt; &#x27; &quot; &amp;</h1>"}))


def repeatable(req):
    names = req.GET.getlist("names")
    return HttpResponse(render(req, "repeatable.html", {"names": names}))


FILTERS_CONTEXT = {
    "name": "andrey",
    "surname": "svyatogorov",
    "to_lower": "CAPITALIZED STRING",
    "to_upper": "lowercase string",
    "now": now()
}


def filters(req):
    context = {"context": FILTERS_CONTEXT}
    context.update(FILTERS_CONTEXT)
    return HttpResponse(render(req, "filters.html", context))
