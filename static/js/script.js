"use strict";


// function to display specific plan information
function individualMedPlan(medicalPlans) {
  
  // create variable to get html table id
  const displayPlanDiv = $('#display-plans-div');
  // console.log('indivPlan', indivPlanDiv)

  // create variable to add all plans in list
  const allTablePlans = [] 

  // loop through all plans
  for(let i = 1; i < medicalPlans.length; i++) {
    // create variable for each individual plan
    const planDetails = medicalPlans[i];
    // console.log('planDetails', planDetails)

    // information needed per table
    const tablePlan = $(`\
    <div class="sub-container indiv-plan"> \
      <table class="table table-hover table-sm"> \
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
};


// tables hidden until event listener activates when user submits
$('#display-plans-div').hide();

// event listener to show tables and get data from server
$('#type-form').on('submit', individualMedPlan, (evt) => {
  evt.preventDefault();
  $('#display-plans-div').show();

  // let userId = $("div[id^='user-id-']").val();
  let url = $(location).attr('href');
  // console.log(url, "url");

  const planOption = $('#test');
  console.log(planOption, "plan option")

  // if (evt === "medical") {

  // currently url hardcoded, fix url to change when form submitted
  $.post(url, individualMedPlan);

});








