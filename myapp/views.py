from django.shortcuts import render,redirect

from django.views.generic import View

from myapp.forms import TaskForm,RegistrationForm,LoginForm

from myapp.models import Task

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from django.utils import timezone

from django.db.models import Count

from django.utils.decorators import method_decorator

from myapp.decorator import signin_required

from django.contrib import messages

from django.views.decorators.cache import never_cache


#  url :localhost:8000/myapp/tasks/add
#  method :get,post

@method_decorator([signin_required,never_cache],name="dispatch")
class TaskCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TaskForm()
        return render(request,"task_add.html",{'form':form})
    

    def post(self,request,*args,**kwargs):
        form=TaskForm(request.POST)
        if form.is_valid():
            form.instance.user_object=request.user
            form.save()
            messages.success(request,"Task Added")
            return redirect('task-list')
        messages.error(request,"Task Added Failed")
        return render(request,'task_add.html',{'form':form})
    

    

@method_decorator([signin_required,never_cache],name="dispatch")
class TaskListView(View):
    def get(self,request,*args,**kwargs):
       
       if not request.user.is_authenticated:
           return redirect("signin")
       cur_month=timezone.now().month
       cur_year=timezone.now().year

       qs=Task.objects.filter(user_object=request.user)
       group_by_qs=Task.objects.filter(
           user_object=request.user,
           created_date__month=cur_month,
           created_date__year=cur_year,
           ).values("status").annotate(status_count=Count("status"))
       print(group_by_qs)
         
       return render(request,"task_list.html",{'data':qs,'status_sum':group_by_qs})
    

    


@method_decorator([signin_required,never_cache],name="dispatch")
class TaskUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        task_object=Task.objects.get(id=id)
        form=TaskForm(instance=task_object)
        return render(request,'task_edit.html',{'form':form})
    

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        task_object=Task.objects.get(id=id)
        form=TaskForm(request.POST,instance=task_object)
        if form.is_valid():
            form.save()
            messages.success(request,"Task Updated SuCCESSFULLY")
            return redirect('task-list')
        messages.error(request,"Task Updated Failed")
        return render(request,'task_edit.html',{'form':form})
    

    

@method_decorator([signin_required,never_cache],name="dispatch")
class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Task.objects.get(id=id).delete()
        messages.success(request,"Task Deleted Successfully")
        return redirect("task-list")
    


@method_decorator([signin_required,never_cache],name="dispatch")
class TaskDetailView(View):
        def get(self,request,*args,**kwargs):
            print(kwargs)
            id=kwargs.get("pk")
            qs=Task.objects.get(id=id)
            return render(request,"task_detail.html",{'data':qs})
        





#  url :localhost:8000/myapp/register/
        
#  method :get,post
        


class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{'form':form})
    

    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Register Successfully")
            # User.objects.create_user(**form.cleaned_data)
            return redirect('signin')
        messages.error(request,"Register Failed")
        return render(request,'register.html',{'form':form})
    




@method_decorator([signin_required,never_cache],name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    
    



# url : localhost:8000//myapp/signin/
# method :get,post
    

class SigninView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,'login.html',{'form':form})
    


    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            uname=data.get("username")
            pwd=data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                messages.success(request,"Login Successfully")
                return redirect("task-list")
            messages.error(request,"Login Failed")
            return render(request,'login.html',{'form':form})
    


        
       


        


