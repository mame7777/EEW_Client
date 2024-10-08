import os

import _thread
import time
import json

import requests
import websocket
from dotenv import load_dotenv

class EEW_Client:
    def __init__(self, debug: bool=False):
        self.debug = debug
        websocket.enableTrace(debug)
        self.ws = None
        
        load_dotenv()
        self.eew_access_token = os.environ["EEW_ACCESS_TOKEN"]
        self.eew_server_list_api_url = os.environ["EEW_SERVER_LIST_API_URL"]

    def on_message(self, ws: websocket.WebSocket, message):
        
        print(message)

    def on_error(self, ws: websocket.WebSocket, error):
        print(error)

    def on_close(self, ws: websocket.WebSocket, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws: websocket.WebSocket):
        print("### open ###")
        
    def get_server_list(self) -> list:
        response = requests.get(self.eew_server_list_api_url, headers={"Authorization": "Bearer %s" % self.eew_access_token})
        if response.status_code != 200:
            print("[Error] cannot connect server-list server!")
            raise ConnectionError()
        response_json = json.loads(response.text)
        server_list = response_json.get("servers", [])
        if len(server_list) < 1:
            print("[Error] cannot get server list!")
            raise ValueError()
        if self.debug:
            print("[Info] server list: %s" % server_list)
        return server_list
    
    def run_forever(self):
        server_list = self.get_server_list()
        for server_list_index in range(len(server_list)):
            server_url = server_list[server_list_index]
            try: 
                self.ws = websocket.WebSocketApp("%s/socket" % server_url, header=["Authorization: Bearer %s" % self.eew_access_token], on_open=self.on_open, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)                
                break
            except:
                if server_list_index == len(server_list) - 1:
                    print("[Error] cannot connect to any server!")
                    raise ConnectionError()
                else:
                    continue
        if self.debug:
            print("[Info] connected to %s" % server_url)
        
        try:
            self.ws.run_forever(ping_interval=25)
            
            
        except KeyboardInterrupt:
            self.ws.close()
        # error everything
        except:
            self.ws.close()
        
if __name__ == "__main__":
    socket = EEW_Client(debug=True)
    socket.run_forever()