from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import CourseEnrollForm

class StudentRegstrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super(StudentRegstrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=['password1'])
        login(self.request, user)

        return result

class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        # NOTE: this mthod gets called when valid form data has been POSTed
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        # By default, form_valid() redirects to get_success_url().
        return super(StudentEnrollCourseView, self).form_valid(form)

    def get_sucess_url(self):
        return reverse_lazy('student_course_detail', args=[self.course.id])