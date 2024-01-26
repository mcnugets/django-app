import json
import logging

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .models import Tag, Product, Category
from django.conf import settings
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.serializers import serialize

# setting configs for the logging messages
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'
)


# Create your views here.

# index
@csrf_protect
def index(request) -> HttpResponse:
    # template = loader.get_template('index.html')
    default_api_url = settings.API_DEFAULT_ENDPOINT
    filter_api_url = settings.API_FILTER_ENDPOINT
    return render(request, 'index.html', {'default_api_url': default_api_url, 'filter_api_url': filter_api_url})


# handles filtering request
@csrf_protect
@require_http_methods(['POST'])
def request_table(request):
    content_type = request.META.get('CONTENT_TYPE', '').lower()
    if 'json' not in content_type:
        return JsonResponse({'error': 'request received is not in json format'}, status=400)

    try:
        dict_data = json.loads(request.body.decode('utf-8'))
        result = Product.objects.none()
        # setting base columns
        columns = ['p_name',
                   'product_tag__tag_name',
                   'cat_id__cat_name']
        # Checking if key exists
        if 'search' in dict_data:
            col_name = ''
            # Checking to see of value is empty then refill the table
            if dict_data['search'] == '':
                result = Product.objects.values('p_name',
                                                'product_tag__tag_name',
                                                'cat_id__cat_name')
            else:
                # lookup for column relevant to requested value
                for c in columns:
                    find_col = Product.objects.filter(**{c: dict_data['search']}).values('p_name',
                                                                                         'product_tag__tag_name',
                                                                                         'cat_id__cat_name')
                    if find_col.exists():
                        col_name = c
                    else:
                        logging.warning('Value does not exist')
                # filter the table based on the request
                if col_name != '':
                    result = Product.objects.filter(**{col_name: dict_data['search']}).values('p_name',
                                                                                              'product_tag__tag_name',
                                                                                              'cat_id__cat_name')

            list_result = list(result)
            print(list_result)

        return JsonResponse({'message': 'Successfully sent a response', 'result': list_result}, safe=False)

    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)


# handles default table state
@csrf_protect
@require_http_methods(['POST'])
def default_table(request):
    # fill the table on page web-load
    try:
        result = list(Product.objects.values('p_name',
                                             'product_tag__tag_name',
                                             'cat_id__cat_name'))

        print('Response was sent without a problem')
        logging.info('Response was sent without a problem')
        print(result)
        return JsonResponse({'message': 'Successfully sent a response', 'result': result}, safe=False)

    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
