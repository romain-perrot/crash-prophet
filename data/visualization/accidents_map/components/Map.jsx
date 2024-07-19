import mapboxgl from 'mapbox-gl';
import { useEffect, useState, useRef } from 'react';
import styles from '../styles/map.module.css';

// Define the access token that will enable to download the vector tileset.
mapboxgl.accessToken = 'pk.eyJ1IjoiaHctZG1tbC1waW5rLXR3aW5zIiwiYSI6ImNsbmJqeXhicTAzcGkyaXRkZm9iNXl1aWgifQ.5EJ_Ybb09Mt3zeLEecjCKQ';

// Define the default configuration of the map.
const mapxboxgl_conf = {
	'style_url': 'mapbox://styles/mapbox/streets-v12', // The style of the map (is it )
	'start_center': [-0.127758, 51.507351], // The coordinate that will be at the center of the map.
	'start_zoom': 11, // The starting zoom scope.
	// The vector tileset is a representation graphical representation of our dataset
	// it can be loaded to be drawn on a map.
	'vector_tileset': {
		'url': 'mapbox://hw-dmml-pink-twins.ds0i3i5u',
		'sourceID': 'accidents-vector-tileset-source',
		'sourceLayerID': 'accidents-coord-78wczu',
		'layerID': 'accidents-layer',
	},
};

export default function Map() {
	const mapContainer = useRef(null);
	const [map, setMap] = useState(null);

	useEffect(() => {
		// Create Map instance with starting configuration.
		const map = new mapboxgl.Map({
			container: mapContainer.current,
			style: mapxboxgl_conf.style_url,
			center: mapxboxgl_conf.start_center,
			zoom: mapxboxgl_conf.start_zoom,
		});

		map.on('load', () => {
			// Download the vector tileset from the Mapbox GL servers.
			map.addSource(mapxboxgl_conf.vector_tileset.sourceID, {
				type: 'vector',
				url: mapxboxgl_conf.vector_tileset.url,
			});

			// Load the vector tileset on the map as a cluster of circles.
			map.addLayer({
				'id': mapxboxgl_conf.vector_tileset.layerID,
				'type': 'circle',
				'source': mapxboxgl_conf.vector_tileset.sourceID,
				'source-layer': mapxboxgl_conf.vector_tileset.sourceLayerID,
				'paint': {
					'circle-radius': {
						'base': 1.75,
						'stops': [
							[12, 2],
							[22, 180]
						]
					},
					'circle-color': '#FF0000',
				},
			});

			// Load the map.
			setMap(map);
		});

		// Clean up on unmount
		return () => map.remove();
	}, []);

  return (
    <div>
      <main>
        <div ref={mapContainer} className={styles.mapContainer} />
      </main>
    </div>
  );
}
