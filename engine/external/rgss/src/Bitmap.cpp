#include <ruby.h>

#include <april/RenderSystem.h>
#include <april/Texture.h>
#include <atres/atres.h>
#include <atres/FontResourceBitmap.h>
#include <atres/Renderer.h>
#include <gtypes/Rectangle.h>
#include <gtypes/Vector2.h>
#include <hltypes/exception.h>
#include <hltypes/harray.h>
#include <hltypes/hfile.h>
#include <hltypes/util.h>

#include "CodeSnippets.h"
#include "Bitmap.h"
#include "Color.h"
#include "Font.h"
#include "Rect.h"
#include "RGSSError.h"

namespace rgss
{
	/****************************************************************************************
	 * Pure C++ code
	 ****************************************************************************************/
	
	VALUE rb_cBitmap;

	Bitmap::Bitmap(int width, int height) : texture(NULL)
	{
		this->texture = april::rendersys->createEmptyTexture(width, height, april::AT_ARGB, april::AT_RENDER_TARGET);
		this->texture->setTextureWrapping(false);
		this->texture->setTextureFilter(april::Nearest);
		this->disposed = false;
	}

	Bitmap::Bitmap(chstr filename) : texture(NULL)
	{
		hstr fullFilename = april::rendersys->findTextureFile(filename);
		if (fullFilename == "")
		{
			/// @todo Has to throw Errno::ENOENT without using eval()
			//rb_raise(rb_eENOENT, ("No such file or directory - " + filename).c_str());
			hstr evalString = "raise Errno::ENOENT.new(\"" + filename + "\")";
			rb_eval_string(evalString.c_str());
		}
		this->_loadTexture(fullFilename);
		this->disposed = false;
	}

	Bitmap::~Bitmap()
	{
		this->dispose();
	}

	int Bitmap::getWidth()
	{
		return this->texture->getWidth();
	}

	int Bitmap::getHeight()
	{
		return this->texture->getHeight();
	}

	void Bitmap::blt(int x, int y, Bitmap* source, int sx, int sy, int sw, int sh)
	{
		this->_renderToTexture(x, y, source->texture, sx, sy, sw, sh);
	}

	void Bitmap::stretchBlt(int x, int y, int w, int h, Bitmap* source, int sx, int sy, int sw, int sh)
	{
		this->_renderToTexture(x, y, w, h, source->texture, sx, sy, sw, sh);
	}

	void Bitmap::_drawText(int x, int y, int w, int h, chstr text, int align)
	{
		atres::Alignment horizontal;
		switch (align)
		{
		case 1:
			horizontal = atres::CENTER;
			break;
		case 2:
			horizontal = atres::RIGHT;
			break;
		default:
			horizontal = atres::LEFT;
			break;
		}
		gmat4 viewMatrix = april::rendersys->getModelviewMatrix();
		gmat4 projectionMatrix = april::rendersys->getProjectionMatrix();
		april::TextureFilter filter = this->texture->getTextureFilter();
		this->texture->setTextureFilter(april::Linear);
		april::Texture* target = april::rendersys->getRenderTarget();
		april::rendersys->setRenderTarget(this->texture);
		april::rendersys->setIdentityTransform();
		april::rendersys->setOrthoProjection(grect(0.0f, 0.0f,
			(float)this->texture->getWidth(), (float)this->texture->getHeight()));
		hstr fontName = this->_getAtresFontName();
		grect destRect((float)x, (float)y, (float)w, atres::renderer->getFontResource(fontName)->getLineHeight());
		atres::renderer->drawText(fontName, destRect, text, horizontal,
			atres::BOTTOM, this->font->getColor()->toAprilColor());
		april::rendersys->setRenderTarget(target);
		this->texture->setTextureFilter(filter);
		april::rendersys->setProjectionMatrix(projectionMatrix);
		april::rendersys->setModelviewMatrix(viewMatrix);
	}

	hstr Bitmap::_getAtresFontName()
	{
		hstr result = this->font->getName();
		int h = this->font->getSize();
		if (!atres::renderer->hasFont(result))
		{
			result = atres::renderer->getFontResource("")->getName(); // default font
		}
		float fontHeight = atres::renderer->getFontHeight(result);
		if (h != fontHeight)
		{
			result += hsprintf(":%f", h / fontHeight);
		}
		return result;
	}

