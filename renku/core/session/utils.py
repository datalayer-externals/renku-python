# -*- coding: utf-8 -*-
#
# Copyright 2018-2022- Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utility functions used for sessions."""
import urllib
from typing import Optional

from renku.command.command_builder import inject
from renku.core.interface.client_dispatcher import IClientDispatcher
from renku.core.util.git import get_remote
from renku.core.util.urls import parse_authentication_endpoint


@inject.autoparams()
def get_renku_project_name(client_dispatcher: IClientDispatcher) -> str:
    """Get the full name of a renku project."""
    client = client_dispatcher.current_client
    project_name = (
        f"{client.remote['owner']}/{client.remote['name']}" if client.remote["name"] else f"{client.path.name}"
    )
    if get_remote(client.repository, name="renku-backup-origin") and project_name.startswith("repos/"):
        project_name = project_name.replace("repos/", "", 1)
    return project_name


def get_renku_url() -> Optional[str]:
    """Derive the URL of the Renku deployment."""
    renku_url = parse_authentication_endpoint(use_remote=True)
    if renku_url:
        renku_url = urllib.parse.urlunparse(renku_url)
    return renku_url


def get_image_repository_host() -> Optional[str]:
    """Derive the hostname for the gitlab container registry."""
    renku_url = get_renku_url()
    if not renku_url:
        return None
    return "registry." + urllib.parse.urlparse(renku_url).netloc