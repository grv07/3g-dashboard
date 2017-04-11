# from django.shortcuts import render
from constants.global_constant import PARENT_KEY_CHILD_VALUE
from django.http import JsonResponse
from django.template.loader import get_template
from django.template import Context


def get_ajax_response(obj_list, file_path, key_name, value_name='title'):
    """
    """
    tempo = [{'option_data': '', 'hidden_field_value': ''}]
    try:
        hidden_field_value = '||'
        t = get_template(file_path)
        html = t.render(Context({'values': obj_list}))

        for obj in obj_list:
            if key_name == 'id':
                hidden_field_value = hidden_field_value + str(obj.id) + ':'
            else:
                obj.code
                hidden_field_value = hidden_field_value + str(obj.code) + ':'

            if value_name == 'title':
                hidden_field_value = hidden_field_value + obj.title + '||'
            print(hidden_field_value)

        tempo[0]['option_data'] = html
        tempo[0]['hidden_field_value'] = hidden_field_value

    except Exception as e:
        print(e.args)

    return tempo


def filter_field(request):
    print(request.POST)
    if request.method == 'POST':
        filter_on = request.POST['field_name']
        model_obj = PARENT_KEY_CHILD_VALUE.get(filter_on)

        # data_list = FILTER_ON_DYNAMIC_MODELS.get(request.POST['model_name']).objects.all()[:50]
        data_list = model_obj.objects.all()

        if filter_on == 'country':
            data = get_ajax_response(data_list, 'form_filter/_state_filter_options.html', 'id')

        if filter_on == 'state':
            data_list = data_list.filter(state__id=request.POST['state'])
            data = get_ajax_response(data_list, 'form_filter/_options.html', 'code')

        if filter_on == 'stream':
            data_list = data_list.filter(course__code=request.POST['stream'])
            data = get_ajax_response(data_list, 'form_filter/_options.html', 'code')

        if filter_on == 'subject':
            data_list = data_list.filter(subject__code=request.POST['subject'])
            data = get_ajax_response(data_list, 'form_filter/_options.html', 'code')

        if filter_on == 'board':
            _used_titles = data_list.values_list('title').filter(board=request.POST['board'])
            data_list = data_list.exclude(title__in=_used_titles).distinct('title')
            data = get_ajax_response(data_list, 'form_filter/_grade_options.html', 'code')

        return JsonResponse(data, safe=False)

# Create your views here.
