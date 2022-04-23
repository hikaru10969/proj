from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.conf import settings
from app.models import FileNameModel
import sys, os
import boto3
UPLOADE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/files/'

def form(request):

    client = boto3.client(
        's3',
        aws_access_key_id='AKIAQRUZASAOJFIHDP7Z',
        aws_secret_access_key='w/sPwtlEvh4WaqZGJnb7pY+MpyyPY/CKlyJkWaAZ',
        region_name='ap-northeast-1'
    )
    Bucket = 'exampleread000-1'

    if request.method != 'POST':
        # POSTでない場合S3(output)の中身を一覧表示
        objs = client.list_objects_v2(Bucket=Bucket, Prefix='output')
        output_list = []
        if objs:
            for o in objs.get('Contents'):
                # ダウンロード用URL生成
                presigned_url = client.generate_presigned_url(
                    ClientMethod='get_object',
                    Params={
                        'Bucket': Bucket,
                        'Key': o.get('Key')
                    },
                    HttpMethod='GET'
                )
                # ファイル名取得
                file_name = o.get('Key').split('/')[1]
                output_list.append({"url":presigned_url, "name": file_name})

        return render(request, 'upload_form/form.html',{'out_list':output_list})

    file = request.FILES['file']
    path = os.path.join(UPLOADE_DIR, file.name)

    # アップロード
    key = 'input/' + str(file)
    client.upload_file(path, Bucket, key)

    return render(request,'upload_form/complete.html')

def complete(request):
    return render(request, 'upload_form/complete.html')