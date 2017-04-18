import json

from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Q

from .forms import LoginForm


class CoreIndexView(TemplateView):
    template_name = 'index.html'


class SiteMapView(TemplateView):
    template_name = 'sitemap.xml'


class SearchMixin(object):

    def get_queryset(self, fields):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            # make a empty QuerySet.
            results = self.model.objects.none()

            for field in fields:
                # trick
                query_dict = {'__'.join([field, 'icontains']): q}

                results = results | queryset.filter(**query_dict)
            return results
        return queryset

class LoginFormMixin(object):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = LoginForm
        return context


class TitleSearchMixin(SearchMixin):

    def get_queryset(self):
        queryset = super().get_queryset(['title',])
        return queryset


class JsonResponseMixin(object):

    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(self.get_data(context), **response_kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        return self.render_to_json_response(context)

    def get_data(self, context):
        # returns a data to be json-serizlized.
        return {}
