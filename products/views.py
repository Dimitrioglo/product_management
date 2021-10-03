from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer
from django.db.models import IntegerField, Value


@api_view(['GET', 'POST'])
def products_list(request):
    """
    List of all Products, or create a new Products.
    """
    if request.method == 'GET':
        products = Product.objects.all()
        annotated_products = []
        for item in products:
            wished_by = item.wishlist_set.all().values('user').distinct().count()
            annotated_products += Product.objects.filter(name=item.name).annotate(
                wished_by=Value(wished_by, output_field=IntegerField()))

        serializer = ProductSerializer(annotated_products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        create_data = request.data
        serializer = ProductSerializer(data=create_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def products_detail(request, pk):
    """
    Retrieve, update or delete a Product.
    """
    try:
        products = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(products)
        return Response(serializer.data)

    elif request.method == 'PUT':
        create_data = request.data
        serializer = ProductSerializer(instance=products, data=create_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
