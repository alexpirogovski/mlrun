# Copyright 2023 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests

from mlrun.genai.actions import IngestItem, ingest
from mlrun.genai.config import config, logger
from mlrun.utils.helpers import dict_to_json


class Client:
    def __init__(self, base_url, username=None, token=None):
        self.base_url = base_url
        self.username = username or "guest"
        self.token = token

    def post_request(
        self, path, data=None, params=None, method="GET", files=None, json=None
    ):
        # Construct the URL
        url = f"{self.base_url}/api/{path}"
        logger.debug(
            f"Sending {method} request to {url}, params: {params}, data: {data}"
        )
        kw = {
            key: value
            for key, value in (
                ("params", params),
                ("data", data),
                ("json", json),
                ("files", files),
            )
            if value is not None
        }
        if data is not None:
            kw["data"] = dict_to_json(kw["data"])
        if params is not None:
            kw["params"] = (
                {k: v for k, v in params.items() if v is not None} if params else None
            )
        # Make the request
        response = requests.request(
            method,
            url,
            headers={"x_username": self.username},
            **kw,
        )

        # Check the response
        if response.status_code == 200:
            # If the request was successful, return the JSON response
            return response.json()
        else:
            # If the request failed, raise an exception
            response.raise_for_status()

    def create_tables(self, drop_old=False, names=None):
        if names is None:
            names = []
        response = self.post_request(
            "tables", params={"drop_old": drop_old, "names": names}, method="POST"
        )
        return response["success"]

    def list_collections(self, owner=None, labels=None, output_mode=None):
        response = self.post_request(
            "collections",
            params={
                "owner": owner,
                "labels": labels,
                "mode": output_mode,
            },
        )
        return response["data"]

    def create_collection(self, name, **kwargs):
        if "name" not in kwargs:
            kwargs["name"] = name
        response = self.post_request(f"collection/{name}", data=kwargs, method="POST")
        return response["success"]

    def update_collection(self, name, **kwargs):
        response = self.post_request(f"collection/{name}", data=kwargs, method="PUT")
        return response["success"]

    def get_collection(self, name):
        response = self.post_request(f"collection/{name}")
        return response["data"]

    def run_pipeline(self, name, query, collection, session_id=None, filter=None):
        response = self.post_request(
            f"pipeline/{name or 'default'}/run",
            data={
                "question": query,
                "collection": collection,
                "session_id": session_id,
                "filter": filter,
            },
            method="POST",
        )
        data = response["data"]
        print(f"response: {response}")
        return data["answer"], data["sources"], data["returned_state"]

    # method to ingest a document
    def ingest(self, collection, path, loader, metadata=None, version=None):
        item = IngestItem(
            path=path,
            loader=loader,
            metadata=metadata,
            version=version,
        )
        return ingest(client=self, collection_name=collection, item=item)

    def get_session(self, session_id):
        response = self.post_request(f"session/{session_id}")
        return response

    def list_sessions(
        self, username=None, created_after=None, last=None, output_mode=None
    ):
        response = self.post_request(
            "sessions",
            params={
                "username": username,
                "created_after": created_after,
                "last": last,
                "mode": output_mode,
            },
        )
        return response

    def transcribe(self, audio_file):
        with open(audio_file, "rb") as af:
            response = self.post_request(
                "transcribe",
                files={"file": af},
                method="POST",
            )
            return response["data"]

    def create_user(self, username: str, email: str, full_name: str = None):
        response = self.post_request(
            f"user/{username}",
            data={"name": username, "email": email, "full_name": full_name},
            method="POST",
        )
        return response["success"]

    def get_user(self, username):
        response = self.post_request(f"user/{username}")
        return response["data"]

    def list_users(
        self, email: str = None, username: str = None, output_mode: str = None
    ):
        response = self.post_request(
            "users",
            params={
                "email": email,
                "username": username,
                "mode": output_mode,
            },
        )
        return response["data"]

    def create_session(
        self,
        name,
        username=None,
        agent_name=None,
        history=None,
        features=None,
        state=None,
    ):
        chat_session = {
            "name": name,
            "username": username,
            "agent_name": agent_name,
            "history": history,
            "features": features,
            "state": state,
        }
        response = self.post_request("session", data=chat_session, method="POST")
        return response["success"]

    def update_session(
        self,
        name,
        username=None,
        agent_name=None,
        history=None,
        features=None,
        state=None,
    ):
        chat_session = {
            "name": name,
            "username": username or self.username,
            "agent_name": agent_name,
            "history": history,
            "features": features,
            "state": state,
        }
        response = self.post_request(f"session/{name}", data=chat_session, method="PUT")
        return response["success"]


client = Client(base_url=config.api_url)
