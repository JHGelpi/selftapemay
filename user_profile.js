// API Reference: https://www.wix.com/velo/reference/api-overview/introduction
// “Hello, World!” Example: https://learn-code.wix.com/en/article/1-hello-world

import wixData from 'wix-data';
import wixUsers from 'wix-users';

$w.onReady(function () {

 //Check if user exists
 //import wixData from 'wix-data';

  let user = wixUsers.currentUser;
  let userId = user.id; // "r5cme-6fem-485j-djre-4844c49"
  let isLoggedIn = user.loggedIn; // true
  let userRole = user.role; // "Member"

  user.getEmail()
    .then((email) => {
    let userEmail = email; // "user@something.com"
    console.log(userEmail);
    console.log(userId);
  
wixData.query("SelfTapeMayParticipationData")
  .eq("emailAddress", userEmail)
  .find()
  .then( (results) => {
    if(results.items.length > 0) {
      //Filter form for current user
      $w("#datasetSelfTapeParticipant").setFilter(wixData.filter()
        .eq("emailAddress", userEmail)
      );

    } else {
      // handle case where no matching items found
      //Here I want to insert the value of email address
      let toInsert = {
       "emailAddress": userEmail,
       "selfTapes": 0
      };

      wixData.insert("SelfTapeMayParticipationData", toInsert)
	      .then( (results) => {
		    let item = results;
	      } )

        //Refresh the data collection
        $w.onReady( () => {
          $w("#datasetSelfTapeParticipant").onReady( () => {
          $w("#datasetSelfTapeParticipant").refresh()
        //Filter the data collection on the current user
          $w("#datasetSelfTapeParticipant").setFilter(wixData.filter()
            .eq("emailAddress", userEmail)
          );


          //.then( () => {
          //  console.log("Done refreshing the dataset");
          //  });
          } );
        } );
      
    }
  })
  .catch( (error) => {
    let errorMsg = error.message;
    let code = error.code;
    } );
    });

});
