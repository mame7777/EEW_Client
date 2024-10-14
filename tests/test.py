# encoding: utf-8
""" 実際に外部のEEW情報配信サーバーと通信を行うテスト用スクリプト """
import os

from dotenv import load_dotenv

import eew_client.eew_client as client

if __name__ == "__main__":

    load_dotenv()
    eew_access_token = os.environ["EEW_ACCESS_TOKEN"]
    eew_server_list_api_url = os.environ["EEW_SERVER_LIST_API_URL"]
    eew_token_reflesh_api_url = os.environ["EEW_TOKEN_REFLESH_API_URL"]
    client = client.EEWClient(eew_service_name="axis", debug=False)
    client.axis.set_token_and_url(
        eew_access_token=eew_access_token,
        eew_server_list_api_url=eew_server_list_api_url,
        eew_token_reflesh_api_url=eew_token_reflesh_api_url,
    )
    client.run_forever()
