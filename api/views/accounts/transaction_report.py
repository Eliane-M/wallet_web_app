from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from models.models import Transaction, Wallet
from django.http import JsonResponse, HttpResponse
from decimal import Decimal
from reportlab.pdfgen import canvas
from django.db.models import Sum

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_report(request):
    try:
        # Get filters from request
        category = request.query_params.get('category')
        transaction_type = request.query_params.get('type')
        account = request.query_params.get('account')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        report_format = request.query_params.get('format', 'json')

        # Fetch transactions with filters
        transactions = Transaction.objects.filter(user=request.user)

        if category:
            transactions = transactions.filter(category__id=category)
        if transaction_type:
            transactions = transactions.filter(transaction_type=transaction_type)
        if account:
            transactions = transactions.filter(account__id=account)
        if start_date and end_date:
            transactions = transactions.filter(timestamp__range=[start_date, end_date])

        # Calculate total income and expenses
        total_income = transactions.filter(transaction_type='Deposit').aggregate(total=Sum('transaction_amount'))['total'] or Decimal(0)
        total_expenses = transactions.filter(transaction_type='Withdrawal').aggregate(total=Sum('transaction_amount'))['total'] or Decimal(0)
        wallet_balance = Wallet.objects.get(user=request.user).balance

        # Prepare data for the report
        report_data = {
            "wallet_balance": wallet_balance,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "transactions": [
                {
                    "id": txn.id,
                    "type": txn.transaction_type,
                    "amount": txn.transaction_amount,
                    # "category": txn.category.name if txn.category else None,
                    # "timestamp": txn.timestamp,
                }
                for txn in transactions
            ]
        }

        # Generate the report in pdf format
        if report_format == 'pdf':
            return generate_pdf_report(report_data)
        else:
            # Default: Return JSON response
            return JsonResponse({
                "status": "success",
                "data": report_data
            }, status=200)

    except Exception as e:
        return JsonResponse({
            "status": "failed",
            "message": str(e)
        }, status=400)


def generate_pdf_report(data):
    """Generate a PDF report."""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transaction_report.pdf"'

    pdf = canvas.Canvas(response)
    pdf.setFont("Helvetica", 12)

    # Add report title
    pdf.drawString(100, 800, "Transaction Report")
    pdf.drawString(100, 780, f"Wallet Balance: {data['wallet_balance']}")
    pdf.drawString(100, 760, f"Total Income: {data['total_income']}")
    pdf.drawString(100, 740, f"Total Expenses: {data['total_expenses']}")

    # Add transactions
    y = 720
    pdf.drawString(100, y, "Transactions:")
    y -= 20
    pdf.drawString(100, y, "ID    Type    Amount    Category    Timestamp")
    y -= 20

    for txn in data['transactions']:
        pdf.drawString(100, y, f"{txn['id']}    {txn['type']}    {txn['amount']}    {txn['category']}    {txn['timestamp']}")
        y -= 20

        if y < 50:  # Create a new page if necessary
            pdf.showPage()
            y = 800

    pdf.save()
    return response
