# `directory-file-mapping`

> Ever wanted to treat a directory as a Python dict? Now you can!

A simple Python class that lets you treat the files in a directory as a mapping object, like a dict. Filenames are keys,
and file contents (as bytes) are values. Changes you make to the mapping immediately update the actual files in
the filesystem. Yes, this works for reading, writing, listing, and deleting files, all using familiar mapping syntax!

It seems almost obvious in retrospect, but neither `collections`, `pathlib`, nor anyone in the Python community appears
to have shipped a general dict-like view of a directory. But now you never need to write a kludge of manual
`os.listdir`, `open()`, and `os.remove` loops again.

## Features

- **Mapping interface**: Get, set, iterate keys, and delete by key, just like a dict.
- **Filenames as keys**.
- **File contents as values** (bytes).
- **Acts instantly on the filesystem**: Any change is reflected (and visible to other processes) right away.
- **No caching**: Reads contents on every access, always up to date.

## Install

```bash
pip install directory-file-mapping
```

## Usage

```python
from directory_file_mapping import DirectoryFileMapping

# Initialize mapping to a directory
m = DirectoryFileMapping('/tmp/exampledir')

# Write new file
m['foo.txt'] = b'hello world'

# Read file contents
data = m['foo.txt']  # b'hello world'

# Check existence
if 'bar.txt' in m:
    print(m['bar.txt'])

# List filenames
for name in m:
    print(name)

# Delete a file
del m['foo.txt']
```

## Caveats & Limitations

- This mapping is **volatile**: other processes may add, remove, or change files under your feet.
- File names and contents are not cached.
- This mapping only exposes regular files, not subdirectories or special files.
- It does not filter out unusually named files or tamper with binary vs. text.
- No atomicity guarantees: if your coworker is deleting files while you iterate, expect surprises.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).