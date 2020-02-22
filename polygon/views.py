from django.shortcuts import render

from assignment.views import AssignmentListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin


# Create your views here.
def polygon_home(request):
    user = request.user
    ctx = {}

    return render(request, 'polygon/home.jinja2', context=ctx)


class PolygonBaseMixin(UserPassesTestMixin):

  def test_func(self):
    return self.request.user.is_authenticated and self.request.user.polygon_enabled





class PolygonAssigmentListView(AssignmentListView):
    template_name = 'polygon/assignment/list.jinja2'



