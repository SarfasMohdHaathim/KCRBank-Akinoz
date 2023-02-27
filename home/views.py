from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.db.models import Q
from datetime import datetime,timedelta
from django.contrib import messages



# Create your views here.
def home(request):
    emi=Emi.objects.all()
    print(emi)
    context={'emi':emi}
    count=News.objects.all().count()
    
    print(count)
    if count==1:
        print('=======================recentsingle')
        singlerecent=News.objects.all()
        context.update({'singlerecent':singlerecent})

    elif count>=2:
        
        recent=News.objects.all()[count-2:count]
        print(recent)
        context.update({'recent':recent})
    return render(request,'index.html',context)
def gallery(request):
    gallery=Gallery.objects.all()
    context={'gallery':gallery}
    return render(request,'gallery.html',context)

def galleryview(request,id):
    gallery=Gallery.objects.get(id=id)
    galleryimg=GalleryImage.objects.filter(title=id)
    context={'gallery':gallery,'galleryimg':galleryimg}
    return render(request,'gallery-view.html',context)


def contactpage(request):
    return render(request,'contact.html')
    


def about(request):
    return render(request,'about.html')
    


def services(request):
    return render(request,'service.html')
    
def newsingle(request,id):
    print(id,'=======================')
    context={'a':1}
    news=News.objects.get(id=id)
    count=News.objects.all().count()
    print(count)
    count1=int(id)+1
    count2=int(id)-1
    count1=(count1)
    if count1<=count:
        f=1
        news1=News.objects.get(id=count1)
        print(count,'======news1=========')
        context.update({'f':f,'news1':news1})

    try:
        if count>=2:
            recent=News.objects.all()[count-2:count]
            context.update({'recent':recent})
            print(recent)
        if count2>0:
            f1=1
            news2=News.objects.get(id=count2)
            context.update({'f1':f1,'news2':news2})
        if(count==1):
            recent=News.objects.all()
            context.update({'x':recent})


    
    except:
        messages.warning(request, 'Something Will Happen')


    


    context.update({'news':news,'count1':count1,'count2':count2})
    return render(request,'news-single.html',context)

def news(request):
    context={}
    news=News.objects.all()
    count=News.objects.all().count()
    print(count)
    if count>=2:
        recent=News.objects.filter(Q(posted_date__gte = datetime.now()))[count-2:count]
        context.update({'recent':recent})
    context={'news':news}
    return render(request,'news.html',context)



def emicalculator(request):
    context={}
    emi=000000
    if request.method=="POST":
        amount=request.POST['amount']
        loanterm=request.POST['loanterm']
        interest=request.POST['interest']
        try:
            a=amount.split('-')
            a=int(a[1])

        except:
            a=amount.split('$')
            a=int(a[1])


        b=loanterm.split('-')
        c=interest.split('-')
        print(b)
        b=int(b[1])
        c=int(c[1])
        totalamount=(a*c*(1+a)**(b*12))//((1+a)**(b*12)-1)
        monthlyemi=totalamount//(b*12)
        intrestamount=a*c//100
        
        Emi.objects.all().delete()
        Emi.objects.create(loanamout=a,loanterm=b,intrestrate=c,monthlyemi=monthlyemi,intrestamount=intrestamount,totalamount=totalamount).save()
        print(Emi.objects.all())
        

        print(amount,loanterm,interest,'==============emicalculator==========')
        context={'amount':amount,'loanterm':loanterm,'interest':interest}
        return redirect(reverse('home')+'#emiform')

    return render(request,'index.html',context)


