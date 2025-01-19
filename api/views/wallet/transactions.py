from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from models.models import Wallet


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_balance(request): 
    try:
        wallet = request.user.wallet
        return Response(
            {"status": "success", "balance": wallet.balance},
            status=status.HTTP_200_OK,
        )
    except Wallet.DoesNotExist:
        return Response(
            {"status": "failed", "message": "No wallet found for this user"},
            status=status.HTTP_404_NOT_FOUND,
        )