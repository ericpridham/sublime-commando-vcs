from Commando import commando
import re
import os

class CommandoGitStatusCommand(commando.WindowCommando):
  def cmd(self, input, args):
    self.commando([
      ['commando_exec', {'cmd': ['git', 'status', '--porcelain']}],
      'commando_git_parse_status',
      'commando_quick_panel',
      'commando_git_status_selected'
    ])

class CommandoGitDiffFileCommand(commando.TextCommando):
  def cmd(self, input, args):
    self.commando([
      ['commando_exec', {'cmd': ['git', 'diff', '$file']}],
      ['commando_new_file', {'syntax': 'Diff', 'ro': True, 'scratch': True, 'name': 'GIT_DIFF_FILE'}]
    ])

class CommandoGitDiffRepoCommand(commando.TextCommando):
  def cmd(self, input, args):
    self.commando([
      ['commando_exec', {'cmd': ['git', 'diff']}],
      ['commando_new_file', {'syntax': 'Diff', 'ro': True, 'scratch': True, 'name': 'GIT_DIFF_REPO'}]
    ])

#
# Helpers
#

class CommandoGitParseStatus(commando.ApplicationCommando):
  def cmd(self, input, args):
    if not input:
      return False
    return input.strip().splitlines()

class CommandoGitStatusSelected(commando.ApplicationCommando):
  def cmd(self, input, args):
    tokens = re.split('\s+', input)
    if tokens and tokens[1] and os.path.exists(self.get_path(tokens[1])):
      self.open_file(self.get_path(tokens[1]))
