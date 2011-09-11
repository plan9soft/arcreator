#include <ruby.h>

#include "RGSSError.h"

namespace rgss
{
	VALUE rb_eRGSSError;

	/****************************************************************************************
	 * Ruby Interfacing, Creation, Destruction, Systematics
	 ****************************************************************************************/

	void RGSSError::init()
	{
	}

	void RGSSError::destroy()
	{
	}

	void RGSSError::createRubyInterface()
	{
		rb_eRGSSError = rb_define_class("RGSSError", rb_eStandardError);
	}

}
