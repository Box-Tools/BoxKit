"""Module with implementation of Server utility"""

import paramiko


class Server(paramiko.SSHClient):
    """
    Server class implementation for remote data access
    """

    def __init__(self, **attributes):
        """
        Constructor for the class

        Arguments
        ---------
        hostname : ip address of host/server
        username : username
        """
        super().__init__()
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self._set_attributes(attributes)

    def __getitem__(self, key):
        """
        Getter
        """
        return getattr(self, "_" + key)

    def _set_attributes(self, attributes):
        """
        Private method for intialization
        """

        self._hostname = None
        self._username = None

        for key, value in attributes.items():
            if hasattr(self, "_" + key):
                setattr(self, "_" + key, value)
            else:
                raise ValueError(
                    "[boxkit.library.utilities.Server] "
                    + f'Attribute "{key}" not present in class Server'
                )

    def connect(self):
        """
        Method to connect to the server
        """
        super().connect(self._hostname, username=self._username)
        self._sftp = self.open_sftp()

    def close(self):
        """
        Method to close server connections
        """
        self._sftp.close()
        super().close()
