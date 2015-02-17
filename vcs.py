from Commando.plugin import ApplicationCommando, TextCommando, WindowCommando
from Commando.core import devlog
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

class VcsRepoCommand(WindowCommando):
  def is_enabled(self):
    return get_vcs_type(self.get_working_dir()) is not None

class VcsFileCommand(TextCommando):
  def is_enabled(self):
    return (
      get_vcs_type(self.get_working_dir()) is not None
      and self.get_view() is not None
      and self.get_view().file_name() is not None
    )


class CommandoVcsStatusCommand(VcsRepoCommand):
  def cmd(self, context, input, args):
    vcs_type = get_vcs_type(self.get_working_dir(context))
    if vcs_type:
      self.commando(context, ['commando_'+vcs_type+'_status'])

class CommandoVcsDiffFileCommand(VcsFileCommand):
  def cmd(self, context, input, args):
    vcs_type = get_vcs_type(self.get_working_dir(context))
    if vcs_type:
      self.commando(context, ['commando_'+vcs_type+'_diff_file'])

class CommandoVcsDiffRepoCommand(VcsRepoCommand):
  def cmd(self, context, input, args):
    vcs_type = get_vcs_type(self.get_working_dir(context))
    if vcs_type:
      self.commando(context, ['commando_'+vcs_type+'_diff_repo'])
