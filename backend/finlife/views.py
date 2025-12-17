import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import DepositProducts, DepositOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, TopRateSerializer
from django.shortcuts import get_object_or_404, get_list_or_404


# Create your views here.
@api_view(["GET"])
def save_deposit_products(request):
    # API, url 설정
    API_KEY = settings.API_KEY
    URL = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"

    params = {"auth": API_KEY, "topFinGrpNo": "020000", "pageNo": 1}

    # API 호출
    response = requests.get(URL, params=params).json()

    baseList = response.get("result", {}).get("baseList", [])

    # DepositProducts 저장
    for product_data in baseList:
        # fin_prdt_cd 기준 중복 체크
        fin_prdt_cd = product_data.get("fin_prdt_cd")

        save_data = {
            # 'fin_co_no': product_data.get('fin_co_no'),
            "fin_prdt_cd": fin_prdt_cd,
            "kor_co_nm": product_data.get("kor_co_nm"),
            "fin_prdt_nm": product_data.get("fin_prdt_nm"),
            "join_way": product_data.get("join_way"),
            "etc_note": product_data.get("etc_note"),
            "join_deny": product_data.get("join_deny"),
            "join_member": product_data.get("join_member"),
            "max_limit": (
                product_data.get("max_limit") if product_data.get("max_limit") else -1
            ),  # 최대 한도가 없는 경우 -1
            "spcl_cnd": product_data.get("spcl_cnd"),
        }

        product = DepositProducts(**save_data)
        product.save()

    # DepositOptions 저장
    optionList = response.get("result", {}).get("optionList", [])

    for option_data in optionList:
        fin_prdt_cd = option_data.get("fin_prdt_cd")

        # 외래 키 연결로 찾아내기
        product = DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).first()

        save_data = {
            "product": product,
            "intr_rate_type_nm": option_data.get("intr_rate_type_nm"),
            "intr_rate": option_data.get("intr_rate"),
            "intr_rate2": option_data.get("intr_rate2"),
            "save_trm": option_data.get("save_trm"),
            "fin_prdt_cd": fin_prdt_cd,
        }

        option = DepositOptions(**save_data)
        option.save()

    return Response({"message": "okay"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def deposit_products(request):
    if request.method == "GET":
        products = get_list_or_404(DepositProducts)
        serializer = DepositProductsSerializer(products, many=True)

        return Response(serializer.data)

    elif request.method == "POST":
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def deposit_options(request, fin_prdt_cd):
    options = get_list_or_404(DepositOptions, fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionsSerializer(options, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def deposit_top_rate(request):
    top_option = DepositOptions.objects.order_by('-intr_rate2').first()
    serializer = TopRateSerializer(top_option)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
