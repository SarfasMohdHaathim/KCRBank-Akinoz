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
from django.contrib.auth.decorators import login_required
from PIL import Image



# Create your views here.
def home(request):
    emi=Emi.objects.all()
    print(emi)
    context={'emi':emi}
    count=News.objects.all().count()
    print('===================count',count)
    print(count)
    if count==1:
        print('=======================recentsingle')
        singlerecent=News.objects.all()
        context.update({'singlerecent':singlerecent})
        print('========================single==')

    elif count>=2:
        
        recent=News.objects.all()[count-2:count]
        print(recent)
        context.update({'recent':recent})
    if count>0:
        flag=1
        context.update({'flag':flag})

    return render(request,'index.html',context)
def gallery(request):
    gallery=Gallery.objects.all().order_by('-id')
    context={'gallery':gallery}
    count=News.objects.all().count()
    if count>0:
        flag=1
        context.update({'flag':flag})
    return render(request,'gallery.html',context)

def galleryview(request,id):
    gallery=Gallery.objects.get(id=id)
    galleryimg=GalleryImage.objects.filter(title=id)
    context={'gallery':gallery,'galleryimg':galleryimg}
    count=News.objects.all().count()
    if count>0:
        flag=1
        context.update({'flag':flag})
    return render(request,'gallery-view.html',context)


def contactpage(request):
    context={}
    count=News.objects.all().count()
    if count>0:
        flag=1
        context.update({'flag':flag})
    return render(request,'contact.html',context)
    


def about(request):
    context={}
    count=News.objects.all().count()
    if count>0:
        flag=1
        context.update({'flag':flag})
    return render(request,'about.html',context)
    


def services(request):
    context={}
    count=News.objects.all().count()
    if count>0:
        flag=1
        context.update({'flag':flag})
    return render(request,'service.html',context)
    
def newsingle(request,id):
    print(id,'=======================')
    context={'a':1}
    news=News.objects.get(id=id)
    count=News.objects.all().count()
    print(count)
    count1=int(id)+1
    count2=int(id)-1
    if count1>count:
        try:
            news1=News.objects.get(id=count1)
            f=1
            context.update({'f':f,'news1':news1})
        except:
            print('next will be none')
    count=News.objects.all().count()
    if count>0:
        flag=1
        context.update({'flag':flag})

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
        messages.warning(request, '')


    


    context.update({'news':news,'count1':count1,'count2':count2})
    return render(request,'news-single.html',context)

def news(request):
    context={}
    news=News.objects.all().order_by('-id')
    count=News.objects.all().count()
    print(count)
    if count>=2:
        recent=News.objects.filter(Q(posted_date__gte = datetime.now()))[count-2:count]
        context.update({'recent':recent})
    context={'news':news}
    count=News.objects.all().count()
    if count>0:
        flag=1
        context.update({'flag':flag})
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
            try:
                send_mail( sub, message, email_from, recipient_list )
                return redirect('home')
            except:
                print('mail not success')
                
        except:
            messages.warning(request, 'Email Failed')
            return redirect('about')
    return redirect('home')




def getcontact(request):
    context={}
    if request.method=="POST":
        name=request.POST['fname']
        phone=request.POST.get('phone','0000000000')
        message=request.POST['message']
        city=request.POST['city']
        email=request.POST['email']
        if not phone:
            return redirect('home')
        Contact.objects.create(name=name,email=email,phone=phone,
                              message=message,city=city ).save()
        
        try:
            message = f'Hi {name} ,Thanks For Your Message, we will contact you to the {phone} shortly'

            recipient_list = [email]
            email_from = settings.EMAIL_HOST_USER
            send_mail( 'KCRBank', message, email_from, recipient_list )
            return redirect('home')
                
        except:
            messages.warning(request, 'Email Failed')
            return redirect('about')
        
    count=News.objects.all().count()
    if count>0:
        flag=1
        context.update({'flag':flag})
    return render(request,'contact.html')



# ADMIN




def adminlogin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        print(username,password,'===========================================')
        user=User.objects.filter(username=username)
        if not user:
            messages.warning(request,'Admin Not Found ')
        else:
            try:
                User.objects.get(username=username,password=password)
            except:
                messages.warning(request,'Invalid Credential')

        
        try:
            user=authenticate(request,username=username,password=password)
            
            if user is not None:
                login(request,user)
                return redirect('admincontactview')
            else:
                messages.warning(request,'')
        except:
            messages.warning(request,'Password is Incorrect')

    return render(request,'admin/admin_login.html')

def adminlogout(request):
    logout(request)
    return redirect('adminlogin')


