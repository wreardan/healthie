import fitbit
unauth_client = fitbit.Fitbit('<consumer_key>', '<consumer_secret>')
# certain methods do not require user keys
unauth_client.food_units()