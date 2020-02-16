"use strict";



// function iterMedPlan(res) {
//   $('#plan-id-hdr').text('Plan ID');
//   $('#carrier-name-hdr').text('Carrier');
  
//   console.log(res.length)

//   // for (let i=0; i < res.length; i ++) {
//     $('#display-name').html(res[i].display_name);
//     $('#plan-id').html(res[i].id);
//     $('#carrier-name').html(res[i].carrier_name);
//   };

// };

// // function to display specific plan information
// // function individualMedPlan(res) {
// //   $('#plan-id-hdr').text('Plan ID');
// //   $('#carrier-name-hdr').text('Carrier');
  

// //   $('#display-name').html(res[num].display_name);
// //   $('#plan-id').html(res[num].id);
// //   $('#carrier-name').html(res[num].user_options);
  
// // };

// // function to get flask response to display individualPlan 
// function showMedPlans(evt){
//   evt.preventDefault();

//   // let rowPlanType = "";
//   // import user id instead of hard coding url

//   // let url = `/users/${res[0].user_id}/show_plans`
//   $('#display-plans').show();
//   // $('#type-form').hide();

//   $.get('/users/1/show_plans', (res) => {
//     $('#plan-id-hdr').text('Plan ID');
//     $('#carrier-name-hdr').text('Carrier');

//     // const allPlans = res.map(plan => {
//     //   $('#display-name').html(plan['display_name'].display_name);
//     //   $('#plan-id').html(plan['id'].id);
//     //   $('#carrier-name').html(plan['carrier_name'].carrier_name);

//     // return allPlans
//   $.get('/users/1/show_plans', individualMedPlan);
//     });

   
//   });
// };

// //     $('#display-name').html(res[i].display_name);
// //     $('#plan-id').html(res[i].id);
// //     $('#carrier-name').html(res[i].carrier_name);

// // table hidden until event listener activates when user submits
// $('#display-plans').hide();
// $('#type-form').on('submit', showMedPlans);

// // create function to obtain user_id
// // function getUserID() {
// //   $.get()
// // }




// // $('#form-plan-group').on('submit', individualPlan, (evt) => {
// //   evt.preventDefault();
  


// function to display specific plan information
function individualMedPlan(medicalPlans) {
  
  // create variable to get html table id
  const indivPlanDiv = $('#indiv-plan')
  console.log('indivPlan', indivPlan)

  // create variable to add all plans in list
  const tablePlans = [] 

  // loop through all plans
  for(let i = 1; i <= 5; i++) {
    // create variable for each individual plan
    const planDetails = medicalPlans[i]
    console.log('planDetails', planDetails)

    const tablePlan = $(`\
    <table class="table table-hover table-sm"> \
      <thead> \
        <tr> \
          <th scope="col" id="display-name">${planDetails.display_name}</th> \
        </tr> \
      </thead> \
      <tbody> \
        <tr> \
          <th scope="row" id="plan-id-hdr">Plan ID</th> \
          <td id="plan-id">${planDetails.id}</td> \
        </tr> \
        <tr> \
          <th scope="row" id="carrier-hdr">Carrier</th> \
          <td id="plan-id">${planDetails.carrier_name}</td> \
        </tr> \
        <tr> \
          <th scope="row" id="type-hdr">Plan Type</th> \
          <td id="plan-id">${planDetails.plan_type}</td> \
        </tr> \
        <tr> \
          <th scope="row" id="pcp-hdr">Primary Care Physician</th> \
          <td id="plan-id">${planDetails.primary_care_physician}</td> \
        </tr> \
        <tr> \
          <th scope="row" id="specialist-hdr">Specialist</th> \
          <td id="plan-id">${planDetails.specialist}</td> \
        </tr> \
        <tr> \
          <th scope="row" id="er-hdr">Emergency Room</th> \
          <td id="plan-id">${planDetails.emergency_room}</td> \
        </tr> \
        <tr> \
          <th scope="row" id="gen-drug-hdr">Generic Drug</th> \
          <td id="plan-id">${planDetails.generic_drugs}</td> \
        </tr> \
        <tr> \
          <th scope="row" id="urg-care-hdr">Urgent Care</th> \
          <td id="plan-id">${planDetails.urgent_care}</td> \
        </tr> \
        <tr> \
          <th scope="row" id="indiv-deduc-hdr">Individual Deductible</th> \
          <td id="plan-id">${planDetails.individual_medical_deductible}</td> \
        </tr> \
        <tr> \
          <th scope="row" id="indiv-med-moop-hdr">Individual Max Out-of-Pocket</th> \
          <td id="plan-id">${planDetails.individual_medical_moop}</td> \
        </tr> \


      
          `)

    // tableData.push(tableRow[0])
  }

  // tablePlanBody.html(tableData)
  // console.log('tableData', tableData)



  // $('#plan-id-hdr').text('Plan ID');
  // $('#carrier-name-hdr').text('Carrier');
  

  // $('#display-name').html(res[num].display_name);
  // $('#plan-id').html(res[num].id);
  // $('#carrier-name').html(res[num].carrier_name);
  
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
  



