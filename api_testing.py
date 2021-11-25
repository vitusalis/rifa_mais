import requests

BASE_URL = "http://127.0.0.1:8000/api/"
# get raffles


def get_raffles():
    response = requests.get(BASE_URL + "raffles/")
    if response.ok:
        return {"success": True, "body": response.json()}
    return {"success": False, "body": response.content}


def post_ticket(raffle_id, ticket_number, name, email, phone=None, instagram=None):
    data = {
        "raffle_id": raffle_id,
        "ticket_number": ticket_number,
        "name": name,
        "email": email,
        "phone": phone,
        "instagram": instagram,
    }

    response = requests.post(BASE_URL + "tickets/", data=data)
    if response.ok:
        return {"success": True, "body": response.json()}
    try:
        return {"success": False, "body": response.json()}
    except:
        return {"success": False, "body": response.content}


def get_ticket_by_email(email):
    response = requests.get(BASE_URL + "tickets/?email=" + email)
    if response.ok:
        return {"success": True, "body": response.json()}
    return {"success": False, "body": response.content}

print(get_raffles())

# print(get_ticket_by_email("victorsalles1997@gmail.com"))
