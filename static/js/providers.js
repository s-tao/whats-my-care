"use strict";


function providerInfo(provider) {
  const providerDesc = (`\
    <p>${provider.presentation_name}</p> \
    <p><b>Organization:</b> ${provider.organization_name}</p> \
    <p><b>Specialty:</b> ${provider.specialty}</p> \
    <p><b>Address:</b> ${provider.street_line_1, provider.street_line_2,
                         provider.city, provider.state, provider.zip_code}</p> \
    <p><b>Phone:</b> ${provider.phone}</p> \
    `);

  return providerDesc;
};

function showProviders(providers) {

  const allProvidersInfo = [];
  const allProviders = $('.all-providers');

  for (const provider of providers) {
    
    const providerDesc = providerInfo(provider);

    allProvidersInfo.push(providerDesc);
  };

  allProviders.html(allProvidersInfo);
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
  
});



  

