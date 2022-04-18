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
