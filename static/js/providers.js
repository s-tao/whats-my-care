"use strict";

// click event to send user input for provider form to server
$('#provider-form').on('submit', (evt) => {
  evt.preventDefault();

  const planId = $('input[type="plan-id"]').val();
  const newPlanId = $('input[type="new-plan-id"]').val();
  const zipCode = $('input[type="zipcode"]').val();
  const radius = $('select[name="radius"]').val();
  const providerType = $('select[name="provider-type"]').val();
  const searchTerm = $('input[type="search-term"]').val();

  const formInput = {
    'planId': planId,
    'newPlanId': newPlanId,
    'zipCode': zipCode,
    'radius': radius,
    'providerType': providerType,
    'searchTerm': searchTerm
  };
  
  // add return value -json after api call is fixed
  $.get('/show_providers', formInput);
  
});



  

