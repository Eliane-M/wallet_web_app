from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from models.serializers import UserSerializer
from django.db import transaction
from models.models import Wallet

@api_view(["POST"])
def new_user(request):
    if request.method == "POST":        
        email = request.data.get("email")
        full_name = request.data.get("full_name")
        password = request.data.get("password")
        first_name, last_name = "", ""

        # Validate required fields
        if not all([email, full_name, password]):
            return Response(
                {"error": "Email, password and names must not be empty"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Split full name
        if full_name:
            parts = full_name.split()
            first_name = parts[0]
            if len(parts) > 1:
                last_name = " ".join(parts[1:])

        try:
            # Validate email
            validate_email(email)
            if User.objects.filter(email=email).exists():
                return Response({"error":"User with same credentials exist"}, status=status.HTTP_409_CONFLICT)
            
            with transaction.atomic():
                user = User.objects.create(
                    email=email,
                    username=email,
                    first_name = first_name,
                    last_name=last_name,
                    password=make_password(password)
                )

                # Creation of wallet with 0.00 initially
                Wallet.objects.create(
                    user=user,
                    balance=0.00,
                    last_transaction_amount=0.00,
                )

            user_info = UserSerializer(user).data
            return Response(user_info, status=status.HTTP_201_CREATED)

        except ValidationError:
            return Response(
                {"error": "Invalid email format"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"There was an error: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return Response(
        {"error": "Method not allowed"}, 
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )