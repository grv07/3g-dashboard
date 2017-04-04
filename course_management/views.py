from django.shortcuts import render
from constants.global_constant import PARENT_KEY_CHILD_VALUE


def filter_field(request):
    # print(request.POST)
    if request.method == 'POST':
        # print(request.POST['model_name'])
        filter_on = request.POST['field_name']
        model_obj = PARENT_KEY_CHILD_VALUE.get(filter_on)

        # data_list = FILTER_ON_DYNAMIC_MODELS.get(request.POST['model_name']).objects.all()[:50]
        data_list = model_obj.objects.all()

        if filter_on == 'stream':
            data_list = data_list.filter(course__code=request.POST['stream'])

        if filter_on == 'subject':
            data_list = data_list.filter(subject__code=request.POST['subject'])

        # for key, value in FILTER_ON_DYNAMIC_MODELS.items():
        #     if not key == request.POST['app_name']:
        #         print(key, value)
        #         data_list.filter()

        # if request.POST['country']:
        #     pass
        # if request.POST['state']:
        #     pass
        # if request.POST['stream']:
        #     pass
        # if request.POST['subject']:
        #     pass
        # if request.POST['chapter']:
        #     pass
        # if request.POST['concept']:
        #     pass
        # if request.POST['module_data']:
        #     pass
    return render(request, 'form_filter/_options.html', {'values': data_list})
# Create your views here.
