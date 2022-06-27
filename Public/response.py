from rest_framework.response import Response as _Response


def Response(status_code: int, error: str = '', message: str = ''):
    return _Response({
        'status_code': status_code,
        'error': error,
        'message': message
    })


def ResponseDict(status_code: int, error: str = '', message: str = ''):
    return {
        'status_code': status_code,
        'error': error,
        'message': message
    }
