from django.shortcuts import render
from .models import Comment
import json
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

# Create your views here.
def _parse_data(request):
    if request.META.get('CONTENT_TYPE', '').startswith('application/json'):
        try:
            return json.loads(request.body.decode('utf-8')) if request.body else {}
        except json.JSONDecodeError:
            return {}
    return request.POST.dict()

def _editable_field_names():
    return [f.attname for f in Comment._meta.concrete_fields if f.editable and not f.auto_created]

@require_http_methods(['POST'])
def comment_create(request, post_id):
    data = _parse_data(request)
    obj = Comment()
    obj.post = post_id
    for name in _editable_field_names():
        if name == 'post_id':
            continue
        if name in data:
            setattr(obj, name, data[name])
    obj.save()
    return JsonResponse(model_to_dict(obj), status=201)

@require_http_methods(['GET'])
def comment_detail(request, pk):
    obj = get_object_or_404(Comment, pk=pk)
    return JsonResponse(model_to_dict(obj))

@require_http_methods(['PUT', 'POST'])
def comment_update(request, pk):
    obj = get_object_or_404(Comment, pk=pk)
    data = _parse_data(request)
    updated = False
    for name in _editable_field_names():
        if name in data:
            setattr(obj, name, data[name])
            updated = True
    if not updated:
        return HttpResponse(status=204)
    obj.save()
    return JsonResponse(model_to_dict(obj))

@require_http_methods(['DELETE', 'POST'])
def comment_delete(request, pk):
    obj = get_object_or_404(Comment, pk=pk)
    obj.delete()
    return HttpResponse(status=204)