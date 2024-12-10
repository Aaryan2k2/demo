from django.contrib import admin
from .models import Question,Choice
# Register your models here.

class ChoiceInLine(admin.StackedInline):
    model=Choice
    extra=3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date", "was_published_recently"]
    fieldsets = [  #fieldsets allows us to group and label fields in the Django admin form.
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines=[ChoiceInLine]

admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)