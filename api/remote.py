import requests


def get_networks():
    #

    try:
        r = requests.get("http://api.citybik.es/v2/networks")
        networks = r.json()["networks"]

        for network in networks:
            yield network

    except Exception as e:
        # Just print the response if the connection fail
        print("Unable to get site data")
        print(e)
        raise e
