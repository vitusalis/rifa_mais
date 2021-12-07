import requests
import json
BASE_URL = "http://127.0.0.1:8000/api/"
# get raffles


def get_raffles():
    response = requests.get(BASE_URL + "raffles/")
    if response.ok:
        return {"success": True, "body": response.json()}
    return {"success": False, "body": response.content}


def post_ticket(raffle_id, ticket_number, name, email, phone, instagram=None):
    data = {
        "raffle": raffle_id,
        "ticket_number": ticket_number,
        "name": name,
        "email": email,
        "phone": phone
    }

    if instagram:
        data["instagram"] = instagram
        

    headers = { "Content-Type": "application/json" }
    response = requests.post(BASE_URL + "tickets/", data=json.dumps(data), headers=headers)
    if response.ok:
        return True
    print(response.status_code)
    print(data)
    return False


def get_ticket_by_email(email):
    response = requests.get(BASE_URL + "tickets/?email=" + email)
    if response.ok:
        return {"success": True, "body": response.json()}
    return {"success": False, "body": response.content}

print("\nGet rifas")
print(get_raffles())

print("\nPost ticket")
response = post_ticket(2, 5, "Victor 2 novo", "victor.teste@gmail.com", "219123445678")
print(response)

print("\nGet ticket by email")
response = get_ticket_by_email("victor.teste@gmail.com")
if response.get('success'):
    for item in response.get('body'):
        print(item)
else:
    print("Failed")
