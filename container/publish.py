import pymaple
import os

def publish_image(basedir):

    # Publish container for use with other applications
    bubblebox = pymaple.Maple(image='akashdhruv/bubblebox:latest',container='bubblebox',
                          source=basedir,target='/home/mount/bubblebox')

    bubblebox.build()
    bubblebox.pour()
    bubblebox.execute('"./setup develop && ./setup build && ./setup install && ./setup clean"')
    bubblebox.commit()
    bubblebox.push('akashdhruv/bubblebox:publish')
    bubblebox.clean()

if __name__ == "__main__":
    basedir = os.getenv('PWD')+'/..'
    publish_image(basedir)
