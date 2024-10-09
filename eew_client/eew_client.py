# encoding: utf-8
from axis_client import AXISClient

class EEWClient:
    def __init__(self,
                eew_service: str = "",
                web_socket_func_open = None,
                web_socket_func_message = None,
                web_socket_func_error = None,
                web_socket_func_close = None,
                debug: bool = False):
        
        self.eew_service_client = None
        if eew_service == "":
            raise ValueError("name of eew service is required.\nPlese set eew_service to 'axis' or 'wolfx'.")
        elif eew_service == "axis":
            self.eew_service_client = AXISClient(
                web_socket_func_open=web_socket_func_open,
                web_socket_func_message=web_socket_func_message,
                web_socket_func_error=web_socket_func_error,
                web_socket_func_close=web_socket_func_close,
                debug=debug
            )
        elif eew_service == "wolfx":
            raise ValueError("Not implemented yet.")
        else:
            raise ValueError("name of eew service is invalid.\nPlese set eew_service to 'axis' or 'wolfx'.")
        
        self.debug = debug
        
    def run_forever(self):
        self.eew_service_client.run_forever()

        
        
if __name__ == "__main__":
    socket = EEWClient(eew_service="axis",  debug=True)
    socket.run_forever()