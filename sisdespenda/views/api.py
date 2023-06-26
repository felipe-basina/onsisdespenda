from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from django.db import connection


@api_view(['POST'])
@csrf_exempt
def despesa_add(request):
    content = request.data
    print('Despesa >>> {}'.format(content))
    save_data(
        'INSERT INTO despesa_tbl (cd_usuario, dt_despesa, vl_despesa, cd_tipo_despesa, ds_despesa, dt_criacao, '
        'dt_atualizacao) VALUES (%s, %s, %s, %s, %s, now(), now())',
        (content['cd_usuario'], content['dt_despesa'], float("{:.2f}".format(content['vl_despesa'])), 7, content['ds_despesa'])
    )
    return Response(data=request.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@csrf_exempt
def renda_add(request):
    content = request.data
    print('Renda >>> {}'.format(content))
    save_data(
        'INSERT INTO renda_tbl (cd_usuario, dt_renda, vl_renda, cd_tipo_renda, dt_criacao, dt_atualizacao) '
        'VALUES (%s, %s, %s, %s, now(), now())',
        (content['cd_usuario'], content['dt_renda'], float("{:.2f}".format(content['vl_renda'])), 3)
    )
    return Response(data=request.data, status=status.HTTP_201_CREATED)


def save_data(sql, params):
    cursor = connection.cursor()
    cursor.execute(sql, params)
