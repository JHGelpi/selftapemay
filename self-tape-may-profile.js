// API Reference: https://www.wix.com/velo/reference/api-overview/introduction
// “Hello, World!” Example: https://learn-code.wix.com/en/article/1-hello-world

import wixData from 'wix-data';
import wixUsers from 'wix-users';
import { currentMember } from 'wix-members'; // Correct

$w('#textLoading').show()
//----saveData function begin----
function saveData(/*itemID, */email) {
  console.log("saveData current member email: " + email);
  let instagramHandle = $w('#inputInstagram').value;
  console.log("instagramHandle: " + instagramHandle);
  let market = $w('#dropdownMarket').value;
  console.log("market: " + market);

  let howManyYrs = Math.abs(parseInt($w('#inputYearsParticipated').value));
  console.log("howManyYrs: " + howManyYrs);

  let howManySixteen = Math.abs(parseInt($w('#inputYearsCompleted16').value));
  console.log("howManySixteen: " + howManySixteen);

  let participatedBefore = $w('#checkboxParticipatedBefore').value;
  console.log("participatedBefore check: " + $w('#checkboxParticipatedBefore').checked);
  console.log("participatedBefore: " + participatedBefore);

  //let participatedBeforeBool = participatedBefore === "true";
  let participatedBeforeBool = $w('#checkboxParticipatedBefore').checked;
  console.log("participatedBeforeBool");
  console.log(participatedBeforeBool)

  let optIn = $w('#checkboxOptIn2024').value;
  console.log("optIn2024 check: " + $w('#checkboxOptIn2024').checked);
  console.log("optIn2024: " + optIn);

  let optInBool = $w('#checkboxOptIn2024').checked;
  console.log("optInBool");
  console.log(optInBool)

  let sixteenBefore = $w('#checkboxCompleted16Before').value;
  console.log("Completed16Before checked: " + $w('#checkboxCompleted16Before').checked);
  console.log("sixteenBefore: " + sixteenBefore);

  //let sixteenBeforeBool = sixteenBefore === "true";
  let sixteenBeforeBool = $w('#checkboxCompleted16Before').checked;
  console.log("sixteenBeforeBool");
  console.log(sixteenBeforeBool);

  let exclProgressBoard = $w('#checkboxExcludeFromLeaderboard').value;
  console.log("ExcludeFromLeaderboard checked: " + $w('#checkboxExcludeFromLeaderboard').checked);
  console.log("exclProgressBoard");

  //let exclProgressBoardBool = exclProgressBoard === "true";
  let exclProgressBoardBool = $w('#checkboxExcludeFromLeaderboard').checked;
  console.log("exclProgressBoardBool");
  console.log(exclProgressBoardBool);

  const toInsert = {
    "email": email,
    "instagram": instagramHandle,
    "market": market,
    "participatedBefore": participatedBeforeBool,
    "numYearsParticipated": howManyYrs,
    "recordedSixteen": sixteenBeforeBool,
    "numYearsSixteen": howManySixteen,
    "excludeFromLeaderboard": exclProgressBoardBool,
    "optIn2024": optInBool
      };
  wixData.insert("gcpOperationalDB/tblSTMParticipantData", toInsert)

  //wixData.update("gcpOperationalDB/tblSTMParticipantData", toUpdate)
    .then((results) => {
      console.log(results); //see item below
    })
    .catch((err) => {
      console.log(err);
    });
}

