#ifndef ZER0_CODE_SNIPPETS_H
#define ZER0_CODE_SNIPPETS_H

// iterator macro
#define for_iter(name, min, max) for (int name = min; name < max; name++)
#define for_iter_step(name, min, max, step) for (int name = min; name < max; name += step)

#define rb_ary_each_index(ary, name) for (int name = 0; name < NUM2INT(rb_ary_size(ary)); name++)

// missing C functions for commonly used classes

/// @brief Gets string size.
/// @param[in] str String to check.
#define rb_str_size(str) rb_funcall(str, rb_intern("size"), 0)
/// @brief Gets array size.
/// @param[in] ary Array to check.
#define rb_ary_size(ary) rb_funcall(ary, rb_intern("size"), 0)
/// @brief Gets hash size.
/// @param[in] ary Hash to check.
#define rb_hash_size(ary) rb_funcall(ary, rb_intern("size"), 0)
/// @brief Calls method with name.
/// @param[in] obj Object to call the method.
/// @param[in] name Name of the method.
#define rb_funcall_0(obj, name) rb_funcall(obj, rb_intern(name), 0)
/// @brief Calls method with name and one argument.
/// @param[in] obj Object to call the method.
/// @param[in] name Name of the method.
/// @param[in] arg First argument.
#define rb_funcall_1(obj, name, arg) rb_funcall(obj, rb_intern(name), 1, arg)
/// @brief Calls method with name and one argument.
/// @param[in] obj Object to call the method.
/// @param[in] name Name of the method.
/// @param[in] arg1 First argument.
/// @param[in] arg2 Second argument.
#define rb_funcall_2(obj, name, arg1, arg2) rb_funcall(obj, rb_intern(name), 2, arg1, arg2)
/// @brief Calls method with name and arguments.
/// @param[in] obj Object to call the method.
/// @param[in] name Name of the method.
/// @param[in] argc Number of arguments.
/// @param[in] argv Argument values.
#define rb_funcall_x(obj, name, argc, argv) rb_funcall2(obj, rb_intern(name), argc, argv)
/// @brief Calls to_s.
/// @param[in] obj Object to use.
#define rb_f_to_s(obj) rb_funcall(obj, rb_intern("to_s"), 0)
/// @brief Calls rb_to_sym.
/// @param[in] obj Object to use.
#define rb_f_to_sym(obj) rb_funcall(obj, rb_intern("to_sym"), 0)
/// @brief Calls inspect.
/// @param[in] obj Object to use.
#define rb_f_inspect(obj) rb_funcall(obj, rb_intern("inspect"), 0)
/// @brief Gets the object ID.
/// @param[in] obj Object to check.
#define rb_f_object_id(obj) rb_funcall(obj, rb_intern("object_id"), 0)
/// @brief Clones object.
/// @param[in] obj Object to clone.
#define rb_f_clone(obj) rb_funcall(obj, rb_intern("clone"), 0)

/// @brief Converts a VALUE to a pointer of type and name
/// @param[in] value The Ruby VALUE.
/// @param[in] type Type of the C++ variable.
/// @param[in] name Name of the C++ variable.
#define RB_VAR2CPP(value, type, name) type* name; Data_Get_Struct(value, type, name);
/// @brief Directly converts self to a pointer of type and name
/// @param[in] type Type of the C++ variable.
/// @param[in] name Name of the C++ variable.
#define RB_SELF2CPP(type, name) type* name; Data_Get_Struct(self, type, name);
/// @brief throws an Errno::ENOENT exception
/// @param[in] filename Filename C-string.
#define RB_RAISE_FILE_NOT_FOUND(filename) \
	{ \
		VALUE errnoModule = rb_funcall_1(rb_mKernel, "const_get", rb_f_to_sym(rb_str_new2("Errno"))); \
		VALUE enoentClass = rb_funcall_1(errnoModule, "const_get", rb_f_to_sym(rb_str_new2("ENOENT"))); \
		rb_raise(enoentClass, filename); \
	}

/// @brief Creates a C++ object with a Ruby reference.
/// @param[in] classe Ruby class VALUE.
/// @param[in] type C++ type.
/// @param[in] var Variable to store the object.
/// @param[in] mark Mark function.
/// @param[in] free Free function.
#define RB_OBJECT_NEW(classe, type, var, mark, free) \
	( \
		var = (type*)xmalloc(sizeof(type)), \
		memset(var, 0, sizeof(type)), \
		Data_Wrap_Struct(classe, mark, free, var) \
	)
/// @brief Deletes the C++ object after the Ruby reference has been destroyed.
/// @param[in] var Variable of the object.
#define RB_OBJECT_DELETE(var) xfree(var)

#endif
