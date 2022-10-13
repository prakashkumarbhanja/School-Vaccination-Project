from audioop import add
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import request, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.generics import ListAPIView

from .models import CustomUser, VaccinationDrive
from .serialization import CustomUserSerialization, VaccinationDriveSerialization
from .pagination import *
# Create your views here.

def login_view(request):

    if request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to='/dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                user_obj = CustomUser.objects.get(username = user)
                request.session['username'] = user_obj.username
                request.session['is_student'] = user_obj.is_student
                request.session['is_school_coordinator'] = user_obj.is_school_coordinator
                return HttpResponseRedirect(redirect_to='/dashboard')

            else:
                return HttpResponseRedirect(redirect_to='/login')

    return render(request, 'login.html')

@login_required()
def logout_view(request):
    del request.session['username']
    del request.session['is_student']
    del request.session['is_school_coordinator']
    logout(request)
    return HttpResponseRedirect(redirect_to='/login')


@login_required(login_url="/login/")
def dashboard(request):
    obj = VaccinationDrive.objects.all().values('id','date', 'no_of_slots', 'is_slote_done')
    vaccination_obj  = VaccinationDriveSerialization(obj, many=True)
    custom_user_obj = CustomUser.objects.filter(vaccination_status=True).count()
    return render(request, 'dashboard.html', {"data": vaccination_obj.data, "data1": custom_user_obj})


@login_required(login_url="/login/")
def student_details_page(request):
    return render(request, 'student_details.html')

@api_view(['POST'])
def save_student_details(request):

    if request.data['formType'] == "using-form":
        first_name = request.data['firstName']
        last_name = request.data['lastName']
        user_name = request.data['userName']
        password = request.data['password']
        email = request.data['email']
        address = request.data['address']
        city = request.data['city']
        state = request.data['state']
        zip = int(request.data['zipCode'])

        student_obj = CustomUser(first_name=first_name, last_name=last_name, username = user_name, email=email,address=address, city=city,state=state,zip=zip, is_student=True)
        student_obj.set_password(password)
        student_obj.save()
        return Response({"success":"User Created Successfully"})
    else:
        try:
            file = request.FILES.get("file")
        except MultiValueDictKeyError:
            return Response({"error": "Error in Excel"})

        if str(file).split('.')[-1] == 'xlsx':
            data = xlsx_get(file)

            user_details = data['user_details']

            for i in user_details[1::]:

                if CustomUser.objects.filter(username=i[2]):
                    return Response({"error": "Username already exists"})
                else:
                    student_obj = CustomUser(first_name=i[0], last_name=i[1], username = i[2], email=i[4],address=i[5], city=i[6],state=i[7],zip=int(i[8]), is_student=True)
                    student_obj.set_password(str(i[3]))
                    student_obj.save()
        else:
             return Response({"error": "The file should be .xlsx format"})

        return Response({"success":"User Created Successfully"})


@login_required(login_url="/login/")
def genearte_report(request):
    return render(request, 'generate_report.html')

class FilterReport(ListAPIView):
    
    serializer_class = CustomUserSerialization
    pagination_class = LimitOffsetPaginationCount

    def get_queryset(self):
        vaccination_status = self.request.query_params['vaccinationStatus']
        vaccination_date = self.request.query_params['vaccinationDate']
        vaccination_name = self.request.query_params['vaccinationName']

        if vaccination_status != "":
            is_vaccinated = True if vaccination_status == "yes" else False
        else:
            is_vaccinated = vaccination_status

        if vaccination_date != "":

            new_date = vaccination_date.split('/')

            vaccin_date = f"{new_date[1]}-{new_date[0]}-{new_date[2]}"
        else:
            vaccin_date = vaccination_date

        if vaccination_status != "" and vaccination_date != "" and vaccination_name != "":

            stud_obj = CustomUser.objects.filter(vaccination_status=is_vaccinated, vaccination_date=vaccin_date, name_of_vaccination=vaccination_name).all().order_by('id')
        
            return stud_obj

        elif vaccination_date == "" and vaccination_name == "":
            stud_obj = CustomUser.objects.filter(vaccination_status=is_vaccinated).all().order_by('id')

            return stud_obj

        elif vaccination_date == "" and vaccination_name != "":
            stud_obj = CustomUser.objects.filter(vaccination_status=is_vaccinated, name_of_vaccination=vaccination_name).all().order_by('id')
        
            return stud_obj
        
        elif vaccination_date != "" and vaccination_name == "":
            stud_obj = CustomUser.objects.filter(vaccination_status=is_vaccinated, vaccination_date=vaccin_date).all().order_by('id')
        
            return stud_obj

        else:
            stud_obj = CustomUser.objects.all().order_by('id')
        
            return stud_obj

