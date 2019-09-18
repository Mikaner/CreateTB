from time import sleep
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup


def get_heart_beating_data_for_niconico(niconico_url):
    webpage_content = requests.get(niconico_url)
    soup = BeautifulSoup(webpage_content.text, "html.parser")
    div = soup.find(id="js-initial-watch-data")
    data = json.loads(div["data-api-data"])["video"]["dmcInfo"]["session_api"]
    postEndpoint = data["urls"][0]["url"] + "?_format=json"
        
    postData = {
        "session": {
            "client_info": {
                "player_id": data["player_id"]
            },
            "content_auth": {
                "auth_type": data["auth_types"]["http"],
                "content_key_timeout": data["content_key_timeout"],
                "service_id": "nicovideo",
                "service_user_id": data["service_user_id"]
            },
            "content_id": data["content_id"],
            "content_src_id_sets": [
                {
                    "content_src_ids": [
                        {
                            "src_id_to_mux": {
                                "audio_src_ids": [
                                
                                ],
                                "video_src_ids": [
                                
                                ]
                            }
                        }
                    ]
                }
            ],
            "content_type": "movie",
            "content_uri": "",
            "keep_method": {
                "heartbeat": {
                    "lifetime": data["heartbeat_lifetime"]
                }
            },
            "priority": data["priority"],
            "protocol": {
                "name": data["protocols"][0],
                "parameters": {
                    "http_parameters": {
                        "parameters": { 
                            "http_output_download_parameters": {
                                "use_ssl": "yes",
                                "use_well_known_port": "yes"
                            }
                        }
                    }
                }
            },
            "recipe_id": data["recipe_id"],
            "session_operation_auth": {
                "session_operation_auth_by_signature": {
                    "signature": data["signature"],
                    "token": data["token"]
                }
            },
            "timing_constraint": "unlimited"
        }
    }

    for audio in data["audios"]:
        postData["session"]["content_src_id_sets"][0]["content_src_ids"][0]["src_id_to_mux"]["audio_src_ids"].append(audio)

    for video in data["videos"]:
            postData["session"]["content_src_id_sets"][0]["content_src_ids"][0]["src_id_to_mux"]["video_src_ids"].append(video)
   
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(postEndpoint, headers=headers, data=json.dumps(postData))
    response_data = response.json()

    return response_data


def create_niconico_session(request_data):
    session_id = request_data["data"]["session"]["id"]
    url = f"https://api.dmc.nico/api/sessions/{session_id}?_format=json&_method=PUT"
    requests.options(url)
    headers = {
        "Content-Type": "application/json"
    }
    response_data = (
        requests.post(
            url,
            headers=headers,
            data=json.dumps(request_data["data"])
        )
    )

    return response_data.json()
