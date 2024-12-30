from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class bookModel(models.Model):
    bookID = models.AutoField(primary_key=True)
    author = models.CharField(max_length=500)
    titel = models.CharField(max_length=500)
    year = models.IntegerField()
    publisher = models.CharField(max_length=500)
    
    def __str__(self):
        return self.titel + '_' + self.author + f"({self.year})"
    
class borrowModels(models.Model):
    borrowID = models.AutoField(primary_key=True)
    BbookID = models.ForeignKey(bookModel,on_delete=models.CASCADE)
    bookname = bookModel.titel
    Buser = models.ForeignKey(User,on_delete=models.CASCADE)
    ##TODO add str method 
    ##TODO add borrowdate and returndate field 
    