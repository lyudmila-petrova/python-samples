import json
import os
from typing import Optional, Dict
import click

import requests
import traceback

from util.log_util import get_logger


class InitIndexCommand:

    def __init__(self, elastic_url: str, index_name: str, index_settings_dir: str, debug_dir: str):
        self.elastic_url = elastic_url
        self.index_name = index_name
        self.index_settings_dir = index_settings_dir
        self.debug_dir = debug_dir

        self.logger = get_logger(self.__class__.__name__)

    @property
    def headers(self):
        return {'content-type': 'application/json'}

    def execute(self):

        index_url = "{}{}" . format(self.elastic_url, self.index_name)
        requests.delete(index_url, headers=self.headers)

        settings: Dict[str, any] = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }

        analysis_settings_path = os.path.join(self.index_settings_dir, 'analysis.json')
        analysis = self.settings_from_file(analysis_settings_path)

        if analysis is not None:
            print(f"Using of analysis settings from {analysis_settings_path}")
            settings["settings"]["analysis"] = analysis

        mappings_settings_path = os.path.join(self.index_settings_dir, 'mappings.json')
        mappings = self.settings_from_file(mappings_settings_path)

        if mappings is not None:
            print(f"Using of mapping settings from {mappings_settings_path}")
            settings["mappings"] = mappings

        response = requests.put(index_url, data=json.dumps(settings), headers=self.headers)

        self.debug(settings)

        if response.status_code == 200:
            click.echo(click.style('Success on index create', fg="green"))
        else:
            click.echo(click.style('Error on index create', fg="red"))

        click.echo(f'Index name is {self.index_name}')

    def settings_from_file(self, file_path) -> Optional[dict]:
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(traceback.format_exc())
            click.echo(click.style(str(e), fg="red"))
            return None

    def debug(self, settings):
        debug_file_path = os.path.join(self.debug_dir, "{}.json" . format(self.index_name))
        with open(debug_file_path, 'w') as f:
            f.write(json.dumps(settings, indent=2, ensure_ascii=False))
            click.echo(f"Index settings dumped into {debug_file_path}")
