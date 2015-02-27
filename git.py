from Commando.plugin import CommandoRun, CommandoCmd
from .vcs import VcsRepoCommando, VcsFileCommando
from Commando import core as commando_core
import re
import os

class GitRepoCommando(VcsRepoCommando):
  def is_enabled(self, context=None):
    return self.get_type(context=context) == 'git'

class GitRepoCommando(VcsFileCommando):
  def is_enabled(self, context=None):
    return (
      self.get_view(context=context) is not None
      and self.get_view(context=context).file_name() is not None
      and self.get_type(context=context) == 'git'
    )

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

class CommandoGitLogRepoCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['git', 'log']}],
      ['commando_new_file', {'syntax': 'Packages/CommandoVCS/GitLog.tmLanguage', 'readonly': True, 'scratch': True, 'name': 'GIT_LOG_REPO'}]
    ]

class CommandoGitCheckoutFileCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_ok_cancel_dialog', {'msg': 'Are you sure?\n\nThis will wipe out all local changes and cannot be undone.'}],
      ['commando_exec', {'cmd': ['git', 'checkout', '$file']}]
    ]

class CommandoGitLogFileCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['git', 'log', '$file']}],
      ['commando_new_file', {'syntax': 'Packages/CommandoVCS/GitLog.tmLanguage', 'readonly': True, 'scratch': True, 'name': 'GIT_LOG_FILE'}]
    ]

class CommandoGitAddFileCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['git', 'add', '$file']}]
    ]

class CommandoGitResetFileCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['git', 'reset', '$file']}]
    ]

class CommandoGitCommitCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['git', 'diff', '--cached']}],
      ['commando_switch', {
        '': [['commando_show_panel', {'input': 'No changes.'}]],
        'default': [
          ['commando_exec', {'cmd': ['git', 'status']}],
          'commando_git_prep_commit_prompt',
          ['commando_new_file', {'scratch': True, 'name': 'GIT_COMMIT'}],
          'commando_git_prep_commit_message',
          ['commando_exec', {'cmd': ['git', 'commit', '-m', '$input']}],
          'commando_show_panel'
        ]
      }]
    ]

class CommandoGitPushCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['git', 'push']}],
      'commando_show_panel'
    ]

class CommandoGitPullCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['git', 'pull']}],
      'commando_show_panel'
    ]

class CommandoGitBlameCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['git', 'blame', '--date=short', '-w', '$file']}],
      ['commando_new_file', {'syntax': 'Packages/CommandoVCS/GitBlame.tmLanguage', 'readonly': True, 'scratch': True, 'name': 'GIT_BLAME_FILE'}]
    ]

#

# Helpers
#

class CommandoGitParseStatus(CommandoCmd):
  def cmd(self, context, input, args):
    if not input:
      context['commands'] = [
        ["commando_show_panel", {"input": "No changes."}]
      ]
    else:
      context['input'] = input.splitlines()

class CommandoGitStatusSelected(CommandoCmd):
  def cmd(self, context, input, args):
    tokens = re.split('\s+', input.strip())
    if tokens and tokens[1] and os.path.exists(self.get_path(context, tokens[1])):
      commando_core.open_file(context, self.get_path(context, tokens[1]))

class CommandoGitPrepCommitPrompt(CommandoCmd):
  def cmd(self, context, input, args):
    context['input'] = "\n" \
      + "# Enter a commit message above.  Any lines beginning with # are ignored.  A blank message will abort the commit.\n" \
      + "#\n" \
      + "\n".join(map(lambda l: "# "+l if not l or l[0] != "#" else l, input.strip().split("\n")))

class CommandoGitPrepCommitMessage(CommandoCmd):
  def cmd(self, context, input, args):
    context['input'] = "\n".join(map(lambda l: l if not l or l[0] != "#" else "", input.strip().split("\n"))).strip()
    if not context['input']:
      return False
