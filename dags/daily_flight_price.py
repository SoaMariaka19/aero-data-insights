import requests
import pandas as pd
from datetime import datetime
import boto3
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'administrateur',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

dag = DAG(
    'daily_flight_price_dag',
    default_args=default_args,
    schedule_interval='@daily',
)

def run_daily_flight_price():
    # Remplacez 'YOUR_CLIENT_ID' et 'YOUR_CLIENT_SECRET' par vos véritables informations d'authentification
    CLIENT_ID = "rFhIuiYJEoRGwtXB0m6LekcFhCta6utw"
    CLIENT_SECRET = "t8j81tZlGcFIWFap"

    # Obtenez un jeton d'authentification
    token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    token_payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    token_response = requests.post(token_url, data=token_payload)

    if token_response.status_code == 200:
        access_token = token_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}

        # Date d'aujourd'hui
        today_date = datetime.today().strftime("%Y-%m-%d")
        
        API_URL = f"https://test.api.amadeus.com/v1/analytics/itinerary-price-metrics?originIataCode=MAD&destinationIataCode=CDG&departureDate={today_date}&currencyCode=EUR&oneWay=false"
        response = requests.get(API_URL, headers=headers)
        
        if response.status_code == 200:
            api_data = response.json()
            if (
                "data" in api_data
                and isinstance(api_data["data"], list)
                and len(api_data["data"]) > 0
            ):
                item = api_data["data"][0]  # Get the first item from the list
                # Extract data from the item dictionary
                price_metrics = item.get("priceMetrics", [])
                records = []
                for metric in price_metrics:
                    record = {
                        "date": today_date,
                        "amount": metric.get("amount"),
                        "quartileRanking": metric.get("quartileRanking"),
                    }
                    records.append(record)
                df = pd.DataFrame(records)
                csv_file = f"flightprice_{today_date}.csv"
                df.to_csv(csv_file, index=False)
                
                # Configuration du client S3 en utilisant vos informations d'identification AWS et votre région
                aws_access_key_id = 'AKIASL44WNUXNPUFN76H'
                aws_secret_access_key = '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'
                region_name = 'us-east-1'  # par exemple, 'us-east-1'

                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name
                )

                # Utilisez today_date pour créer le nom du fichier dans S3
                s3_key = f"flightprice_{today_date}.csv"
                s3_client.upload_file(csv_file, 'daily-flight-price', s3_key)

                print(f"Data saved to {csv_file} and uploaded to S3 as {s3_key}")
        else:
            print(f"Failed to fetch data for date {today_date}. Status code: {response.status_code}")
    else:
        print(f"Failed to get access token. Status code: {token_response.status_code}")

run_task = PythonOperator(
    task_id='run_daily_flight_price',
    python_callable=run_daily_flight_price,
    dag=dag,
    email_on_failure=True,     # Envoyer un e-mail en cas d'échec
    email='stevenmitia18@gmail.com',   # L'adresse e-mail à laquelle envoyer l'alerte
    email_on_retry=False,      # Désactiver les e-mails en cas de réessai
)
