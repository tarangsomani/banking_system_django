from rest_framework.response import Response


def send_response(response_code, data=dict(), error=dict(), ui_message=None, developer_message=None):
    if response_code == 90 and not error:
        import sys, traceback
        type_, value_, traceback_ = sys.exc_info()

        error = traceback.format_exception(type_, value_, traceback_)

    return Response({'data': data, 'error': error, 'ui_message': ui_message, 'developer_message': developer_message,
                     'response_code': response_code})


def send_counter_response(response_code, data=dict(), error=dict(), ui_message=None, developer_message=None,
                          global_data=dict()):
    if response_code == 90 and not error:
        import sys, traceback
        type_, value_, traceback_ = sys.exc_info()

        error = traceback.format_exception(type_, value_, traceback_)

    return Response({'data': data, 'global_data': global_data, 'error': error, 'ui_message': ui_message, 'developer_message': developer_message,
                     'response_code': response_code})
