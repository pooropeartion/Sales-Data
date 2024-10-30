from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import JokeSerializer
import json
import requests
# Create your views here.
import pandas as pd
from rest_framework.response import Response
from django.shortcuts import render, HttpResponse
from .models import Order, OrderItem 

def Extract_data(request):
    # Load data from CSV files
    # file_path1 = 'C://Users//91938//Downloads\\order_region_a.csv'
    # file_path2 = 'C://Users//91938//Downloads//order_region_b.csv'
    # column_names = ["OrderId", "OrderItemId", "QuantityOrdered", "ItemPrice", "PromotionDiscount"]
    df_a = pd.read_excel(r'C:\Users\91938\Downloads\order_region_a.xlsx')
    df_a['region'] = 'A'
    df_b = pd.read_excel(r'C:\Users\91938\Downloads\order_region_b.xlsx')
    df_b['region'] = 'B'

    # Combine data
    # df = pd.concat([df_a, df_b], ignore_index=True)

    df = pd.concat([df_a, df_b], ignore_index=True)

# Convert relevant columns to numeric, coerce errors to NaN
    df['QuantityOrdered'] = pd.to_numeric(df['QuantityOrdered'], errors='coerce')
    df['ItemPrice'] = pd.to_numeric(df['ItemPrice'], errors='coerce')
    df['PromotionDiscount'] = pd.to_numeric(df['PromotionDiscount'], errors='coerce')

    
    df['total_sales'] = df['QuantityOrdered'] * df['ItemPrice']
    df['net_sale'] = df['total_sales'] - df['PromotionDiscount']

    df = df.drop_duplicates(subset='OrderId')
    df = df[df['net_sale'] > 0]

  
    for _, row in df.iterrows():
       
        order, created = Order.objects.update_or_create(
            order_id=row['OrderId'],
            defaults={
                'promotion_discount': row['PromotionDiscount'],
                'total_sales': row['total_sales'],
                'net_sale': row['net_sale'],
                'region': row['region']
            }
        )
       
        OrderItem.objects.create(
            order=order,
            quantity_ordered=row['QuantityOrdered'],
            item_price=row['ItemPrice']
        )

    return HttpResponse("Data loaded and processed successfully")





@api_view(['GET'])
def fetch_and_store_jokes(request):
    jokes = []
    total_jokes_fetched = 0

    while total_jokes_fetched < 100:
        url = "https://v2.jokeapi.dev/joke/Any?amount=10" 
        response = requests.get(url)
        if response.status_code == 200:
            jokes_data = response.json()
            for joke in jokes_data.get('jokes', []):
                if joke['type'] == 'single':
                    jokes.append({
                        'joke_text': joke['joke'],
                        'category': joke['category'],
                        'type': joke['type'],
                        'nsfw': joke['flags'].get('nsfw', False),
                        'political': joke['flags'].get('political', False),
                        'sexist': joke['flags'].get('sexist', False),
                        'safe': joke['flags'].get('safe', False),
                        'lang': joke['lang'],
                    })
                else:
                    jokes.append({
                        'setup': joke['setup'],
                        'punchline': joke['delivery'],
                        'category': joke['category'],
                        'type': joke['type'],
                        'nsfw': joke['flags'].get('nsfw', False),
                        'political': joke['flags'].get('political', False),
                        'sexist': joke['flags'].get('sexist', False),
                        'safe': joke['flags'].get('safe', False),
                        'lang': joke['lang'],
                    })

            total_jokes_fetched += len(jokes_data.get('jokes', []))
        else:
            return Response({"error": "Failed to fetch jokes"})

    # Store jokes in the database
    serializer = JokeSerializer(data=jokes, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors)
