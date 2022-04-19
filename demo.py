import requests

food_name = "cherry"

res = requests.get("https://api.nal.usda.gov/fdc/v1/foods/search?api_key=DEMO_KEY&query={}".format(food_name)).json()

print(res)