def adminhome(request):

    return render(request,'admin/admin_home.html')

@login_required(login_url='adminlogin')
def admingallery(request):
    cover=None
    context={}
    if request.method=='POST':
        id=request.POST['gid']

        if id:
            g=Gallery.objects.get(id=id)
            gallerycover=g.cover
            
            title=request.POST['title']
            des=request.POST['des']
            try:
                cover=request.FILES['coverimg']
                if cover:
                    g.cover=cover
                    g.title=title
                    g.des=des
                    g.save()
                    image = Image.open(g.cover)
                    cropped_image = image.convert('RGB')
                    resized_image = cropped_image.resize((350,250), Image.ANTIALIAS)
                    resized_image.save(g.cover.path)
                    return redirect('adminviewgallery')
            except:                
                g.title=title
                g.des=des
                g.cover=gallerycover
                g.save()
                return redirect('adminviewgallery')
                
                    


        else:
                title=request.POST['title']
                des=request.POST['des']
                cover=request.FILES['coverimg']
                gallery=Gallery.objects.create(title=title,des=des,cover=cover)
                image = Image.open(gallery.cover)
                cropped_image = image.convert('RGB')
                resized_image = cropped_image.resize((350,250), Image.ANTIALIAS)
                resized_image.save(gallery.cover.path)
                return redirect('adminviewgallery')
        

    return render(request,'admin/add_gallary.html',context)

@login_required(login_url='adminlogin')
def admingalleryimageadd(request):
    if request.method=='POST':
        id=request.POST['id']
        x=request.POST['x']
        y=request.POST['y']
        h=request.POST['height']
        w=request.POST['width']


        print(x,y,h,w)
        img1=request.FILES['img1']
        img2=img1
        gallery=Gallery.objects.get(id=id)
        gi=GalleryImage.objects.create(title=gallery,img1=img1)
        

        image = Image.open(gi.img1)
        cropped_image = image.convert('RGB')
        # cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((350,250), Image.ANTIALIAS)
        resized_image.save(gi.img1.path)
        return redirect('admingalleryimage',gallery.id)
    return render(request,'admin/add_galleryimage.html')


def editgallery(request,id):
    gallery=Gallery.objects.get(id=id)
    img=gallery.cover
    context={'gallery':gallery,'img':img}
    return render(request,'admin/add_gallary.html',context)













@login_required(login_url='adminlogin')
def admingalleryimage(request,id):
    gallery=Gallery.objects.get(id=id)
    galleryimg=GalleryImage.objects.filter(title=id)
    print(galleryimg,'==========999995555555559999=====')
    context={'galleryimg':galleryimg,'gallery':gallery}
    return render(request,'admin/add_galleryimage.html',context)


@login_required(login_url='adminlogin')
def adminnews(request):
    if request.method=='POST':
        nid=request.POST['nid']
        try:
            news=News.objects.get(id=nid)
            im1=news.cover
            im2=news.img1
            title=request.POST['title']
            category=request.POST['category']
            
            section_title=request.POST['section_title']
            phar1=request.POST['phar1']
            phar2=request.POST['phar2']
            phar3=request.POST['phar3']
            phar4=request.POST['phar4']
            try:
                coverimage=request.FILES['img3']
                image=request.FILES['nocropimg']
                news.title=title
                news.category=category
                news.cover=coverimage
                news.img1=image
                news.sectiontitle=section_title
                news.paragraph1=phar1
                news.paragraph2=phar2
                news.paragraph3=phar3
                news.paragraph4=phar4
                news.save()
                image = Image.open(news.img1)
                cropped_image = image.convert('RGB')
                resized_image = cropped_image.resize((350,250), Image.ANTIALIAS)
                resized_image.save(news.img1.path)
                return redirect('newsview')
            except:
                news.title=title
                news.category=category
                news.sectiontitle=section_title
                news.paragraph1=phar1
                news.paragraph2=phar2
                news.paragraph3=phar3
                news.paragraph4=phar4
                news.save()
                return redirect('newsview')


            # if not coverimage:
            #     news.title=title
            #     news.category=category
            #     news.cover=im1
            #     news.img1=image
            #     news.sectiontitle=section_title
            #     news.paragraph1=phar1
            #     news.paragraph2=phar2
            #     news.paragraph3=phar3
            #     news.paragraph4=phar4
            #     news.save()
                
            #     return redirect('adminnewsview')

            # elif not image:
            #     news.title=title
            #     news.category=category
            #     news.cover=coverimage
            #     news.img1=im2
            #     news.sectiontitle=section_title
            #     news.paragraph1=phar1
            #     news.paragraph2=phar2
            #     news.paragraph3=phar3
            #     news.paragraph4=phar4
            #     news.save()
            #     image = Image.open(news.img1)
            #     cropped_image = image.convert('RGB')
            #     resized_image = cropped_image.resize((350,250), Image.ANTIALIAS)
            #     resized_image.save(news.img1.path)
            #     return redirect('adminnewsview')

            # else:
            #     news.title=title
            #     news.category=category
            #     news.cover=im1
            #     news.img1=im2
            #     news.sectiontitle=section_title
            #     news.paragraph1=phar1
            #     news.paragraph2=phar2
            #     news.paragraph3=phar3
            #     news.paragraph4=phar4
            #     news.save()
            #     return redirect('adminnewsview')
        except:




            title=request.POST['title']
            category=request.POST['category']
            coverimage=request.FILES['img3']
            image=request.FILES['nocropimg']
            section_title=request.POST['section_title']
            phar1=request.POST['phar1']
            phar2=request.POST['phar2']
            phar3=request.POST['phar3']
            phar4=request.POST['phar4']

            news=News.objects.create(title=title,category=category,
            cover=coverimage,img1=image,
            sectiontitle=section_title,
            paragraph1=phar1,
            paragraph2=phar2,
            paragraph3=phar3,
            paragraph4=phar4,
            )
            print(news.cover,news.img1)

            image = Image.open(news.img1)
            cropped_image = image.convert('RGB')
            resized_image = cropped_image.resize((350,250), Image.ANTIALIAS)
            resized_image.save(news.img1.path)
            return redirect('newsview')
    return render(request,'admin/admin_news.html')

