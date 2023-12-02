import React, { useState, useEffect } from 'react';
import { GoogleMap, useLoadScript, DirectionsRenderer } from '@react-google-maps/api';
import GlassMarker from '../GlassMarker';

const libraries = ['places'];
const mapContainerStyle = {
  width: '100%',
  height: '92vh',
};

// st. gallen city center
const center = {
  lat: 47.4245, // default latitude
  lng: 9.3767, // default longitude
};
const zoom = 13;

const GlassCollectionMap = () => {

  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
    libraries,
  });
  const [response, setResponse] = useState(null);
  const [travelMode, setTravelMode] = useState('DRIVING'); // You can change the travel mode as needed

  const origin = center;
  const destination = { lat: 47.4215, lng: 9.2375 };

  useEffect(() => {
    if (isLoaded) {
      const directionsService = new window.google.maps.DirectionsService();

      directionsService.route(
        {
          origin: new window.google.maps.LatLng(origin.lat, origin.lng),
          destination: new window.google.maps.LatLng(destination.lat, destination.lng),
          travelMode: travelMode,
        },
        (result, status) => {
          if (status === 'OK') {
            setResponse(result);
          } else {
            console.error(`Directions request failed due to ${status}`);
          }
        }
      );
    }
  }, [isLoaded, origin, travelMode]);

  if (loadError) {
    return <div>Error loading maps</div>;
  }

  if (!isLoaded) {
    return <div>Loading maps</div>;
  }

  const directions = response ? (
    <DirectionsRenderer
      directions={response}
      options={{
        polylineOptions: {
          strokeColor: '#1E90FF', // You can customize the color of the route polyline
          strokeWeight: 4,
        },
        suppressMarkers: true
      }}
    />
  ) : null;

  return (
    <GoogleMap
      mapContainerStyle={mapContainerStyle}
      mapTypeId='hybrid'
      zoom={zoom}
      center={center}
    >

      <GlassMarker position={center} title={'test !!!'} />

      <GlassMarker position={destination} title={'Test 2'} />
      
      {directions}

    </GoogleMap>
  );

}

export default GlassCollectionMap;