#!/usr/bin/python
#
# trivial version of the Unix ls program to list a directory hierarchy with
# indentation and following soft links
#
# XXX actually it's a bit more than ls... (and a lot less)

import getopt, os, os.path, sys

# first argument is the parent path; second is the local directory name
def report_dir(parent, dir, indent=0, follow=False, islink=False):

    # report directory
    # XXX append a dot because really we are simulating a data model
    link = readfile(parent, dir) if islink else ''
    link = ' (%s)' % link if link else ''
    print '%s%s.%s' % ('  ' * indent, dir, link)

    # check for too-deep recursion
    if indent > 10:
        print '%s... (too deep)' % ('  ' * indent)
        return

    # full directory path
    dpath = os.path.join(parent, dir)

    # collect separate lists of the directory's files and sub-directories
    files = []
    dirs = []
    for file in sorted(os.listdir(dpath)):
        fpath = os.path.join(dpath, file)
        islink = os.path.islink(fpath)
        if os.path.isfile(fpath) or (not follow and islink):
            files.append((file, islink))
        else:
            dirs.append((file, islink))

    # report files first
    for (file, islink) in files:
        report_file(dpath, file, indent+1, follow, islink)
    
    # report directories last
    for (dir, islink) in dirs:
        report_dir(dpath, dir, indent+1, follow, islink)

# first argument is the parent path; second is the local file name
def report_file(parent, file, indent=0, follow=False, islink=False):

    # report file
    value = readfile(parent, file)
    print '%s%s = %s' % ('  ' * indent, file, value)

# read value of link (if link) or file (otherwise)
def readfile(parent, file):
    path = os.path.join(parent, file)
    if os.path.islink(path):
        value = os.readlink(path)
    else:
        value = '"%s"' % open(path, 'r').read().rstrip('\r\n')
    return value

# main program
if __name__ == '__main__':

    try:
        (opts, dirs) = getopt.getopt(sys.argv[1:], 'fh', ['follow', 'help'])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    follow = False
    indent = 0
    for o, a in opts:
        if o in ('-f', '--follow'):
            follow = True
        elif o in ('-h', '--help'):
            usage()
            sys.exit()
        else:
            assert False, 'unhandled option'

    if len(dirs) == 0:
        dirs = ['Device']

    for dir in dirs:
        report_dir('', dir, indent, follow)
