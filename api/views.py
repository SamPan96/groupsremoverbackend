from django.http import HttpResponse
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from rest_framework.views import APIView
from rest_framework.response import Response
import asyncio
from rest_framework import generics,status

api_id = 1168235
api_hash = 'e04fa44ac5acaff12b738b40c3cc075a'



class RemoveGroups(APIView):
    def post(self,request,format=None):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        phone = request.data.get('phone')
        client = TelegramClient(phone, api_id, api_hash,loop=loop)
        client.connect()
        if not client.is_user_authorized():
            if not request.data.get('vcode'):
                client.send_code_request(phone)
                phone_code_hash = client.send_code_request(phone).phone_code_hash
                return Response({'Message':'Not logged in, send vcode'},status = status.HTTP_401_UNAUTHORIZED)
            else:
                client.sign_in(phone, request.data.get("vcode"),phone_code_hash=phone_code_hash) # Enter the login code sent to your telegram 

        chats = []
        last_date = None
        chunk_size = 200
        groups=[]

        result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
            ))
        chats.extend(result.chats)

        for chat in chats:
            try:
                client.delete_dialog(chat)
            except:
                continue
        client.disconnect()
        return Response(status = status.HTTP_200_OK)