def contactus(request):
    if request.method=="POST":
        name=request.POST['fname']
        phone=request.POST['phone']
        sub=request.POST['sub']
        email=request.POST['email']
        msg=request.POST['message']
        Contact.objects.create(name=name,email=email,phone=phone,
                               subject=sub,message=msg)
        try:
            message = f'Hi {name} ,Thanks For Your Message, we will contact you to the {phone} shortly'

            recipient_list = [email]
            email_from = settings.EMAIL_HOST_USER
            send_mail( sub, message, email_from, recipient_list )
            print('erorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
            return redirect('home')
                
        except:
            messages.warning(request, 'Email Failed')
            return redirect('about')
    return redirect('home')




def getcontact(request):
    if request.method=="POST":
        name=request.POST['fname']
        phone=request.POST['phone']
        state=request.POST['state']
        city=request.POST['city']
        email=request.POST['email']
        Contact.objects.create(name=name,email=email,phone=phone,
                              state=state,city=city ).save()
        
        try:
            message = f'Hi {name} ,Thanks For Your Message, we will contact you to the {phone} shortly'

            recipient_list = [email]
            email_from = settings.EMAIL_HOST_USER
            send_mail( 'KCRBank', message, email_from, recipient_list )
            print('erorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
            return redirect('home')
                
        except:
            messages.warning(request, 'Email Failed')
            return redirect('about')
    return render(request,'contact.html')



# ADMIN




def adminlogin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        print(username,password,'===========================================')
        user=User.objects.filter(username=username)


        
        try:
            user=authenticate(request,username=username,password=password)

            # print(user.password,'===========================================')
            
            return redirect('admincontactview')
        except:
            message="INVALID"

    return render(request,'admin/admin_login.html')

def adminlogout(request):
    logout(request)
    return redirect('adminlogin')


def adminhome(request):

    return render(request,'admin/admin_home.html')


def admingallery(request):
    cover=None
    context={}
    if request.method=='POST':
        title=request.POST['title']
        des=request.POST['des']
        cover=request.FILES['coverimg']
        Gallery.objects.create(title=title,des=des,cover=cover)
        if cover:
            context.update({'cover':cover})

    return render(request,'admin/add_gallary.html',context)


def admingalleryimageadd(request):
    if request.method=='POST':
        id=request.POST['id']
        img1=request.FILES['img1']
        print(img1,'===================+++++++++++++++')
        gallery=Gallery.objects.get(id=id)
        GalleryImage.objects.create(title=gallery,img1=img1).save()
        return redirect('admingalleryimage',gallery.id)
    return render(request,'admin/add_galleryimage.html')



def admingalleryimage(request,id):
    gallery=Gallery.objects.get(id=id)
    galleryimg=GalleryImage.objects.filter(title=id)
    print(galleryimg,'==========999995555555559999=====')
    context={'galleryimg':galleryimg}

    return render(request,'admin/add_galleryimage.html',context)



def adminnews(request):
    if request.method=='POST':
        title=request.POST['title']
        category=request.POST['category']
        coverimage=request.FILES['img3']
        image=request.FILES['img']
        section_title=request.POST['section_title']
        phar1=request.POST['phar1']
        phar2=request.POST['phar2']
        phar3=request.POST['phar3']
        phar4=request.POST['phar4']
        News.objects.create(title=title,category=category,
        cover=coverimage,img1=image,
        sectiontitle=section_title,
        paragraph1=phar1,
        paragraph2=phar2,
        paragraph3=phar3,
        paragraph4=phar4,
        )
        return redirect('news')
    return render(request,'admin/admin_news.html')


def adminadd(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        repassword=request.POST['repassword']
        print('=====')
        if not password != repassword:
            print('=====')

            User.objects.create_superuser(username=username,email=email,password=password)
        else:
            messages.warning(request, 'Confrim Password is Missmatch')
    return render(request,'admin/add_admin.html')



def admincontactview(request):
    contact=Contact.objects.all().order_by('-id')
    context={'contact':contact}
    return render(request,'admin/contact_view.html',context)


def contactviewsingle(request,id):
    contact=Contact.objects.get(id=id)
    a=contact.date+ timedelta(days=-10)
    context={'contact':contact,'a':a}
    return render(request,'admin/contact_single.html',context)




def adminviewgallery(request):
    gallery=Gallery.objects.all()
    
    context={'gallery':gallery}
    return render(request,'admin/aview_gallery.html',context)



def adminnewsview(request):
    news=News.objects.all()
    context={'news':news}

    return render(request,'admin/anews_view.html',context)










