@api_view(['GET'])
def downlaod_as_csv(request):

        vaccination_status = request.query_params['vaccinationStatus']
        vaccination_date = request.query_params['vaccinationDate']
        vaccination_name = request.query_params['vaccinationName']

        if vaccination_status != "":
            is_vaccinated = True if vaccination_status == "yes" else False
        else:
            is_vaccinated = vaccination_status

        if vaccination_date != "":

            new_date = vaccination_date.split('/')

            vaccin_date = f"{new_date[1]}-{new_date[0]}-{new_date[2]}"
        else:
            vaccin_date = vaccination_date

        if vaccination_status != "" and vaccination_date != "" and vaccination_name != "":

            stud_obj = CustomUser.objects.filter(vaccination_status=is_vaccinated, vaccination_date=vaccin_date, name_of_vaccination=vaccination_name).all()
        
            serialization = CustomUserSerialization(stud_obj, many=True)
            return Response(serialization.data)

        elif vaccination_date == "" and vaccination_name == "":
            stud_obj = CustomUser.objects.filter(vaccination_status=is_vaccinated).all()
        
            serialization = CustomUserSerialization(stud_obj, many=True)
            return Response(serialization.data)

        elif vaccination_date == "" and vaccination_name != "":
            stud_obj = CustomUser.objects.filter(vaccination_status=is_vaccinated, name_of_vaccination=vaccination_name).all()
        
            serialization = CustomUserSerialization(stud_obj, many=True)
            return Response(serialization.data)
        
        elif vaccination_date != "" and vaccination_name == "":
            stud_obj = CustomUser.objects.filter(vaccination_status=is_vaccinated, vaccination_date=vaccin_date).all()
        
            serialization = CustomUserSerialization(stud_obj, many=True)
            return Response(serialization.data)

        else:
            stud_obj = CustomUser.objects.all()
        
            serialization = CustomUserSerialization(stud_obj, many=True)
            return Response(serialization.data)

        
# class FilterReport(APIView):

#     pagination_class = PaginationCount

#     def get(self, request):

#         vaccination_status = self.request.query_params['vaccinationStatus']
#         vaccination_date = self.request.query_params['vaccinationDate']
#         vaccination_name = self.request.query_params['vaccinationName']

#         if vaccination_status != "":
#             is_vaccinated = True if vaccination_status == "yes" else False
#         else:
#             is_vaccinated = vaccination_status

#         if vaccination_date != "":

#             new_date = vaccination_date.split('/')

#             vaccin_date = f"{new_date[1]}-{new_date[0]}-{new_date[2]}"
#         else:
#             vaccin_date = vaccination_date

#         if vaccination_status != "" and vaccination_date != "" and vaccination_name != "":

#             stud_obj = CustomUser.objects.filter(vaccination_status=is_vaccinated, vaccination_date=vaccin_date, name_of_vaccination=vaccination_name).all()
        
#             serialization = CustomUserSerialization(stud_obj, many=True)
#             return Response(serialization.data)

#         elif vaccination_date == "" and vaccination_name == "":
#             stud_obj = CustomUser.objects.filter(vaccination_status=is_vaccinated).all()
        
#             serialization = CustomUserSerialization(stud_obj, many=True)
#             return Response(serialization.data)

#         elif vaccination_date == "" and vaccination_name != "":
#             stud_obj = CustomUser.objects.filter(vaccination_status=is_vaccinated, name_of_vaccination=vaccination_name).all()
        
#             serialization = CustomUserSerialization(stud_obj, many=True)
#             return Response(serialization.data)
        
#         elif vaccination_date != "" and vaccination_name == "":
#             stud_obj = CustomUser.objects.filter(vaccination_status=is_vaccinated, vaccination_date=vaccin_date).all()
        
#             serialization = CustomUserSerialization(stud_obj, many=True)
#             return Response(serialization.data)

#         else:
#             stud_obj = CustomUser.objects.all()
        
#             serialization = CustomUserSerialization(stud_obj, many=True)
#             return Response(serialization.data)


@login_required(login_url="/login/")
def create_vaccine_form(request):
    return render(request, 'manage_vaccination.html')

@api_view(['POST'])
def create_vaccination_details(request):
    date = request.data.get('date')
    no_of_vaccine = request.data.get('noOfVaccine')

    if date != "":
        new_date = date.split('/')
        vaccin_date = f"{new_date[1]}-{new_date[0]}-{new_date[2]}"

        obj = VaccinationDrive.objects.create(date = vaccin_date, no_of_slots = int(no_of_vaccine))
        obj.save()
        return Response({"success": "Vaccination Details Created Successfully"})
    else:
        return Response({"error": "Date maynot blank"})

@api_view(['PUT'])
def update_vaccination_drive(request):
    date = request.data['date']
    no_of_vaccin = request.data['noOfVaccin']
    id = request.data['id']
    return Response({"success": "Updated Successfuly"})


@login_required(login_url="/login/")
def update(request, id):
  mymember = VaccinationDrive.objects.get(id=id)
  context = {
    'mymember': mymember,
    }
  return render(request, 'update.html', context)


@login_required(login_url="/login/")
def updaterecord(request, id):
  date = request.POST['first']
  no_of_vaccin = request.POST['last']

  try:
    new_date = date.split('/')
    vaccin_date = f"{new_date[1]}-{new_date[0]}-{new_date[2]}"
  except Exception as e:
    new_date = date.split('-')
    vaccin_date = f"{new_date[1]}-{new_date[0]}-{new_date[2]}"
    
  member = VaccinationDrive.objects.get(id=id)
  member.date = vaccin_date
  member.no_of_slots = no_of_vaccin
  member.save()
  return HttpResponseRedirect(redirect_to='/dashboard')