#!/usr/bin/env python

import os
from glob import glob

from fabric.api import *

def less():
  """
  Render .less files to .css
  """
  for path in glob('less/*.less'):
    filename = os.path.split(path)[-1]
    name = os.path.splitext(filename)[0]
    out_path = 'www/css/%s.css' % name

    local('node_modules/.bin/lessc %s %s' % (path, out_path))

def jst():
  """
  Render Underscore templates to a JST package.
  """
  local('node_modules/.bin/jst --template underscore jst www/js/templates.js')
