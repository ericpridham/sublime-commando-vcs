from Commando.plugin import CommandoRun, CommandoCmd
from Commando import core as commando_core
import re
import os

class CommandoSvnStatusCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['svn', 'status']}],
      'commando_svn_parse_status',
      'commando_quick_panel',
      'commando_svn_status_selected'
    ]

class CommandoSvnDiffFileCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['svn', 'diff', '$file']}],
      ['commando_new_file', {'syntax': 'Diff', 'readonly': True, 'scratch': True, 'name': 'SVN_DIFF_FILE'}]
    ]

class CommandoSvnDiffRepoCommand(CommandoRun):
  def commands(self):
    self.commando(context, [
      ['commando_exec', {'cmd': ['svn', 'diff']}],
      ['commando_new_file', {'syntax': 'Diff', 'readonly': True, 'scratch': True, 'name': 'SVN_DIFF_REPO'}]
    ])

#
# Helpers
#

class CommandoSvnParseStatus(CommandoCmd):
  def cmd(self, context, input, args):
    if not input:
      return False
    context['input'] = input.splitlines()

class CommandoSvnStatusSelected(CommandoCmd):
  def cmd(self, context, input, args):
    tokens = re.split('\s+', input.strip())
    if tokens and tokens[1] and os.path.exists(self.get_path(context, tokens[1])):
      commando_core.open_file(context, self.get_path(context, tokens[1]))
