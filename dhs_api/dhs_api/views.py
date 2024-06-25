from rest_framework.decorators import api_view
import requests
from rest_framework.response import Response
from rest_framework import status
import json
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen,Request
import logging
import pandas as pd
from datetime import datetime

current_time = datetime.now()

from django.utils import timezone
import os
logger = logging.getLogger(__name__)
# from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiExample, OpenApiRequestBody
# from drf_spectacular.types import OpenApiTypes
from django.core.mail import EmailMessage
from django.conf import settings
import smtplib

def send_email_with_attachment(to_email, subject, body, file_path):
  # send_failure = []
  # send_success = []
  for recipient in to_email:
    try:
        email = EmailMessage(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [recipient]
        )
        email.attach_file(file_path)
        email.send()
    except Exception as e:  
        raise ValueError(f"Exception occured: {str(e)}")

@api_view(http_method_names=["POST"])
def log_ticket(request):
    access_token=get_refresh_token()
    # logger.info(f'Generating new ticket for provided information.')
    # logger.info(f'{request.data}')
    res=create_request(access_token,request.data)
    res=json.loads(res)
    # logger.info(f'Ticket has been generated with display Id {res["request"]["display_id"]}')
    return Response(data=res,status=status.HTTP_200_OK)

@api_view(http_method_names=["POST"])
def log_ticketV2(request):
    access_token=get_refresh_token()
    # logger.info(f'Generating new ticket for provided information.')
    # logger.info(f'{request.data}')
    res=create_request_v2(access_token,request.data)
    res=json.loads(res)
    current_time = timezone.now()
    logger.info(f"Current time: {current_time}")
    if "request" in res:
      logger.info(f'Ticket has been generated with display Id {res["request"]["display_id"]}')
    else:
      logger.info(f'Failed to generate ticket {res} ')
    return Response(data=res,status=status.HTTP_200_OK)
  
@api_view(http_method_names=["POST"])
def log_reviews(request):
  
    try:
        data={
          'Email': request.data.get("email"),
          'Review':request.data.get("reviews"),
          'Rating':request.data.get("ratings"),
          'Created At':datetime.now().date()
        }
        # print(data)
        write_reviews(data)
        return Response(data=data,status=status.HTTP_200_OK)
    except Exception as e:
            # print(e)
            data={"error":str(e)}
            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)
 

def write_reviews(data): 
  file_path="reviews.xlsx"
  if os.path.exists(file_path):
        df = pd.read_excel(file_path)  
  else:
        df = pd.DataFrame(columns=['Email', 'Review', 'Rating']) 
        
  new_entry=pd.DataFrame([data])
  df = pd.concat([df, new_entry], ignore_index=True)
  # print(df)
  df.to_excel(file_path,index=False, engine='openpyxl')
  send_email_with_attachment(
                to_email=['sheetal.warbhuvan@aeriestechnology.com','shreeshalini.r@aeriestechnology.com',
                          'asish.barik@aeriestechnology.com','nirmal.nathani@aeriestechnology.com','neha.patil@aeriestechnology.com'],
                subject='New Review Logged',
                body='A new review has been logged. Please find the attached Excel file.',
                file_path=file_path
            )
  
def get_refresh_token():
    url = "https://accounts.zoho.in/oauth/v2/token"
    data ={"Content-Type": "application/x-www-form-urlencoded",
    "refresh_token" : "1000.36e9e456ca5702a34375d0dfb4145217.8dcad6af9f16bbf6ad3076f91703c80d",
    "grant_type" : "refresh_token",
    "client_id" : "1000.XF2DTSF0J2VSBTHI738BZ7LYX95G8H",
    "client_secret" : "4520676351533e90d15fcb8e86c12eba5334165bce",
    "redirect_uri" : "https://accounts.zoho.in" }          
    response = requests.post(url,data=data,verify=False)
    python_dict = json.loads(response.text)
    # logger.info(f'Authentication is successful')
    return python_dict.get("access_token")

def create_request(access_token,data):
    url = "https://sdpondemand.manageengine.in/api/v3/requests"
    headers ={"Accept": "application/vnd.manageengine.sdp.v3+json", 
          "Authorization" : f"Zoho-oauthtoken {access_token}", 
          "Content-Type" : "application/x-www-form-urlencoded"}
    input_data='''
    {
    "request": {
      "subject": "Test from DHS Server",
      "group": {
        "name": "IT SupportCenter"
      },
      "requester": {
        "email_id": "sairam.thummala@deliverhealth.com" 
      },
      "impact": {
        "name": "Minor / Limited"
      },
      "request_type": {
        "name": "Incident"
      },
      "priority": {
        "name": "Normal"
      },
      "status": {
        "name": "OPEN"
      },
      "description": "Test from Aeries Server"
    }
  
}
    
    '''
   
    python_dict = json.loads(data["data"])
    input_data = json.dumps(python_dict, indent=2)
    data = urlencode({"input_data":input_data}).encode()
    httprequest = Request(url, headers=headers,data=data, method="POST")
    try:
        with urlopen(httprequest) as response:
            res=response.read().decode()
            # logger.info(f'Ticket has been generated -> {res}')
            return res
    except HTTPError as e:
        res=e.read().decode()
        # logger.error(f'Failed to generate Ticket -> {res}')
        return res
      
      
      
def create_request_v2(access_token,data):
    url = "https://sdpondemand.manageengine.in/api/v3/requests"
    headers ={"Accept": "application/vnd.manageengine.sdp.v3+json", 
          "Authorization" : f"Zoho-oauthtoken {access_token}", 
          "Content-Type" : "application/x-www-form-urlencoded"}
    input_data='''
    {
    "request": {
      "subject": "Test from DHS Server",
      "group": {
        "name": "IT SupportCenter"
      },
      "requester": {
        "email_id": "sairam.thummala@deliverhealth.com" 
      },
      "impact": {
        "name": "Minor / Limited"
      },
      "request_type": {
        "name": "Incident"
      },
      "priority": {
        "name": "Normal"
      },
      "status": {
        "name": "OPEN"
      },
      "description": "Test from Aeries Server"
    }
  
}
    
    '''
   
    python_dict = json.loads(input_data)
    python_dict['request']['subject'] = data.get("subject")
    python_dict['request']['requester']['email_id'] = data.get('email')
    python_dict['request']['description'] = data.get('description')
    input_data = json.dumps(python_dict, indent=2)
    data = urlencode({"input_data":input_data}).encode()
    httprequest = Request(url, headers=headers,data=data, method="POST")
    try:
        with urlopen(httprequest) as response:
            res=response.read().decode()
            # logger.info(f'Ticket has been generated -> {res}')
            return res
    except HTTPError as e:
        res=e.read().decode()
        # logger.error(f'Failed to generate Ticket -> {res}')
        return res
      