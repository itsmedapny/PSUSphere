from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, OrgMember, Student, College, Program
from studentorg.forms import OrganizationForm, OrgMemberForm, StudentForm, CollegeForm, ProgramForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.shortcuts import render

@method_decorator(login_required, name="dispatch")
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5 

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get("q")
            qs = qs.filter(Q(name__icontains=query) | 
                           Q(description__icontains=query) |
                           Q(college__college_name__icontains=query))
        return qs

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

class OrganizationMemberList(ListView):
    model = OrgMember
    context_object_name = 'home'
    template_name = 'org_mem_list.html'
    paginate_by = 5 

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationMemberList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get("q")
            qs = qs.filter(Q(date_joined__icontains=query) | 
                       Q(organization__name__icontains=query) |
                       Q(student__lastname__icontains=query) |
                       Q(student__firstname__icontains=query) |
                       Q(student__middlename__icontains=query))

        return qs


class OrganizationMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'org_mem_add.html'
    success_url = reverse_lazy('organization-mem-list')


class OrganizationMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'org_mem_edit.html'
    success_url = reverse_lazy('organization-mem-list')


class OrganizationMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'org_mem_del.html'
    success_url = reverse_lazy('organization-mem-list')

class StudentList(ListView):
    model = Student
    context_object_name = 'home'
    template_name = 'student_list.html'
    paginate_by = 5 

    def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get("q")
            qs = qs.filter(Q(student_id__icontains=query) | 
                       Q(lastname__icontains=query) |
                       Q(firstname__icontains=query) |
                       Q(middlename__icontains=query) |
                       Q(program__prog_name__icontains=query))

        return qs

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_add.html'
    success_url = reverse_lazy('student-list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_edit.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_del.html'
    success_url = reverse_lazy('student-list')


class CollegeList(ListView):
    model = College
    context_object_name = 'home'
    template_name = 'college_list.html'
    paginate_by = 5 

    def get_queryset(self, *args, **kwargs):
        qs = super(CollegeList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get("q")
            qs = qs.filter(Q(college_name__icontains=query))
        return qs

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_add.html'
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college-list')

class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('student-list')

class ProgramList(ListView):
    model = Program
    context_object_name = 'home'
    template_name = 'program_list.html'
    paginate_by = 5 

    def get_queryset(self, *args, **kwargs):
        qs = super(ProgramList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get("q")
            qs = qs.filter(Q(prog_name__icontains=query) |
                           Q(college__college_name__icontains=query))
                           
        return qs

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_add.html'
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_edit.html'
    success_url = reverse_lazy('program-list')


class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'program_del.html'
    success_url = reverse_lazy('program-list')


from django.shortcuts import render
from .models import OrgMember, Program, Student, College
from django.db.models import Count, F

def index(request):
    #Chart1
    org_members_counts = OrgMember.objects.values('organization__name').annotate(num_students=Count('student')).order_by('-num_students')[:5]
    labels = [org_member['organization__name'] for org_member in org_members_counts]
    data = [org_member['num_students'] for org_member in org_members_counts]

    #Chart2
    top_colleges = Program.objects.values(college_name=F('college__college_name')).annotate(program_count=Count('prog_name')).order_by('-program_count')[:5]
    colleges = []
    for college in top_colleges:
        college_name = college['college_name']
        if college_name == 'College of Sciences': 
            colleges.append('CS')
        elif college_name == 'College of Teacher Education':
            colleges.append('CTE')
        elif college_name == 'College of Arts and Humanities':
            colleges.append('CAH')
        elif college_name == 'College of Business and Accountancy':
            colleges.append('CBA')
        elif college_name == 'College of Engineering Architecture and Technology':
            colleges.append('CEAT')
    num_programs = [college['program_count'] for college in top_colleges]

    #Chart3
    student_counts = Student.objects.values('program__prog_name').annotate(num_students=Count('student_id')).order_by('-num_students')[:5]
    programs = [student['program__prog_name'] for student in student_counts]
    num_students = [student['num_students'] for student in student_counts]

    #Chart4
    organizations_per_college = Organization.objects.values('college__college_name').annotate(num_organizations=Count('id'))
    college_names = [entry['college__college_name'] for entry in organizations_per_college]
    num_organizations = [entry['num_organizations'] for entry in organizations_per_college]

    #Chart5
    student_less = Student.objects.values('program__prog_name').annotate(less_students=Count('student_id')).order_by('less_students')[:5]
    program_names = [student['program__prog_name'] for student in student_less]
    programx = []
    for program_name in program_names:
        if program_name == 'Bachelor of Elementary Education':
            programx.append('BEED')
        elif program_name == 'Bachelor of Arts in Communication':
            programx.append('BAC')
        elif program_name == 'Bachelor of Arts in Political Science':
            programx.append('BAPS')
        elif program_name == 'Bachelor of Science in Accountancy':
            programx.append('BSA')
        elif program_name == 'Bachelor of Secondary Education':
            programx.append('BSE')
        else:
            programx.append(program_name)  
    less_students = [student['less_students'] for student in student_less]

    #Chart6

    organizations = Organization.objects.all()

    #render
    return render(request, 'index.html', {'labels': labels, 'data': data, 'colleges': colleges, 'num_programs': num_programs, 'programs': programs, 'num_students': num_students, 'college_names': college_names, 'num_organizations': num_organizations, 'program': programx,'less_students': less_students, 'organizations': organizations })



    
    

















