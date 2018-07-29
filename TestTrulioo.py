# import requests
# # import json
# #
# # # a = "{\"AcceptTruliooTermsAndConditions\":\"false\",\"ConfigurationName\":\"\",\"DataFields\":{\"PersonInfo\":{\"FirstGivenName\":\"Andy\",\"MiddleName\":\"\",\"FirstSurName\":\"Smith\",\"DayOfBirth\":1,\"MonthOfBirth\":1,\"YearOfBirth\":1995,\"Gender\":\"M\"},\"Location\":{\"BuildingNumber\":\"123\",\"BuildingName\":\"\",\"StreetName\":\"Hat\",\"StreetType\":\"St\",\"City\":\"Willson\",\"StateProvinceCode\":\"\",\"PostalCode\":\"94414\"},\"Communication\":{\"MobileNumber\":\"1234655123\",\"EmailAddress\":\"test@gmail.com\"}},\"CountryCode\":\"US\"}"
# # # a = json.loads(a)
# # # print(json.dumps(a, indent = 4))
# # # print(a)
# # url = "https://Conrad_API:Password123@@api.globalgateway.io/configuration/v1/testentities/Identity%20Verification/US"
# # response = requests.request("GET", url)
# # # a = response.json()
# # #
# # # print(response.text)
# # # with open("input.json", "w") as info:
# # #     json.dump(a, info)
# #
# #
# # import requests
# # import json
# #
# #
# # def validate(first_name, last_name, email, phone, street_num, street, city, zipcode):
# #     person = {
# #         "AcceptTruliooTermsAndConditions": True,
# #         "ConfigurationName": "Identity Verification",
# #         "Demo": True,
# #         "CountryCode": "US",
# #         "DataFields": {
# #             "PersonInfo": {
# #                 "FirstGivenName": first_name,
# #                 "FirstSurName": last_name,
# #             },
# #             "Location": {
# #                 "BuildingNumber": street_num,
# #                 "StreetName": street,
# #                 "City": city,
# #                 "PostalCode": zipcode
# #             },
# #             "Communication": {
# #                 "MobileNumber": phone,
# #                 "EmailAddress": email
# #             }
# #         },
# #     }
# import requests
# import base64
#
# packet = """ {"AcceptTruliooTermsAndConditions":true,"Demo":true,"ConfigurationName":"Identity Verification","ConsentForDataSources":[],"CountryCode":"US","DataFields":{"PersonInfo":{"FirstGivenName":"Test","FirstSurName":"Test","DayOfBirth":2,"MonthOfBirth":4,"YearOfBirth":1982},"Location":{}}} """
# url = "https://api.globalgateway.io/verifications/v1/verify"
# h = "Q29ucmFkX0FQSTpQYXNzd29yZDEyM0A="
# response = requests.request("POST", url, data=packet, headers = {"Authorization": "Basic " + h})
# print(response)
# #
# # respone = validate("Justin", "Willaims", "testpersonUS@gdctest.com", "221-214-4456", "1111", "West Kagy", "Bozeman",  "90010")
# #
#
#
# import requests
# #
# # url = "https://Conrad_API:Password123@@api.globalgateway.io/connection/v1/testauthentication"
# #
# # response = requests.request("GET", url)
# #
# # print(response.text)
#
#
#




import requests

url = "https://COnrad_API:Password123@@api.globalgateway.io/verifications/v1/verify"

payload = "{\"AcceptTruliooTermsAndConditions\":\"true\",\"Demo\":\"true\",\"CountryCode\":\"US\",\"DataFields\":{\"PersonInfo\":{\"FirstGivenName\":\"Identity\",\"FirstSurName\":\"Last\"}}}"
response = requests.request("POST", url, data=payload)

print(response)