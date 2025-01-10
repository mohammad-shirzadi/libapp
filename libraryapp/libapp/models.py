from django.db import models
from django.contrib.auth.models import User
from datetime import date
from datetime import timedelta

# Create your models here.


class bookModel(models.Model):
    bookID = models.AutoField(primary_key=True)
    author = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    year = models.IntegerField()
    publisher = models.CharField(max_length=500)
    bookcounter = models.IntegerField(default=1)
    
    def __str__(self):
        return self.title + '_' + self.author + f"({self.year})"
    
def returndeffult(n=14):
    return date.today()+timedelta(days=n)

class borrowModel(models.Model):
    borrowID = models.AutoField(primary_key=True)
    Bbook = models.ForeignKey(bookModel,on_delete=models.CASCADE)
    Buser = models.ForeignKey(User,on_delete=models.CASCADE)
    borrowdate = models.DateField(default=date.today,)
    returndate = models.DateField(default=returndeffult)

    def __str__(self):
        return f"{self.Buser} - {self.Bbook.title} - {self.returndate}"
