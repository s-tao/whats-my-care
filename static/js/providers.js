"use strict";

// click event to send user input for provider form to server
$('#provider-form').on('submit', (evt) => {
  evt.preventDefault();

  const zipCode = $('input[type="zipcode"]').val();
  const radius = $('select[name="radius"]').val();
  const planId = $('input[type="plan-id"]').val();

  const formInput = {
    'submit': true,
    'zipCode': zipCode,
    'radius': radius,
    'planId': planId
  };
  
  // add return value -json after api call is fixed
  $.get(url, formInput);
  
});



  

