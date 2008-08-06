/* EINA - EFL data type library
 * Copyright (C) 2007-2008 Jorge Luis Zapata Muga
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

#ifndef EINA_MEMPOOL_H_
#define EINA_MEMPOOL_H_

#include "eina_types.h"

/**
 * @defgroup Memory_Pool_Group Memory Pool
 * @{
 */
typedef struct _Eina_Mempool Eina_Mempool;

EAPI int eina_mempool_init(void);
EAPI int eina_mempool_shutdown(void);

EAPI Eina_Mempool * eina_mempool_new(const char *module, const char *context, const char *options, ...);
EAPI void eina_mempool_delete(Eina_Mempool *mp);

EAPI void * eina_mempool_realloc(Eina_Mempool *mp, void *element, unsigned int size);
EAPI void * eina_mempool_alloc(Eina_Mempool *mp, unsigned int size);
EAPI void eina_mempool_free(Eina_Mempool *mp, void *element);

/** @} */

#endif /* EINA_MEMPOOL_H_ */
