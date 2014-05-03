#!./bin/zopepy

print 'This script generates an avatar for the whole alphabet' + \
    ' with the default avatar generator.'
print ''

from time import time
import os
import sys


try:
    from ftw.avatar.default import DefaultAvatarGenerator
except ImportError, exc:
    print 'ImportError:', str(exc)
    print 'Please run the script with ./bin/zopepy test-generate-avatars.py'
    sys.exit(1)


from ftw.avatar.default import FREETYPE_MISSING
if FREETYPE_MISSING:
    print 'FAILURE: {0}'.format(FREETYPE_MISSING)
    sys.exit(1)


def names():
    for firstname in map(chr, range(97, 97+26)):
        for lastname in map(chr, range(97, 97+26)):
            yield (firstname, lastname)


target_directory = os.path.join(os.path.dirname(__file__),
                                'parts',
                                'example-avatars')
print 'Target directory:', target_directory
if not os.path.exists(target_directory):
    print '.. creating directory'
    os.makedirs(target_directory)
else:
    print '.. purging directory'
    for name in os.listdir(target_directory):
        os.unlink(os.path.join(target_directory, name))
print ''


generator = DefaultAvatarGenerator()
durations = []

for firstname, lastname in names():
    path = os.path.join(target_directory,
                        '%s%s.png' % (firstname, lastname))
    with open(path, 'w+') as output_file:
        print 'Creating', path, '...',
        start = time()
        generator.generate(' '.join((firstname, lastname)), output_file)
        duration = time() - start
        durations.append(duration)
        print 'in', duration, 'seconds'

print ''
print 'Done.'
print 'Created', len(durations), 'avatars'
print 'Average duration:', sum(durations) / len(durations), 'seconds'
print 'Min duration:', min(durations), 'seconds'
print 'Max duration:', max(durations), 'seconds'
print 'Trying to open the images...'
os.system('open %s/*.png' % target_directory)
