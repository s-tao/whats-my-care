"use strict";

$('#form-plan-group').on('submit', (evt) => {
  evt.preventDefault();
  
  const formData ={
    option: $('#plan-type-field').val()
  };

  $.get('/users/{{ user.user_id }}/show_plans', formData, (res) => {
    alert("hi");
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
