from .models import Questions
import datetime

# delete old questions after 24 hours
def deleteOldQuestions():
    today = datetime.datetime.now()
    x = Questions.objects.all()
    for i in x:
        if (today-i.date_at).total_seconds()//3600 > 24:
            i.delete()