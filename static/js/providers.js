"use strict";

// initialize google maps 
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

// create provider object for google maps
function providerObjectMap(provider) {

  const providerObject = new Object();
    providerObject.name = provider.presentation_name;
    providerObject.coords = {'lat': provider.latitude,
                             'lng': provider.longitude}; 
  
  return providerObject
}


const providerInfo = (provider) => {
  const providerDesc = (`\
    <div class="provider">
      <p>${provider.presentation_name}</p> \
      <p><b>Organization:</b> ${provider.organization_name}</p> \
      <p><b>Specialty:</b> ${provider.specialty}</p> \
      <p><b>Address:</b> ${provider.street_line_1} ${provider.street_line_2}
                        ${provider.city} ${provider.state} ${provider.zip_code}</p> \
      <p><b>Phone:</b> ${provider.phone}</p> \
    </div> \
      `);

  return providerDesc;
};

// function to process provider information
const showProviders = (providers) => {

  // display text information
  const allProvidersInfo = [];
  
  // object information for google maps
  // const allProviderObjects = [];
  const allProviderObjects = new Set();

  const allProviders = $('#display-providers-div');

  for (const provider of providers) {
    
    const providerDesc = providerInfo(provider);
    allProvidersInfo.push(providerDesc);

    const providerObject = providerObjectMap(provider);
    allProviderObjects.add(providerObject);
    // if (!( providerObject) in allProviderObjects) {
    //   allProviderObjects.push(providerObject);
    // };

  };

  console.log(allProviderObjects);
  allProviders.html(allProvidersInfo);
  // call google maps api
  initMap();
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
  
  $.get('/show_providers', formInput, showProviders);
  $('#map').show()
});



  


