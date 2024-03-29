import json
import os
from typing import Optional

from mcdreforged.api.all import *

plugin_metadata = ServerInterface.get_instance().as_plugin_server_interface().get_self_metadata()


class Config(Serializable):
    minimum_permission_level: int = 2


config: Optional[Config] = None


def get_plugin_metadata():
    return plugin_metadata


def load_config(source: Optional[CommandSource], server: PluginServerInterface):
    global config
    config_file_path = os.path.join('config', '{}.json'.format(plugin_metadata.id))
    config = server.load_config_simple(config_file_path, in_data_folder=False, source_to_reply=source,
                                       echo_in_console=False, target_class=Config)


def get_config():
    return config


def send_info(source: CommandSource, message):
    source.reply(RText(message, color=RColor.green))
    if source.is_player:
        source.get_server().logger.info(message)


def send_warning(source: CommandSource, message):
    source.reply(RText(message, color=RColor.gold))
    if source.is_player:
        source.get_server().logger.warning(message)


def send_error(source: CommandSource, message, error):
    source.reply(RText(message, color=RColor.red))
    if source.is_player:
        source.get_server().logger.error(message)
    if error is not None:
        source.get_server().logger.error(error)


def find_file(source: CommandSource, file_path):
    # check if file with path given exists
    if os.path.isfile(file_path):
        return True
    send_error(source, f'Couldn\'t found file: {file_path}', None)
    return False


def load_file(source: CommandSource, file_path):
    try:
        # open, load & close file in read mode
        read_file = open(file_path, 'r')
        file_json = json.load(read_file)
        read_file.close()
        return file_json
    except Exception as error:
        send_error(source, f'Couldn\'t load file: {file_path}', error)


def dump_file(source: CommandSource, file_path, file_json):
    try:
        # open file in write mode
        write_file = open(file_path, 'w')
        # save changes into the file in the disk, then closes it
        json.dump(file_json, write_file, indent=2)
    except Exception as error:
        send_error(source, f'Couldn\'t dump file: {file_path}', error)
