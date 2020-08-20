from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as log
from scrap.models import Post
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup as bs
import facebook as fbb
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def login(request):
    if request.method=='POST':
        name=request.POST['uname']
        password=request.POST['psw']
        user=authenticate(request,username=name,password=password)
        p=Post.objects.order_by('status')
        if user is not None:
            log(request,user)
            return render(request,'data.html',{'data':p,'num':len(p)})
        else:
            messages.info(request,'Invalid Details Please Login Again')
            return redirect('/')
    else:
        return render(request,'registration/login.html')
def home(request):

    return render(request,'home.html')
@login_required
def wscrap(request):
    page=requests.get('https://www.offcampusjobs4u.com/freshers-job/').text
    sp=bs(page,'lxml')
    h3=sp.find_all('h3')
    l=[]
    for i in h3:
        z=bs(str(i),'lxml')
        #print(z.h3.get('class'))

        if str(z.h3.get('class'))=="['entry-title', 'td-module-title']":

            l.append(z.h3.a.get('href'))
    z=[]
    for i in l:
        zz=[]
        pg=requests.get(i).text
        sp2=bs(pg,'lxml')
        stg=sp2.find_all('strong')
        for i in stg:
            if i.a:
                zz.append(i.a.get('href'))
                break
            zz.append(i.text)
        z.append(zz)
    #return render(request,'data.html',{'data':z})
    num=0
    for i in z:
        del i[0]
        title=i[0]
        data=''
        for j in i[1:]:
            data+=j+'@$'
        try:
            Post.objects.create(title=title,info=data)
            num+=1
        except:
            continue
    messages.info(request,str(num)+' records created')
    return redirect('/display')
@login_required
def display(request):
    p=Post.objects.order_by('status')

    return render(request,'data.html',{'data':p,'num':len(p)})
@login_required
def fp(request,id):
    p=Post.objects.get(id=id)
    l=[]
    l.append(p.title)
    k=p.info.split('@$')
    for i in k:
        l.append(i)
    return render(request,'item.html',{'list':l,'id':id})
@login_required
def fb(request,id):
    l=request.POST.getlist('sv')
    s='\n\n'.join(l)
    at='EAAJXpEkICvIBAD1nBZAEI5SKPf6N4jBW4uER5fsmZA0cv7Fpd1l57yVPufRgxN3ZCEuSdxQxmYhDzc2YKrZBXZAF2oCyTpTqzFOCgeLyTWibYYGUjh3U34ZBiyJtDce7tcxQILZAN6qBVWXl98jGY9jZAJ0FqISzRNq2pwYwaYjzZAl6zq2TzsffFBXLOIIdEeZBAZD'
    pi='107172831105697'
    p=Post.objects.get(id=id)
    p.status=True
    p.save()
    gp=fbb.GraphAPI(access_token=at)
    gp.put_object(parent_object=pi,connection_name='feed',message=s)
    messages.info(request,'One Post Succussfully Posted')
    return redirect('/display')