@login_required(login_url='adminlogin')
def adminadd(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        repassword=request.POST['repassword']
        if password and repassword and password != repassword:
            messages.warning(request,'Password Missmatch')
        try:
            User.objects.create_superuser(username=username,email=email,password=password)
            return redirect('admintable')
        except:
            messages.warning(request, 'Admin is Already Exist')
    return render(request,'admin/add_admin.html')


@login_required(login_url='adminlogin')
def admincontactview(request):
    user=request.user
    print(user)
    contact=Contact.objects.all().order_by('-id')
    a=datetime.now().date() + timedelta(days=-5)
    print(a,'0000000000')
    print(a)
    context={'contact':contact}
    return render(request,'admin/contact_view.html',context)

@login_required(login_url='adminlogin')
def contactviewsingle(request,id):
    contact=Contact.objects.get(id=id)
    a=contact.date+ timedelta(days=-10)
    context={'contact':contact,}
    return render(request,'admin/contact_single.html',context)

@login_required(login_url='adminlogin')
def adminviewgallery(request):
    gallery=Gallery.objects.all()
    
    context={'gallery':gallery}
    return render(request,'admin/aview_gallery.html',context)


@login_required(login_url='adminlogin')
def adminnewsview(request):
    news=News.objects.all()
    context={'news':news}

    return render(request,'admin/anews_view.html',context)


def deletecontact(request,id):
    Contact.objects.get(id=id).delete()
    return redirect('admincontactview')






def deletegallery(request,id):
    Gallery.objects.get(id=id).delete()
    return redirect('adminviewgallery')


def newsview(request):
    news=News.objects.all().order_by('-id')
    context={'news':news}
    return render(request,'admin/newsadmin.html',context)

def editnews(request,id):
    news=News.objects.get(id=id)
    context={'news':news}
    return render(request,'admin/admin_news.html',context)








def deletenewssingle(request,id):
    News.objects.get(id=id).delete()
    return redirect('newsview')



def newsingleview(request,id):
    news=News.objects.get(id=id)
    return render(request,'admin/newsingleview.html',{'news':news})




def admintable(request):
    user=User.objects.all()
    return render(request,'admin/admin.html',{'user':user})



def deleteadmin(request,id):
    User.objects.get(id=id).delete()
    return redirect('admintable')







def deletegallerysingle(request,id):
    gi=GalleryImage.objects.get(id=id)
    gid=gi.title.id
    gi.delete()
    return redirect('admingalleryimage',id=str(gid))


















# cropper new
from .forms import *














# CROPPER
def photo_list(request):
    photos = Photo.objects.all()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            x = request.POST.get('x')
            y = request.POST.get('y')
            w = request.POST.get('width')
            h = request.POST.get('height')
            print(x,y,w,h)
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'admin/add_photo.html', {'form': form, 'photos': photos})






def galleryimage(request):
    photos = GalleryImage.objects.all()
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('galleryimage')
    else:
        form = GalleryImageForm()
    return render(request, 'admin/gallery_image.html', {'form': form, 'photos': photos})





