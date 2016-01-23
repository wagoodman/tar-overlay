# Tar-Overlay
A shell script which creates and manages named overlayfs mounts backed by the contents from tar files.

Note: this is a work in progress, so it is not stable yet.

## Example
Given a tar with a set of files, create two independent scratch 'instances' where you can add, modify,
and delete files that can be reverted on command:

1) install a tar, this becomes an immutable 'image':
```
[wagoodman@vm1 ~]$ tar-overlay install-image ~/Downloads/msgpack-python-0.4.6.tar.gz
[wagoodman@vm1 ~]$ tar-overlay list-images
   msgpack-python-0.4.6
```

2) create a few instances and mount them:
```
[wagoodman@vm1 ~]$ tar-overlay create-overlay foo msgpack-python-0.4.6
[wagoodman@vm1 ~]$ tar-overlay create-overlay bar msgpack-python-0.4.6
[wagoodman@vm1 ~]$ tar-overlay list-overlays
   scratch1
   scratch2

[wagoodman@vm1 ~]$ tar-overlay mount-overlay foo
   ~/bin/tar-overlay/store/instances/foo/rootfs

[wagoodman@vm1 ~]$ tar-overlay mount-overlay bar
   ~/bin/tar-overlay/store/instances/bar/rootfs
```
Note: the output for each mount attempt is where the instance mountpoint is.

3) Make some changes in one of the instances (foo):
```
[wagoodman@vm1 ~]$ tree -L 1 ~/bin/tar-overlay/store/instances/foo/rootfs
~/bin/tar-overlay/store/instances/foo/rootfs
├── COPYING
├── msgpack
├── PKG-INFO
├── README.rst
├── setup.py
└── test

2 directories, 4 files

[wagoodman@vm1 ~]$ rm -rf ~/bin/tar-overlay/store/instances/foo/rootfs/test
```

Notice that we can query which files have changed:
```
[wagoodman@vm1 ~]$ tar-overlay show-changes foo
.
└── test
    ├── test_buffer.py
    ├── test_case.py
    ├── test_except.py
    ├── test_extension.py
    ├── test_format.py
    ├── test_limits.py
    ├── test_newspec.py
    ├── test_obj.py
    ├── test_pack.py
    ├── test_read_size.py
    ├── test_seq.py
    ├── test_sequnpack.py
    ├── test_subtype.py
    ├── test_unpack.py
    └── test_unpack_raw.py

1 directories, 15 files
```

Also notice that the other instance (bar) still has the original file:
```
[wagoodman@vm1 ~]$ tree -L 1 ~/bin/tar-overlay/store/instances/bar/rootfs
~/bin/tar-overlay/store/instances/bar/rootfs
├── COPYING
├── msgpack
├── PKG-INFO
├── README.rst
├── setup.py
└── test

2 directories, 4 files

[wagoodman@vm1 ~]$ rm -rf ~/bin/tar-overlay/store/instances/bar/rootfs/test
```
(See, the 'test' dir is still there)

4) Restore the 'foo' instance back to the original contents from the tar:
```
[wagoodman@vm1 ~]$ tar-overlay reset-overlay foo
[wagoodman@vm1 ~]$ tree -L 1 ~/bin/tar-overlay/store/instances/foo/rootfs
~/bin/tar-overlay/store/instances/foo/rootfs
├── COPYING
├── msgpack
├── PKG-INFO
├── README.rst
├── setup.py
└── test

2 directories, 4 files

```

# Motivation
The motivation for this was to take a read-only directory tree and make several
read-write 'instances' of that directory tree, where changes made in each instance would
not affect files in the other instances. Furthermore, there were benefits with
having the functionality to restore any instance to the original directory tree,
as if no modifications were done. This could all be done by making copies of the
tar contents for each instance, however, some of these directory trees were 1 GB
or more in size and only a few files are modified between all of the instances.

Docker provides almost the same functionality via dockerfiles, however, I am
not using docker for this project... so building and managing images this way seemed
awkward if I wasn't planning to use docker for containers. Instead, since overlayfs
has been integrated into the kernel and a wrapper script seemed simple enough to
make, tar-overlay was born!

# Usage
```
tar-overlay [command] [options]

Image commands:
    install-image <tar-file>   Take the given tar and make it available as in immutable image.
    list-images                List all known images.

Overlay Commands:
    create <name> <image-name>  Instantiate an image (make an instance).
    list                        List image instantiations.
    mount  <name>               Mount an instantiation for use.
    mount-all                   Mount all overlays.
    info <name>                 Show all information regardin the given overlay name.
    rename <name> <new name>    Rename the given instantiation.
    reset <name>                Undo all changes made to original image.
    show-changes <name>         Show a tree of all modified files
    status <name>               Shows if the given overlay is mounted.
    umount <name>               Unmount an instantiation.
    unmount-all                 Unmount all overlays.

Future Commands:
    rename-image <iamge-name>    Rename the given image.
    delete-image <image-name>    Delete the given image.
    mount-image                  Mounts an image directly (not advised).
    umount-image                 Unmounts a directly mounted image.
    delete <name>                Delete the given instantiation.
```
