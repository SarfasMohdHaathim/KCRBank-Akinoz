from django.db import models

# Create your models here.


class Gallery(models.Model):
    title=models.CharField(max_length=100)
    des=models.TextField()
    cover=models.ImageField(upload_to="media",blank=True,null=True)


    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    title=models.ForeignKey(Gallery,on_delete=models.CASCADE)
    img1=models.ImageField(upload_to="media",blank=True,null=True)

    
class News(models.Model):
    title=models.CharField(max_length=100,blank=True,null=True)
    category=models.TextField(blank=True,null=True)
    cover=models.ImageField(upload_to="media",blank=True,null=True)
    posted_date = models.DateField( auto_now_add=True, blank=True)
    posted_time = models.TimeField( auto_now_add=True, blank=True)
    img1=models.ImageField(upload_to="media",blank=True,null=True)
    sectiontitle=models.CharField(max_length=100,blank=True,null=True)
    paragraph1=models.TextField(blank=True,null=True)
    paragraph2=models.TextField(blank=True,null=True)
    paragraph3=models.TextField(blank=True,null=True)
    paragraph4=models.TextField(blank=True,null=True)
    



    def __str__(self):
        return self.title





class Contact(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    email=models.EmailField(blank=True,null=True)
    phone=models.PositiveIntegerField(null=True, blank=True)
    subject=models.CharField(max_length=100,blank=True,null=True)
    message=models.TextField(blank=True,null=True)
    state=models.CharField(max_length=100,blank=True,null=True)
    city=models.CharField(max_length=100,blank=True,null=True)
    date = models.DateField(auto_now_add=True, blank=True,null=True)



class Emi(models.Model):
    loanamout=models.PositiveIntegerField(null=True, blank=True)
    loanterm=models.PositiveIntegerField(null=True, blank=True)
    intrestrate=models.PositiveIntegerField(null=True, blank=True)
    monthlyemi=models.PositiveIntegerField(null=True, blank=True)
    intrestamount=models.PositiveIntegerField(null=True, blank=True)
    totalamount=models.PositiveIntegerField(null=True, blank=True)

