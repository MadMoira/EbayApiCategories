# Ebay API categories

## Required

Install all required dependences with "pip install requirements.txt"

Add a settings.py file in the main directory, the settings file must have the next parameters:

* ENDPOINT: 'https://api.sandbox.ebay.com/ws/api.dll'
* HEADERS: required headers for the Ebay API
* XLM_PARAMETERS: Must be a string with the next structure

``` python
'<?xml version="1.0" encoding="utf-8"?> ' \
'<GetCategoriesRequest xmlns="urn:ebay:apis:eBLBaseComponents">' \
'<ViewAllNodes>True</ViewAllNodes> ' \
'<DetailLevel>ReturnAll</DetailLevel> ' \
'<RequesterCredentials> ' \
'<eBayAuthToken> Ebay developer authentication token </eBayAuthToken>' \
'</RequesterCredentials> ' \
'</GetCategoriesRequest>'
```

## Use instructions in Ubuntu

* Run first the command python3 main.py --rebuild
* Run the command python3 main.py --render category_id  where category id is the CategoryID in the Ebay Category Database
