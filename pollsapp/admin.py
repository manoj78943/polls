from django.contrib import admin
from .models import Questions,Answers,Profile

# Register your models here.
admin.site.register(Questions)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id','date_at','question','first','second','third','fourth']
    
admin.site.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ['id','user','question','answers']

admin.site.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','phone']