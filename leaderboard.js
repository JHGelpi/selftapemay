// API Reference: https://www.wix.com/velo/reference/api-overview/introduction
// “Hello, World!” Example: https://learn-code.wix.com/en/article/1-hello-world
import wixData from 'wix-data';
import wixUsers from 'wix-users';
import wixWindow from 'wix-window';

import { currentMember } from 'wix-members'; // Correct

$w.onReady( function () {

	/************************************************************************* */
	//Rank the entire population based on self tapes recorded and updated date
	//This is working as expected 27-apr-2022
	rankLeaderboard();
	/************************************************************************* */

	/************************************************************************ */
	//This identifies the current user so I can filter the repeater to just 
	//return the data for the current user.
	/************************************************************************ */
	let user = wixUsers.currentUser;
	user.getEmail().then((email) => {
    	let userEmail = email;

	$w("#datasetRepeaterLeaderboard").setFilter(wixData.filter().eq("emailAddress", userEmail));
	/*I had to use the setTimeout function to wait for data set to be available.
	I don't know how else to make this work.  The refresh needs to take place AFTER the
	rankLeaderboard() function has successfully completed. */
	setTimeout($w("#datasetRepeaterLeaderboard").refresh, 1000);
	});
	/************************************************************************* */
	setTimeout($w("#datasetSelfTapeMayParticipation").refresh, 1000);
});


export function rankLeaderboard() { 
	/*This function is intended to look at all of the entries in the SelfTapeMayParticipationData collection
	and rank them in order of # of self tapes first and then by the selfTapesUpdateDate field which is updated
	every time they change their data in the Self Tape May Profile page. */
	wixData.query("SelfTapeMayParticipationData")
		.descending("selfTapes")
		.ascending("selfTapesUpdateDate")
		.find()
		.then( (results) => {
    		if(results.items.length > 0) {
				for(let i = 0; i < results.items.length; i++) {
          			let item = results.items[i];
          			item.leaderBoardRank = i + 1;
          			wixData.update("SelfTapeMayParticipationData", item);
				}
    		} else {
     			// handle case where no matching items found
			}

		} )


}

/*export function buttonFilterInstagram_click(event) {
	
	let instagramFilter = $w('#inputInstagram').value
	console.log("Instagram handle value" + instagramFilter)
	$w("#datasetSelfTapeMayParticipation").setFilter(wixData.filter().eq("instagramHandle", instagramFilter));
	
	$w("#datasetSelfTapeMayParticipation").refresh()
		.then( () => {
		console.log("Done refreshing datasetSelfTapeParticipant");
	} );
}*/

export function radioGroupSort_change(event) {
	/*This is used to sort the table tableSelfTapeMayLeaderboard by the indicated options*/ 
	if ($w("#radioGroupSort").value === 'market_az')
	//Sort by Market
   {
        //$w("#datasetSelfTapeMayParticipation").setSort(wixData.sort().ascending("market"));
		$w("#datasetSelfTapeMayParticipation").setSort( wixData.sort()
			.ascending("market")
			.ascending("leaderBoardRank")
  			.descending("selfTapes")
  			.ascending("_updatedDate")
		);
    } 
	else if ($w("#radioGroupSort").value === 'market_za') 
  {
        //$w("#datasetSelfTapeMayParticipation").setSort(wixData.sort().descending("yearsParticipatedBefore"));
		$w("#datasetSelfTapeMayParticipation").setSort( wixData.sort()
			.descending("market")
			.ascending("leaderBoardRank")
  			.descending("selfTapes")
  			.ascending("_updatedDate")
		);
    } 
	else if ($w("#radioGroupSort").value === 'years_participated_lowhigh') 
  {
		$w("#datasetSelfTapeMayParticipation").setSort( wixData.sort()
			.ascending("yearsParticipatedBefore")
			.ascending("leaderBoardRank")
  			.descending("selfTapes")
  			.ascending("_updatedDate")
		);
    }
	else if ($w("#radioGroupSort").value === 'years_participated_highlow') 
  {
		$w("#datasetSelfTapeMayParticipation").setSort( wixData.sort()
			.descending("yearsParticipatedBefore")
			.ascending("leaderBoardRank")
  			.descending("selfTapes")
  			.ascending("_updatedDate")
		);
    }
}

export function buttonResetSort_click(event) {
	/**This should reset the sort of the table tableSelfTapeMayLeaderboard back to the originally intended sort order */

	$w("#datasetSelfTapeMayParticipation").setSort( wixData.sort()
		.ascending("leaderBoardRank")
  		.descending("selfTapes")
  		.ascending("_updatedDate")
);
}

export function buttonResetFilter_click(event) {
	/**This should reset all of the filter options back to default/starting position */
	$w("#datasetSelfTapeMayParticipation").setFilter(wixData.filter());
	$w("#rangeSliderSelfTapes").value=[0,16];
	$w("#inputInstagram").value = "";
}

export function buttonFilterSlider_click(event) {
	/**This slider will allow the users to filter the table based on the range of self tapes completed that have been selected with the slider */
	let sliderMin = $w("#rangeSliderSelfTapes").value[0]
	let sliderMax = $w("#rangeSliderSelfTapes").value[1]
	let marketValue = $w("#dropdownMarket").value
	let instagramFilter = $w('#inputInstagram').value
	console.log("Instagram handle value" + instagramFilter)
	console.log("Slider min value: " + sliderMin)
	console.log("Slider max value: " + sliderMax)
	console.log("Market value is: " + marketValue)
	
	// init the filter
	//HUGE credit to the answer given here: https://www.wix.com/velo/forum/coding-with-velo/add-a-filter-to-dataset-but-also-keep-the-previous-filter
	 var filter = wixData.filter();

	//Filter for Self Tapes
	if (sliderMin == 0 && sliderMax == 16) {
		//do nothing
		console.log("I did nothing to filter slider")
	} else {
		//Filter for self tape #
		filter = filter.between("selfTapes", sliderMin - 1, sliderMax + 1);
	}

	//Filter for Market
	if (marketValue == "") {
		//do nothing
		console.log("I did nothing because Market Value = " + marketValue)
	} else {
		//Apply market filter
		filter = filter.eq("market", marketValue)
	}
	
	//Filter for Instagram Handle
	if (instagramFilter == "") {
		//Do nothing
		console.log("I did nothing because instagram value == " + instagramFilter)
	} else {
		//Filter for Instagram handle
		filter = filter.contains("instagramHandle", instagramFilter)
	}
	//Apply filter
	$w("#datasetSelfTapeMayParticipation").setFilter(filter);	
}
