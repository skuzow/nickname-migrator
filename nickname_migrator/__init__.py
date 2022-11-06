import nickname_migrator.commands as commands
import nickname_migrator.utils as utils
from mcdreforged.api.all import *

plugin_metadata = utils.get_plugin_metadata()


prefix = '!!nickm'
description = plugin_metadata.description
help_message = '''
--- MCDR {1} v{2} ---
- {3} plugin
§7{0} migrate §6[old_username] §6[new_username] §rMigrate data from one player to another
§7{0} reload §rReload plugin itself
'''.strip().format(prefix, plugin_metadata.name, plugin_metadata.version, description)


def on_load(server: PluginServerInterface, old):
    utils.load_config(None, server)
    server.register_help_message(prefix, description)
    register_commands(server)


def register_commands(server: PluginServerInterface):
    def get_usernames(callback):
        return Text('old_username').then(Text('new_username').runs(callback))
    server.register_command(
        Literal(prefix).
        requires(lambda src: src.has_permission(utils.get_config().minimum_permission_level)).
        on_error(RequirementNotMet, lambda src: src.reply(RText('Insufficient permission!', color=RColor.red)), handled=True).
        on_error(UnknownArgument, lambda src: src.reply(f'Parameter error! Please enter §7{prefix}§r to get plugin help'), handled=True).
        runs(lambda src: src.reply(help_message)).
        then(Literal('migrate').then(get_usernames(lambda src, ctx: commands.nickname_migrate(src, ctx['old_username'], ctx['new_username'])))).
        then(Literal('reload').runs(commands.reload_plugin))
    )
