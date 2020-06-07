from django.db import models

# Create your models here.

class Search(models.Model):                     #Here we created a model name Search 
    search=models.CharField(max_length=500)     #Here we created a searching field for searching in search bar.
    created=models.DateTimeField(auto_now=True) #Here we created a time field to show the time of adding something(field).

    # def __str__(self):                        #If you use it then you will see the same objects name in database in english when you search in search box. Otherwise you will get names like Object(1),Object(2),Object(3)..and so on how much time you search.
    #     return '{}'.format(self.search)
    class Meta:                                    #For changing the name like from searchs to searches
        verbose_name_plural='Searches'