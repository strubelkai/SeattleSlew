from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Sample
from .forms import SampleForm


def index(request):
    samples_list = Sample.objects.order_by('-sample_date')[:5]
    context = {
        'samples_list': samples_list,
    }
    return render(request, 'cytology/index.html', context)


def results(request, sample_id):
    try:
        sample = Sample.objects.get(pk=sample_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'cytology/results.html', {'sample': sample})



def sample(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SampleForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/cytology/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SampleForm()

    return render(request, 'cytology/sample.html', {'form': form})
