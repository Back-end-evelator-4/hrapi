from django.contrib import admin

from .models import Category, Company, Skill, Job, Responsibility

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')
    search_fields = ('name', 'location')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', )


class ResponsibilityInlineAdmin(admin.TabularInline):
    model = Responsibility
    extra = 0


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    inlines = (ResponsibilityInlineAdmin, )
    list_display = ('id', 'title', 'company', 'job_type', 'category', 'experience', 'salary', 'vacancy', 'created_date')
    search_fields = ('title', 'company__name')
    filter_horizontal = ('skills', )
    list_filter = ('job_type', 'category', 'experience', 'salary')
    date_hierarchy = 'created_date'

