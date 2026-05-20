from django.contrib import admin

from .models import EducationalProgram, Person, ProgramReview, SitePage

@admin.register(EducationalProgram)
class EducationalProgramAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title", "description")

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("fio", "role", "email", "phone", "city", "program")
    list_filter = ("role", "city", "program")
    search_fields = ("fio", "email", "phone", "city")

@admin.register(ProgramReview)
class ProgramReviewAdmin(admin.ModelAdmin):
    list_display = ("nickname", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("nickname", "text")
    readonly_fields = ("created_at",)

@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "category", "order", "is_published", "updated_at")
    list_filter = ("category", "is_published")
    search_fields = ("title", "content", "category")
    prepopulated_fields = {"slug": ("title",)}
