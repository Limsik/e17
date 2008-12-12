/* EXCHANGE - a library to interact with exchange.enlightenment.org
 * Copyright (C) 2008 Massimiliano Calamelli
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library;
 * if not, see <http://www.gnu.org/licenses/>.
 */
 
#ifndef _EXCHANGE_THEME_LIST_H
#define _EXCHANGE_THEME_LIST_H

/**
 * @file exchange_theme_list.h
 * @brief This file contains theme listing functions
 *
 * Sample code
 *
 * @code
 * Eina_List *l, *l1;
 * l = exchange_theme_list_all(0, 0);
 * printf("All themes available\n");
 * for (l1 = l; l1; l1 = eina_list_next(l1))
 * {
 *   if (l1->data)
 *   {
 *     Exchange_Theme *tld;
 *     tld = (Exchange_Theme *)l1->data;
 *     printf("Name: %s\n", (char *)tld->name);
 *   }
 * }
 * @endcode 
 *
 */

#ifdef HAVE_CONFIG_H
# include <config.h>
#endif

/**
 * @cond LOCAL
 */

typedef enum {
   PARSER_THEME_LIST_START,
   PARSER_THEME_LIST_RSP,
   PARSER_THEME_LIST,
   PARSER_THEME_LIST_NAME,
   PARSER_THEME_LIST_ID,
   PARSER_THEME_LIST_VERSION,
   PARSER_THEME_LIST_DESCRIPTION,
   PARSER_THEME_LIST_URL,
   PARSER_THEME_LIST_SCREENSHOT,
   PARSER_THEME_LIST_THUMBNAIL,
   PARSER_THEME_LIST_RATING,
   PARSER_THEME_LIST_UNKNOWN
} Theme_List_States;

typedef struct _Theme_List_Parser {
   Theme_List_States state;
   Theme_List_States prev_state;
} Theme_List_Parser;

/**
 * @endcond
 */


EAPI Eina_List *exchange_theme_list_filter_by_user_id(int user_id, int limit, int offset);
EAPI Eina_List *exchange_theme_list_filter_by_user_name(const char *user_name, int limit, int offset);
EAPI Eina_List *exchange_theme_list_filter_by_group_title(const char *group_title, int limit, int offset);
EAPI Eina_List *exchange_theme_list_filter_by_group_name(const char *group_name, int limit, int offset);
EAPI Eina_List *exchange_theme_list_filter_by_application_id(int application_id, int limit, int offset);
EAPI Eina_List *exchange_theme_list_filter_by_module_id(int module_id, int limit, int offset);
EAPI Eina_List *exchange_theme_list_all(int limit, int offset);

/**
 * @cond LOCAL
 */

// Callbacks for SAX parser
void _start_document_theme_list_cb(Theme_List_Parser *state);
void _end_document_theme_list_cb(Theme_List_Parser *state);
void _start_element_theme_list_cb(Theme_List_Parser *state, const xmlChar *name, const xmlChar **attrs);
void _end_element_theme_list_cb(Theme_List_Parser *state, const xmlChar *name);
void _chars_theme_list_cb(Theme_List_Parser *state, const xmlChar *chars, int len);
int _theme_list_connect(const char *filter, int limit, int offset);

/**
 * @endcond
 */

#endif /* _EXCHANGE_THEME_LIST_H */
