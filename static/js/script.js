"use strict";

// function to display specific plan information
function individualMedPlan(res) {
  $('#plan-id-hdr').text('Plan ID');
  $('#carrier-name-hdr').text('Carrier');
  

  $('#display-name').html(res[num].display_name);
  $('#plan-id').html(res[num].id);
  $('#carrier-name').html(res[num].user_options);
  
};

// function to get flask response to display individualPlan 
function showMedPlans(evt){
  evt.preventDefault();

  let rowPlanType = "";
  // import user id instead of hard coding url

  // let url = `/users/${res[0].user_id}/show_plans`
  $('#display-plans').show();
  // $('#type-form').hide();

  $.get('/users/1/show_plans', individualMedPlan);
};

// table hidden until event listener activates when user submits
$('#display-plans').hide();
$('#type-form').on('submit', showMedPlans);

// create function to obtain user_id
// function getUserID() {
//   $.get()
// }


  let num = 0;
  num ++



// same action w.o functions
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


