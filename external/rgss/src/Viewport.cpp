#include <ruby.h>

#include <april/RenderSystem.h>
#include <gtypes/Matrix4.h>
#include <gtypes/Rectangle.h>
#include <hltypes/hstring.h>
#include <hltypes/util.h>

#include "CodeSnippets.h"
#include "Color.h"
#include "Graphics.h"
#include "Rect.h"
#include "RenderQueue.h"
#include "Tone.h"
#include "Viewport.h"

namespace rgss
{
	/****************************************************************************************
	 * Pure C++ code
	 ****************************************************************************************/

	VALUE rb_cViewport;

	/// @todo Still needs to be implemented fully.
	void Viewport::draw()
	{
		gmat4 viewMatrix = april::rendersys->getModelviewMatrix();
		if (this->rect->x != 0 || this->rect->y != 0)
		{
			april::rendersys->translate((float)this->rect->x, (float)this->rect->y);
		}
		this->_render();
		april::rendersys->setModelviewMatrix(viewMatrix);
	}

	void Viewport::_render()
	{
		this->renderQueue->draw();
	}

	void Viewport::dispose()
	{
		if (this->renderQueue != NULL)
		{
			delete this->renderQueue;
			this->renderQueue = NULL;
		}
	}

	/****************************************************************************************
	 * Ruby Interfacing, Creation, Destruction, Systematics
	 ****************************************************************************************/

	void Viewport::init()
	{
	}

	void Viewport::createRubyInterface()
	{
		rb_cViewport = rb_define_class("Viewport", rb_cObject);
		rb_define_alloc_func(rb_cViewport, &Viewport::rb_new);
		// initialize
		rb_define_method(rb_cViewport, "initialize", RUBY_METHOD_FUNC(&Viewport::rb_initialize), -1);
		rb_define_method(rb_cViewport, "dispose", RUBY_METHOD_FUNC(&Viewport::rb_dispose), 0);
		// getters and setters
		rb_define_method(rb_cViewport, "visible", RUBY_METHOD_FUNC(&Viewport::rb_getVisible), 0);
		rb_define_method(rb_cViewport, "visible=", RUBY_METHOD_FUNC(&Viewport::rb_setVisible), 1);
		rb_define_method(rb_cViewport, "z", RUBY_METHOD_FUNC(&Viewport::rb_getZ), 0);
		rb_define_method(rb_cViewport, "z=", RUBY_METHOD_FUNC(&Viewport::rb_setZ), 1);
		rb_define_method(rb_cViewport, "ox", RUBY_METHOD_FUNC(&Viewport::rb_getOX), 0);
		rb_define_method(rb_cViewport, "ox=", RUBY_METHOD_FUNC(&Viewport::rb_setOX), 1);
		rb_define_method(rb_cViewport, "oy", RUBY_METHOD_FUNC(&Viewport::rb_getOY), 0);
		rb_define_method(rb_cViewport, "oy=", RUBY_METHOD_FUNC(&Viewport::rb_setOY), 1);
		rb_define_method(rb_cViewport, "disposed?", RUBY_METHOD_FUNC(&Viewport::rb_isDisposed), 0);
		// methods
	}

	void Viewport::gc_mark(Viewport* viewport)
	{
		if (!NIL_P(viewport->rb_color))
		{
			rb_gc_mark(viewport->rb_color);
		}
		if (!NIL_P(viewport->rb_rect))
		{
			rb_gc_mark(viewport->rb_rect);
		}
		if (!NIL_P(viewport->rb_tone))
		{
			rb_gc_mark(viewport->rb_tone);
		}
		Renderable::gc_mark(viewport);
	}

	void Viewport::gc_free(Viewport* viewport)
	{
		viewport->rb_color = Qnil;
		viewport->color = NULL;
		viewport->rb_rect = Qnil;
		viewport->rect = NULL;
		viewport->rb_tone = Qnil;
		viewport->tone = NULL;
		Renderable::gc_free(viewport);
	}

	VALUE Viewport::rb_new(VALUE classe)
	{
		Viewport* viewport;
		VALUE result = Data_Make_Struct(rb_cViewport, Viewport, Viewport::gc_mark, Viewport::gc_free, viewport);
		viewport->disposed = true;
		viewport->type = TYPE_VIEWPORT;
		return result;
	}

	VALUE Viewport::rb_initialize(int argc, VALUE* argv, VALUE self)
	{
		if (argc != 1 && argc != 4)
		{
			hstr message = hsprintf("wrong number of arguments (%d for 1 or 4)", argc);
			rb_raise(rb_eArgError, message.c_str());
		}
		RB_SELF2CPP(Viewport, viewport);
		viewport->renderQueue = new RenderQueue();
		viewport->initializeRenderable(Graphics::renderQueue);
		VALUE arg1, arg2, arg3, arg4;
		rb_scan_args(argc, argv, "13", &arg1, &arg2, &arg3, &arg4);
		if (NIL_P(arg2) && NIL_P(arg3) && NIL_P(arg4))
		{
			Viewport::rb_setRect(self, arg1);
		}
		else
		{
			Viewport::rb_setRect(self, Rect::create(arg1, arg2, arg3, arg4));
		}
		VALUE argv2[4] = {INT2FIX(0), INT2FIX(0), INT2FIX(0), INT2FIX(0)};
		Viewport::rb_setColor(self, Color::create(4, argv2));
		VALUE argv3[4] = {INT2FIX(0), INT2FIX(0), INT2FIX(0), INT2FIX(0)};
		Viewport::rb_setTone(self, Tone::create(4, argv3));
		return self;
	}

	VALUE Viewport::rb_inspect(VALUE self)
	{
		RB_SELF2CPP(Viewport, viewport);
		return Color::rb_inspect(viewport->rb_color);
	}

	/****************************************************************************************
	 * Ruby Getters/Setters
	 ****************************************************************************************/

	VALUE Viewport::rb_getColor(VALUE self)
	{
		RB_SELF2CPP(Viewport, viewport);
		return viewport->rb_color;
	}

	VALUE Viewport::rb_setColor(VALUE self, VALUE value)
	{
		RB_GENERATE_SETTER(Viewport, sprite, Color, color);
		return value;
	}

	VALUE Viewport::rb_getRect(VALUE self)
	{
		RB_SELF2CPP(Viewport, viewport);
		return viewport->rb_rect;
	}

	VALUE Viewport::rb_setRect(VALUE self, VALUE value)
	{
		RB_GENERATE_SETTER(Viewport, sprite, Rect, rect);
		return value;
	}

	VALUE Viewport::rb_getTone(VALUE self)
	{
		RB_SELF2CPP(Viewport, viewport);
		return viewport->rb_tone;
	}

	VALUE Viewport::rb_setTone(VALUE self, VALUE value)
	{
		RB_GENERATE_SETTER(Viewport, sprite, Tone, tone);
		return value;
	}

	/****************************************************************************************
	 * TODO
	 ****************************************************************************************/

	void Viewport::flash(Color clr, int duration)
	{
			
	}
	
}
