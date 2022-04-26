// API Reference: https://www.wix.com/velo/reference/api-overview/introduction
// “Hello, World!” Example: https://learn-code.wix.com/en/article/1-hello-world

import wixData from 'wix-data';
import wixUsers from 'wix-users';
import { currentMember } from 'wix-members'; // Correct

$w.onReady(function () {
//--------------------------------
  let userEmail = currentMember.getMember().then((member) => {
            //console.log("Member email: " + member.loginEmail);
            
            let userEmail = member.loginEmail;
            //console.log("Member email INSIDE currentMember function: " + userEmail);
            return member.loginEmail;
            
        })
    //console.log("userEmail value AFTER currentMember function: ")
    //console.log(userEmail)
    //console.log("--------------------")
//-------------------------------------

  let user = wixUsers.currentUser;
  //console.log("Current User: " + user)
  let userId = user.id; // "r5cme-6fem-485j-djre-4844c49"
  //console.log("userId: " + userId)
  let isLoggedIn = user.loggedIn; // true
  //console.log("isLoggedIn: " + isLoggedIn)
  let userRole = user.role; // "Member"
  //console.log("userRole: " + userRole)

  /*********************************************************************************************************************** */
  
  wixData.query("SelfTapeMayParticipationData")
    .eq("emailAddress", userEmail)
    .find()
    .then((res) => {  
      /************************************************************************************************************************ */
      //**********************Filter form for current user******************************************************************** */
      //Reference: https://www.wix.com/velo/forum/coding-with-velo/how-to-filter-a-table-according-to-the-current-user
      //********************************************************************************************************************* */
      user.getEmail().then((email) => {
        let userEmail = email; // "user@something.com"
        //console.log("getEmail() results: " + userEmail);

        /*********************************************************************************************************** */
        let toInsert = {
        "emailAddress": userEmail,
        "selfTapes": 0
        };
        
        wixData.query("SelfTapeMayParticipationData")
        .eq("emailAddress", toInsert.emailAddress)
        .ascending("emailAddress")
        .limit(3)
        .find()
        .then( (results) => {
          //console.log("Results logging:")
          //console.log(results.length)
          //console.log(results)
          //console.log("---------------")
          if(results.length == 0) {
            //If query returns nothing then I need to insert row of data
            /*********************BEGIN INSERT STATEMENT**************************** */
            //console.log("Inserting the following data points into SelfTapeMayParticipationData:")
            //console.log(toInsert)
            //console.log(toInsert.emailAddress)
            //console.log(toInsert.selfTapes)
            //console.log("------------------------------------------------------------------------")

            wixData.insert("SelfTapeMayParticipationData", toInsert)
              .then ( (results) => {
                let item = results;
              })
              .catch ( (err) => {
                let errorMsg = err;
              });
            //console.log("DONE with toInsert")
            
              /**************END INSERT STATEMENT**************************** */
              /*********************REFRESHING DATASET*************** */
              $w("#datasetSelfTapeParticipant").refresh()
                .then( () => {
                console.log("Done refreshing datasetSelfTapeParticipant");
              } );
              /**********************DONE REFRESHING******************** */
              //console.log("Insert record complete.")
              //console.log("Filtering...")
              /*********************************************************************************************************** */
              //console.log("Filtering for the following email address:")
              //console.log(toInsert.emailAddress)
              //console.log("------------------------------------------")
              $w("#datasetSelfTapeParticipant").setFilter(wixData.filter().eq("emailAddress", toInsert.emailAddress));
              //********************************************************************************************************************* */
          } else {
            //email must exist so I just need to filter for the email address value
            /*********************************************************************************************************** */
            //console.log("Filtering for the following email address:")
            //console.log(toInsert.emailAddress)
            //console.log("------------------------------------------")
            $w("#datasetSelfTapeParticipant").setFilter(wixData.filter().eq("emailAddress", toInsert.emailAddress));
            //********************************************************************************************************************* */
          }
          //console.log(results.items);
        } );

    });

    })
  
});

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function buttonSave_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
  //let selfTapeDate = Date.now();
  let selfTapeDate = wixTimestamp();
  //let selfTapeDate = getTimestamp();
  $w("#datasetSelfTapeParticipant").setFieldValue("selfTapesUpdateDate", new Date(selfTapeDate));
  $w("#datasetSelfTapeParticipant").save();

  rankLeaderboard();

}
function wixTimestamp () {
  var monthNames = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ];
  var d = new Date();
  var curr_date = d.getDate();
  var curr_month = monthNames[d.getMonth()];
  var curr_year = d.getFullYear();
  var curr_hr = d.getHours();
  var curr_ampm = "";
  if(curr_hr > 12) {
    curr_hr = curr_hr - 12
    curr_ampm = "PM"
  } else if (curr_hr == 12) {
    curr_ampm = "PM"
  } else {
    curr_ampm = "AM"
  }
  var curr_min = d.getMinutes();
  var curr_time = d.getTime();

  //mmmm dd, yyyy hh:mm pm

  return curr_month + " " + curr_date + ", " + curr_year + " " + curr_hr + ":" + curr_min + " " + curr_ampm;
}

function rankLeaderboard() { 

	wixData.query("SelfTapeMayParticipationData")
		.descending("selfTapes")
		.ascending("selfTapesUpdateDate")
		.find()
		.then( (results) => {
    		if(results.items.length > 0) {
				for(let i = 0; i < results.items.length; i++) {
					let toUpdate = {
						"_id": results.items[i]._id,
						"leaderBoardRank": i + 1,
						"selfTapes": results.items[i].selfTapes,
						"instagramHandle": results.items[i].instagramHandle,
						"market": results.items[i].market,
						"witcherSides": results.items[i].witcherSides,
						"emailAddress": results.items[i].emailAddress,
						"participatedBefore": results.items[i].participatedBefore,
						"yearsParticipatedBefore": results.items[i].yearsParticipatedBefore,
						"recorded16Before": results.items[i].recorded16Before,
						"yearsRecorded16Before": results.items[i].yearsRecorded16Before,
						"selfTapesUpdateDate": results.items[i].selfTapesUpdateDate
					};

					wixData.update("SelfTapeMayParticipationData", toUpdate)
						.then ( (results) => {
							let item = results;
						})
						.catch( (err) => {
							let errorMsg = err;
						})
				}
    		} else {
     			// handle case where no matching items found
			}
		} )

}
