# Copyright (c) 2025 Jifeng Wu
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
import os
import os.path
import sys

if sys.version_info < (3, 5):
    from scandir import scandir
else:
    from os import scandir
from typing import MutableMapping


class DirectoryFileMapping(MutableMapping):
    """
    Mapping from file name to file contents in a directory.

    - Keys: filenames
    - Values: file contents (bytes)
    - Reads and writes files in binary mode
    - Reflects current state (volatile)
    - Exceptions from file access are not suppressed
    """
    __slots__ = ('absolute_directory_path',)

    def __init__(self, directory_path):
        self.absolute_directory_path = os.path.abspath(directory_path)

    def key_to_file_path(self, key):
        absolute_file_path = os.path.abspath(os.path.join(self.absolute_directory_path, key))
        if os.path.dirname(absolute_file_path) == self.absolute_directory_path:
            return absolute_file_path
        else:
            raise ValueError('Key %r does not map to a file directly inside the directory' % (key,))

    def __iter__(self):
        for entry in scandir(self.absolute_directory_path):
            if not entry.name.startswith('.') and entry.is_file():
                yield entry.name

    def __len__(self):
        return sum(1 for _ in self)

    def __contains__(self, key):
        file_path = self.key_to_file_path(key)
        return os.path.isfile(file_path)

    def __getitem__(self, key):
        file_path = self.key_to_file_path(key)
        with open(file_path, 'rb') as f:
            return f.read()

    def __setitem__(self, key, value):
        file_path = self.key_to_file_path(key)
        with open(file_path, 'wb') as f:
            f.write(value)

    def __delitem__(self, key):
        file_path = self.key_to_file_path(key)
        os.remove(file_path)
