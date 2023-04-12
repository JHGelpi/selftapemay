// API Reference: https://www.wix.com/velo/reference/api-overview/introduction
// “Hello, World!” Example: https://learn-code.wix.com/en/article/1-hello-world

import wixData from 'wix-data';
import wixUsers from 'wix-users';
import { currentMember } from 'wix-members'; // Correct

//----saveData function begin----
/*
let checkboxValue = $w('#checkboxId').value;
let isChecked = checkboxValue === "true";
 */
function saveData(itemID, email) {
  console.log("saveData current member email: " + email);
  let instagramHandle = $w('#inputInstagram').value;
  console.log("instagramHandle: " + instagramHandle);
  let market = $w('#dropdownMarket').value;
  console.log("market: " + market);
  let howManyYrs = parseInt($w('#inputYearsParticipated').value);
  console.log("howManyYrs: " + howManyYrs);
  let howManySixteen = parseInt($w('#inputYearsCompleted16').value);
  console.log("howManySixteen: " + howManySixteen);
  let participatedBefore = $w('#checkboxParticipatedBefore').value;
  console.log("participatedBefore: " + participatedBefore);
  let participatedBeforeBool = participatedBefore === "true";
  console.log("participatedBeforeBool");
  console.log(participatedBeforeBool)
  let sixteenBefore = $w('#checkboxCompleted16Before').value;
  console.log("sixteenBefore: " + sixteenBefore);
  let sixteenBeforeBool = sixteenBefore === "true";
  console.log("sixteenBeforeBool");
  console.log(sixteenBeforeBool);
  let exclProgressBoard = $w('#checkboxExcludeFromLeaderboard').value;
  console.log("exclProgressBoard");
  let exclProgressBoardBool = exclProgressBoard === "true";
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
    "excludeFromLeaderboard": exclProgressBoardBool
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

//----init function begin----
async function init() {
  try {
    const member = await currentMember.getMember();
    const userEmail = member.loginEmail;
    const res = await wixData.query("gcpOperationalDB/viewSTMParticipantData")
      .eq("email", userEmail)
      .find();
    console.log("res.length: " + res.length);
    if (res.length === 0) {
      const toInsert = {
        "email": userEmail
      };
      await wixData.insert("gcpOperationalDB/tblSTMParticipantData", toInsert);
      $w("#dataViewGCPOperational").refresh();
      $w("#dataViewGCPOperational").setFilter(wixData.filter().eq("email", userEmail));
    } else {
      $w("#dataViewGCPOperational").setFilter(wixData.filter().eq("email", userEmail));
    }
  } catch (error) {
    console.log("Error: ", error);
  }
}

//----init function end----

$w.onReady(function () {
  console.log("Calling init() function...")
  init()
  console.log("Done with init() function...")
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

  let item = $w('#dataViewGCPOperational').getCurrentItem()
  console.log("Calling saveData() function with the following variables:")
  console.log("item._id " + item._id)
  console.log("item.email " + item.email)
  console.log("--------------")
  saveData(item._id, item.email);
}
