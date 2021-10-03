from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from wishlists.models import Wishlist
from products.models import Product
from wishlists.serializers import WishlistSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import itertools


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def wishlists_list(request):
    """
    List of all Wishlists, or create a new Wishlists.
    """
    if request.method == 'GET':
        wishlists = Wishlist.objects.all()
        serializer = WishlistSerializer(wishlists, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        create_data = request.data
        create_data['user'] = str(request.user.id)
        serializer = WishlistSerializer(data=create_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def wishlists_detail(request, pk):
    """
    Retrieve, update or delete a Wishlist.
    """
    try:
        wishlists = Wishlist.objects.filter(user=str(request.user.id)).get(pk=pk)

    except Wishlist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WishlistSerializer(wishlists)
        return Response(serializer.data)

    elif request.method == 'PUT':
        create_data = request.data
        create_data['user'] = str(request.user.id)
        serializer = WishlistSerializer(instance=wishlists, data=create_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        wishlists.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def wishlists_product(request, wishlist_id, product_id):
    
    try:
        wishlist = Wishlist.objects.get(pk=wishlist_id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        if wishlist.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        create_data = request.data
        tuple_prod = Wishlist.objects.filter(pk=wishlist_id).values_list("products")
        create_data['products'] = list(itertools.chain(*tuple_prod))
        create_data['products'].append(product_id)
        serializer = WishlistSerializer(instance=wishlist, data=create_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'DELETE':
        Wishlist.objects.filter(user=str(request.user.id)).get(id=wishlist_id).products.through.objects.get(product_id=product_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
