"use strict";

// initialize google maps 
function initMap(providers) {
  const generalMap = new google.maps.Map(
    document.querySelector('#map'), {
      center: {
        lat: 37.773972, 
        lng: -122.431297
      },
      zoomControl: true,
      controlSize: 20,
    });
  
  const latLngs = [];
  const markers = [];

  for (const providerLocation of providers) {

    if (!(providerLocation.street_line_2)) {
      providerLocation.street_line_2 = ''
    };

    markers.push(new google.maps.Marker({
      position: {
        lat: providerLocation.latitude,
        lng: providerLocation.longitude
      },
      adr: {
        street1: providerLocation.street_line_1,
        street2: providerLocation.street_line_2,
        city: providerLocation.city,
        state: providerLocation.state,
        zipCode: providerLocation.zip_code
      },
      providerId: providerLocation.id,
      title: providerLocation.presentation_name,
      map: generalMap,
      icon: {
        url: '/static/img/healthcare_marker.svg',
        scaledSize: {
          width: 30,
          height: 30
          }
        }
      })
    );

    
    
    // Sets the map on all markers in the array.
    latLngs.push({
      lat: providerLocation.latitude,
      lng: providerLocation.longitude
    });
  }

  // set boundary for viewport relative to markers 
  const bounds = new google.maps.LatLngBounds();
  for (const latLng of latLngs) {
    bounds.extend(latLng);
  };

  generalMap.setCenter(bounds.getCenter());
  generalMap.fitBounds(bounds);

  // object to match marker to infoWindow
  const markerToInfoWindow = {};
  // creating infoWindow content for each marker
  for (const marker of markers) {
    const markerInfo = (` 
    <label>
      ${marker.title}
    </label> 
    <p>Located at: 
    <br>
      <em>
        ${marker.adr.street1} 
        ${marker.adr.street2} 
        ${marker.adr.city} 
        ${marker.adr.state} 
        ${marker.adr.zip_code}
      </em>
    </p>
    `);

    const infoWindow = new google.maps.InfoWindow({
      content: markerInfo,
      maxWidth: 200,
    });

    markerToInfoWindow[marker.providerId] = infoWindow;

    marker.addListener('mouseover', () => {
      infoWindow.open(generalMap, marker);
    });

    marker.addListener('mouseout', () => {
      infoWindow.close();
    });
  }

  // current active markers from accordion
  const selectMarkers = [];

  $('.accordion-item').click(function() {

    const accordionId = $(this).attr('id');
    const accordionActive = $(this).hasClass('is-active');
    if (accordionActive == true) {
      for (const marker of markers) {
        if (accordionId == marker.providerId) {
          selectMarkers.push(marker);
          marker.setMap(generalMap);
          markerToInfoWindow[marker.providerId].open(generalMap, marker);
        }
      };
    } else {
      for (const marker of selectMarkers) { 
        if (accordionId == marker.providerId) {
          marker.setMap(null);
        };
      };
    };
  });

  // show buttons for google map functions
  $('#floating-panel').show();
  
  // Removes the markers from the map, but keeps them in the array.
  $('#btn-hide-markers').on('click', () => {
    for (let i = 0; i < markers.length; i++) {
      markers[i].setMap(null);
    };
  });
  
  // Shows all markers
  $('#btn-show-markers').on('click', () => {
    for (let i = 0; i < markers.length; i++) {
      markers[i].setMap(generalMap);
    };
  });
  
}


const providerInfo = (provider) => {

  if (!(provider.street_line_2)) {
    provider.street_line_2 = ''
  };

  if (!(provider.organization_name)) {
    provider.organization_name = 'N/A'
  };


  const providerDesc = (`
    <li class="accordion-item" data-accordion-item id="${provider.id}">
      <a href="#" class="accordion-title">
        ${provider.presentation_name}
      </a>
      <div class="accordion-content" data-tab-content>
        <p>
          <b>Organization:</b> 
          ${provider.organization_name}
        </p>
        <p>
          <b>Specialty:</b> 
          ${provider.specialty}
        </p>
        <p>
          <b>Address:</b>
          ${provider.street_line_1}
          ${provider.street_line_2}
          ${provider.city}
          ${provider.state}
          ${provider.zip_code}
        </p>
        <p>
          <b>Phone:</b> 
          ${provider.phone}
        </p>
      </div>
    </li>
  `);

  return providerDesc;
};

// function to process provider information
const showProviders = (providers) => {
  const allProviders = $('#display-providers');

  for (const provider of providers) {
    const providerDesc = providerInfo(provider);
    allProviders.append(providerDesc);
  };

  // reload foundation script once provider information is displayed
  Foundation.reInit(allProviders);
 
  // call google maps api
  initMap(providers);
};

// click event to send user input for provider form to server
$('#provider-form').on('submit', showProviders, (evt) => {
  evt.preventDefault();


  const planId = $('input[list="plan-id"]').val();
  const zipCode = $('input[type="zipcode"]').val();
  const radius = $('select[name="radius"]').val();
  const providerType = $('select[name="provider-type"]').val();
  const searchTerm = $('input[type="search-term"]').val();

  const formInput = {
    'planId': planId,
    'zipCode': zipCode,
    'radius': radius,
    'providerType': providerType,
    'searchTerm': searchTerm
  };
  
  $.get('/show_providers.json', formInput, showProviders);
  $('#map').show()

});


