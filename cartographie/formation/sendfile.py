from mimetypes import guess_type

from django.http import HttpResponse


def send_file(requested_file):
    mimetype, encoding = guess_type(requested_file.path)
    mimetype = mimetype or 'application/octet-stream'
    return HttpResponse(requested_file, mimetype=mimetype)
