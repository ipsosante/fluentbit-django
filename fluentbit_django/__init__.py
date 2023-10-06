import fluentbit_python

from django import get_version


def get_raw_uri(request):
    return '{scheme}://{host}{path}'.format(
        scheme=request.scheme,
        host=request._get_raw_host(),
        path=request.get_full_path(),
    )


class FluentbitDjangoHandler(fluentbit_python.FluentbitHandler):

    def format(self, record):

        message = super(FluentbitDjangoHandler, self).format(record)

        message["@type"] = "python.django"
        message["django_version"] = get_version()

        try:
            request = record.request
        except AttributeError:
            request = None

        if request:
            message.update({
                "django_request_method": record.request.META['REQUEST_METHOD'],
                "django_request_url": get_raw_uri(record.request),
                "django_request_remote_addr": record.request.META['REMOTE_ADDR'],
            })

        return message
