
SUBDIRS = evas_op_add evas_op_blend evas_op_copy evas_op_mask evas_op_mul evas_op_sub

MAINTAINERCLEANFILES = Makefile.in

AM_CPPFLAGS	     = -I. \
		       -I$(top_srcdir)/src/lib \
		       -I$(top_srcdir)/src/lib/cserve \
		       -I$(top_srcdir)/src/lib/cserve2 \
		       -I$(top_srcdir)/src/lib/include \
		       -DPACKAGE_BIN_DIR=\"$(bindir)\" \
		       -DPACKAGE_LIB_DIR=\"$(libdir)\" \
		       -DPACKAGE_DATA_DIR=\"$(datadir)/$(PACKAGE)\" \
		       @FREETYPE_CFLAGS@ @VALGRIND_CFLAGS@ \
                       @PIXMAN_CFLAGS@ \
		       @EET_CFLAGS@ @pthread_cflags@ \
		       @EVAS_GENERAL_CFLAGS@ \
                       @FRIBIDI_CFLAGS@ @HARFBUZZ_CFLAGS@ \
                       @PIXMAN_CFLAGS@

noinst_LTLIBRARIES      = libevas_engine_common.la
libevas_engine_common_la_SOURCES  = \
evas_op_copy_main_.c \
evas_op_blend_main_.c \
evas_op_add_main_.c \
evas_op_sub_main_.c \
evas_op_mask_main_.c \
evas_op_mul_main_.c \
evas_blend_main.c \
evas_blit_main.c \
evas_convert_color.c \
evas_convert_colorspace.c \
evas_convert_gry_1.c \
evas_convert_gry_4.c \
evas_convert_gry_8.c \
evas_convert_main.c \
evas_convert_rgb_16.c \
evas_convert_rgb_24.c \
evas_convert_rgb_32.c \
evas_convert_rgb_8.c \
evas_convert_grypal_6.c \
evas_convert_yuv.c \
evas_cpu.c \
evas_draw_main.c \
evas_font_draw.c \
evas_font_load.c \
evas_font_main.c \
evas_font_query.c \
evas_image_load.c \
evas_image_save.c \
evas_image_main.c \
evas_image_data.c \
evas_image_scalecache.c \
evas_line_main.c \
evas_polygon_main.c \
evas_rectangle_main.c \
evas_scale_main.c \
evas_scale_sample.c \
evas_scale_smooth.c \
evas_scale_span.c \
evas_tiler.c \
evas_regionbuf.c \
evas_pipe.c \
language/evas_bidi_utils.c \
language/evas_language_utils.c \
evas_text_utils.c \
evas_font_ot.c \
evas_map_image.c \
evas_map_image.h

EXTRA_DIST = \
evas_blend.h \
evas_blend_private.h \
evas_convert_color.h \
evas_convert_colorspace.h \
evas_convert_gry_1.h \
evas_convert_gry_4.h \
evas_convert_gry_8.h \
evas_convert_grypal_6.h \
evas_convert_main.h \
evas_convert_rgb_16.h \
evas_convert_rgb_24.h \
evas_convert_rgb_32.h \
evas_convert_rgb_8.h \
evas_convert_yuv.h \
evas_draw.h \
evas_font.h \
evas_font_default_walk.x \
evas_font_private.h \
evas_image.h \
evas_image_private.h \
evas_line.h \
evas_polygon.h \
evas_rectangle.h \
evas_scale_main.h \
evas_scale_smooth.h \
evas_scale_smooth_scaler.c \
evas_scale_smooth_scaler_down.c \
evas_scale_smooth_scaler_downx.c \
evas_scale_smooth_scaler_downx_downy.c \
evas_scale_smooth_scaler_downy.c \
evas_scale_smooth_scaler_noscale.c \
evas_scale_smooth_scaler_up.c \
evas_scale_span.h \
evas_pipe.h \
language/evas_bidi_utils.h \
language/evas_language_utils.h \
language/evas_script_table.h \
evas_text_utils.h \
evas_font_ot.h \
evas_map_image_internal.c \
evas_map_image_core.c \
evas_map_image_loop.c

libevas_engine_common_la_LIBADD = \
evas_op_blend/libevas_engine_common_op_blend_master_sse3.la
