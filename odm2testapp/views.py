from django.http import HttpResponse
from django.template.response import TemplateResponse
#from odm2testapp.forms import VariablesForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
#from .forms import MeasurementresultvaluesForm
#form .forms import MeasurementresultsForm

def index(request):
    return HttpResponse("odm2testsite says hello world!")

def PeopleAndOrgs(request):
    #return HttpResponse("odm2testsite says hello world!")
    return TemplateResponse(request, 'PeopleAndOrgs.html', {})

def AddSensor(request):
    #return HttpResponse("odm2testsite says hello world!")
    return TemplateResponse(request, 'AddSensor.html', {})

def about(request):
    return HttpResponse("odm2testsite about page.")
	
#def get_measurements(request):
    #if request.method == 'POST':


# def add_variable(request):
    # # Get the context from the request.
    # context = RequestContext(request)

    # # A HTTP POST?
    # if request.method == 'POST':
        # form = VariablesForm(request.POST)

        # # Have we been provided with a valid form?
        # if form.is_valid():
            # # Save the new category to the database.
            # form.save(commit=True)

            # # Now call the index() view.
            # # The user will be shown the homepage.
            # return index(request)
        # else:
            # # The supplied form contained errors - just print them to the terminal.
            # print (form.errors)
    # else:
        # # If the request was not a POST, display the form to enter details.
        # form = VariablesForm()

    # # Bad form (or form details), no form supplied...
    # # Render the form with error messages (if any).
    # return render_to_response('odm2testapp/add_variable.html', {'form': form}, context)