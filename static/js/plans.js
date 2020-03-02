"use strict";

// let url = $(location).attr('href');

// set counter for slicing in for loop
let begin = 0;
let end = 5;

const moreButton = $('#click-more-plans');
const previousButton = $('#click-previous-plans');


// standard table showing all plan's information including deductibles
const tableDisplay = (planDetails) => {

  const tablePlan = (`\
  <div class="indiv-plan"> \
    <table class="table table-hover table-sm"> \
      <thead> \
        <tr> \
          <th scope="col" id="display-name">${planDetails.display_name}</th> \
        </tr> \
      </thead> \
      <tbody> \
        <tr> \
          <th scope="row" class="plan-id-hdr">Plan ID</th> \
          <td class="plan-detail-id">${planDetails.id}</td> \
        </tr> \
        <tr> \
          <th scope="row" class="carrier-hdr">Carrier</th> \
          <td class="plan-detail-carrier">${planDetails.carrier_name}</td> \
        </tr> \
        <tr> \
          <th scope="row" class="type-hdr">Plan Type</th> \
          <td class="plan-detail-type">${planDetails.plan_type}</td> \
        </tr> \
        <tr> \
          <th scope="row" class="pcp-hdr">Primary Care Physician</th> \
          <td class="plan-detail-pcp">${planDetails.pcp}</td> \
        </tr> \
        <tr> \
          <th scope="row" class="specialist-hdr">Specialist</th> \
          <td class="plan-detail-s">${planDetails.specialist}</td> \
        </tr> \
        <tr> \
          <th scope="row" class="er-hdr">Emergency Room</th> \
          <td class="plan-detail-er">${planDetails.emerg_rm}</td> \
        </tr> \
        <tr> \
          <th scope="row" class="gen-drug-hdr">Generic Drug</th> \
          <td class="plan-detail-gd">${planDetails.gen_drug}</td> \
        </tr> \
        <tr> \
          <th scope="row" class="urg-care-hdr">Urgent Care</th> \
          <td class="plan-detail-uc">${planDetails.urg_care}</td> \
        </tr> \
        <tr> \
          <th scope="row" class="indiv-deduc-hdr">Individual Deductible</th> \
          <td class="plan-detail-imd">${planDetails.med_deduct}</td> \
        </tr> \
        <tr> \
          <th scope="row" class="indiv-med-moop-hdr">Individual Max Out-of-Pocket</th> \
          <td class="plan-detail-moop">${planDetails.med_moop}</td> \
        </tr> \
        <tr> \
          <th scope="row" class="premium-hdr">Premium</th> \
          <td class="plan-detail-premium">${planDetails.premium}</td> \
        </tr> \
        <tr> \
          <td colspan="2" align="center"> \
          <div class="form-check"> \
            <input class="form-check-input" type="checkbox" \
                                            value="plan_id"" \
                                            name="${planDetails.id}"> \
            <label class="form-check-label" for="${planDetails.id}"> \
              Default checkbox \
            </label> \
          </div> \
          </td> \
        </tr> \
      </tbody> \
    </table> \
  </div> \
`);

return tablePlan;
};


// function to display specific plan information
const individualMedPlan = (medicalPlans) => {

  const allTablePlans = [] 

  // querying class to insert tables 
  const indivPlan = $('.all-plans');

  // slice to only display a few plans 
  const sliceCounter = medicalPlans.slice(begin, end);
  if (end > medicalPlans.length) {
    moreButton.hide();
  };

  if (end <= 5) {
    previousButton.hide();
  };

  for (let data in sliceCounter) {

    const planDetails = sliceCounter[data];
    const tablePlan = tableDisplay(planDetails);

    allTablePlans.push(tablePlan);
  };
  // convert allTablesPlans to html
  indivPlan.html(allTablePlans);

};


const applicantForm = () => {

  if ($('input[name="smoker"]:checked').length > 0) {
    var smoker = $('input[name="smoker"]:checked').val();
  };
  
  if ($('input[name="child"]:checked').length > 0) {
    var child = $('input[name="child"]:checked').val();
  };

  // create key for form return value
  const formInput = {
    // 'planOption': $('select[name="plan-option"]').val(),
    'age': $('select[name="age"]').val(),
    'smoker': smoker,
    'child': child
  };

  return formInput;
};


// event listener to show tables and get data from server when user submits
$('#plan-form').on('submit', individualMedPlan, (evt) => {
  evt.preventDefault();

  const formInput = applicantForm();
  // const formInput = $('#plan-form').serialize();

  // send return value from front-end to server
  $.get('/show_plans', formInput, individualMedPlan); 

  // display shows once function runs to generate tables
  $('#display-plans-div').show();
  moreButton.show();
});


// click event to generate button allowing users to see more plans
moreButton.on('click', individualMedPlan, (evt) => {
  // $('#display-plans-div').hide();

  // counter show next 5 tables every click
  begin += 5;
  end += 5;

  const formInput = applicantForm();

  $.get('/show_plans', formInput, individualMedPlan); 
  previousButton.show();

});


// click event to generate button allowing users to see previous plans
previousButton.on('click', individualMedPlan, (evt) => {
  
  // counter show previous 5 tables every click
  begin -= 5;
  end -= 5;

  const formInput = applicantForm();

  $.get('/show_plans', formInput, individualMedPlan); 
  
});


// click event to remove plan from user profile 
const removePlan = $('.remove-plan');

removePlan.click(function() {

  const planId = $(this).attr('id');
  const formInput = {

    'planId': planId
  };

  $.post('/remove_plan', formInput, (res) => {

    const removeTable = $(`#table-${planId}`);
    
    removeTable.fadeOut(1000, function() {
    removeTable.remove();
    $(`#${planId}`).hide();

    });

    alert(res);

  });
});

