from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from models.models import TransactionCategory
from models.serializers import TrnsactionCategorySerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    name = request.data.get('name')
    description = request.data.get('description')

    try:
        category = TransactionCategory.objects.create(name=name, description=description)
        serializer = TrnsactionCategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)