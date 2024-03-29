// This is the post-initialisation support code for the QtCore module.
//
// Copyright (c) 2015 Riverbank Computing Limited <info@riverbankcomputing.com>
// 
// This file is part of PyQt4.
// 
// This file may be used under the terms of the GNU General Public License
// version 3.0 as published by the Free Software Foundation and appearing in
// the file LICENSE included in the packaging of this file.  Please review the
// following information to ensure the GNU General Public License version 3.0
// requirements will be met: http://www.gnu.org/copyleft/gpl.html.
// 
// If you do not wish to use this file under the terms of the GPL version 3.0
// then you may purchase a commercial license.  For more information contact
// info@riverbankcomputing.com.
// 
// This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
// WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.


#include <Python.h>

#include <QMetaType>
#include <QMutex>

#include "qpycore_pyqtboundsignal.h"
#include "qpycore_pyqtmethodproxy.h"
#include "qpycore_pyqtproperty.h"
#include "qpycore_pyqtproxy.h"
#include "qpycore_pyqtpyobject.h"
#include "qpycore_pyqtsignal.h"
#include "qpycore_sip.h"


// The name attribute name as an object.
PyObject *qpycore_name_attr_name;

// The signature attribute name as an object.
PyObject *qpycore_signature_attr_name;


// Perform any required post-initialisation.
void qpycore_post_init(PyObject *module_dict)
{
    // Add the meta-type to the module dictionary.
    if (PyDict_SetItemString(module_dict, "pyqtWrapperType",
                (PyObject *)&qpycore_pyqtWrapperType_Type) < 0)
        Py_FatalError("PyQt4.QtCore: Failed to set pyqtWrapperType type");

    // Initialise the pyqtProperty type and add it to the module dictionary.
    if (PyType_Ready(&qpycore_pyqtProperty_Type) < 0)
        Py_FatalError("PyQt4.QtCore: Failed to initialise pyqtProperty type");

    if (PyDict_SetItemString(module_dict, "pyqtProperty",
                (PyObject *)&qpycore_pyqtProperty_Type) < 0)
        Py_FatalError("PyQt4.QtCore: Failed to set pyqtProperty type");

    // Initialise the pyqtSignal type and add it to the module dictionary.
    if (PyType_Ready(&qpycore_pyqtSignal_Type) < 0)
        Py_FatalError("PyQt4.QtCore: Failed to initialise pyqtSignal type");

    if (PyDict_SetItemString(module_dict, "pyqtSignal",
                (PyObject *)&qpycore_pyqtSignal_Type) < 0)
        Py_FatalError("PyQt4.QtCore: Failed to set pyqtSignal type");

    // Initialise the pyqtBoundSignal type and add it to the module dictionary.
    if (PyType_Ready(&qpycore_pyqtBoundSignal_Type) < 0)
        Py_FatalError("PyQt4.QtCore: Failed to initialise pyqtBoundSignal type");

    if (PyDict_SetItemString(module_dict, "pyqtBoundSignal",
                (PyObject *)&qpycore_pyqtBoundSignal_Type) < 0)
        Py_FatalError("PyQt4.QtCore: Failed to set pyqtBoundSignal type");

    // Initialise the private pyqtMethodProxy type.
    if (PyType_Ready(&qpycore_pyqtMethodProxy_Type) < 0)
        Py_FatalError("PyQt4.QtCore: Failed to initialise pyqtMethodProxy type");

    // Register the C++ type that wraps Python objects.
    PyQt_PyObject::metatype = qRegisterMetaType<PyQt_PyObject>("PyQt_PyObject");
    qRegisterMetaTypeStreamOperators<PyQt_PyObject>("PyQt_PyObject");

    // Register the lazy attribute getter.
    if (sipRegisterAttributeGetter(sipType_QObject, qpycore_get_lazy_attr) < 0)
        Py_FatalError("PyQt4.QtCore: Failed to register attribute getter");

    // Objectify some strings.
#if PY_MAJOR_VERSION >= 3
    qpycore_signature_attr_name = PyUnicode_FromString("__pyqtSignature__");
#else
    qpycore_signature_attr_name = PyString_FromString("__pyqtSignature__");
#endif

    if (!qpycore_signature_attr_name)
        Py_FatalError("PyQt4.QtCore: Failed to objectify '__pyqtSignature__'");

#if PY_MAJOR_VERSION >= 3
    qpycore_name_attr_name = PyUnicode_FromString("__name__");
#else
    qpycore_name_attr_name = PyString_FromString("__name__");
#endif

    if (!qpycore_name_attr_name)
        Py_FatalError("PyQt4.QtCore: Failed to objectify '__name__'");

    // Embed the configuration.
    PyObject *config = PyDict_New();

    if (!config)
        Py_FatalError("PyQt4.QtCore: Failed to create PYQT_CONFIGURATION dict");

#if PY_MAJOR_VERSION >= 3
    PyObject *sip_flags = PyUnicode_FromString("-x VendorID -t WS_X11 -x PyQt_NoPrintRangeBug -t Qt_4_8_6 -x Py_v3");
#else
    PyObject *sip_flags = PyString_FromString("-x VendorID -t WS_X11 -x PyQt_NoPrintRangeBug -t Qt_4_8_6 -x Py_v3");
#endif

    if (!sip_flags)
        Py_FatalError("PyQt4.QtCore: Failed to create PYQT_CONFIGURATION.sip_flags");

    if (PyDict_SetItemString(config, "sip_flags", sip_flags) < 0)
        Py_FatalError("PyQt4.QtCore: Failed to set PYQT_CONFIGURATION.sip_flags");

    Py_DECREF(sip_flags);

    if (PyDict_SetItemString(module_dict, "PYQT_CONFIGURATION", config) < 0)
        Py_FatalError("PyQt4.QtCore: Failed to set PYQT_CONFIGURATION dict");

    Py_DECREF(config);

    // Create the mutex that serialises access to the signal/slot proxies.  We
    // don't use a statically initialised one because Qt needs some things to
    // be initialised first (at least for Windows) and this is the only way to
    // guarantee things are done in the right order.
    PyQtProxy::mutex = new QMutex(QMutex::Recursive);
}
