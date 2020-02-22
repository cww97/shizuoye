from polygon.views import PolygonBaseMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateResponseMixin, ContextMixin
from course.models import Course
from course.views import CourseListView


class PolygonCourseListView(PolygonBaseMixin, CourseListView):
    template_name = 'polygon/course/list.jinja2'


class PolygonCourseMixin(TemplateResponseMixin, ContextMixin, PolygonBaseMixin):
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, pk=kwargs.get('pk'))
        return super(PolygonCourseMixin, self).dispatch(request, *args, **kwargs)

    def test_func(self):
        if not is_course_manager(self.request.user, self.contest):
            return False
        return super(PolygonCourseMixin, self).test_func()

    def get_context_data(self, **kwargs):
        data = super(PolygonCourseMixin, self).get_context_data(**kwargs)
        data['course'] = self.course
        return data


class CourseEditView(UpdateView):
    model = Course
    fields = ['title', 'description', 'access_level', 'teachers', 'assistants'] # 'start_time',
    template_name = 'polygon/course/edit.jinja2'
    # queryset = Course.objects.all()
