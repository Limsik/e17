MAINTAINERCLEANFILES = Makefile.in

AM_CPPFLAGS = @EIO_CFLAGS@ \
@EFL_PTHREAD_CFLAGS@ \
@EFL_EIO_BUILD@

lib_LTLIBRARIES = libeio.la

includes_HEADERS = Eio.h eio_inline_helper.x
includesdir = $(includedir)/eio-@VMAJ@

libeio_la_SOURCES = \
eio_dir.c \
eio_eet.c \
eio_file.c \
eio_main.c \
eio_map.c \
eio_monitor.c \
eio_monitor_poll.c \
eio_single.c \
eio_xattr.c

if EIO_HAVE_INOTIFY
libeio_la_SOURCES += eio_monitor_inotify.c
else
if EIO_HAVE_WINCHANGE
libeio_la_SOURCES += eio_monitor_win32.c
endif
endif

libeio_la_LIBADD = @EIO_LIBS@ @EFL_PTHREAD_LIBS@
libeio_la_LDFLAGS  = -no-undefined @lt_enable_auto_import@ -version-info @version_info@ @release_info@

EXTRA_DIST = eio_private.h
