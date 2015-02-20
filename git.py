from Commando.plugin import CommandoRun, CommandoCmd
from Commando import core as commando_core
import re
import os

class CommandoGitStatusCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['git', 'status', '--porcelain']}],
      'commando_git_parse_status',
      'commando_quick_panel',
      'commando_git_status_selected'
    ]

class CommandoGitDiffFileCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['git', 'diff', '$file']}],
      ['commando_new_file', {'syntax': 'Diff', 'readonly': True, 'scratch': True, 'name': 'GIT_DIFF_FILE'}]
    ]

class CommandoGitDiffRepoCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['git', 'diff']}],
      ['commando_new_file', {'syntax': 'Diff', 'readonly': True, 'scratch': True, 'name': 'GIT_DIFF_REPO'}]
    ]

#
# Helpers
#

class CommandoGitParseStatus(CommandoCmd):
  def cmd(self, context, input, args):
    if not input:
      return False
    context['input'] = input.splitlines()

class CommandoGitStatusSelected(CommandoCmd):
  def cmd(self, context, input, args):
    tokens = re.split('\s+', input.strip())
    if tokens and tokens[1] and os.path.exists(self.get_path(context, tokens[1])):
      commando_core.open_file(context, self.get_path(context, tokens[1]))
