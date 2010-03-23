# Copyright (C) 2009 Samsung Electronics.
#
# This file is part of Editje.
#
# Editje is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Editje is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with Editje. If not, see <http://www.gnu.org/licenses/>.

import evas
import edje
import elementary

import re

from clist import CList
from floater import Wizard
from groupselector import NameEntry
from operation import Operation
import objects_data


class PartsList(CList):
    def __init__(self, parent, editable_grp, operation_stack_cb):
        CList.__init__(self, parent)

        self._edit_grp = editable_grp
        self._operation_stack_cb = operation_stack_cb

        self._options_load()

        self._edit_grp.callback_add("parts.changed", self._parts_update_cb)
        self._edit_grp.callback_add("part.added", self._part_added_cb)
        self._edit_grp.callback_add("part.removed", self._part_removed_cb)

        self._edit_grp.part.callback_add("part.changed", self._part_changed_cb)
        self._edit_grp.part.callback_add(
            "part.unselected", self._part_changed_cb)
        self._edit_grp.part.callback_add("name.changed", self._name_changed_cb)

    def _parts_update_cb(self, emissor, data):
        parts_list = data

        self.clear()
        for i in parts_list[::-1]:
            self.add(i)
        self.go()

    def _part_added_cb(self, emissor, data):
        self.add(data)
        self.go()
        self.open = True
        self.select(data)

    def _part_removed_cb(self, emissor, data):
        self.remove(data)

    def _part_changed_cb(self, emissor, data):
        self.selection_clear()
        self.select(data)

    def _name_changed_cb(self, emissor, data):
        for s in self._selected.iterkeys():
            item = self._items[s]
            if item.label_get() == data[0]:
                item.label_set(data[1])
                self._selected[data[1]] = self._selected[data[0]]
                self._items[data[1]] = self._items[data[0]]
                del self._selected[data[0]]
                del self._items[data[0]]
                return

    # Selection
    def _selected_cb(self, list_, list_item):
        CList._selected_cb(self, list_, list_item)
        name = list_item.label_get()

        self._edit_grp.part.name = name
        if (len(self._items) > 1):
            self._options_edje.signal_emit("up,enable", "")
            self._options_edje.signal_emit("down,enable", "")
        self._options_edje.signal_emit("remove,enable", "")

    def _unselected_cb(self, li, it):
        CList._unselected_cb(self, li, it)
        if not self._selected:
            if (len(self._items) > 1):
                self._options_edje.signal_emit("up,disable", "")
                self._options_edje.signal_emit("down,disable", "")
            self._options_edje.signal_emit("remove,disable", "")

    # Options
    def _options_load(self):
        self._options_edje = edje.Edje(
            self.evas, file=self._theme_file,
            group="editje/collapsable/list/options/parts")
        self._options_edje.signal_callback_add(
            "new", "editje/collapsable/list/options", self._new_cb)
        self._options_edje.signal_callback_add(
            "up", "editje/collapsable/list/options", self._up_cb)
        self._options_edje.signal_callback_add(
            "down", "editje/collapsable/list/options", self._down_cb)
        self._options_edje.signal_callback_add(
            "remove", "editje/collapsable/list/options", self._remove_cb)
        self._options_edje.signal_emit("up,disable", "")
        self._options_edje.signal_emit("down,disable", "")
        self._options_edje.signal_emit("remove,disable", "")
        self.content_set("options", self._options_edje)
        self._options = False

    def _new_cb(self, obj, emission, source):
        new_part_wiz = NewPartWizard(
            self._parent, self._edit_grp, self._operation_stack_cb)
        new_part_wiz.open()

    def _part_restack_above(self, part_name):
        part = self._edit_grp.part_get(part_name)
        if not part:
            return False

        r = part.restack_above()
        if r is True:
            # FIXME: turning a blind eye on it
            self._edit_grp._parts_reload_cb(self, None)

        return r

    def _part_restack_below(self, part_name):
        part = self._edit_grp.part_get(part_name)
        if not part:
            return False

        r = part.restack_below()
        if r is True:
            # FIXME: turning a blind eye on it
            self._edit_grp._parts_reload_cb(self, None)

        return r

    def _current_part_get(self):
        curr_part = self._edit_grp.part
        if not curr_part:
            return None

        return curr_part.name

    def _up_cb(self, obj, emission, source):
        curr_part_name = self._current_part_get()
        if curr_part_name is None:
            return

        r = self._part_restack_above(curr_part_name)
        if not r:
            return

        op = Operation("part re-stacking (above)")
        op.redo_callback_add(self._part_restack_above, curr_part_name)
        op.undo_callback_add(self._part_restack_below, curr_part_name)
        self._operation_stack_cb(op)

    def _down_cb(self, obj, emission, source):
        curr_part_name = self._current_part_get()
        if curr_part_name is None:
            return

        r = self._part_restack_below(curr_part_name)
        if not r:
            return

        op = Operation("part re-stacking (below)")
        op.redo_callback_add(self._part_restack_below, curr_part_name)
        op.undo_callback_add(self._part_restack_above, curr_part_name)
        self._operation_stack_cb(op)

    def _remove_cb(self, obj, emission, source):

        def part_restore(part_save):
            name = part_save.name
            source = part_save["source"] or ""

            if self._edit_grp.part_add(name, part_save.type, source):
                part_save.apply_to(self._edit_grp.part_get(name))
                # ugly hack: second "part.added" emitted
                self._edit_grp.event_emit("part.added", name)

        for to_del in self.selected:
            part_name = to_del[0]
            part_save = objects_data.Part(self._edit_grp.part_get(part_name))

            r = self._edit_grp.part_del(part_name)
            if not r:
                del part_save
                return

            op = Operation("part deletion")
            op.redo_callback_add(self._edit_grp.part_del, part_name)
            op.undo_callback_add(part_restore, part_save)
            self._operation_stack_cb(op)

    def remove(self, item):
        i = self._items.get(item)
        if i:
            next = i.next
            prev = i.prev
            if not prev:
                self._first = next
            i.delete()
            self._list.go()
            del self._items[item]
            self.event_emit("item.removed", item)
            if next:
                next.selected_set(True)
            elif prev:
                prev.selected_set(True)


