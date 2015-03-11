from Commando.plugin import CommandoRun, CommandoCmd
from Commando import core as commando_core
import os

def get_vcs_type(cur_dir):
  end = False
  while cur_dir and not end:
    if os.path.exists(cur_dir+'/.git'):
      return 'git'
    if os.path.exists(cur_dir+'/.svn'):
      return 'svn'
    if cur_dir == os.path.abspath(os.path.join(cur_dir, '..')):
      end = True
    else:
      cur_dir = os.path.abspath(os.path.join(cur_dir, '..'))
  return None

def get_redirect(command_obj):
  vcs_type = command_obj.get_type()
  if vcs_type is None:
    return []
  return

#
# Base
#
class VcsCommando(CommandoRun):
  def get_type(self, context=None):
    return get_vcs_type(self.get_path(context))

  def commands(self):
    """Magic!  Forward commando_vcs_* to commando_[type]_*."""
    vcs_type = self.get_type()
    if vcs_type is None:
      return []
    cmd = commando_core.class_to_command(type(self))
    if not cmd:
      return []
    # just being extra safe here
    cmd = cmd.replace('commando_vcs', 'commando_'+vcs_type)
    return [cmd]

class VcsRepoCommando(VcsCommando):
  def is_enabled(self, context=None):
    return self.get_type(context=context) is not None

class VcsFileCommando(VcsCommando):
  def is_enabled(self, context=None):
    return (
      self.get_view(context=context) is not None
      and self.get_view(context=context).file_name() is not None
      and self.get_type(context=context) is not None
    )

#
# Thinky commands
#
class CommandoVcsRevertFileCommand(VcsRepoCommando):
  def commands(self):
    vcs_type = self.get_type()
    if vcs_type == 'git':
      return ['commando_git_checkout_file']
    elif vcs_type == 'svn':
      return ['commando_svn_revert_file']
    return []

class CommandoVcsUpdateCommand(VcsRepoCommando):
  def commands(self):
    vcs_type = self.get_type()
    if vcs_type == 'git':
      return ['commando_git_pull']
    elif vcs_type == 'svn':
      return ['commando_svn_update']
    return []


#
# Forwarding Commands
#
class CommandoVcsStatusCommand(VcsRepoCommando):
  pass

class CommandoVcsDiffRepoCommand(VcsRepoCommando):
  pass

class CommandoVcsLogRepoCommand(VcsRepoCommando):
  pass

class CommandoVcsCommitCommand(VcsRepoCommando):
  pass

class CommandoVcsDiffFileCommand(VcsFileCommando):
  pass

class CommandoVcsLogFileCommand(VcsFileCommando):
  pass

class CommandoVcsBlameCommand(VcsFileCommando):
  pass
