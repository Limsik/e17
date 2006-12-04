#ifndef EWL_LABEL_H
#define EWL_LABEL_H

/**
 * @addtogroup Ewl_Label Ewl_Label: A fully-themable text label
 * Defines a class for a fullty-themable text label
 * 
 * @remarks Inherits from Ewl_Widget.
 * @image html Ewl_Label_inheritance.png
 *
 * @{
 */

/**
 * @themekey /label
 */

/**
 * @def EWL_LABEL_TYPE
 * The type name for the Ewl_Label widget
 */
#define EWL_LABEL_TYPE "label"

/**
 * The Ewl_Label widget
 */
typedef struct Ewl_Label Ewl_Label;

/**
 * @def EWL_LABEL(label)
 * Typecasts a pointer to an Ewl_Label pointer
 */
#define EWL_LABEL(label) ((Ewl_Label *)label)

/**
 * Inherits from Ewl_Widget class
 */
struct Ewl_Label
{
	Ewl_Widget widget;      /**< Inherit from Ewl_Widget */
};

Ewl_Widget 	*ewl_label_new(void);
int 		 ewl_label_init(Ewl_Label *la);

void 		 ewl_label_text_set(Ewl_Label *la, const char *text);
const char 	*ewl_label_text_get(Ewl_Label *la);

Ewl_View 	*ewl_label_view_get(void);

/**
 * @}
 */

#endif