//----saveData function end----
function initData(userEmail) {
  console.log("initData current member email: " + userEmail);
  
  $w('#inputInstagram').value = ""
  $w('#dropdownMarket').value = ""
  $w('#inputYearsParticipated').value = ""
  $w('#inputYearsCompleted16').value = ""
  $w('#checkboxParticipatedBefore').checked = false
  $w('#checkboxCompleted16Before').checked = false
  $w('#checkboxExcludeFromLeaderboard').checked = false
  $w('#checkboxOptIn2024').checked = false

  wixData.query("gcpOperationalDB/viewSTMParticipantData")
  .eq("email", userEmail)
  .find()
  .then(results => {
    if (results.items.length > 0) {
      const item = results.items[0]; // get the first item in the array
      $w('#inputEmail').value = item.email;
      $w('#inputInstagram').value = item.instagram
      $w('#textInstagramPost').value = item.instagram
      $w('#dropdownMarket').value = item.market
      $w('#inputYearsParticipated').value = item.numYearsParticipated
      $w('#inputYearsCompleted16').value = item.numYearsSixteen
      $w('#checkboxParticipatedBefore').checked = item.participatedBefore
      $w('#checkboxCompleted16Before').checked = item.recordedSixteen
      $w('#checkboxExcludeFromLeaderboard').checked = item.excludeFromLeaderboard
      $w('#checkboxOptIn2024').checked = item.optIn2024
      $w('#inputInstagram').enable()
    } else {
      console.log("Something went wrong!!  initData query failed to return results for " + userEmail)
      // handle case where no results are found
    }
  })
  .catch(error => {
    console.log(error);
  });

}
//----init function begin----
async function init() {
  try {
    const member = await currentMember.getMember();
    const userEmail = member.loginEmail;
    const res = await wixData.query("gcpOperationalDB/viewSTMParticipantData")
      .eq("email", userEmail)
      .find();
    //console.log("res.length: " + res.length);
    if (res.length === 0) {
      const toInsert = {
        "email": userEmail
      };
      await wixData.insert("gcpOperationalDB/tblSTMParticipantData", toInsert);
      $w("#inputEmail").value = userEmail
      //$w("#dataViewGCPOperational").refresh();
      //$w("#dataViewGCPOperational").setFilter(wixData.filter().eq("email", userEmail));
    } else {
      /*wixData.query("gcpOperationalDB/viewSTMParticipantData")
		    .gt("email", userEmail)*/
      initData(userEmail)
      //$w("#dataViewGCPOperational").setFilter(wixData.filter().eq("email", userEmail));
    }
  } catch (error) {
    console.log("Error: ", error);
  }
}

function checkString(str) {
  if (str.startsWith('@') && str.length <= 33) {
    // String starts with '@' and is no longer than 33 characters
    console.log('Valid string');
    return true
    // Perform further actions or logic here
  } else {
    // String does not meet the criteria
    console.log('Invalid string');
    return false
    // Perform alternative actions or error handling here
  }
}
//----init function end----

$w.onReady(function () {
  console.log("Calling init() function...")
  init()
  console.log("Done with init() function...")
  $w('#textLoading').hide()
});

/**
*	Adds an event handler that runs when an input element's value
 is changed.
	[Read more](https://www.wix.com/corvid/reference/$w.ValueMixin.html#onChange)
*	 @param {$w.Event} event
*/
export function inputInstagram_change(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 

}

/**
*	Adds an event handler that runs when an input element's value
 is changed.
	[Read more](https://www.wix.com/corvid/reference/$w.ValueMixin.html#onChange)
*	 @param {$w.Event} event
*/
export function dropdownMarket_change(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here:

}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function buttonSave_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
  if (checkString($w('#inputInstagram').value)){
    //let item = $w('#dataViewGCPOperational').getCurrentItem()
    console.log("Calling saveData() function with the following variables:")
    //console.log("item._id " + item._id)
    console.log("#inputEmail.value " + $w("#inputEmail").value)
    console.log("--------------")
    $w('#textInstagramPost').value = $w('#inputInstagram').value
    saveData($w("#inputEmail").value);
    // Show the text box
    $w('#imageSaved').show();

    // Hide the text box after 3 seconds
    setTimeout(() => {
      $w('#imageSaved').hide();
    }, 2000);
  } else {
    console.log("Invalid Instagram handle")
    // Show the text box
    $w('#textBadInstagram').show();

    // Hide the text box after 3 seconds
    setTimeout(() => {
      $w('#textBadInstagram').hide();
    }, 2000);
  }
  
}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function mobileSaveButton_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here:
  if (checkString($w('#inputInstagram').value)){ 
    console.log("Calling saveData() function with the following variables:")
    //console.log("item._id " + item._id)
    console.log("#inputEmail.value " + $w("#inputEmail").value)
    console.log("--------------")
    $w('#textInstagramPost').value = $w('#inputInstagram').value
    saveData($w("#inputEmail").value);

    // Show the text box
    $w('#imageMobileSaved').show();

    // Hide the text box after 3 seconds
    setTimeout(() => {
      $w('#imageMobileSaved').hide();
    }, 2000);
  } else {
    console.log("Invalid Instagram handle")
    // Show the text box
    $w('#textBadInstagram').show();

    // Hide the text box after 3 seconds
    setTimeout(() => {
      $w('#textBadInstagram').hide();
    }, 2000);
  }
}