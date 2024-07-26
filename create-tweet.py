from requests_oauthlib import OAuth1Session
import json # json verilerini python nesnelerine dönüştürülmesini sağlar

# In your terminal please set your environment variables by running the following lines of code.
# Terminalinizde lütfen aşağıdaki kod satırlarını çalıştırarak ortam değişkenlerinizi ayaarlayın.
# export 'CONSUMER_KEY'='<your_consumer_key>'
# export 'CONSUMER_SECRET'='<your_consumer_secret>'

consumer_key = ""
consumer_secret = ""

# Be sure to add replace the text of the with the text you wish to Tweet. You can also add parameters to post polls, quote Tweets, Tweet with reply settings, and Tweet to Super Followers in addition to other features.
# payload = {"text": "Hello world!"}

# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

from datetime import datetime
import time
from exchange_rate_api import data
while True: #Döngü true olduğundan sürekli çalışmaya devam eder ve durmaz
    myToday = str(datetime.now())
    data_list = []
    conversion_rates = data["conversion_rates"]

    # Şimdi ilk 10 kur oranını yazdırabilirsiniz
    for i, (currency, rate) in enumerate(conversion_rates.items()):
        if currency == "TRY" or currency == "EUR" or currency == "GBP":
            data_new = f"1 USD = {rate} {currency} "
            data_list.append(data_new)

    tweet_text = myToday + "\n" + 'GÜNCEL DÖVİZ KURU:\n' + '\n'.join(data_list)

    # Payload oluşturma
    payload = {
        'text': tweet_text
    }

    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))

    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))

    time.sleep(180) # Her döngünün sonunda 10 saniye bekleyecek
