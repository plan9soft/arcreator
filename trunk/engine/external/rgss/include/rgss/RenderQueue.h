#ifndef RGSS_RENDER_QUEUE_H
#define RGSS_RENDER_QUEUE_H

#include <hltypes/harray.h>

#include "rgssExport.h"

namespace rgss
{
	class Renderable;
	class Tilemap;

	/// @brief Represents a render queue to organize renderable objects by Z order and creation order and make functionality of RGSS's Viewport class easier to implement.
	class rgssExport RenderQueue
	{
	public:
		/// @brief Constructor.
		RenderQueue();
		/// @brief Destructor.
		~RenderQueue();

		/// @brief Draws this RenderQueue.
		void draw();
		/// @brief Adds a new renderable object.
		/// @param[in] renderable The renderable object to be added.
		void add(Renderable* renderable);
		/// @brief Removes the renderable object.
		/// @param[in] renderable The renderable object to be removed.
		void remove(Renderable* renderable);
		/// @brief Updates a renderable object because of a change in the Z coordinate.
		/// @param[in] renderable The renderable object that has changed.
		void update(Renderable* renderable);

		void addCollection(Tilemap* collection);
		void removeCollection(Tilemap* collection);

	protected:
		/// @brief Contains all renderable objects.
		harray<Renderable*> renderables;
		/// @brief Contains all collection objects.
		harray<Renderable*> collections;
		/// @brief Needs-Sorting flag.
		bool needsSorting;

	};

}
#endif