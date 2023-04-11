// API Reference: https://www.wix.com/velo/reference/api-overview/introduction
// “Hello, World!” Example: https://learn-code.wix.com/en/article/1-hello-world

import wixData from 'wix-data';
import wixUsers from 'wix-users';
import { currentMember } from 'wix-members'; // Correct

//----saveData function begin----
function saveData(itemID, email) {
  console.log("saveData current member email: " + email);
  let instagramHandle = $w('#inputInstagram').value;
  let market = $w('#dropdownMarket').value;
  let howManyYrs = parseInt($w('#inputYearsParticipated').value);
  let howManySixteen = parseInt($w('#inputYearsCompleted16').value);
  let participatedBefore = $w('#checkboxParticipatedBefore').checked;
  let sixteenBefore = $w('#checkboxCompleted16Before').checked;
  let exclProgressBoard = $w('#checkboxExcludeFromLeaderboard').checked;

  let toUpdate = {
    "_id": itemID,
    "email": email,
    "instagram": instagramHandle,
    "market": market,
    "participatedBefore": participatedBefore,
    "numYearsParticipated": howManyYrs,
    "recordedSixteen": sixteenBefore,
    "numYearsSixteen": howManySixteen,
    "excludeFromLeaderboard": exclProgressBoard
  };

  wixData.update("gcpOperationalDB/tblSTMParticipantData", toUpdate)
    .then((results) => {
      console.log(results); //see item below
    })
    .catch((err) => {
      console.log(err);
    });
}

//----saveData function end----

//----init function begin----
function init() {
  //ERROR: "Error: WDE0116: default undefined, No matching signature for operator = for argument types: STRING, STRUCT<>. Supported signature: ANY = ANY at [1:241]"
  let userEmail = currentMember.getMember()
    .then((member) => {
      const userEmail = member.loginEmail;
      //console.log("currentMember.getMember() userEmail: " + userEmail);
      return userEmail;
    })
    //console.log("userEmail before .query(gcpOperationalDB/tblSTMParticipantData) " + userEmail)
    wixData.query("gcpOperationalDB/tblSTMParticipantData")
    .eq("email", userEmail)
    .find()
    .then((res) => { 
      console.log("res.length: " + res.length);
      if(res.length === 0) {
        const toInsert = {
          "email": userEmail
        };
        wixData.insert("gcpOperationalDB/tblSTMParticipantData", toInsert)
        .then(() => {
          $w("#dataGCPOperational").refresh()
          $w("#dataGCPOperational").setFilter(wixData.filter().eq("email", userEmail));
        })
      } else {
        $w("#dataGCPOperational").setFilter(wixData.filter().eq("email", userEmail));
      }
    })
    .catch((error) => {
      console.log("Error: ", error);
    });
}
//----init function end----

$w.onReady(function () {
  console.log("Calling init() function...")
  init()
  console.log("Done with init() function...")
  //$w("#dataGCPOperational").refresh()
  /*currentMember.getMember()
    .then((member) => {
      const userEmail = member.loginEmail;
      console.log("currentMember.getMember() userEmail: " + userEmail);
      return userEmail;
    })
    .then((userEmail) => {
      console.log("userEmail before init function: " + userEmail)
      //return init(userEmail)
      init(userEmail)
      $w("#dataGCPOperational").refresh()
    })
    .then((userEmail) => {
      //$w("#dataGCPOperational").refresh()
        //.then((userEmail) => {
          console.log("userEmail after .refresh(): " + userEmail)
          $w("#dataGCPOperational").setFilter(wixData.filter().eq("email", userEmail));
          let profItem = $w("#dataGCPOperational").getCurrentItem();
          console.log("profItem " + profItem);
        //});
    })
    .catch((error) => {
      console.log("Error: ", error);
    });*/
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
  /*console.log("inputInstagram_change function called");
  //let item = $w('#dataGCPOperational').getCurrentItem();
  let item = $w('#dataLocalSelfTapeMayParticipantData').getCurrentItem();
  
  console.log("current item:", item);
  saveData(item._id, item.email);*/
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
  /*console.log("inputInstagram_change function called");
  //let item = $w('#dataGCPOperational').getCurrentItem();
  let item = $w('#dataLocalSelfTapeMayParticipantData').getCurrentItem();
  
  console.log("current item:", item);
  saveData(item._id, item.email); */
}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function buttonSave_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
  let item = $w('#dataGCPOperational').getCurrentItem()
  /*let userEmail = currentMember.getMember()
    .then((member) => {
      const userEmail = member.loginEmail;
      return userEmail;
    })*/
  .then(() => {
    console.log("Calling saveData() function with the following variables:")
    console.log("item._id " + item._id)
    console.log("item.email " + item.email)
    console.log("--------------")
    saveData(item._id, item.email); 
  })
}
