from django.contrib import admin
from .models import BlogPhotos, Student, SeniorStaff, StudyGroup, MyUser, Faculty, Rank, BlogCategory, BlogItem, Contact
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserCreationForm, MyUserChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AdminPasswordChangeForm

class MyUserAdmin(UserAdmin):
    model = MyUser
    add_form = MyUserCreationForm
    list_display = ("last_name", "first_name", "middle_name", "email",)
    ordering = ("last_name", "first_name", "middle_name",)
    fieldsets = (
        (None, {"fields": ("first_name", "last_name","middle_name","gender", "password")}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("last_name", "first_name", "middle_name",'email', 'gender', "password1", "password2"),
            },
        ),
    )
    form = MyUserChangeForm
    change_password_form = AdminPasswordChangeForm
    list_filter = ("last_name", "gender", "is_staff", "groups")
    search_fields = ("first_name", "last_name", "middle_name", "email", "gender")
    ordering = ("last_name", "first_name", "middle_name",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

class StudentAdmin(admin.ModelAdmin):
    model = Student
    autocomplete_fields = ["student"]
    # raw_id_fields = ('student',)

class SeniorStaffAdmin(admin.ModelAdmin):
    model = SeniorStaff
    autocomplete_fields = ["senior"]

class BlogPhotosAdmin(admin.TabularInline):
    fk_name = 'blog'
    model = BlogPhotos

class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogPhotosAdmin]
    model = BlogItem
    list_display = ('title', 'category', 'published', 'published_at')
    fields = ('title','slug', 'content', 'category', 'published')
    list_editable = ('published',)
    prepopulated_fields = {'slug': ('title', )}


class BlogCategoryAdmin(admin.ModelAdmin):
    model = BlogCategory
    list_display = ('name', )
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(SeniorStaff, SeniorStaffAdmin)
admin.site.register(BlogItem, BlogAdmin)
admin.site.register(StudyGroup)
admin.site.register(Faculty)
admin.site.register(Rank)
admin.site.register(Contact)
admin.site.register(BlogCategory, BlogCategoryAdmin)
