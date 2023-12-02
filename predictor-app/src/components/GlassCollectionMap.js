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
  //const predictedRoute = useSelector((state) => state.predictedRoute.predictedRoute);

  const predictedRoute = [
    [
      47.4156038,
      9.3325804
    ],
    {
      "date": "Sat, 21 May 2022 00:00:00 GMT",
      "lat": "47.4351834416",
      "level": 0.1217434210526317,
      "lng": "9.3918149135",
      "sensor_id": "107132 | 255E",
      "type": "Glas / Grün,YMATRON"
    },
    {
      "date": "Mon, 10 Oct 2022 00:00:00 GMT",
      "lat": "47.412065012904804",
      "level": 0.6643749999999999,
      "lng": "9.335980774191682",
      "sensor_id": "107026 | 67BE",
      "type": "YMATRON,Glas / Braun"
    },
    {
      "date": "Mon, 10 Oct 2022 00:00:00 GMT",
      "lat": "47.41208",
      "level": 0.4225,
      "lng": "9.33586",
      "sensor_id": "107068 | 4455",
      "type": "YMATRON,Glas / Grün"
    },
    {
      "date": "Mon, 10 Oct 2022 00:00:00 GMT",
      "lat": "47.41209608066285",
      "level": 0.40874999999999995,
      "lng": "9.33591068841119",
      "sensor_id": "107072 | F389",
      "type": "Glas / Weiss,YMATRON"
    },
    {
      "date": "Mon, 10 Oct 2022 00:00:00 GMT",
      "lat": "47.40792974774064",
      "level": 0.67225,
      "lng": "9.33352525794038",
      "sensor_id": "107065 | 4A3D",
      "type": "Glas / Weiss,YMATRON"
    },
    {
      "date": "Mon, 10 Oct 2022 00:00:00 GMT",
      "lat": "47.40798",
      "level": 0.6775,
      "lng": "9.33388",
      "sensor_id": "107077 | 2CC4",
      "type": "YMATRON,Glas / Grün"
    },
    [
      47.4156038,
      9.3325804
    ]
  ];

  console.log(sensors);

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

      //console.log(waypoints);
      console.log(origin);
      console.log(destination);

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
  }, [isLoaded, travelMode,]);

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