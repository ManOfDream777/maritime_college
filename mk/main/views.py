import datetime
from typing import Any, Dict

from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse, Http404

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.contrib.auth import authenticate, login, logout

from .models import BlogCategory, BlogItem, Faculty, SeniorStaff, Rank, Student, StudyGroup
from .models import Contact as ContactModel
from .models import type_of_education_choices

from .serializers import SeniorStaffSerializer, SignUpSerializer, LoginSerializer, FacultiesSerializer, ContactSerializer

from .services.validation import SignUpValidator, merge_dicts, create_user

from .mixins import BlogCategoriesMixin, FacultiesMixin


class Index(FacultiesMixin, BlogCategoriesMixin,TemplateView):
    template_name: str = 'main/index.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['teachers'] = SeniorStaff.objects.filter(rank__name = 'Преподаватели').count()
        context['blog_items'] = BlogItem.objects.all()
        return context

class About(FacultiesMixin, BlogCategoriesMixin, TemplateView):
    template_name: str = 'main/about.html'

class Contact(BlogCategoriesMixin, TemplateView):
    template_name: str = 'main/contact.html'

class Blog(BlogCategoriesMixin, TemplateView):
    template_name: str = 'main/blog.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['blog_items'] = BlogItem.objects.all()
        return context

class Faculties(FacultiesMixin, BlogCategoriesMixin, TemplateView):
    template_name: str = 'main/courses.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['teachers'] = Rank.objects.get(name = 'Преподаватели').seniorstaff_set.all().count()
        return context

class Seniors(BlogCategoriesMixin, TemplateView):
    template_name: str = 'main/seniors.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ranks'] = Rank.objects.all()
        context['seniors'] = SeniorStaff.objects.filter(rank__importancy = 1)
        return context

class AuthView(FacultiesMixin, TemplateView):
    template_name: str = 'main/auth.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['study_groups'] = StudyGroup.objects.filter(group_faculty = context['faculties'].first())
        context['types_of_education'] = type_of_education_choices
        return context

class BlogListView(BlogCategoriesMixin, TemplateView):
    template_name: str = 'main/blog_list.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        category_qs = BlogCategory.objects.filter(slug = kwargs.get('slug'))
        if category_qs.exists():
            context['blogs'] = category_qs.first().blogitem_set.all()
            return super().get(request, *args, **context)
        else:
            raise Http404()

class BlogDetailView(BlogCategoriesMixin, TemplateView):
    template_name: str = 'main/blog_detail.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data(**kwargs)
        category_qs = BlogCategory.objects.filter(slug = kwargs.get('category_slug'))
        if category_qs.exists():
            category = category_qs.first()
        else:
            raise Http404()

        blog_qs = category.blogitem_set.filter(slug = kwargs.get('slug'))
        if blog_qs.exists():
            blog = blog_qs.first()
            context['blog'] = blog
            return super().get(request, *args, **context)
        else:
            raise Http404()

class ApiRankView(ListAPIView):
    serializer_class = SeniorStaffSerializer
    queryset = SeniorStaff.objects.none()

    def get(self, request: Request, *args, **kwargs) -> Response:
        senior_qs = SeniorStaff.objects.filter(rank=kwargs['id'])
        self.queryset = senior_qs
        return super().get(request, *args, **kwargs)

class ApiAuthView(APIView):

    def post(self, request:Request, *args, **kwargs) -> Response:
        marker = request.headers.get('marker')
        data = request.data
        if marker == 'login':
            serializer = LoginSerializer(data = request.data)
            if serializer.is_valid():
                user = authenticate(email = serializer.validated_data['email'], password = serializer.validated_data['password'])
                if user is not None:
                    login(request, user)
                    return Response(status=201)
                else:
                    return Response(data={'error': 'Такого пользователя не существует'}, status=401)
            else:
                return Response(data=serializer.errors, status=401)
        elif marker == 'sign up':
            signup_data = SignUpValidator(data)
            validation_status, data = signup_data.is_valid()
            serializer = SignUpSerializer(data = data)
            if serializer.is_valid() and validation_status:
                user = create_user(serializer)
                try:
                    if data.get('make_student') != None:
                        Student.objects.create(
                            student = user,
                            birth_place = data.get('birth_place'),
                            faculty = Faculty.objects.get(id = data.get('faculty')),
                            study_group = StudyGroup.objects.get(group_number = float(data.get('group'))),
                            date_of_admission = datetime.datetime.strptime(data.get('admission'), '%d / %m / %Y'),
                            type_of_education = data.get('type')
                        )
                except Exception as ex:
                    pass
                user = authenticate(email = serializer.validated_data['email'], password = serializer.validated_data['password'])
                if user is not None:
                    login(request, user)
                    return Response(status=201)
                else:
                    return Response(data={'error': 'Авторизация провалилась по неизвестным причинам. Обратитесь в поддержку.'}, status=500)
            else:
                return Response(data={'error': merge_dicts(serializer.errors, signup_data.errors)}, status=401)

        else:
            return Response(data={'error': 'Нераспознанный запрос. Пожалуйста заполните форму.'}, status=401)
    
class ApiLogout(APIView):

    def get(self, request: Request | HttpRequest, *args, **kwargs):

        if request.user.is_authenticated:
            logout(request)
            return Response(status = 302)
        else:
            return Response(status = 302)

class ApiFacultiesGroups(ListAPIView):
    serializer_class = FacultiesSerializer
    queryset = Faculty.objects.none()

    def get(self, request: HttpRequest, *args, **kwargs):
        faculty = kwargs.get('faculty')
        self.queryset = Faculty.objects.filter(id = faculty)
        return super().get(request, *args, **kwargs)

class APIContactCreate(APIView):
    
    def post(self, request: Request, **kwargs) -> Response:
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            ContactModel.objects.create(**serializer.validated_data)
            return Response(status=201)
        else:
            return Response(data={'errors': serializer.errors}, status=400)