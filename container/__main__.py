import pymaple
import os

def run_container(basedir):

    # Publish container for use with other applications
    bubblebox = pymaple.Maple(image='akashdhruv/bubblebox:latest',container='bubblebox',
                          source=basedir,target='/home/mount/bubblebox')

    bubblebox.build()
    bubblebox.pour()
    bubblebox.execute('"./setup develop && ./setup clean && python3 tests/container && \
                         /home/user/.local/bin/jupyter notebook --port=8888 --no-browser --ip=0.0.0.0"')
    bubblebox.clean()

if __name__ == "__main__":
    basedir = os.getenv('PWD')
    os.chdir(basedir + '/container')
    run_container(basedir)
