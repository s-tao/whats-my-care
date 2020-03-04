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
        zip_code: providerLocation.zip_code
      },
      specialty: providerLocation.specialty,
      title: providerLocation.presentation_name,
      map: generalMap,
      icon: {
        url: '/static/img/healthcare_marker.svg',
        scaledSize: {
          width: 30,
          height: 30
        }
      }
    }));

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

  for (const marker of markers) {
    const markerInfo = (` \
    <label>${marker.title}</label> \
    <p> Located at: <br>
      <em>${marker.adr.street1} ${marker.adr.street2} ${marker.adr.city} 
      ${marker.adr.state} ${marker.adr.zip_code}</em>
    </p>
    `);

    const infoWindow = new google.maps.InfoWindow({
      content: markerInfo,
      maxWidth: 200,
    });

    marker.addListener('mouseover', () => {
      infoWindow.open(generalMap, marker);
    });

    marker.addListener('mouseout', () => {
      infoWindow.close();
    });
  }
};


const providerInfo = (provider) => {

  if (!(provider.street_line_2)) {
    provider.street_line_2 = ''
  };

  if (!(provider.organization_name)) {
    provider.organization_name = 'N/A'
  };

  const providerDesc = (`\
    <li class="accordion-item" data-accordion-item> \
      <a href="#${provider.id}" class="accordion-title">${provider.presentation_name}</a> \
      <div class="accordion-content" data-tab-content id="${provider.id} > \
        <p><b>Organization:</b> ${provider.organization_name}</p> \
        <p><b>Specialty:</b> ${provider.specialty}</p> \
        <p><b>Address:</b> ${provider.street_line_1} ${provider.street_line_2} \
                            ${provider.city} ${provider.state} ${provider.zip_code}</p> \
        <p><b>Phone:</b> ${provider.phone}</p> \
      </div> \
    </li> \
  `)

  return providerDesc;
};

// function to process provider information
const showProviders = (providers) => {

  // display text information
  const allProvidersInfo = [];
  
  const allProviders = $('#display-providers');

  for (const provider of providers) {
    
    const providerDesc = providerInfo(provider);
    allProvidersInfo.push(providerDesc);

  };

  allProviders.html(allProvidersInfo);
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


// const toggleProvider = $('abv');

// toggleProvider.click(function() {
  
//   const providerId = $(this).attr('div id');
//   console.log(providerId);

//   // $('.accordion-item').foundation('toggle', '.accordion-content');
//   // $('#' + providerId ).toggle( ".accordion-content" );
//   $('#display-providers').foundation('toggle', $(providerId));

// });

// $('#display-providers').foundation('toggle', $('#abv'));


