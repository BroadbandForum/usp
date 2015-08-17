#!/usr/bin/python
#
# trivial version of the Unix ls program to list a directory hierarchy with
# indentation and following soft links

import getopt, os, os.path, sys

options = {
    'check': False,
    'follow': False,
    'maxfollow': 5
}

state = {
    'visited': {}
}
    
# first argument is the parent path; second is the local directory name
def report_dir(parent, dir, indent=0, numfollow=0):
    check = options['check']
    follow = options['follow']
    maxfollow = options['maxfollow']

    islink = os.path.islink(os.path.join(parent, dir))

    # report directory
    (value, already) = readfile(parent, dir, islink)
    almsg = '*' if check and already else ''
    flmsg = '!' if numfollow > maxfollow else ''
    dot = '' if islink else '.'
    pre = ' = ' if value else ''
    suf = '' if value else ''
    print '%s%s%s%s%s%s%s%s' % ('  ' * indent, dir, dot, pre,
                                value, almsg, flmsg, suf)

    # check for already visited
    if check and already:
        return
    
    # check for too many follows
    if numfollow > maxfollow:
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
        report_file(dpath, file, indent+1)
    
    # report directories last
    for (dir, islink) in dirs:
        report_dir(dpath, dir, indent+1,
                   numfollow+1 if follow and islink else numfollow)

# first argument is the parent path; second is the local file name
def report_file(parent, file, indent):
    check = options['check']

    islink = os.path.islink(os.path.join(parent, file))

    (value, already) = readfile(parent, file, islink)
    almsg = '*' if check and already else ''
    print '%s%s = %s%s' % ('  ' * indent, file, value, almsg)

# read value of link (if link) or file (otherwise)
# XXX reading a link follows multiple levels of soft link, so subverts
#     maxfollow; should really do this by hand
def readfile(parent, file, islink):
    visited = state['visited']
    
    path = os.path.join(parent, file)
    ino = os.stat(path).st_ino
    already = visited.has_key(ino)
    if os.path.islink(path):
        value = os.readlink(path)
        value = os.path.relpath(os.path.abspath(os.path.join(parent, value)))
        value = value.replace('/', '.')
    elif os.path.isdir(path):
        value = ''
    else:
        value = '"%s"' % open(path, 'r').read().rstrip('\r\n')
    visited[ino] = True
    return (value, already)

# output usage
def usage():
    print 'Usage: %s [--check] [--follow] [--help] [dirs]' % sys.argv[0]
    print
    print '--check  check for (and avoid) duplicate results'
    print '--follow follow soft links (implied by --check)'
    print '--help   output help'
    print
    print 'dirs     directories to list; default "Device"'

# main program
if __name__ == '__main__':

    try:
        (opts, dirs) = getopt.getopt(sys.argv[1:],
                                     'cfhm:',
                                     ['check', 'follow', 'help', 'maxfollow'])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-c', '--check'):
            options['check'] = True
            options['follow'] = True
        elif o in ('-f', '--follow'):
            options['follow'] = True
        elif o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-m', '--maxfollow'):
            options['maxfollow'] = int(a)
        else:
            assert False, 'unhandled option'

    if len(dirs) == 0:
        dirs = ['Device']

    for dir in dirs:
        report_dir('', dir)
