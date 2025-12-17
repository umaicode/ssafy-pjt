import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import DepositProduct, DepositOption
from .serializers import DepositProductSerializer

# Create your views here.
@api_view(['GET'])
def save_deposit_products(request):
    API_KEY = settings.API_KEY
    URL = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
    params = {"auth": API_KEY, "topFinGrpNo": '020000', "pageNo": 1}

    response = requests.get(URL, params=params).json()

    baseList = response.get("result", {}).get("baseList", [])
    optionList = response.get("result", {}).get("optionList", [])

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
        
    return Response({"message": "saved"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def deposit_products(request):
    # 프론트에서 필터/검색/정렬을 할 예정
    # (전체 상품 + 해당 옵션들)을 한번에 내려주는 API
    products = DepositProduct.objects.all().order_by("kor_co_nm", "fin_prdt_nm")

    serializer = DepositProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)