class ExternalSelector(elementary.Box):
    def __init__(self, parent, type_cb):
        elementary.Box.__init__(self, parent)

        self.horizontal_set(True)
        self.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        self.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)

        self._module = ""
        self._type = ""
        self._type_selected_cb = type_cb

        self._types_load()
        self._modules_init()
        self._types_init()
        self._modules_load()

    def _type_get(self):
        return self._type

    type = property(_type_get)

    def _module_get(self):
        return self._module

    module = property(_module_get)

    def _types_load(self):
        self._loaded_types = {}
        for type in edje.ExternalIterator():
            module = type.module
            name = type.name
            label = type.label_get()

            list = self._loaded_types.get(module)
            if not list:
                list = []
                self._loaded_types[module] = list
            elif (name, label, type) in list:
                continue
            list.append((name, label, type))

    def _modules_init(self):
        self._modules = elementary.List(self)
        self._modules.size_hint_weight_set(evas.EVAS_HINT_EXPAND,
                                           evas.EVAS_HINT_EXPAND)
        self._modules.size_hint_align_set(evas.EVAS_HINT_FILL,
                                          evas.EVAS_HINT_FILL)
        self.pack_end(self._modules)
        self._modules.show()

    def _types_init(self):
        self._types = elementary.List(self)
        self._types.size_hint_weight_set(evas.EVAS_HINT_EXPAND,
                                         evas.EVAS_HINT_EXPAND)
        self._types.size_hint_align_set(evas.EVAS_HINT_FILL,
                                        evas.EVAS_HINT_FILL)
        self.pack_end(self._types)
        self._types.show()

    def _modules_load(self):
        self._module = ""
        self._modules.clear()
        list = self._loaded_types.keys()

        list.sort(key=str.lower)

        if list:
            self._modules.item_append(list[0], None, None, self._module_select,
                                      list[0]).selected_set(True)
        for item in list[1:]:
            self._modules.item_append(item, None, None,
                                      self._module_select, item)
        self._modules.go()

    def _module_select(self, li, it, module):
        self._module = module
        self._types.clear()
        list = self._loaded_types.get(module)

        list.sort(key=lambda x: (str.lower(x[0])))

        if list:
            name, label, type = list[0]

            ico = type.icon_add(self.evas)

            self._types.item_append(label, ico, None, self._type_select,
                                    name).selected_set(False)
        for (name, label, type) in list[1:]:
            ico = type.icon_add(self.evas)
            self._types.item_append(label, ico, None, self._type_select, name)

        self._types.go()

    def _type_select(self, li, it, type):
        self._type = type
        if self._type_selected_cb:
            name = it.label_get().replace(" ", "")
            self._type_selected_cb(name)


class TypesList(elementary.List):
    def __init__(self, parent, type_select_cb=None):
        elementary.List.__init__(self, parent)
        self._parent = parent
        self._type_select_cb = type_select_cb

        self.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        self.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)

        self.item_append("Rectangle", None, None, self._type_select_cb,
                         edje.EDJE_PART_TYPE_RECTANGLE)
        self.item_append("Text", None, None, self._type_select_cb,
                         edje.EDJE_PART_TYPE_TEXT)
        self.item_append("Image", None, None, self._type_select_cb,
                         edje.EDJE_PART_TYPE_IMAGE)
        self.item_append("Swallow", None, None, self._type_select_cb,
                         edje.EDJE_PART_TYPE_SWALLOW)
        self.item_append("Textblock", None, None, self._type_select_cb,
                         edje.EDJE_PART_TYPE_TEXTBLOCK)
        self.item_append("Group", None, None, self._type_select_cb,
                         edje.EDJE_PART_TYPE_GROUP)
        # self.item_append("Box", None, None, self._type_select_cb,
        #                  edje.EDJE_PART_TYPE_BOX)
        # self.item_append("Table", None, None, self._type_select_cb,
        #                  edje.EDJE_PART_TYPE_TABLE)
        self.item_append("External widget", None, None, self._type_select_cb,
                         edje.EDJE_PART_TYPE_EXTERNAL)
        self.go()


