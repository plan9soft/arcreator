#include <april/Keys.h>
#ifndef LEGACY_ONLY
#include <aprilui/aprilui.h>
#endif
#include <hltypes/harray.h>
#include <legacy/Input.h>

#include "CodeSnippets.h"
#include "Context.h"
#include "System.h"

namespace reactor
{
	Context* context = NULL;
	
	/****************************************************************************************
	 * Construct/Destruct
	 ****************************************************************************************/

	Context::Context() : mouse(IDLE)
	{
		for_iter (i, 0, MAX_KEYS)
		{
			this->controlKeys += i;
		}
		this->reset();
	}

	Context::~Context()
	{
	}

	/****************************************************************************************
	 * Properties
	 ****************************************************************************************/

	Context::State Context::getState()
	{
		return (this->states.size() == 0 ? Context::DEFAULT : this->states.back());
	}
	
	void Context::setState(Context::State value)
	{
		this->states += value;
	}
	
	/****************************************************************************************
	 * Update
	 ****************************************************************************************/
	
	void Context::update()
	{
		switch (this->mouse)
		{
		case TRIGGER:
			this->mouse = PRESS;
			break;
		case RELEASE:
			this->mouse = IDLE;
			break;
		}
		foreach (unsigned int, it, this->controlKeys)
		{
            if (this->keys[*it])
			{
                this->released[*it] = false;
                if (!this->pressed[*it])
				{
                    this->pressed[*it] = true;
                    this->triggered[*it] = true;
				}
                else
				{
                    this->triggered[*it] = false;
				}
			}
            else if (!this->released[*it])
			{
                this->triggered[*it] = false;
                if (this->pressed[*it])
				{
                    this->pressed[*it] = false;
                    this->released[*it] = true;
				}
			}
            else
			{
                this->released[*it] = false;
			}
		}
	}

	void Context::reset()
	{
		this->mouse = IDLE;
		for_iter (i, 0, MAX_KEYS)
		{
			this->triggered[i] = false;
			this->pressed[i] = false;
			this->released[i] = false;
			this->keys[i] = false;
		}
		this->states.clear();
	}

	void Context::onMouseDown(float x, float y, int button)
	{
		reactor::context->mouse = TRIGGER;
	}

	void Context::onMouseUp(float x, float y, int button)
	{
		reactor::context->mouse = RELEASE;
	}
	
	void Context::onMouseMove(float x, float y)
	{
#ifndef LEGACY_ONLY
		aprilui::updateCursorPosition();
#endif
	}
	
	void Context::onKeyDown(unsigned int keycode)
	{
		reactor::context->keys[keycode] = true;
		legacy::Input::onKeyDown(keycode);
	}

	void Context::onKeyUp(unsigned int keycode)
	{
		reactor::context->keys[keycode] = false;
		legacy::Input::onKeyUp(keycode);
	}
	
	void Context::onChar(unsigned int charcode)
	{
	}
	
	/****************************************************************************************
	 * Mouse States
	 ****************************************************************************************/

	bool Context::isMouseTriggered()
	{
		return (this->mouse == TRIGGER);
	}

	bool Context::isMousePressed()
	{
		return (this->mouse == TRIGGER || this->mouse == PRESS);
	}

	bool Context::isMouseReleased()
	{
		return (this->mouse == RELEASE);
	}

	/****************************************************************************************
	 * Keyboard States
	 ****************************************************************************************/

	bool Context::isKeyTriggered(unsigned int keycode)
	{
		return this->triggered[keycode];
	}
	
	bool Context::isKeyPressed(unsigned int keycode)
	{
		return this->pressed[keycode];
	}
	
	bool Context::isKeyReleased(unsigned int keycode)
	{
		return this->released[keycode];
	}

	/****************************************************************************************
	 * Context States setters
	 ****************************************************************************************/

	void Context::setPrevious()
	{
		if (this->states.size() > 0)
		{
			this->states.pop_back();
		}
	}

}