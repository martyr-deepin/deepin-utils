#include <cairo.h>
#include <cairo/cairo-ft.h>

#include <stdlib.h>
#include <ft2build.h>
#include FT_FREETYPE_H

#include <gio/gio.h>
#include <Python.h>
#include <pycairo.h>
#include "pygobject.h"

/* define a variable for the C API */
static Pycairo_CAPI_t *Pycairo_CAPI;

static unsigned long
vfs_stream_read (FT_Stream stream,
		 unsigned long offset,
		 unsigned char *buffer,
		 unsigned long count)
{
    GFileInputStream *handle = stream->descriptor.pointer;
    gssize bytes_read = 0;

    if (!count && offset > stream->size)
        return 1;

    if (!g_seekable_seek (G_SEEKABLE (handle), offset, G_SEEK_SET, NULL, NULL))
        return (count ? 0 : 1);

    if (count > 0) {
        bytes_read = g_input_stream_read (G_INPUT_STREAM (handle), buffer,
					  count, NULL, NULL);

        if (bytes_read == -1)
            return 0;
    }

    return bytes_read;
}

static void
vfs_stream_close (FT_Stream stream)
{
    GFileInputStream *handle = stream->descriptor.pointer;

    if (handle == NULL)
        return;

    /* this also closes the stream */
    g_object_unref (handle);

    stream->descriptor.pointer = NULL;
    stream->size = 0;
    stream->base = NULL;
}

static FT_Error
vfs_stream_open (FT_Stream stream,
		 const char *uri)
{
    GFile *file;
    GFileInfo *info;
    GFileInputStream *handle;

    file = g_file_new_for_uri (uri);
    handle = g_file_read (file, NULL, NULL);

    if (handle == NULL) {
	g_object_unref (file);
        return FT_Err_Cannot_Open_Resource;
    }

    info = g_file_query_info (file,
			      G_FILE_ATTRIBUTE_STANDARD_SIZE,
                              G_FILE_QUERY_INFO_NONE, NULL,
			      NULL);
    g_object_unref (file);

    if (info == NULL) {
        return FT_Err_Cannot_Open_Resource;
    }

    stream->size = g_file_info_get_size (info);

    g_object_unref (info);

    stream->descriptor.pointer = handle;
    stream->pathname.pointer = NULL;
    stream->pos = 0;

    stream->read = vfs_stream_read;
    stream->close = vfs_stream_close;

    return FT_Err_Ok;
}

/* load a typeface from a URI */
FT_Error
FT_New_Face_From_URI (FT_Library library,
		      const gchar* uri,
		      FT_Long face_index,
		      FT_Face *aface)
{
    FT_Open_Args args;
    FT_Stream stream;
    FT_Error error;

    stream = calloc (1, sizeof (*stream));

    if (stream == NULL)
	return FT_Err_Out_Of_Memory;

    error = vfs_stream_open (stream, uri);

    if (error != FT_Err_Ok) {
	free (stream);
	return error;
    }

    args.flags = FT_OPEN_STREAM;
    args.stream = stream;

    error = FT_Open_Face (library, &args, face_index, aface);

    if (error != FT_Err_Ok) {
	if (stream->close != NULL)
	    stream->close(stream);

	free (stream);
	return error;
    }

    /* so that freetype will free the stream */
    (*aface)->face_flags &= ~FT_FACE_FLAG_EXTERNAL_STREAM;

    return error;
}

static cairo_font_face_t *
font_face_create(gchar *fontfile){
    FT_Error error;
    FT_Library library;
    FT_Face face;
    GFile *file;
    gchar *font_file;

    error = FT_Init_FreeType (&library);
    if (error) {
        g_printerr("Could not initialise freetype\n");
        exit(1);
    }

    file = g_file_new_for_commandline_arg (fontfile);
    font_file = g_file_get_uri (file);
    g_object_unref (file);

    if (!font_file) {
        g_printerr("Could not parse argument into a URI\n");
        exit(1);
    }
    error = FT_New_Face_From_URI (library, font_file, 0, &face);
    if (error) {
        g_printerr("Could not load face '%s'\n", font_file);
        exit(1);
    }
    return cairo_ft_font_face_create_for_ft_face (face, 0);
}

static PyObject * 
deepin_font_icon_font_face_create(PyObject *self, PyObject *args) {
    gchar *fontfile;
    if (!(PyArg_ParseTuple(args, "s", &fontfile))) {
        return NULL;
    }

    PyObject *obj = PycairoFontFace_FromFontFace(font_face_create(fontfile));
    Py_INCREF(obj);
    return (PyObject *)obj;
}

static PyMethodDef 
deepin_font_iconMethods[] = {
    {"font_face_create", deepin_font_icon_font_face_create, METH_VARARGS}, 
    {NULL, NULL},
};

PyMODINIT_FUNC initdeepin_font_icon(void) {
    PyObject *m;

    /* This is necessary step for Python binding, otherwise got sefault error */
    init_pygobject();
     
    m = Py_InitModule("deepin_font_icon", deepin_font_iconMethods);
    /* import pycairo - add to the init<module> function */
    Pycairo_IMPORT;

    if (!m) {
        return;
    }
}