	void Bitmap::_loadTexture(chstr filename)
	{
		april::Texture* loadTexture = april::rendersys->loadTexture(filename);
		loadTexture->setTextureWrapping(false);
		int w = loadTexture->getWidth();
		int h = loadTexture->getHeight();
		this->texture = april::rendersys->createEmptyTexture(w, h, april::AT_ARGB, april::AT_RENDER_TARGET);
		this->texture->setTextureWrapping(false);
		this->texture->setTextureFilter(april::Nearest);
		this->_renderToTexture(0, 0, loadTexture, 0, 0, w, h);
		delete loadTexture;
	}

	void Bitmap::_renderToTexture(int x, int y, april::Texture* source, int sx, int sy, int sw, int sh, unsigned char alpha)
	{
		gmat4 viewMatrix = april::rendersys->getModelviewMatrix();
		gmat4 projectionMatrix = april::rendersys->getProjectionMatrix();
		april::TextureFilter filter = source->getTextureFilter();
		source->setTextureFilter(april::Nearest);
		april::Texture* target = april::rendersys->getRenderTarget();
		april::rendersys->setRenderTarget(this->texture);
		april::rendersys->setTexture(source);
		april::rendersys->setIdentityTransform();
		april::rendersys->setOrthoProjection(grect(0.0f, 0.0f,
			(float)this->texture->getWidth(), (float)this->texture->getHeight()));
		float width = (float)source->getWidth();
		float height = (float)source->getHeight();
		grect destRect((float)x, (float)y, (float)sw, (float)sh);
		grect srcRect(sx / width, sy / height, sw / width, sh / height);
		if (alpha == 255)
		{
			april::rendersys->drawTexturedQuad(destRect, srcRect);
		}
		else
		{
			april::rendersys->drawTexturedQuad(destRect, srcRect, april::Color(APRIL_COLOR_WHITE, alpha));
		}
		april::rendersys->setRenderTarget(target);
		source->setTextureFilter(filter);
		april::rendersys->setProjectionMatrix(projectionMatrix);
		april::rendersys->setModelviewMatrix(viewMatrix);
	}

	void Bitmap::_renderToTexture(int x, int y, int w, int h, april::Texture* source, int sx, int sy, int sw, int sh, unsigned char alpha)
	{
		if (w == sw && h == sh)
		{
			this->_renderToTexture(x, y, source, sx, sy, sw, sh, alpha);
			return;
		}
		gmat4 viewMatrix = april::rendersys->getModelviewMatrix();
		gmat4 projectionMatrix = april::rendersys->getProjectionMatrix();
		april::TextureFilter filter = source->getTextureFilter();
		source->setTextureFilter(april::Linear);
		april::Texture* target = april::rendersys->getRenderTarget();
		april::rendersys->setRenderTarget(this->texture);
		april::rendersys->setIdentityTransform();
		april::rendersys->setOrthoProjection(grect(0.0f, 0.0f,
			(float)this->texture->getWidth(), (float)this->texture->getHeight()));
		april::rendersys->setTexture(source);
		float width = (float)source->getWidth();
		float height = (float)source->getHeight();
		grect destRect((float)x, (float)y, (float)w, (float)h);
		grect srcRect(sx / width, sy / height, sw / width, sh / height);
		if (alpha == 255)
		{
			april::rendersys->drawTexturedQuad(destRect, srcRect);
		}
		else
		{
			april::rendersys->drawTexturedQuad(destRect, srcRect, april::Color(APRIL_COLOR_WHITE, alpha));
		}
		april::rendersys->setRenderTarget(target);
		source->setTextureFilter(filter);
		april::rendersys->setProjectionMatrix(projectionMatrix);
		april::rendersys->setModelviewMatrix(viewMatrix);
	}

