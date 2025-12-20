import pandas as pd
import os

from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
@api_view(['GET'])
def metal_prices(request):
    metal = request.GET.get('metal')
    start = request.GET.get('start')
    end = request.GET.get('end')

    # 1) 파일 경로 (BASE_DIR 기준)
    if metal == 'gold':
        file_path = os.path.join(settings.BASE_DIR, 'data', 'Gold_prices.xlsx')
    elif metal == 'silver':
        file_path = os.path.join(settings.BASE_DIR, 'data', 'Silver_prices.xlsx')
    else:
        return Response({'detail': '잘못된 현물자산입니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    df = pd.read_excel(file_path)

    date_col = 'Date'
    price_col = 'Close/Last'

    # 3) 날짜 처리(안전)
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])

    # 4) 가격 처리 (쉼표 제거 → 숫자 변환)
    df[price_col] = (
        df[price_col]
        .astype(str)
        .str.replace(',', '', regex=False)
    )
    df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
    df = df.dropna(subset=[price_col])

    # 5) 날짜 필터
    if start and end:
        start_dt = pd.to_datetime(start, errors='coerce')
        end_dt = pd.to_datetime(end, errors='coerce')

        if pd.isna(start_dt) or pd.isna(end_dt) or start_dt > end_dt:
            return Response({'detail': '날짜 범위를 확인하세요.'}, status=status.HTTP_400_BAD_REQUEST)

        df = df[(df[date_col] >= start_dt) & (df[date_col] <= end_dt)]

        if df.empty:
            return Response({'detail': '선택한 조건에 해당하는 데이터가 없습니다.'}, status=status.HTTP_200_OK)

    # 6) JSON 응답
    data = [
        {'date': d.strftime('%Y-%m-%d'), 'price': float(p)}
        for d, p in zip(df[date_col], df[price_col])
    ]

    return Response(data, status=status.HTTP_200_OK)