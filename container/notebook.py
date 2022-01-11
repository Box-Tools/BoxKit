import pymaple
import os

if __name__ == "__main__":
    """
    Launch the local container with jupyter notebook
    """

    basedir = os.getenv('PWD')+'/..'

    # Publish container for use with other applications
    bubblebox = pymaple.Maple(image='akashdhruv/bubblebox:latest',container='bubblebox',
                              source=basedir,target='/home/mount/bubblebox')

    bubblebox.build()
    bubblebox.pour()
    bubblebox.execute('./setup develop && ./setup clean && \
                       jupyter notebook --port=8888 --no-browser --ip=0.0.0.0')
    bubblebox.rinse()
    bubblebox.clean()
    bubblebox.remove()