	void Bitmap::_renderColor(grect rect, april::Color color)
	{
		gmat4 viewMatrix = april::rendersys->getModelviewMatrix();
		gmat4 projectionMatrix = april::rendersys->getProjectionMatrix();
		april::Texture* target = april::rendersys->getRenderTarget();
		april::rendersys->setRenderTarget(this->texture);
		april::rendersys->setIdentityTransform();
		april::rendersys->setOrthoProjection(grect(0.0f, 0.0f,
			(float)this->texture->getWidth(), (float)this->texture->getHeight()));
		april::rendersys->clear(true, false, rect, color);
		april::rendersys->setRenderTarget(target);
		april::rendersys->setProjectionMatrix(projectionMatrix);
		april::rendersys->setModelviewMatrix(viewMatrix);
	}

	void Bitmap::dispose()
	{
		if (!this->disposed)
		{
			if (this->texture != NULL)
			{
				delete this->texture;
				this->texture = NULL;
			}
			this->disposed = true;
		}
	}

	/****************************************************************************************
	 * Ruby Interfacing, Creation, Destruction, Systematics
	 ****************************************************************************************/
	
	void Bitmap::init()
	{
	}

	void Bitmap::destroy()
	{
	}

	void Bitmap::createRubyInterface()
	{
		rb_cBitmap = rb_define_class("Bitmap", rb_cObject);
		rb_define_alloc_func(rb_cBitmap, &Bitmap::rb_new);
		// initialize
		rb_define_method(rb_cBitmap, "initialize", RUBY_METHOD_FUNC(&Bitmap::rb_initialize), -1);
		rb_define_method(rb_cBitmap, "initialize_copy", RUBY_METHOD_FUNC(&Bitmap::rb_initialize_copy), 1);
		// getters and setters
		rb_define_method(rb_cBitmap, "width", RUBY_METHOD_FUNC(&Bitmap::rb_getWidth), 0);
		rb_define_method(rb_cBitmap, "height", RUBY_METHOD_FUNC(&Bitmap::rb_getHeight), 0);
		rb_define_method(rb_cBitmap, "rect", RUBY_METHOD_FUNC(&Bitmap::rb_getRect), 0);
		rb_define_method(rb_cBitmap, "font", RUBY_METHOD_FUNC(&Bitmap::rb_getFont), 0);
		rb_define_method(rb_cBitmap, "font=", RUBY_METHOD_FUNC(&Bitmap::rb_setFont), 1);
		// methods
		rb_define_method(rb_cBitmap, "get_pixel", RUBY_METHOD_FUNC(&Bitmap::rb_getPixel), 2);
		rb_define_method(rb_cBitmap, "set_pixel", RUBY_METHOD_FUNC(&Bitmap::rb_setPixel), 3);
		rb_define_method(rb_cBitmap, "fill_rect", RUBY_METHOD_FUNC(&Bitmap::rb_fillRect), -1); 
		rb_define_method(rb_cBitmap, "clear", RUBY_METHOD_FUNC(&Bitmap::rb_clear), 0); 
		rb_define_method(rb_cBitmap, "blt", RUBY_METHOD_FUNC(&Bitmap::rb_blt), -1); 
		rb_define_method(rb_cBitmap, "stretch_blt", RUBY_METHOD_FUNC(&Bitmap::rb_stretchBlt), -1); 
		// TODO - not implemented yet
			
		rb_define_method(rb_cBitmap, "dispose", RUBY_METHOD_FUNC(&Bitmap::rb_dispose), 0); 
		rb_define_method(rb_cBitmap, "disposed?", RUBY_METHOD_FUNC(&Bitmap::rb_isDisposed), 0); 
		rb_define_method(rb_cBitmap, "draw_text", RUBY_METHOD_FUNC(&Bitmap::rb_drawText), -1); 
		rb_define_method(rb_cBitmap, "hue_change", RUBY_METHOD_FUNC(&Bitmap::rb_changeHue), 1); 
		rb_define_method(rb_cBitmap, "text_size", RUBY_METHOD_FUNC(&Bitmap::rb_textSize), 1); 
	}
	
	void Bitmap::gc_mark(Bitmap* bitmap)
	{
		if (!NIL_P(bitmap->rb_font))
		{
			rb_gc_mark(bitmap->rb_font);
		}
	}

	void Bitmap::gc_free(Bitmap* bitmap)
	{
		bitmap->dispose();
	}

	VALUE Bitmap::rb_new(VALUE classe) 
	{
		Bitmap* bitmap;
		VALUE result = Data_Make_Struct(classe, Bitmap, Bitmap::gc_mark, Bitmap::gc_free, bitmap);
		bitmap->disposed = true;
		return result;
	}

