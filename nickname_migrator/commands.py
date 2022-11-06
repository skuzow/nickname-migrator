import nickname_migrator.utils as utils
from mcdreforged.api.all import *


def nickname_migrate(source: PlayerCommandSource, old_username, new_username):
    utils.send_info(source, old_username)
    utils.send_info(source, new_username)


def reload_plugin(source: PlayerCommandSource):
    plugin_metadata = utils.get_plugin_metadata()
    if source.get_server().reload_plugin(plugin_metadata.id):
        utils.send_info(source, f'{plugin_metadata.name} plugin successfully reloaded!')
    else:
        utils.send_error(source, f'There was an error reloading {plugin_metadata.name} plugin', None)
