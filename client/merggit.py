import praw
import sys
import subprocess
import re

subreddit_name = 'merggit_testing'

if 'push' in sys.argv:
  print "Push to remote!"

  r = praw.Reddit(user_agent='merggit')
  r.login()

  subreddit = r.get_subreddit(subreddit_name)

  # extract change-id somehow

  # get the diff
  p = subprocess.Popen(['git', 'diff', 'HEAD'], stdout=subprocess.PIPE)
  patch = p.communicate()[0]

  patch_lines = patch.splitlines()
  patch_string = '\n'.join(['    ' + line for line in patch_lines])

  p = subprocess.Popen(['git', 'log', '--oneline', '-1'], stdout=subprocess.PIPE)
  commit_info = p.communicate()[0].split()

  # post on reddit with the patch

  title = "[%s]: %s"%(commit_info[0], " ".join(commit_info[1:]))
  contents = patch

  submit_result = r.submit(subreddit, title, text=patch_string)

  print submit_result.url


