from Commando import commando
import re
import os

class CommandoSvnStatusCommand(commando.WindowCommando):
  def cmd(self, input, args):
    self.commando([
      ['commando_exec', {'cmd': ['svn', 'status']}],
      'commando_svn_parse_status',
      'commando_quick_panel',
      'commando_svn_status_selected'
    ])

class CommandoSvnDiffFileCommand(commando.TextCommando):
  def cmd(self, input, args):
    self.commando([
      ['commando_exec', {'cmd': ['svn', 'diff', '$file']}],
      ['commando_new_file', {'syntax': 'Diff', 'ro': True, 'scratch': True, 'name': 'SVN_DIFF_FILE'}]
    ])

class CommandoSvnDiffRepoCommand(commando.TextCommando):
  def cmd(self, input, args):
    self.commando([
      ['commando_exec', {'cmd': ['svn', 'diff']}],
      ['commando_new_file', {'syntax': 'Diff', 'ro': True, 'scratch': True, 'name': 'SVN_DIFF_REPO'}]
    ])

#
# Helpers
#

class CommandoSvnParseStatus(commando.ApplicationCommando):
  def cmd(self, input, args):
    if not input:
      return False
    return input.strip().splitlines()

class CommandoSvnStatusSelected(commando.ApplicationCommando):
  def cmd(self, input, args):
    tokens = re.split('\s+', input)
    if tokens and tokens[1] and os.path.exists(self.get_path(tokens[1])):
      self.open_file(self.get_path(tokens[1]))
