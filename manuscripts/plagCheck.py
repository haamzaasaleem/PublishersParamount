import base64
import random
from copyleaks.copyleaks import Copyleaks
from copyleaks.exceptions.command_error import CommandError
from copyleaks.models.submit.document import FileDocument, UrlDocument, OcrFileDocument
from copyleaks.models.submit.properties.scan_properties import ScanProperties
from copyleaks.models.export import *
def plagCheck(path):
    import pdb;pdb.set_trace()
    EMAIL_ADDRESS = 'hamzaasaleem04@gmail.com'
    KEY = 'e8363887-67ea-4e1b-a7dd-ec400a8be4dc'

    try:
        auth_token = Copyleaks.login(EMAIL_ADDRESS, KEY)
    except CommandError as ce:
        response = ce.get_response()
        print(f"An error occurred (HTTP status code {response.status_code}):")
        print(response.content)
        exit(1)

    print("Logged successfully!\nToken:")
    print(auth_token)

    print("Submitting a new file...")

    file_submission = UrlDocument()
    print(file_submission)
    file_submission.set_url(path)
    scan_id = random.randint(100, 100000)  # generate a random scan id
    scan_properties = ScanProperties('https://132e-182-185-158-29.in.ngrok.io/api/manuscript/plag-webhook/')
    scan_properties.set_sandbox(True)  # Turn on sandbox mode. Turn off on production.
    file_submission.set_properties(scan_properties)
    Copyleaks.submit_file(auth_token, scan_id, file_submission)
    print("You will notify, using your webhook, once the scan was completed.")