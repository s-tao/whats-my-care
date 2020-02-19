"use strict";

let url = $(location).attr('href');
// set counter for slicing in for loop
let i = 1

const hideMoreButton = () => {
  $('#click-more-plans').hide();
};

const showMoreButton = () => {
  $('#click-more-plans').show();
};

const hidePreviousButton = () => {
  $('#click-previous-plans').hide();
};

const showPreviousButton = () => {
  $('#click-previous-plans').show();
};

// function to display specific plan information
function individualMedPlan(medicalPlans) {
  const allTablePlans = [] 

  if (i > medicalPlans.length) {
    hideMoreButton.call();
    console.log(i, "no more plans to show");
    console.log(medicalPlans.length, "length");
  };

  console.log(allTablePlans, "allTables");
  // let i = 1

  console.log(i,"i after post click")
  
  const displayPlanDiv = $('#display-plans-div');
  
  // slice to only display a few plans 
  const sliceCounter = medicalPlans.slice(i, i += 80);

  for (let data in sliceCounter) {
    console.log(i, "i")
  
    const planDetails = sliceCounter[data];

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
  showMoreButton.call();
};



// tables hidden until event listener activates when user submits
$('#display-plans-div').hide();

// event listener to show tables and get data from server
$('#type-form').on('submit', individualMedPlan, (evt) => {
  evt.preventDefault();
  
  // create key for form return value
  const formInput = {
    'planOption': $('#type-form').val()
  }

  // send return value from front-end to server
  $.post(url, formInput, individualMedPlan); 

});


// click event to generate button allowing users to see more plans
$('#click-more-plans').on('click', individualMedPlan, (evt) => {
  console.log(individualMedPlan);
  // supposed to hide old plans, generate new plans when function runs
  $('#display-plans-div').hide();

   i += 3;
   
  $.post(url, individualMedPlan); 
});

// potential form submittal for users to submit plan based off click
// in the works
// $('table').on('click', () => {
//   alert("this works");
// });

// $('table.table').on('click', (evt) => {
//   alert('this works');
//   // const divColor = $(evt.target);
//   // console.log("this work")

//   // const selectedDiv = divColor.attr('id');
//   // console.log("this work")

//   // $('div').css('background-color', 'yellow');
// });


