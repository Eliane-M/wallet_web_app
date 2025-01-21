from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from models.models import Wallet, Transaction
from models.serializers import TransactionSerializer, WalletSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_transactions(request):
    try:
        category = request.query_params.get('category')
        transaction_type = request.query_params.get('type')
        account = request.query_params.get('account')

        wallet = request.user.wallet.balance

        # Start with base query
        transactions = Transaction.objects.filter(user=request.user)

        # Apply filters optionally
        if category:
            transactions = transactions.filter(category__id=category)
        if transaction_type:
            transactions = transactions.filter(transaction_type=transaction_type)
        if account:
            transactions = transactions.filter(account__id=account)

        serializer = TransactionSerializer(transactions, many=True)
        return Response({"status": "success", "Wallet balance": wallet, "data": serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"status": "failed", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_balance(request): 
    try:
        wallet = Wallet.objects.get(user=request.user)
        return Response(
            {"status": "success", "balance": wallet.balance},
            status=status.HTTP_200_OK,
        )
    except Wallet.DoesNotExist:
        return Response(
            {"status": "failed", "message": "No wallet found for this user"},
            status=status.HTTP_404_NOT_FOUND,
        )
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdrawal(request):
    """Create a new transaction"""
    amount = request.data.get('amount')
    transaction_type = request.data.get('transaction_type')

    # validate given information
    if transaction_type is None or amount is None:
        return Response({'error': 'transaction_type and amount are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = request.user
        wallet = request.user.wallet
        
        # Check if it's an expense and if there's enough balance
        if 'transaction_type' == 'Withdrawal':
            if amount < 100:
                return Response({
                    "status": "failed",
                    "message": "Withdrawal amount should be at least 100"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if wallet.balance < amount:
                return Response({
                    "status": "failed",
                    "message": "Insufficient balance"
                }, status=status.HTTP_400_BAD_REQUEST)

        wallet.balance -= amount
        
        wallet.save()
        
        # Create a new transaction
        transaction = Transaction.objects.create(
            user=user,
            wallet=wallet,
            transaction_type=transaction_type,
            transaction_amount=amount
        )
    
        # Save the wallet and transaction
        transaction.save()
        transaction_serializer = TransactionSerializer(transaction).data
        
        return Response({"Message": 'success', "data": transaction_serializer}, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            "status": "failed",
            "message": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit(request):
    """Create a new transaction"""
    amount = request.data.get('amount')
    transaction_type = request.data.get('transaction_type')

    if transaction_type is None or amount is None:
        return Response({'error': 'transaction_type and amount are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = request.user
        wallet = request.user.wallet

        if transaction_type == 'Deposit':
            wallet.balance += amount
            wallet.save()
        
        else:
            return Response({'error': "transaction_type invalid"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            transaction = Transaction.objects.create(
                user=user,
                wallet=wallet,
                transaction_type=transaction_type,
                transaction_amount=amount
            )
            transaction.save()
            transaction_serializer = TransactionSerializer(transaction).data

            return Response({"status": "success", "data": transaction_serializer}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"status": "failed", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    except Wallet.DoesNotExist:
        return Response(
            {"status": "failed", "message": "No wallet found for this user"},
            status=status.HTTP_404_NOT_FOUND,
        )