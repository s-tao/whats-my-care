"use strict";

function showProviders(providers) {
  const allProviders = $('.all-providers');
  allProviders.html(providers);
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



  

