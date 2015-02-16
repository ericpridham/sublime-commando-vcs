from Commando.plugin import ApplicationCommando, TextCommando, WindowCommando
from Commando.core import devlog
import re
import os

class CommandoSvnStatusCommand(WindowCommando):
  def cmd(self, context, input, args):
    self.commando(context, [
      ['commando_exec', {'cmd': ['svn', 'status']}],
      'commando_svn_parse_status',
      'commando_quick_panel',
      'commando_svn_status_selected'
    ])

class CommandoSvnDiffFileCommand(TextCommando):
  def cmd(self, context, input, args):
    self.commando(context, [
      ['commando_exec', {'cmd': ['svn', 'diff', '$file']}],
      ['commando_new_file', {'syntax': 'Diff', 'readonly': True, 'scratch': True, 'name': 'SVN_DIFF_FILE'}]
    ])

class CommandoSvnDiffRepoCommand(WindowCommando):
  def cmd(self, context, input, args):
    self.commando(context, [
      ['commando_exec', {'cmd': ['svn', 'diff']}],
      ['commando_new_file', {'syntax': 'Diff', 'readonly': True, 'scratch': True, 'name': 'SVN_DIFF_REPO'}]
    ])

#
# Helpers
#

class CommandoSvnParseStatus(ApplicationCommando):
  def cmd(self, context, input, args):
    if not input:
      return False
    return input.splitlines()

class CommandoSvnStatusSelected(ApplicationCommando):
  def cmd(self, context, input, args):
    tokens = re.split('\s+', input.strip())
    if tokens and tokens[1] and os.path.exists(self.get_path(tokens[1])):
      self.open_file(self.get_path(tokens[1]))
