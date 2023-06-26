from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers


@api_view(['GET'])
def get_fake_data(_):
    serializer_class = DataSerializer({
        'linkedin': 'https://br.linkedin.com/in/felipebasina',
        'github': 'https://github.com/felipe-basina',
        'my_website': 'https://about.me/escapistabr'
    })
    return Response(serializer_class.data)


@api_view(['POST'])
def post_fake_data(request):
    print('Request data>>>> {}'.format(request.data))
    print('Request data.app_user>>>> {}'.format(request.data['app_user']))
    print('Request data.job>>>> {}'.format(request.data['job']))
    print('Request data.location>>>> {}'.format(request.data['location']))
    return Response(data=request.data, status=status.HTTP_201_CREATED)


class DataSerializer(serializers.Serializer):
    linkedin = serializers.CharField()
    github = serializers.CharField()
    my_website = serializers.CharField()