	VALUE Bitmap::rb_initialize(int argc, VALUE* argv, VALUE self)
	{
		RB_SELF2CPP(Bitmap, bitmap);
		bitmap->disposed = false;
		VALUE arg1, arg2;
		rb_scan_args(argc, argv, "11", &arg1, &arg2);
		if (NIL_P(arg2))
		{
			hstr filename = StringValuePtr(arg1);
			hstr fullFilename = april::rendersys->findTextureFile(filename);
			if (fullFilename == "")
			{
				/// @todo Has to throw Errno::ENOENT without using eval()
				//rb_raise(rb_eENOENT, ("No such file or directory - " + filename).c_str());
				hstr evalString = "raise Errno::ENOENT.new(\"" + filename + "\")";
				rb_eval_string(evalString.c_str());
			}
			bitmap->_loadTexture(fullFilename);
		}
		else
		{
			int w = NUM2INT(arg1);
			int h = NUM2INT(arg2);
			if (w < 1 || h < 1)
			{
				rb_raise(rb_eRGSSError, "failed to create bitmap");
			}
			bitmap->texture = april::rendersys->createEmptyTexture(w, h, april::AT_ARGB, april::AT_RENDER_TARGET);
			bitmap->texture->setTextureWrapping(false);
			bitmap->texture->setTextureFilter(april::Nearest);
		}
		Bitmap::rb_setFont(self, Font::create(0, NULL));
		return self;
	}

	VALUE Bitmap::rb_initialize_copy(VALUE self, VALUE original)
	{
		RB_SELF2CPP(Bitmap, bitmap);
		RB_VAR2CPP(original, Bitmap, other);
		bitmap->disposed = false;
		int w = other->texture->getWidth();
		int h = other->texture->getHeight();
		bitmap->texture = april::rendersys->createEmptyTexture(w, h, april::AT_ARGB, april::AT_RENDER_TARGET);
		bitmap->texture->setTextureWrapping(false);
		bitmap->texture->setTextureFilter(april::Nearest);
		bitmap->_renderToTexture(0, 0, other->texture, 0, 0, w, h);
		// TODO - should be changed to call an actual clone method for convenience
		Bitmap::rb_setFont(self, rb_funcall(other->rb_font, rb_intern("clone"), 0, NULL));
		return self;
	}

	VALUE Bitmap::rb_dispose(VALUE self)
	{
		RB_SELF2CPP(Bitmap, bitmap);
		if (!bitmap->disposed)
		{
			//rb_raise(rb_eRGSSError, "disposed bitmap");
		}
		bitmap->dispose();
		return Qnil;
	}

	VALUE Bitmap::create(int argc, VALUE* argv)
	{
		VALUE object = Bitmap::rb_new(rb_cBitmap);
		object = Bitmap::rb_initialize(argc, argv, object);
		return object;
	}

	/****************************************************************************************
	 * Ruby Getters/Setters
	 ****************************************************************************************/

	VALUE Bitmap::rb_getWidth(VALUE self)
	{
		RB_SELF2CPP(Bitmap, bitmap);
		if (bitmap->disposed)
		{
			//rb_raise(rb_eRGSSError, "disposed bitmap");
		}
		return INT2FIX(bitmap->getWidth());
	}

	VALUE Bitmap::rb_getHeight(VALUE self)
	{
		RB_SELF2CPP(Bitmap, bitmap);
		if (bitmap->disposed)
		{
			//rb_raise(rb_eRGSSError, "disposed bitmap");
		}
		return INT2FIX(bitmap->getHeight());
	}

	VALUE Bitmap::rb_getRect(VALUE self)
	{
		RB_SELF2CPP(Bitmap, bitmap);
		if (bitmap->disposed)
		{
			//rb_raise(rb_eRGSSError, "disposed bitmap");
		}
		return Rect::create(INT2FIX(0), INT2FIX(0), INT2FIX(bitmap->getWidth()), INT2FIX(bitmap->getHeight()));
	}

	VALUE Bitmap::rb_getFont(VALUE self)
	{
		RB_SELF2CPP(Bitmap, bitmap);
		if (bitmap->disposed)
		{
			//rb_raise(rb_eRGSSError, "disposed bitmap");
		}
		return bitmap->rb_font;
	}

