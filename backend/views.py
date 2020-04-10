from rest_framework.response import Response
from rest_framework.decorators import api_view
from model.helpers import get_all_scores


@api_view(["POST"])
def get_pred(request):
    res_ = get_all_scores(request.data)
    return Response({
        'success': True,
        'result': res_
    })
