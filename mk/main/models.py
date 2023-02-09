from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .managers import MyUserManager
from django.urls import reverse

gender = (
    ('M', _("Мужчина")),
    ('F', _("Женщина"))
)

type_of_education_choices = (
    ('очная', 'Очная'),
    ('заочная', 'Заочная')
)

class MyAbstractBaseUser(AbstractUser, models.Model):
    username = None
    last_name = models.CharField(verbose_name = _('Фамилия'), max_length = 256)
    first_name = models.CharField(verbose_name = _('Имя'), max_length = 256)
    middle_name = models.CharField(verbose_name = _('Отчество'), max_length = 256)
    email = models.EmailField(_("email address"), unique = True)
    gender = models.CharField(verbose_name = 'Пол', choices = gender, max_length = 7, default = '')
    phone_number = models.CharField(verbose_name = 'Номер телефона', max_length = 19, default = '')
    birth_date = models.DateField(verbose_name = 'Дата рождения', blank = True, null = True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["last_name", "first_name", "middle_name"]

    objects = MyUserManager()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self.get_extra_full_name()}'
    
    def get_extra_full_name(self) -> str:
        return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'
        
class MyUser(MyAbstractBaseUser):
    pass

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ["last_name", "first_name", "middle_name"]

class Faculty(models.Model):
    # добавить картинку на факультет
    name = models.CharField(verbose_name = 'Подразделение', max_length = 128)
    price_per_year = models.IntegerField(verbose_name = 'Цена за год', help_text = 'Указывать в рублях', default = 0)
    description = models.TextField(verbose_name = 'Описание к подразделению', help_text = 'Необходимая для абитуриентов информация')
    duration = models.IntegerField(verbose_name = 'Длительность обучения', help_text = 'Указывать в годах')
    image = models.ImageField(verbose_name='Картинка факультета', upload_to='faculty_imgs/', default='')

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        ordering = ['name', 'price_per_year']

    def __str__(self) -> str:
        return f'Подразделение {self.name}'

    def get_groups_count(self):
        return self.group_faculty.count()

    def get_groups(self):          
        return [group.group_number for group in self.studygroup_set.all()]

    def get_total_students(self):
        groups = self.group_faculty.all()
        total = 0
        for group in groups:
            total += group.get_students_count()
        return total

class StudyGroup(models.Model):
    group_number = models.FloatField(verbose_name = 'Учебная группа', default = 0)
    group_faculty = models.ForeignKey(Faculty, on_delete = models.PROTECT, verbose_name = 'К какому подразделению')

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'
        ordering = ['group_number']

    def __str__(self) -> str:
        return f'{self.group_number} '

    def get_students_count(self) -> int:
        return self.study_group.count()

    def correct_group_number(self):
        return str(self.group_number).replace(',', '.')

class Student(models.Model):
    student = models.OneToOneField(MyUser, on_delete = models.CASCADE, verbose_name = 'Студент')
    birth_place = models.CharField(verbose_name = 'Место рождения', help_text = 'Заполнять в форме: Страна, Город', max_length = 256)
    faculty = models.ForeignKey(Faculty, on_delete = models.PROTECT, verbose_name = 'Подразделение',)
    type_of_education = models.CharField(verbose_name = 'Форма обучения', choices = type_of_education_choices, max_length = 256)
    date_of_admission = models.DateField(verbose_name = 'Дата поступления', help_text = 'пример: 01.09.2015', null = True, blank = True)
    study_group = models.ForeignKey(StudyGroup, on_delete = models.PROTECT, verbose_name = 'Учебная группа', related_name = 'study_group')

    class Meta:
        verbose_name = 'Курсант'
        verbose_name_plural = 'Курсанты'
        ordering = ['student__first_name', 'student__last_name', 'student__middle_name']

    def __str__(self) -> str:
        return f'{self.student.get_extra_full_name()} учится на подразделении "{self.faculty.name}" форма обучения {self.type_of_education}. Группа {self.study_group.group_number}'

@receiver(post_save, sender=Student)
def create_student_and_add_them_group(sender, instance: Student, created, **kwargs):
    if created:
        group_qs = Group.objects.filter(name='Курсант')
        if group_qs.exists():
            group = group_qs.first()
            instance.student.groups.add(group)
            instance.save()

