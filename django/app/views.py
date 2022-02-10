from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "application.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
