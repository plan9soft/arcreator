#ifndef RGSS_RGSS_ERROR_H
#define RGSS_RGSS_ERROR_H

#include <ruby.h>

#include "rgssExport.h"

namespace rgss
{
	extern VALUE rb_eRGSSError;

	class rgssExport RGSSError
	{
	public:
		/// @brief Initializes.
		static void init();
		/// @brief Destroys.
		static void destroy();
		/// @brief Exposes this class to Ruby.
		static void createRubyInterface();

	};
	
}
#endif