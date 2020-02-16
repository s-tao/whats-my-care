"use strict";



$('#form-plan-group').on('submit', (evt) => {
  evt.preventDefault();
  
  // find a way to transfer over user_id to obtain url 
  $.get(`/users/${user_id}/show_plans`, (res) => {
    $('#display-name').html(res.display_name);
    $('#plan-id').html(res.id);
    $('#carrier-name').html(res.carrier_name);
  });
});




// // $( "#get-login" ).submit(function( evt ) {
// //   if ( $( "email" ).first().val() != { email } ) {
// //     $( ".login-process" ).text( "Incorrect Login" ).show().fadeOut( 1000 );
// //     event.preventDefault();
// //   }
// // });

// // $('#get-login').on('submit', (evt) => {
// //   evt.preventDefault();

// //   const formInputs = {
// //     'email': $('email').val(),
// //     'password': $('password').val()
// //   };

// //   $.post('/login', formInputs, (res) => {
// //     alert(res);
// //   });
// // });


// $('#select-plan-type').on('submit', (evt) => {
//   evt.preventDefault();


// $('#favorite').on('click', () => {

//   fetch('/test/1')
//     .then((resp) => resp.json()) // Transform the data into json
//     .then(function(data) {
//     alert(JSON.stringify(data))
//     });
//   });
