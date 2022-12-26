from copyleaks.copyleaks import Copyleaks
from copyleaks.models.submit.document import FileDocument
from copyleaks.models.submit.properties.scan_properties import ScanProperties
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .utils import get_token
import base64
import random


# class PlagiarismCheckView(APIView):
#     # authentication_classes = []
#     permission_classes = []
#     auth_token = get_token()
#
#     def get(self, request):
#         return Response({'status': 'ok'})
#
#     def post(self, request):
#         test_file = request.FILES['file']  # get the file from the request
#         b64_encoded_file = base64.b64encode(test_file.read()).decode(
#             'utf8')  # encode the file to base64 (very important)
#         # import pdb;
#         # pdb.set_trace()
#         scan_id = random.randint(100, 100000)  # generate a random scan id
#         file_submission = FileDocument(b64_encoded_file, test_file.name)
#         scan_properties = ScanProperties(
#             'https://1f2e-2400-adc5-15b-3800-00-1.ap.ngrok.io/api/webhook/{STATUS}/')
#         scan_properties.set_sandbox(True)  # Turn on sandbox mode. Turn off on production.
#         file_submission.set_properties(scan_properties)
#         Copyleaks.submit_file(self.auth_token, scan_id, file_submission)  # sending the submission to scanning
#         return Response({'status': 'ok'})


def plagCheck(test_file):
    auth_token = get_token()
    # test_file = request.FILES['file']  # get the file from the request
    b64_encoded_file = base64.b64encode(test_file.read()).decode(
        'utf8')  # encode the file to base64 (very important)
    # import pdb;
    # pdb.set_trace()
    scan_id = random.randint(100, 100000)  # generate a random scan id
    file_submission = FileDocument(b64_encoded_file, test_file.name)
    scan_properties = ScanProperties(
        'https://50a7-111-68-102-206.ap.ngrok.io/api/webhook/{STATUS}/')
    scan_properties.set_sandbox(True)  # Turn on sandbox mode. Turn off on production.
    file_submission.set_properties(scan_properties)
    Copyleaks.submit_file(auth_token, scan_id, file_submission)  # sending the submission to scanning
    return Response({'status': 'ok'})

@csrf_exempt
def webhook(request, **kwargs):
    if request.method == 'POST':
        print(request.body)

    # add code here to prettify the data and represxent it in a better way
    # return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})