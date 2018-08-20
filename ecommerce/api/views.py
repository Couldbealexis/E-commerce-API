from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializer import *
from django.core.exceptions import ObjectDoesNotExist
import json
import decimal
from django.http import QueryDict


def index(request):
    return HttpResponse("Hello, world!")


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        try:
            name = request.POST.get('name')
            npc = request.POST.get('npc')
            print(npc)
            description = request.POST.get('description')
            stock = request.POST.get('stock')
            price = request.POST.get('price')
            likes = request.POST.get('likes')
            last_update = request.POST.get('last_update')
            price = decimal.Decimal(price)

            product = Product.objects.create(name=name, npc=npc, description=description, stock=stock,
                                             price=price, likes=likes, last_update=last_update)
            product.save()
            data = {"id":product.pk, "name":product.name, "npc":product.npc, "description":product.description,
                    "stock":product.stock, "price":str(product.price), "likes":product.likes,
                    "last_update":str(product.last_update)}
            data = json.dumps(data)
            return HttpResponse(data, status=201)

        except Exception as e:
            print('# Error #')
            print(e)
            return HttpResponse(status=400)

    return HttpResponse(status=400)


@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=200)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'PATCH':
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=200)

    elif request.method == 'DELETE':
        product.delete()
        return HttpResponse(status=204)

    return HttpResponse(status=400)


@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = User_e.objects.all()
        serializer = User_eSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    return HttpResponse(status=400)


@csrf_exempt
@api_view(['POST'])
def buy_products(request):
    if request.method == 'POST':
        # print(request.data)
        # print("------")
        customer_id = request.data['customer']
        try:
            customer = User_e.objects.get(pk=customer_id)
            if customer.type == UserType.objects.get(pk=2):
                products = request.data['products']
                for order in products:
                    try:
                        product = Product.objects.get(pk=order['product'])
                        if product.stock >= int(order['quantity']):
                            continue
                        else:
                            data = {"error": "Not enough stock: " + str(product)}
                            data = json.dumps(data)
                            return HttpResponse(data, status=400)
                    except ObjectDoesNotExist:
                        data = {"error": "product not found"}
                        data = json.dumps(data)
                        return HttpResponse(data, status=404)


                total = decimal.Decimal(0)
                items = 0
                header = SaleHeader.objects.create(customer=customer)
                for order in products:
                    product = Product.objects.get(pk=order['product'])
                    product.stock = product.stock - int(order['quantity'])
                    product.save()
                    detail = SaleDetail.objects.create(header=header, product=product,
                                                       quantity=order['quantity'], unitPrice=product.price,
                                                       fullPrice=( product.price * decimal.Decimal(order['quantity']) ))
                    total += detail.fullPrice
                    items += int(order['quantity'])
                    detail.save()

                header.total = total
                header.items = items
                header.save()

                serializer = SaleHeaderSerializer(header)
                return JsonResponse(serializer.data, status=200, safe=False)


            else:
                data = {"error":"not a customer"}
                data = json.dumps(data)
                return HttpResponse(data, status=403)

        except ObjectDoesNotExist:
            data = {"error":"customer not found"}
            data = json.dumps(data)
            return HttpResponse(data, status=404)

    return HttpResponse(status=400)


@csrf_exempt
def sales(request):
    if request.method == 'GET':
        salesH = SaleHeader.objects.all()
        serializer = SaleHeaderSerializer(salesH, many=True)
        return JsonResponse(serializer.data, safe=False)

    return HttpResponse(status=400)


@csrf_exempt
def sale_detail(request, pk):
    try:
        header = SaleHeader.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        salesD = SaleDetail.objects.filter(header=header)
        serializer = SaleDetailSerializer(salesD, many=True)
        return JsonResponse(serializer.data, safe=False)

    return HttpResponse(status=400)


@csrf_exempt
def like(request, pk):
    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=pk)
            product.likes += 1
            product.save()
            serializer = ProductSerializer(product)
            return JsonResponse(serializer.data, status=200, safe=False)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)

    return HttpResponse(status=400)