class Rank(models.Model):
    name = models.CharField(max_length = 128, verbose_name = 'Должность', help_text='Преподаватели, Начальство и тд')
    importancy = models.IntegerField(default = 1, verbose_name = 'Важность', help_text = 'Определяет порядок показа категорий на странице')

    class Meta:
        verbose_name = 'Должностная отрасль'
        verbose_name_plural = 'Должностные отрасли'
        ordering = ['importancy']

    def __str__(self) -> str:
        return f"{self.name}"

class SeniorStaff(models.Model):
    senior = models.OneToOneField(MyUser, on_delete = models.CASCADE, verbose_name = 'Высший состав')
    rank = models.ForeignKey(Rank, on_delete = models.PROTECT, verbose_name = 'Должность человека')
    photo = models.ImageField(upload_to = 'staff/', verbose_name = 'Фотография человека')
    description = models.TextField(verbose_name = 'Описание', blank = True, max_length = 500, null=True)

    class Meta:
        verbose_name = 'Должностное лицо'
        verbose_name_plural = 'Должностные лица'

    def __str__(self) -> str:
        return f'{self.get_extra_full_name()} - должность {self.rank.name}'

    def get_extra_full_name(self):
        return self.senior.get_extra_full_name()
    
    def get_only_photo_path(self): 
        return self.photo.url

@receiver(post_save, sender=SeniorStaff)
def create_senior_and_add_them_group(sender, instance: SeniorStaff, created, **kwargs):
    if created:
        group_qs = Group.objects.filter(name='Высший состав')
        if group_qs.exists():
            group = group_qs.first()
            instance.senior.groups.add(group)
            instance.save()

class BlogCategory(models.Model):
    name = models.CharField(max_length = 256, verbose_name = 'Название категории', help_text = 'Название категории для блога. Изба-читальня, Морские котики и тд')
    slug = models.SlugField(unique = True, help_text = 'Не заполнять!', verbose_name = 'URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name', )
    
    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('blog_list', kwargs={
            'slug': self.slug
        })

class BlogItem(models.Model):
    title = models.CharField(max_length = 256, verbose_name = 'Название публикации')
    slug = models.SlugField(unique = True)
    content = models.TextField(verbose_name = 'Контент публикации', default = '')
    category = models.ForeignKey(BlogCategory, on_delete = models.CASCADE, verbose_name = 'Категория')
    published = models.BooleanField(default = False, verbose_name = 'Опубликовать', help_text = 'Записи с галочкой будут показаны на сайте')
    published_at = models.DateTimeField(verbose_name = 'Дата публикации', auto_now_add = True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('published', )

    def __str__(self) -> str:
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={
            'category_slug': self.category.slug,
            'slug': self.slug
        })

    def first_image(self):
        return self.blog_imgs.first().image.url

    def formatted_published_at(self):
        return self.published_at.strftime('%b %m')

    def short_description(self):
        if len(self.content) > 20:
            return f'{self.content[:21]}...'
        return self.content

    def show_remaining_images(self):
        paths = []
        for img in self.blog_imgs.all()[1:]:
            src = {}
            src['src'] = img.image.url
            paths.append(src)
        return paths

class BlogPhotos(models.Model):
    image = models.ImageField(
        upload_to='blog_photos/', verbose_name='Фотография к посту')
    blog = models.ForeignKey(
        BlogItem, on_delete=models.PROTECT, related_name='blog_imgs')

    class Meta:
        verbose_name = 'Фотография к новости'
        verbose_name_plural = 'Фотографии к новостям'

    def __str__(self) -> str:
        return f'Изображение для {self.blog.title}'

# class Review(models.Model):
# Узнать, как будет удобно принимать отзывы. Только от зарегистрированных пользователей или в свободной манере
#     author = models.CharField()
#     rank = models.ForeignKey()
#     body = models.TextField()
#     image = models.ImageField()

#     def __str__(self) -> str:
#         return self.author

class Contact(models.Model):
    first_name = models.CharField(max_length=256, verbose_name='Имя отправителя')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия отправителя')
    email = models.EmailField(max_length=256, verbose_name='Email отправителя', unique=True)
    subject = models.CharField(max_length=100, verbose_name='Тема сообщения')
    body = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(verbose_name='Отправлено в', auto_now=True)
    handled = models.BooleanField(verbose_name='Заявка обработана', default=False)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}. Тема {self.subject}'