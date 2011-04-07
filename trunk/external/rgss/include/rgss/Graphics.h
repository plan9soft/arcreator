#ifndef RGSS_GRAPHICS_H
#define RGSS_GRAPHICS_H

#include <ruby.h>

#include "rgssExport.h"

namespace rgss
{
	extern VALUE rb_mGraphics;

	class Renderable;

	class rgssExport Graphics
	{
	public:
		/// @brief Adds a new renderable object to the rendering queue.
		/// @param[in] renderable The renderable object to be added.
		static void addRenderable(Renderable* renderable);
		/// @brief Removes the renderable object from the rendering queue.
		/// @param[in] renderable The renderable object to be removed.
		static void removeRenderable(Renderable* renderable);
		/// @brief Updates a renderable object within the rendering queue because of a change in the Z coordinate.
		/// @param[in] renderable The renderable object that has changed.
		static void updateRenderable(Renderable* renderable);
		/// @brief Sets whether Graphics is still running.
		/// @param[in] value The new value.
		static void setRunning(bool value) { running = value; }

		/// @brief Intializes the module.
		static void init();
		/// @brief Exposes this class to Ruby.
		static void createRubyInterface();

		/// @brief Gets the frame count.
		static VALUE getFrameCount(VALUE self);
		/// @brief Sets the frame count.
		/// @param[in] value The new frame count.
		static VALUE setFrameCount(VALUE self, VALUE value);
		/// @brief Gets the frame rate.
		static VALUE getFrameRate(VALUE self);
		/// @brief Sets the frame rate.
		/// @param[in] value The new frame rate.
		static VALUE setFrameRate(VALUE self, VALUE value);

		/// @brief Refreshes the game screen and advances time by 1 frame.
		static VALUE update(VALUE self);
		/// @brief Resets the screen refresh timing.
		static VALUE frameReset(VALUE self);
		/// @brief Fixes the current screen in preparation for transitions.
		static VALUE freeze(VALUE self);
		/// @brief Carries out a transition from the screen fixed in Graphics.freeze to the current screen.
		/// @param[in] duration The number of frames the transition will last. 
		/// @param[in] filename The transition graphic file name.
		/// @param[in] vague Sets the ambiguity of the borderline between the graphic's starting and ending points.
		static VALUE transition(VALUE self, VALUE duration, VALUE filename, VALUE vague);

	private:
		/// @brief The number of frames that have passed.
		static unsigned int frameCount;
		/// @brief The frame rate.
		static unsigned int frameRate;
		/// @brief Flag whether it is still running.
		static bool running;
			
	};

}
#endif