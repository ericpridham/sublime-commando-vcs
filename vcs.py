from Commando.plugin import CommandoRun, CommandoCmd
import os

def get_vcs_type(cur_dir):
  end = False
  while not end:
    if os.path.exists(cur_dir+'/.git'):
      return 'git'
    if os.path.exists(cur_dir+'/.svn'):
      return 'svn'
    if cur_dir == os.path.abspath(os.path.join(cur_dir, '..')):
      end = True
    else:
      cur_dir = os.path.abspath(os.path.join(cur_dir, '..'))
  return None

#
# Base
#
class VcsCommando(CommandoRun):
  def get_type(self):
    return get_vcs_type(self.get_path())

class VcsRepoCommando(VcsCommando):
  def is_enabled(self):
    return self.get_type() is not None

class VcsFileCommando(VcsCommando):
  def is_enabled(self):
    return (
      self.get_type() is not None
      and self.get_view() is not None
      and self.get_view().file_name() is not None
    )

#
# Commands
#
class CommandoVcsStatusCommand(VcsRepoCommando):
  def commands(self):
    vcs_type = self.get_type()
    if vcs_type is None:
      return []
    return ['commando_'+vcs_type+'_status']

class CommandoVcsDiffRepoCommand(VcsRepoCommando):
  def commands(self):
    vcs_type = self.get_type()
    if vcs_type is None:
      return []
    return ['commando_'+vcs_type+'_diff_repo']

class CommandoVcsDiffFileCommand(VcsFileCommando):
  def commands(self):
    vcs_type = self.get_type()
    if vcs_type is None:
      return []
    return ['commando_'+vcs_type+'_diff_file']
