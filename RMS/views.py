from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required 
from django.shortcuts import get_object_or_404
# Create your views here.

def Index(request):
    return render(request,'index.html')


def Admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')
        user = authenticate(request, username= username, password = password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:   
            error = 'invalid condential or uaurtharized'
            return redirect('admin_login')
        
        
    return render(request,'login.html',{'error': error})


def Logout(request):
    logout(request)
    return redirect('admin_login')

def admin_dashboard(request):
    
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    
    return render(request,'admindashboard.html')



@login_required
def create_class(request):
    if request.method == 'POST':
        try:
            class_name = request.POST.get('classname')
            class_numeric = request.POST.get('classnumeric')
            section = request.POST.get('section')
            Class.objects.create(class_name = class_name,class_numeric = class_numeric,section = section)
            messages.success(request, "Class created successfully!")  
            return redirect('create_class')                            
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")  
            return redirect('create_class')                              
    return render(request, 'create_class.html')


@login_required
def manage_class(request):
    classes = Class.objects.all()
    
    if request.GET.get('delete'):
        try:
            class_id = request.GET.get('delete')
            class_obj = get_object_or_404(Class,id = class_id)
            class_obj.delete()
            messages.success(request,"class deleted successfully")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")  
        return redirect('manage_class')
      
                              
                          
    return render(request, 'manage_class.html', {'classes': classes})


@login_required
def edit_class(request, id):
    class_obj = get_object_or_404(Class, id=id)

    if request.method == "POST":
        class_obj.class_name = request.POST.get("classname")
        class_obj.class_numeric = request.POST.get("classnumeric")
        class_obj.section = request.POST.get("section")
        class_obj.save()

        messages.success(request, "Class updated successfully.")
        return redirect("manage_class")

    return render(request, "edit_class.html", {
        "class_obj": class_obj
    })
    
@login_required
def create_subject(request):
    if request.method == 'POST':
        try:
            subject_name = request.POST.get('subjectname')
            subject_code = request.POST.get('subjectcode')
            Subject.objects.create(subject_name=subject_name, subject_code=subject_code)
            messages.success(request, "Subject created successfully!")  
            return redirect('create_subject')                            
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")  
            return redirect('create_subject')                              
    return render(request, 'create_subject.html')


@login_required
def manage_subject(request):
    subjects = Subject.objects.all()
    
    if request.GET.get('delete'):
        try:
            subject_id = request.GET.get('delete')
            subject_obj = get_object_or_404(Subject, id=subject_id)
            subject_obj.delete()
            messages.success(request, "Subject deleted successfully")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")  
        return redirect('manage_subject')
      
    return render(request, 'manage_subject.html', {'subjects': subjects})


@login_required
def edit_subject(request, id):
    subject_obj = get_object_or_404(Subject, id=id)

    if request.method == "POST":
        subject_obj.subject_name = request.POST.get("subjectname")
        subject_obj.subject_code = request.POST.get("subjectcode")
        subject_obj.save()

        messages.success(request, "Subject updated successfully.")
        return redirect("manage_subject")

    return render(request, "edit_subject.html", {
        "subject_obj": subject_obj
    })


@login_required
def create_subject_combination(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    if request.method == 'POST':
        try:
            class_id = request.POST.get('student_class')
            subject_id = request.POST.get('subject')
            student_class = get_object_or_404(Class, id=class_id)
            subject = get_object_or_404(Subject, id=subject_id)
            SubjectCombination.objects.create(student_class=student_class, subject=subject)
            messages.success(request, "Subject combination added successfully!")
            return redirect('create_subject_combination')
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('create_subject_combination')
    return render(request, 'create_subject_combination.html', {'classes': classes, 'subjects': subjects})


@login_required
def manage_subject_combination(request):
    combinations = SubjectCombination.objects.select_related('student_class', 'subject').all()
    if request.GET.get('delete'):
        try:
            combo_id = request.GET.get('delete')
            combo = get_object_or_404(SubjectCombination, id=combo_id)
            combo.delete()
            messages.success(request, "Subject combination deleted successfully")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
        return redirect('manage_subject_combination')
    return render(request, 'manage_subject_combination.html', {'combinations': combinations})


@login_required
def create_student(request):
    classes = Class.objects.all()
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            roll_id = request.POST.get('roll_id')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            student_class = get_object_or_404(Class, id=request.POST.get('student_class'))
            Student.objects.create(
                name=name,
                roll_id=roll_id,
                email=email,
                gender=gender,
                dob=dob,
                student_class=student_class
            )
            messages.success(request, "Student added successfully!")
            return redirect('create_student')
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('create_student')
    return render(request, 'create_student.html', {'classes': classes})


@login_required
def manage_student(request):
    students = Student.objects.select_related('student_class').all()
    if request.GET.get('delete'):
        try:
            student_id = request.GET.get('delete')
            student_obj = get_object_or_404(Student, id=student_id)
            student_obj.delete()
            messages.success(request, "Student deleted successfully")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
        return redirect('manage_student')
    return render(request, 'manage_student.html', {'students': students})


@login_required
def create_result(request):
    students = Student.objects.select_related('student_class').all()
    subjects = Subject.objects.all()
    if request.method == 'POST':
        try:
            student = get_object_or_404(Student, id=request.POST.get('student'))
            subject = get_object_or_404(Subject, id=request.POST.get('subject'))
            marks = int(request.POST.get('marks') or 0)
            Result.objects.create(
                student=student,
                student_class=student.student_class,
                subject=subject,
                marks=marks
            )
            messages.success(request, "Result created successfully!")
            return redirect('create_result')
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('create_result')
    return render(request, 'create_result.html', {'students': students, 'subjects': subjects})


@login_required
def manage_result(request):
    results = Result.objects.select_related('student', 'student_class', 'subject').all()
    if request.GET.get('delete'):
        try:
            result_id = request.GET.get('delete')
            result_obj = get_object_or_404(Result, id=result_id)
            result_obj.delete()
            messages.success(request, "Result deleted successfully")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
        return redirect('manage_result')
    return render(request, 'manage_result.html', {'results': results})


@login_required
def create_notice(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            detail = request.POST.get('detail')
            Notice.objects.create(title=title, detail=detail)
            messages.success(request, "Notice created successfully!")
            return redirect('create_notice')
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('create_notice')
    return render(request, 'create_notice.html')


@login_required
def manage_notice(request):
    notices = Notice.objects.all()
    if request.GET.get('delete'):
        try:
            notice_id = request.GET.get('delete')
            notice_obj = get_object_or_404(Notice, id=notice_id)
            notice_obj.delete()
            messages.success(request, "Notice deleted successfully")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
        return redirect('manage_notice')
    return render(request, 'manage_notice.html', {'notices': notices})


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user = request.user
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('change_password')
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect('change_password')
        if len(new_password) < 8:
            messages.error(request, "New password must be at least 8 characters.")
            return redirect('change_password')
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Password changed successfully.")
        return redirect('change_password')
    return render(request, 'change_password.html')