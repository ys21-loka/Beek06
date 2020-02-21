from django.views.generic import TemplateView

# template view
class HomeView(TemplateView):
    template_name = 'home.html'