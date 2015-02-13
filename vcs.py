from Commando import commando
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

class CommandoVcsStatusCommand(commando.WindowCommando):
  def cmd(self, input, args):
    vcs_type = get_vcs_type(self.get_working_dir())
    if vcs_type:
      self.commando(['commando_'+vcs_type+'_status'])

class CommandoVcsDiffFileCommand(commando.TextCommando):
  def cmd(self, input, args):
    vcs_type = get_vcs_type(self.get_working_dir())
    if vcs_type:
      self.commando(['commando_'+vcs_type+'_diff_file'])

class CommandoVcsDiffRepoCommand(commando.WindowCommando):
  def cmd(self, input, args):
    vcs_type = get_vcs_type(self.get_working_dir())
    if vcs_type:
      self.commando(['commando_'+vcs_type+'_diff_repo'])
