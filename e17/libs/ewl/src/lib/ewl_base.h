/* vim: set sw=8 ts=8 sts=8 noexpandtab: */
/*
 * Header that wraps the core widget functionality includes to insure they are
 * included in the proper order.
 */
#ifndef EWL_BASE_H
#define EWL_BASE_H

#include <Ecore.h>
#include <Ecore_Data.h>

/* typedef to allow inclusion of ewl_filelist.h */
/* and ewl_filelist_model.h on Windows */
#ifdef _WIN32
typedef unsigned long uid_t;
typedef unsigned long gid_t;
#endif /* _WIN32 */

#include <ewl_enums.h>
#include <ewl_object.h>
#include <ewl_widget.h>
#include <ewl_attach.h>
#include <ewl_container.h>
#include <ewl_callback.h>
#include <ewl_events.h>
#include <ewl_misc.h>
#include <ewl_config.h>
#include <ewl_theme.h>
#include <ewl_cell.h>
#include <ewl_embed.h>
#include <ewl_window.h>
#include <ewl_engines.h>
#include <ewl_cursor.h>
#include <ewl_dnd.h>

#endif /* EWL_BASE_H */
