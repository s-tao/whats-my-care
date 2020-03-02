"use strict";

function initMap() {
  const generalMap = new google.maps.Map(
    document.querySelector('#map'), {
      center: {
        lat: 37.773972, 
        lng: -122.431297
      },
      zoom: 10,
      zoomControl: true,
    }
  );

};


