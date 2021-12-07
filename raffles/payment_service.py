import json
from datetime import datetime, timedelta

import requests
from raffles.models import raffle
from rifa_mais.settings import ASAAS_KEY, ASAAS_URL


class PaymentService:
    @staticmethod
    def asaas_resquest(api_endpoint, method="GET", data=None):
        url = f"{ASAAS_URL}{api_endpoint}"

        if method in ["GET", "POST"]:
            if method == "GET":
                r = requests.get(url, headers={"access_token": ASAAS_KEY})
            elif method == "POST":
                r = requests.post(url, data=json.dumps(data), headers={"access_token": ASAAS_KEY})
            return r.json()

        return False

    @staticmethod
    def create_asaas_customer(customer_data):
        # Customer sample data keys {"name", "cpfCnpj", "email", "phone"}
        url = f"{ASAAS_URL}/customers"
        response = requests.post(url, json=customer_data, headers={"access_token": ASAAS_KEY})
        return response

    @staticmethod
    def create_asaas_payment(customer_id, total_value, raffle_name, ticket_number):
        url = "payments"
        data = {
            "customer": customer_id,
            "billingType": "UNDEFINED",  # let the user decide
            "value": total_value,
            "dueDate": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "description": f"Rifa Mais - Rifa: '{raffle_name}' Número #{ticket_number}",
            # "cycle": "MONTHLY",
        }

        response = PaymentService.asaas_resquest(url, method="POST", data=data)
        return response
