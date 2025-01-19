from django.utils.dateparse import parse_datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from models.models import Transaction
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_report(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    account_id = request.query_params.get('account_id')

    # if start_date

    transactions = Transaction.objects.filter(account__user=request.user)

    if start_date:
        transactions = transactions.filter(timestamp__gte=parse_datetime(start_date))
    if end_date:
        transactions = transactions.filter(timestamp__lte=parse_datetime(end_date))
    if account_id:
        transactions = transactions.filter(account_id=account_id)

    data = [
        {
            "id": tx.id,
            "amount": tx.amount,
            "type": tx.transaction_type,
            "timestamp": tx.timestamp,
            "account": tx.account.name,
            "category": tx.category.name if tx.category else None,
            "subcategory": tx.subcategory.name if tx.subcategory else None,
        }
        for tx in transactions
    ]

    return Response({"status": "success", "transactions": data}, status=status.HTTP_200_OK)
