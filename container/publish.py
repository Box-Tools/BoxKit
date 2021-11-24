import pymaple
import os

if __name__ == "__main__":
    """
    Publish container
    """
    basedir = os.getenv('PWD')+'/..'

    # Publish container for use with other applications
    bubblebox = pymaple.Maple(image='akashdhruv/ubuntu:user',container='bubblebox',
                          source=basedir,target='/home/mount/bubblebox')

    bubblebox.build()

    bubblebox.pour()
    bubblebox.execute('./setup develop && ./setup build && ./setup install && ./setup clean && \
                       pip3 install jupyter')
    bubblebox.commit()
    bubblebox.rinse()

    bubblebox.push('akashdhruv/bubblebox:publish')
    bubblebox.clean()
    bubblebox.remove()
