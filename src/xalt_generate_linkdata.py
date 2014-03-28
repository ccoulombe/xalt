#!/usr/bin/env python
# -*- python -*-
from __future__  import print_function
import os, sys, re, json, socket, subprocess

parenPat  = re.compile(r'.*\((.*)\).*')
tmpObjPat = re.compile(r'/tmp/[_a-zA-Z0-9-]+.o')

def cleanup(xaltobj, fn):
  f     = open(fn,"r")
  lines = f.readlines()
  d     = {}
  for s in lines:

    # remove lines with ':'
    if (s.find(":")     != -1):
      continue

    # remove line with the xalt.o file
    if (s.find(xaltobj) != -1):
      continue

    # remove a file that is something like: /tmp/ccT33qQt.o
    m = tmpObjPat.search(s)
    if (m):
      continue

    # Capture the library name in the parens:
    # -lgcc_s (/usr/lib/gcc/x86_64-linux-gnu/4.8/libgcc_s.so)
    m = parenPat.search(s)
    if (m):
      s    = os.path.abspath(m.group(1))
      d[s] = True
      continue
  
    # Save everything else
    idx = s.find("\n")
    if (idx != -1):
      s = s[:idx]

    s = os.path.abspath(s)
    d[s] = True

  # make the list unique  
  sA = d.keys()
  
  sA = sorted(sA)

  return sA
    
def capture(cmd):
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE,  stderr=subprocess.STDOUT)
  return p.communicate()[0]
  
def main():
  uuid        = sys.argv[1]
  status      = sys.argv[2]
  wd          = sys.argv[3]
  execname    = sys.argv[4]
  xaltobj     = sys.argv[5]
  build_epoch = sys.argv[6]
  linklineFn  = sys.argv[7]
  resultFn    = sys.argv[8]

  if (execname.find("conftest") != -1):
    return 1
  
  hash_line   = capture(['sha1sum', execname])
  if (hash_line.find("No such file or directory") != -1):
    return 1
  hash_id     = hash_line.split()[0]

  # Step one clean up linkline data
  sA = cleanup(xaltobj, linklineFn)
  
  resultT                = {}
  resultT['uuid']        = uuid
  resultT['build_user']  = os.environ['USER']
  resultT['exit_code']   = status
  resultT['build_epoch'] = build_epoch
  resultT['exec_path']   = os.path.abspath(execname)
  resultT['hash_id']     = hash_id
  resultT['wd']          = wd
  resultT['build_host']  = socket.getfqdn()
  resultT['linkA']       = sA
  
  dirname,fn = os.path.split(resultFn)

  tmpFn      = os.path.join(dirname, "." + fn)

  try:
    if (not os.path.isdir(dirname)):
      os.mkdir(dirname);
    
    s = json.dumps(resultT, sort_keys=True, indent=2, separators=(',',': '))

    f = open(tmpFn,'w')
    f.write(s)
    f.write("\n")

    if (hash_line.find("sha1sum:") != -1):
      f.write(hash_line)

    f.close()
    os.rename(tmpFn, resultFn)
  except (OSError):
    print("failed")

  return 0

if ( __name__ == '__main__'):
  iret = main()
  sys.exit(iret)
