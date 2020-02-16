"use strict";

// function to display specific plan information
function individualMedPlan(res) {

  $('#display-name').html(res[num].display_name);
  $('#plan-id').html(res[num].id);
  $('#carrier-name').html(res[num].carrier_name);
};

// function to get flask response to display individualPlan 
function showMedPlans(evt){
  evt.preventDefault();

  // import user id instead of hard coding url

  // let url = `/users/${res[0].user_id}/show_plans`
  $.get('/users/1/show_plans', individualMedPlan);
};

// event listener activates when user submits
$('#form-plan-group').on('submit', showMedPlans);

// create function to obtain user_id
// function getUserID()


  let num = 0;
  num ++




//   $.get('/users/1/show_plans', (res) => {

//     $('#display-name').html(res[num].display_name);
//     $('#plan-id').html(res[num].id);
//     $('#carrier-name').html(res[num].carrier_name);
//   });
// };

// $('#form-plan-group').on('submit', individualPlan, (evt) => {
//   evt.preventDefault();
  




// LOGIN & REGISTER
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
