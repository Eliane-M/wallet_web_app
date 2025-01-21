from models.models import AccountDetails, Wallet
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from models.serializers import AccountDetailsSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_account(request):
    if request.method == 'POST':
        name = request.data.get('name')
        account_type = request.data.get('account_type')

        bank_name = request.data.get('bank_name')
        account_number = request.data.get('account_number')
        account_holder_name = request.data.get('account_holder_name')

        phone_number = request.data.get('phone_number')
        provider = request.data.get('provider')

        card_number = request.data.get('card_number')
        expiration_date = request.data.get('expiration_date')

        try:
            wallet, created = Wallet.objects.get_or_create(user=request.user)
            
            if account_type == 'bank_account':
                AccountDetails.objects.create(
                    user=request.user,
                    name = name,
                    account = wallet,
                    account_number=account_number,
                    account_type=account_type,
                    bank_name=bank_name,
                    account_holder_name=account_holder_name,
                )
                return Response({'message': 'Bank account created successfully'}, status=status.HTTP_201_CREATED)
            
            if account_type == 'momo_account':
                AccountDetails.objects.create(
                    user=request.user,
                    name = name,
                    account = wallet,
                    account_number=account_number,
                    phone_number = phone_number,
                    provider = provider
                )
                return Response({'message': 'Momo account created successfully'}, status=status.HTTP_201_CREATED)
            
            if account_type == 'cash':
                AccountDetails.objects.create(
                    user = request.user,
                    name = name,
                    account = wallet,
                )
                return Response({'message': 'Cash account created successfully'}, status=status.HTTP_201_CREATED)

            account_details_serializer = AccountDetailsSerializer(AccountDetails).data
            return Response({'Message': account_details_serializer}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    return Response(status=status.HTTP_400_BAD_REQUEST)