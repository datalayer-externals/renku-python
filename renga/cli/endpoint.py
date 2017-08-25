# -*- coding: utf-8 -*-
#
# Copyright 2017 Swiss Data Science Center
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
"""Manage set of API endpoints."""

import datetime
import os

import click

from ._config import with_config


@click.group(invoke_without_command=True)
@click.option('-v', '--verbose', count=True)
@with_config
@click.pass_context
def endpoint(ctx, config, verbose):
    """Manage set of API endpoints."""
    if ctx.invoked_subcommand is None:
        # TODO default_endpoint = config.get('core', {}).get('default')
        for endpoint, values in config.get('endpoints', {}).items():
            # TODO is_default = default_endpoint == endpoint
            if not verbose:
                click.echo(endpoint)
            else:
                click.echo('{endpoint}\t{url}'.format(
                    endpoint=endpoint, url=values.get('url', '')))


@endpoint.command(name='set-default')
@click.argument('endpoint')
@with_config
@click.pass_context
def set_default(ctx, config, endpoint):
    """Set endpoint as default."""
    if endpoint not in config.get('endpoints', {}):
        click.UsageError('Unknown endpoint: {0}'.format(endpoint))

    config.setdefault('core', {})
    config['core']['default'] = endpoint