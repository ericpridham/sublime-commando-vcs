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
    return [
      ['commando_exec', {'cmd': ['svn', 'diff']}],
      ['commando_new_file', {'syntax': 'Diff', 'readonly': True, 'scratch': True, 'name': 'SVN_DIFF_REPO'}]
    ]

class CommandoSvnDiffRevisionCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_input_panel', {'caption': 'Revision'}],
      ['commando_exec', {'cmd': ['svn', 'diff', '-c', '$input']}],
      ['commando_new_file', {'syntax': 'Diff', 'readonly': True, 'scratch': True, 'name': 'SVN_DIFF_REV'}]
    ]

class CommandoSvnRevertFileCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_ok_cancel_dialog', {'msg': 'Are you sure?\n\nThis will wipe out all local changes and cannot be undone.'}],
      ['commando_exec', {'cmd': ['svn', 'revert', '$file']}]
    ]

class CommandoSvnLogFileCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['svn', 'log', '$file']}],
      ['commando_new_file', {'syntax': 'Packages/CommandoVCS/SvnLog.tmLanguage', 'readonly': True, 'scratch': True, 'name': 'SVN_LOG_FILE'}]
    ]

class CommandoSvnCommitCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['svn', 'status']}],
      ['commando_switch', {
        '': [['commando_show_panel', {'input': 'No changes.'}]],
        'default': [
          ['commando_exec', {'cmd': ['svn', 'status']}],
          'commando_svn_prep_commit_prompt',
          ['commando_new_file', {
            'scratch': True,
            'name': 'SVN_COMMIT',
            'on_close': [
              'commando_svn_prep_commit_message',
              ['commando_exec', {'cmd': ['svn', 'commit', '-m', '$input']}],
              'commando_show_panel'
            ]
          }],
        ]
      }]
    ]

class CommandoSvnBlameCommand(CommandoRun):
  def commands(self):
    return [
      ['commando_exec', {'cmd': ['svn', 'blame', '$file']}],
      ['commando_new_file', {'syntax': 'Packages/CommandoVCS/SvnBlame.tmLanguage', 'readonly': True, 'scratch': True, 'name': 'SVN_BLAME_FILE'}]
    ]

#
# Helpers
#

class CommandoSvnParseStatus(CommandoCmd):
  def cmd(self, context, input, args):
    if not input:
      context['commands'] = [
        ["commando_show_panel", {"input": "No changes."}]
      ]
    else:
      context['input'] = input.splitlines()

class CommandoSvnStatusSelected(CommandoCmd):
  def cmd(self, context, input, args):
    tokens = re.split('\s+', input.strip())
    if tokens and tokens[1] and os.path.exists(self.get_path(context, tokens[1])):
      commando_core.open_file(context, self.get_path(context, tokens[1]))

class CommandoSvnPrepCommitPrompt(CommandoCmd):
  def cmd(self, context, input, args):
    context['input'] = "\n" \
      + "# Enter a commit message above.  Any lines beginning with # are ignored.  A blank message will abort the commit.\n" \
      + "#\n" \
      + "\n".join(map(lambda l: "# "+l if not l or l[0] != "#" else l, input.strip().split("\n")))

class CommandoSvnPrepCommitMessage(CommandoCmd):
  def cmd(self, context, input, args):
    context['input'] = "\n".join(map(lambda l: l if not l or l[0] != "#" else "", input.strip().split("\n"))).strip()
    if not context['input']:
      return False
