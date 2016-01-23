Name:         tar-overlay
Version:      %{Version}
Release:      %{Release}
License:      None
BuildArch:    noarch
Summary:      Create and manage named, overlayfs mounts backed by the contents from tar files.

%description
Create and manage named, overlayfs mounts backed by the contents from tar files.

# Redifine rpmbuild system default macros
%define _basedir %(echo $PWD)
%define _topdir %{_basedir}/rpm
%define _buildrootdir %{_topdir}/BUILDROOT

## MACROS

# dirs
%define _prod_dir       /opt/tar-overlay
%define _bin_dir        /opt/tar-overlay/bin
%define _store_dir      /opt/tar-overlay/store
%define _image_dir      /opt/tar-overlay/store/images
%define _instances_dir  /opt/tar-overlay/store/instances

#%%prep
#%%setup
#%%build
#%%configure

%install
rm -rf %{_buildrootdir}
mkdir -p $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_prod_dir}
mkdir -p $RPM_BUILD_ROOT/%{_bin_dir}
mkdir -p $RPM_BUILD_ROOT/%{_store_dir}
mkdir -p $RPM_BUILD_ROOT/%{_image_dir}
mkdir -p $RPM_BUILD_ROOT/%{_instances_dir}
cp -r %{_basedir}/bin/*   $RPM_BUILD_ROOT/%{_bin_dir}

%clean

%files
%defattr(755, root, root, 755)

%{_prod_dir}/
%{_bin_dir}/
%{_store_dir}/

%pre
if [ "$1" = "1" ]; then
    # This is the initial installation.
    /bin/true

elif [ "$1" = "2" ]; then
    # This is an upgrade.
    /bin/true
fi

%post

if [ "$1" = "1" ]; then
    # This is the initial installation.

    # - When you open a terminal emulator (gnome-terminal for example), you
    #   are executing what is known as an interactive, non-login shell.
    # - When you log into your machine from the command line, via ssh, or run
    #   a command such as su user, you are running an interactive login shell.
    # - When you log in graphically you typically get a login shell. While
    #   many graphical shells will read /etc/profile not all of them do.
    # - When you run a shell script, it is run in a non-interactive, non-login shell.

    # Implications: if you want to use a binary via sudo, it must be on $PATH
    # to remain accessible, but /etc/profile is not always sourced (especially
    # by root, and not necessarily with non-interactive, non-login shells).
    # This means that you should link your binaries to /usr/bin for truly
    # ubiquitous access. (for use as is, with sudo, sudo -E, su, su - , etc.)

    # place bin on path
    ln -s %{_bin_dir}/tar-overlay /usr/bin/tar-overlay

elif [ "$1" = "2" ]; then
    # This is an upgrade.
    /bin/true
fi

%preun
if [ "$1" = "0" ]; then
    # The package is being removed.
    /bin/true

elif [ "$1" = "1" ]; then
    # This is an upgrade.
    /bin/true
fi

%postun
if [ "$1" = "0" ]; then
    # The package is being removed.

    # remove bin from path
    unlink /usr/bin/tar-overlay

elif [ "$1" = "1" ]; then
    # This is an upgrade.
    /bin/true
fi
