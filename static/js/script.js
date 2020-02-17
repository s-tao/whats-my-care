"use strict";



// function to display specific plan information
function individualMedPlan(medicalPlans) {
  
  // create variable to get html table id
  const indivPlanDiv = $('#indiv-plan')
  // console.log('indivPlan', indivPlanDiv)

  // create variable to add all plans in list
  const allTablePlans = [] 

  // loop through all plans
  for(let i = 1; i < medicalPlans.length; i++) {
    // create variable for each individual plan
    const planDetails = medicalPlans[i]
    // console.log('planDetails', planDetails)

    // information needed per table
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
      </tbody> \
    </table> \
    `)

    allTablePlans.push(tablePlan)
  };
  indivPlanDiv.html(allTablePlans)
};


// tables hidden until event listener activates when user submits
$('#display-plans').hide();

// event listener to show tables and get data from server
$('#type-form').on('submit', individualMedPlan, (evt) => {
  evt.preventDefault();

  $('#display-plans').show();
  $.get('/users/1/show_plans', individualMedPlan);
});

// create function to obtain user_id
// function getUserID() {
//   $.get()
// }






