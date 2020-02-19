"use strict";

let url = $(location).attr('href');
const allTablePlans = [] 
let i = 1

// function to display specific plan information
function individualMedPlan(medicalPlans) {
  
  const displayPlanDiv = $('#display-plans-div');

  for (i in medicalPlans.slice(i, i+2)) {
  console.log(i,"i")
  const planDetails = medicalPlans[i];

  const tablePlan = $(`\
    <div class="sub-container indiv-plan"> \
      <table class="table table-hover table-sm" id="${planDetails.id}"> \
        <thead> \
          <tr> \
            <th scope="col" id="display-name">${planDetails.display_name}</th> \
          </tr> \
        </thead> \
        <tbody> \
          <tr> \
            <th scope="row" class="plan-id-hdr">Plan ID</th> \
            <td class="plan-detail">${planDetails.id}</td> \
          </tr> \
          <tr> \
            <th scope="row" class="carrier-hdr">Carrier</th> \
            <td class="plan-detail">${planDetails.carrier_name}</td> \
          </tr> \
          <tr> \
            <th scope="row" class="type-hdr">Plan Type</th> \
            <td class="plan-detail">${planDetails.plan_type}</td> \
          </tr> \
          <tr> \
            <th scope="row" class="pcp-hdr">Primary Care Physician</th> \
            <td class="plan-detail">${planDetails.primary_care_physician}</td> \
          </tr> \
          <tr> \
            <th scope="row" class="specialist-hdr">Specialist</th> \
            <td class="plan-detail">${planDetails.specialist}</td> \
          </tr> \
          <tr> \
            <th scope="row" class="er-hdr">Emergency Room</th> \
            <td class="plan-detail">${planDetails.emergency_room}</td> \
          </tr> \
          <tr> \
            <th scope="row" class="gen-drug-hdr">Generic Drug</th> \
            <td class="plan-detail">${planDetails.generic_drugs}</td> \
          </tr> \
          <tr> \
            <th scope="row" class="urg-care-hdr">Urgent Care</th> \
            <td class="plan-detail">${planDetails.urgent_care}</td> \
          </tr> \
          <tr> \
            <th scope="row" class="indiv-deduc-hdr">Individual Deductible</th> \
            <td class="plan-detail">${planDetails.individual_medical_deductible}</td> \
          </tr> \
          <tr> \
            <th scope="row" class="indiv-med-moop-hdr">Individual Max Out-of-Pocket</th> \
            <td class="plan-detail">${planDetails.individual_medical_moop}</td> \
          </tr> \
        </tbody> \
      </table> \
    </div> \
    `);
  
    allTablePlans.push(tablePlan);
  };
  displayPlanDiv.html(allTablePlans);

  // display shows once function runs to generate tables
  $('#display-plans-div').show();

  // click button shows
  $('#click-more-plans').show();
};



// find better way to replace tables w/o browser pushing up
// tables hidden until event listener activates when user submits
$('#display-plans-div').hide();
$('#click-more-plans').hide();
// event listener to show tables and get data from server
$('#type-form').on('submit', individualMedPlan, (evt) => {
  // evt.currentTarget.submit().preventDefault();

  evt.preventDefault();
  // $('#plan-type').text(JSON.stringify($('#type-form').serialize()));

  // evt.stopPropagation();
  // let userId = $("div[id^='user-id-']").val();
  // console.log(url, "url");
  $.post(url, individualMedPlan); 

});


// click event to generate button allowing users to see more plans
$('#click-more-plans').on('click', individualMedPlan, (evt) => {
  console.log(individualMedPlan);
  // supposed to hide old plans, generate new plans when function runs
  $('#display-plans-div').hide();

  let i = 3;
  $.post(url, individualMedPlan); 

});

// potential form submittal for users to submit plan based off click
// in the works
$('table').on('click', () => {
  alert("this works");
});

// $('table.table').on('click', (evt) => {
//   alert('this works');
//   // const divColor = $(evt.target);
//   // console.log("this work")

//   // const selectedDiv = divColor.attr('id');
//   // console.log("this work")

//   // $('div').css('background-color', 'yellow');
// });


