import PyInstaller.__main__

if __name__ == '__main__':
    PyInstaller.__main__.run([
        '--name=%s' % 'main',
        '-F',
        #'-w',
        r'--workpath=C:\pack',
        r'--distpath=C:\v1.0',
	r'--icon=./src/icon.ico',
        # '--hidden-import=',
        # '--clean',
        # '--add-data={0};.'.format('redacted.xml'),
        # '--exclude-module={0}'.format('.git'),
        '--log-level=WARN',
        'main.py'
    ])