	VALUE Bitmap::rb_setFont(VALUE self, VALUE value)
	{
		RB_GENERATE_SETTER(Bitmap, bitmap, Font, font);
		if (bitmap->disposed)
		{
			//rb_raise(rb_eRGSSError, "disposed bitmap");
		}
		return value;
	}

	VALUE Bitmap::rb_isDisposed(VALUE self)
	{
		RB_SELF2CPP(Bitmap, bitmap);
		return (bitmap->disposed ? Qtrue : Qfalse);
	}

	/****************************************************************************************
	 * Ruby Methods
	 ****************************************************************************************/

	VALUE Bitmap::rb_getPixel(VALUE self, VALUE x, VALUE y)
	{
		RB_SELF2CPP(Bitmap, bitmap);
		if (bitmap->disposed)
		{
			//rb_raise(rb_eRGSSError, "disposed bitmap");
		}
		april::Color color = bitmap->texture->getPixel(NUM2INT(x), NUM2INT(y));
		VALUE argv[4] = {INT2FIX(color.r), INT2FIX(color.g), INT2FIX(color.b), INT2FIX(color.a)};
		return Color::create(4, argv);
	}

	VALUE Bitmap::rb_setPixel(VALUE self, VALUE x, VALUE y, VALUE color)
	{
		RB_SELF2CPP(Bitmap, bitmap);
		if (bitmap->disposed)
		{
			//rb_raise(rb_eRGSSError, "disposed bitmap");
		}
		RB_VAR2CPP(color, Color, cColor);
		bitmap->_renderColor(grect((float)NUM2INT(x), (float)NUM2INT(y), 1.0f, 1.0f), cColor->toAprilColor());
		return Qnil;
	}

	VALUE Bitmap::rb_fillRect(int argc, VALUE* argv, VALUE self)
	{
		if (argc != 2 && argc != 5)
		{
			hstr message = hsprintf("wrong number of arguments (%d for 2 or 5)", argc);
			rb_raise(rb_eArgError, message.c_str());
		}
		RB_SELF2CPP(Bitmap, bitmap);
		if (bitmap->disposed)
		{
			//rb_raise(rb_eRGSSError, "disposed bitmap");
		}
		int x, y, w, h;
		VALUE arg1, arg2, arg3, arg4, color;
		rb_scan_args(argc, argv, "23", &arg1, &arg2, &arg3, &arg4, &color);
		if (NIL_P(arg3) && NIL_P(arg4) && NIL_P(color))
		{
			color = arg2;
			RB_VAR2CPP(arg1, Rect, rect);
			x = rect->x;
			y = rect->y;
			w = rect->width;
			h = rect->height;
		}
		else
		{
			x = NUM2INT(arg1);
			y = NUM2INT(arg2);
			w = NUM2INT(arg3);
			h = NUM2INT(arg4);
		}
		RB_VAR2CPP(color, Color, cColor);
		bitmap->_renderColor(grect((float)x, (float)y, (float)w, (float)h), cColor->toAprilColor());
		return Qnil;
	}

	VALUE Bitmap::rb_clear(VALUE self)
	{
		RB_SELF2CPP(Bitmap, bitmap);
		if (bitmap->disposed)
		{
			//rb_raise(rb_eRGSSError, "disposed bitmap");
		}
		bitmap->_renderColor(grect(0.0f, 0.0f, (float)bitmap->texture->getWidth(),
			(float)bitmap->texture->getHeight()), APRIL_COLOR_CLEAR);
		return Qnil;
	}

	VALUE Bitmap::rb_blt(int argc, VALUE* argv, VALUE self)
	{
		RB_SELF2CPP(Bitmap, bitmap);
		if (bitmap->disposed)
		{
			//rb_raise(rb_eRGSSError, "disposed bitmap");
		}
		VALUE arg1, arg2, arg3, arg4, arg5;
		rb_scan_args(argc, argv, "41", &arg1, &arg2, &arg3, &arg4, &arg5);
		int x = NUM2INT(arg1);
		int y = NUM2INT(arg2);
		RB_VAR2CPP(arg3, Bitmap, source);
		RB_VAR2CPP(arg4, Rect, rect);
		if (NIL_P(arg5))
		{
			bitmap->_renderToTexture(x, y, source->texture, rect->x, rect->y, rect->width, rect->height);
		}
		else
		{
			bitmap->_renderToTexture(x, y, source->texture, rect->x, rect->y, rect->width, rect->height,
				(unsigned char)NUM2INT(arg5));
		}
		return Qnil;
	}

