import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import DepositProduct, DepositOption, SavingProduct, SavingOption, Wishlist
from .serializers import DepositProductSerializer, SavingProductSerializer, WishlistSerializer

# Create your views here.
@api_view(['GET'])
def save_deposit_products(request):
    API_KEY = settings.API_KEY
    URL = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"

    page = 1
    total_products = 0
    total_options = 0

    while True:
        params = {"auth": API_KEY, "topFinGrpNo": '020000', "pageNo": page}
        response = requests.get(URL, params=params).json()

        baseList = response.get("result", {}).get("baseList", [])
        optionList = response.get("result", {}).get("optionList", [])

        if not baseList:
            break

        # 1) DepositProducts 저장 (중복이면 update)
        for product_data in baseList:
            fin_prdt_cd = product_data.get("fin_prdt_cd")
            if not fin_prdt_cd:
                continue
            
            product = DepositProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).first()

            save_data = {
                "fin_prdt_cd": fin_prdt_cd,
                "kor_co_nm": product_data.get("kor_co_nm", ""),
                "fin_prdt_nm": product_data.get("fin_prdt_nm", ""),
                "join_way": product_data.get("join_way", ""),
                "etc_note": product_data.get("etc_note", ""),
                "join_deny": product_data.get("join_deny") or 0,
                "join_member": product_data.get("join_member", ""),
                "spcl_cnd": product_data.get("spcl_cnd", ""),
            }

            if product:
                # 업데이트
                for k, v in save_data.items():
                    setattr(product, k, v)
                product.save()
            
            else:
                product = DepositProduct(**save_data)
                product.save()
                total_products += 1
        
        # 2) DepositOption 저장
        for option_data in optionList:
            fin_prdt_cd = option_data.get("fin_prdt_cd")
            if not fin_prdt_cd:
                continue

            product = DepositProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).first()
            if not product:
                continue
                
            # save_trm은 API에서 문자열로 올때가 많아서 int로 변환을 GPT가 추천하였습니다.
            try:
                save_trm = int(option_data.get("save_trm"))
            except (TypeError, ValueError):
                save_trm = None
            
            intr_rate_type_nm = option_data.get("intr_rate_type_nm", "")

            option = DepositOption.objects.filter(product=product, save_trm=save_trm, intr_rate_type_nm=intr_rate_type_nm, rsrv_type=option_data.get("rsrv_type", ""),).first()

            save_data = {
                "product": product,
                "intr_rate_type_nm": intr_rate_type_nm,
                "intr_rate": option_data.get("intr_rate") or 0,
                "intr_rate2": option_data.get("intr_rate2") or 0,
                "save_trm": save_trm,
                "rsrv_type": option_data.get("rsrv_type", ""),
                "max_limit": option_data.get("max_limit", None),
            }

            if option:
                for k, v in save_data.items():
                    setattr(option, k, v)
                option.save()
            else:
                option = DepositOption(**save_data)
                option.save()
                total_options += 1

        page += 1
        
    return Response({"message": "saved"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def deposit_products(request):
    # 프론트에서 필터/검색/정렬을 할 예정
    # (전체 상품 + 해당 옵션들)을 한번에 내려주는 API
    products = DepositProduct.objects.all().order_by("kor_co_nm", "fin_prdt_nm")

    serializer = DepositProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def save_saving_products(request):
    API_KEY = settings.API_KEY
    URL = f"http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"

    page = 1

    while True:
        params = {"auth": API_KEY, "topFinGrpNo": '020000', "pageNo": page}
        response = requests.get(URL, params=params).json()

        baseList = response.get("result", {}).get("baseList", [])
        optionList = response.get("result", {}).get("optionList", [])

        if not baseList:
            break

        # 1) SavingProducts 저장 (중복이면 update)
        for product_data in baseList:
            fin_prdt_cd = product_data.get("fin_prdt_cd")
            if not fin_prdt_cd:
                continue
            
            product = SavingProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).first()

            save_data = {
                "fin_prdt_cd": fin_prdt_cd,
                "kor_co_nm": product_data.get("kor_co_nm", ""),
                "fin_prdt_nm": product_data.get("fin_prdt_nm", ""),
                "join_way": product_data.get("join_way", ""),
                "etc_note": product_data.get("etc_note", ""),
                "join_deny": product_data.get("join_deny") or 0,
                "join_member": product_data.get("join_member", ""),
                "spcl_cnd": product_data.get("spcl_cnd", ""),
            }

            if product:
                # 업데이트
                for k, v in save_data.items():
                    setattr(product, k, v)
                product.save()
            
            else:
                product = SavingProduct(**save_data)
                product.save()
        
        # 2) SavingOption 저장
        for option_data in optionList:
            fin_prdt_cd = option_data.get("fin_prdt_cd")
            if not fin_prdt_cd:
                continue

            product = SavingProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).first()
            if not product:
                continue
                
            # save_trm은 API에서 문자열로 올때가 많아서 int로 변환을 GPT가 추천하였습니다.
            try:
                save_trm = int(option_data.get("save_trm"))
            except (TypeError, ValueError):
                save_trm = None
            
            intr_rate_type_nm = option_data.get("intr_rate_type_nm", "")

            option = SavingOption.objects.filter(product=product, save_trm=save_trm, intr_rate_type_nm=intr_rate_type_nm, rsrv_type=option_data.get("rsrv_type", ""),).first()

            save_data = {
                "product": product,
                "intr_rate_type_nm": intr_rate_type_nm,
                "intr_rate": option_data.get("intr_rate") or 0,
                "intr_rate2": option_data.get("intr_rate2") or 0,
                "save_trm": save_trm,
                "rsrv_type": option_data.get("rsrv_type", ""),
                "max_limit": option_data.get("max_limit", None),
            }

            if option:
                for k, v in save_data.items():
                    setattr(option, k, v)
                option.save()
            else:
                option = SavingOption(**save_data)
                option.save()

        page += 1
        
    return Response({"message": "saved"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def saving_products(request):
    # 프론트에서 필터/검색/정렬을 할 예정
    # (전체 상품 + 해당 옵션들)을 한번에 내려주는 API
    products = SavingProduct.objects.all().order_by("kor_co_nm", "fin_prdt_nm")

    serializer = SavingProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def deposit_product_detail(request, fin_prdt_cd):
    deposit = get_object_or_404(DepositProduct, fin_prdt_cd=fin_prdt_cd)
    data = DepositProductSerializer(deposit).data
    
    liked = False
    if request.user.is_authenticated:
        liked = Wishlist.objects.filter(user=request.user, fin_prdt_cd=fin_prdt_cd).exists()
    
    data["liked"] = liked

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def saving_product_detail(request, fin_prdt_cd):
    saving = get_object_or_404(SavingProduct, fin_prdt_cd=fin_prdt_cd)
    data = SavingProductSerializer(saving).data

    liked = False
    if request.user.is_authenticated:
        liked = Wishlist.objects.filter(user=request.user, fin_prdt_cd=fin_prdt_cd).exists()
    
    data["liked"] = liked

    return Response(data, status=status.HTTP_200_OK)


# wish리스트 좋아요 버튼
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_wishlist(request):
    user = request.user
    fin_prdt_cd = request.data.get('fin_prdt_cd')
    product_type = request.data.get('product_type')

    wish = Wishlist.objects.filter(user=user, fin_prdt_cd=fin_prdt_cd).first()

    if wish:
        wish.delete()
        return Response({'liked': False})
    else:
        Wishlist.objects.create(user=user, fin_prdt_cd=fin_prdt_cd, product_type=product_type)
        return Response({'liked': True}, status=status.HTTP_201_CREATED)


# wish리스트 읽기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_wishlist(request):
    my_wishes = Wishlist.objects.filter(user=request.user)
    serializer = WishlistSerializer(my_wishes, many=True)
    return Response(serializer.data)