#!/usr/bin/env python
# -*- python -*-
#
# Git Version: @git@

#-----------------------------------------------------------------------
# XALT: A tool that tracks users jobs and environments on a cluster.
# Copyright (C) 2013-2014 University of Texas at Austin
# Copyright (C) 2013-2014 University of Tennessee
# 
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of 
# the License, or (at your option) any later version. 
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser  General Public License for more details. 
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA 02111-1307 USA
#-----------------------------------------------------------------------

from __future__ import print_function
import os, sys, re, MySQLdb

dirNm, execName = os.path.split(os.path.realpath(sys.argv[0]))
sys.path.append(os.path.realpath(os.path.join(dirNm, "../libexec")))

from XALTdb     import XALTdb
from xalt_util  import dbConfigFn
import argparse
class CmdLineOptions(object):
  """ Command line Options class """

  def __init__(self):
    """ Empty Ctor """
    pass
  
  def execute(self):
    """ Specify command line arguments and parse the command line"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbname",      dest='dbname', action="store",      default = "xalt", help="xalt")
    args = parser.parse_args()
    return args

def main():
  """
  This program upgrade the XALT database schema from 0.7.5 to 1.1.3
  """

  args     = CmdLineOptions().execute()
  configFn = dbConfigFn(args.dbname)

  if (not os.path.isfile(configFn)):
    dirNm, exe = os.path.split(sys.argv[0])
    fn         = os.path.join(dirNm, configFn)
    if (os.path.isfile(fn)):
      configFn = fn
    else:
      configFn = os.path.abspath(os.path.join(dirNm, "../site", configFn))
      
  xalt = XALTdb(configFn)
  db   = xalt.db()

  try:
    conn   = xalt.connect()
    cursor = conn.cursor()

    # If MySQL version < 4.1, comment out the line below
    cursor.execute("SET SQL_MODE=\"NO_AUTO_VALUE_ON_ZERO\"")
    cursor.execute("USE "+xalt.db())

    idx = 1

    print("start")
    
     ALTER TABLE xalt_link ADD COLUMN cwd varchar(1024) NULL AFTER link_line
    
    # 1
    cursor.execute("""
        ALTER TABLE `xalt_link`
          ADD COLUMN `cwd`  varchar(1024) NULL AFTER `link_line`
          """)
    print("(%d) upgraded xalt_link table" % idx); idx += 1
    
    cursor.close()
  except  MySQLdb.Error as e:
    print ("Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit (1)

if ( __name__ == '__main__'): main()
