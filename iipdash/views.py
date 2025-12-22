from django.contrib import admin
from django.views.generic import TemplateView


class AdminView(TemplateView):
    title = ""

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context.update(
            {
                **admin.site.each_context(self.request),
                "title": self.title,
            }
        )

        return context
