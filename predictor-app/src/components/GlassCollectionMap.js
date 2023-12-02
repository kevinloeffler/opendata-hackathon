import React, { useState, useEffect } from 'react';
import { GoogleMap, useLoadScript, DirectionsRenderer } from '@react-google-maps/api';
import GlassMarker from './GlassMarker';
import {  useSelector } from "react-redux";


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

const GlassCollectionMap = ({ key }) => {
  useEffect(() => {
    // This effect will run whenever the key prop changes
    console.log('ChildComponent has been re-rendered with a new key:', key);

    // Add any logic here to update the component with new data
  }, [key]);

  const sensors = useSelector((state) => state.sensor.sensors);
  const predictedRoute = useSelector((state) => state.predictedRoute.predictedRoute);

  console.log(sensors);
  console.log(predictedRoute);

  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
    libraries,
  });
  const [response, setResponse] = useState(null);
  const [travelMode, setTravelMode] = useState('DRIVING'); // You can change the travel mode as needed

  useEffect(() => {
    if (isLoaded && predictedRoute) {
      const directionsService = new window.google.maps.DirectionsService();

      const origin = {
        lat: Number(predictedRoute[0][0]),
        lng: Number(predictedRoute[0][1]),
      };

      const destination = {
        lat: Number(predictedRoute[predictedRoute.length - 1][0]),
        lng: Number(predictedRoute[predictedRoute.length - 1][1]),
      };

      const waypoints = predictedRoute.slice(1, predictedRoute.length - 1).map((sensor) => {
        console.log(parseFloat(sensor.lat).toFixed(7), parseFloat(sensor.lng).toFixed(7));

        return {
          location: new window.google.maps.LatLng(parseFloat(sensor.lat).toFixed(7), parseFloat(sensor.lng).toFixed(7)),
          stopover: true,
        };
      });
    
      directionsService.route(
        {
          origin: new window.google.maps.LatLng(origin.lat, origin.lng),
          destination: new window.google.maps.LatLng(destination.lat, destination.lng),
          waypoints: waypoints,
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
  }, [isLoaded, travelMode, predictedRoute]);

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

      { sensors ? 
        sensors.map((sensor, index) => (
          <GlassMarker
            key={index}
            title={sensor.sensor_id}
            position={{ lat: Number(sensor.geo_point_2d.split(',')[0]), 
                        lng:  Number(sensor.geo_point_2d.split(',')[1]) }}
            prediction={sensor.prediction}
            type={sensor.type}
            date={sensor.date}
            level={sensor.level}
          />
        )) : null
      }

      {directions}

    </GoogleMap>
  );

}

export default GlassCollectionMap;