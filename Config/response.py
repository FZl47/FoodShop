from rest_framework.response import Response as _Response


def Response(status_code: int, data: dict = {}, message: str = '', error: str = ''):
    return _Response({
        'status_code': status_code,
        'error': error,
        'message': message,
        'data': data
    })


def ResponseDict(status_code: int, data: dict = {}, message: str = '', error: str = ''):
    return {
        'status_code': status_code,
        'error': error,
        'message': message,
        'data': data
    }