class NewPartWizard(Wizard):
    def __init__(self, parent, editable_grp, operation_stack_cb):
        Wizard.__init__(self, parent)
        self._parent = parent
        self._edit_grp = editable_grp
        self._operation_stack_cb = operation_stack_cb
        self._type = None

        self.page_add("default", "New Part",
                      "Name the new part to be inserted and choose its type.")

        self._part_name_entry = NameEntry(
            self, changed_cb=self._name_changed_cb,
            weight_hints=(evas.EVAS_HINT_EXPAND, 0.0),
            align_hints=(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL))
        self.content_add("default", self._part_name_entry)
        self._part_name_entry.show()

        self._types_list = TypesList(self, self._type_select)
        self.content_add("default", self._types_list)
        self._types_list.show()

        self._ext_list = ExternalSelector(self, self._default_name_set)
        self._ext_list.size_hint_weight_set(0.0, 0.0)
        self.content_add("default", self._ext_list)
        self._ext_list.show()

        self.action_add("default", "Cancel", self._cancel)
        self.action_add("default", "Add", self._add)
        self.action_disabled_set("default", "Add", True)

        edje.message_signal_process()
        self._name_changed = False

    def _name_changed_cb(self, obj):
        self._name_changed = True
        self._check_name_and_type()

    def _type_select(self, list_, item, label, *args, **kwargs):
        self._type = label
        if self._type == edje.EDJE_PART_TYPE_EXTERNAL:
            self._external_selector_toggle(True)
        else:
            self._external_selector_toggle(False)
            self._default_name_set(item.label_get())
        self._check_name_and_type()

    def _check_name_and_type(self):
        error_msg = "This part name is already used in this group"

        def good():
            self._part_name_entry.status_label = ""
            self.action_disabled_set("default", "Add", False)

        def bad():
            self._part_name_entry.status_label = error_msg
            self.action_disabled_set("default", "Add", True)

        def incomplete():
            self._part_name_entry.status_label = ""
            self.action_disabled_set("default", "Add", True)

        name = self._part_name_entry.entry
        if not name or not self._type:
            incomplete()
            return

        if name in self._edit_grp.parts:
            bad()
            return

        good()

    def _default_name_set(self, name):
        if self._name_changed:
            return
        max = 0
        for p in self._edit_grp.parts:
            if re.match("%s\d{2,}" % name, p):
                num = int(p[len(name):])
                if num > max:
                    max = num
        self._part_name_entry.entry = name + "%.2d" % (max + 1)
        edje.message_signal_process()
        self._name_changed = False

    def _add(self):
        name = self._part_name_entry.entry

        if (self._type == edje.EDJE_PART_TYPE_EXTERNAL):
            ext_name = self._ext_list.type
            ext_module = self._ext_list.module
        else:
            ext_name = ""
            ext_module = None

        def add_internal(name, edje_type, ext_name="", ext_module=None):
            success = self._edit_grp.part_add(name, edje_type, ext_name)
            if success:
                if self._type == edje.EDJE_PART_TYPE_EXTERNAL:
                    self._edit_grp.external_add(ext_module)
                self._part_init(name, edje_type)
            else:
                self.notify("Error adding new part.")
            return success

        if add_internal(name, self._type, ext_name, ext_module):
            op = Operation("part addition")
            op.redo_callback_add(
                add_internal, name, self._type, ext_name, ext_module)
            op.undo_callback_add(self._edit_grp.part_del, name)
            self._operation_stack_cb(op)

        self.close()

    def _part_init(self, name, type_):
        # part and state should be selected after self._edit_grp.part_add()
        part = self._edit_grp.part
        state = part.state

        w, h = self._edit_grp.group_size

        state.rel1_to = (None, None)
        state.rel1_relative = (0.0, 0.0)
        state.rel1_offset = (w / 4, h / 4)

        state.rel2_to = (None, None)
        state.rel2_relative = (0.0, 0.0)
        state.rel2_offset = (w * 3 / 4, h * 3 / 4)

        if type_ == edje.EDJE_PART_TYPE_RECTANGLE:
            self._part_init_rectangle(part, state)
        elif type_ == edje.EDJE_PART_TYPE_TEXT:
            self._part_init_text(part, state)
        elif type_ == edje.EDJE_PART_TYPE_EXTERNAL:
            self._part_init_external(part, state)

    def _part_init_rectangle(self, part, state):
        part.mouse_events = False
        state.color = (0, 255, 0, 128)

    def _part_init_text(self, part, state):
        part.mouse_events = False
        state.color = (0, 0, 0, 255)
        state.text = "YOUR TEXT HERE"
        state.font = "Sans"
        state.text_size = 16

    def _part_init_external(self, part, state):
        pass

    def _external_selector_toggle(self, show):
        if show:
            self._ext_list.size_hint_weight_set(evas.EVAS_HINT_EXPAND,
                                                evas.EVAS_HINT_EXPAND)
        else:
            self._ext_list.size_hint_weight_set(0, 0)

    def _cancel(self):
        self.close()