	VALUE Bitmap::rb_stretchBlt(int argc, VALUE* argv, VALUE self)
	{
		RB_SELF2CPP(Bitmap, bitmap);
		if (bitmap->disposed)
		{
			//rb_raise(rb_eRGSSError, "disposed bitmap");
		}
		VALUE arg1, arg2, arg3, arg4;
		rb_scan_args(argc, argv, "31", &arg1, &arg2, &arg3, &arg4);
		RB_VAR2CPP(arg1, Rect, dest_rect);
		RB_VAR2CPP(arg2, Bitmap, source);
		RB_VAR2CPP(arg3, Rect, src_rect);
		if (NIL_P(arg4))
		{
			bitmap->_renderToTexture(dest_rect->x, dest_rect->y, dest_rect->width, dest_rect->height,
				source->texture, src_rect->x, src_rect->y, src_rect->width, src_rect->height);
		}
		else
		{
			bitmap->_renderToTexture(dest_rect->x, dest_rect->y, dest_rect->width, dest_rect->height,
				source->texture, src_rect->x, src_rect->y, src_rect->width, src_rect->height,
				(unsigned char)NUM2INT(arg4));
		}
		return Qnil;
	}

	/****************************************************************************************
	 * TODO
	 ****************************************************************************************/

	VALUE Bitmap::rb_drawText(int argc, VALUE* argv, VALUE self)
	{
		if (argc != 2 && argc != 3 && argc != 5 && argc != 6)
		{
			hstr message = hsprintf("wrong number of arguments (%d for 2, 3, 5 or 6)", argc);
			rb_raise(rb_eArgError, message.c_str());
		}
		RB_SELF2CPP(Bitmap, bitmap);
		if (bitmap->disposed)
		{
			//rb_raise(rb_eRGSSError, "disposed bitmap");
		}
		int x, y, w, h;
		hstr text;
		VALUE arg1, arg2, arg3, arg4, arg5, arg6;
		rb_scan_args(argc, argv, "24", &arg1, &arg2, &arg3, &arg4, &arg5, &arg6);
		if (NIL_P(arg4) && NIL_P(arg5) && NIL_P(arg6))
		{
			RB_VAR2CPP(arg1, Rect, rect);
			x = rect->x;
			y = rect->y;
			w = rect->width;
			h = rect->height;
			text = hstr(StringValuePtr(arg2));
		}
		else
		{
			x = NUM2INT(arg1);
			y = NUM2INT(arg2);
			w = NUM2INT(arg3);
			h = NUM2INT(arg4);
			text = hstr(StringValuePtr(arg5));
			arg3 = arg6;
		}
		int align = (NIL_P(arg3) ? 0 : NUM2INT(arg3));
		bitmap->_drawText(x, y, w, h, text, align);
		return Qnil;
	}

	VALUE Bitmap::rb_changeHue(VALUE self, VALUE hue)
	{
		RB_SELF2CPP(Bitmap, bitmap);
		if (bitmap->disposed)
		{
			//rb_raise(rb_eRGSSError, "disposed bitmap");
		}
		bitmap->texture->rotateHue((float)NUM2DBL(hue));
		return Qnil;
	}

	VALUE Bitmap::rb_textSize(VALUE self, VALUE string)
	{
		/// @todo Test this.
		RB_SELF2CPP(Bitmap, bitmap);
		if (bitmap->disposed)
		{
			//rb_raise(rb_eRGSSError, "disposed bitmap");
		}
		hstr text = StringValuePtr(string);
		hstr fontName = bitmap->_getAtresFontName();
		float w = atres::renderer->getTextWidthUnformatted(fontName, text);
		int h = bitmap->font->getSize();
		return Rect::create(INT2FIX(0), INT2FIX(0), INT2FIX((int)ceil(w)), INT2FIX(h));
	}

}
