// API Reference: https://www.wix.com/velo/reference/api-overview/introduction
// “Hello, World!” Example: https://learn-code.wix.com/en/article/1-hello-world
import wixData from 'wix-data';
import wixUsers from 'wix-users';
import wixWindow from 'wix-window';

import { currentMember } from 'wix-members'; // Correct
//$w("#repeaterMyRank").hide();

$w.onReady( function () {

	/************************************************************************* */
	//Rank the entire population based on self tapes recorded and updated date
	//This is working as expected 27-apr-2022
	//console.log("Running rankLeaderboard()...")

	rankLeaderboard()
		.then(() => {
			let email = userEmail()
				.then((email) => {
					console.log("Getting ready to call refreshRepetear with the email address: ")
					console.log(email)
					refreshRepeater(email)
				})
		})
	$w('#datasetTotalSelftapes').refresh
	/************************************************************************* */
	
});

export function rankLeaderboard() {
  return new Promise((resolve, reject) => {
    /*This function is intended to look at all of the entries in the SelfTapeMayParticipationData collection
    and rank them in order of # of self tapes first and then by the selfTapesUpdateDate field which is updated
    every time they change their data in the Self Tape May Profile page. */
    wixData.query("gcpOperationalDB/view-stm-leaderboard")
      .gt("numSelftapes", 0)
      .descending("maxTimestamp")
      .descending("userRank")
      .limit(1000)
      .find()
      .then((results) => {
        if (results.items.length > 0) {
          for (let i = 0; i < results.items.length; i++) {
            let item = results.items[i];
            item.leaderBoardRank = i + 1;
            wixData.update("SelfTapeMayParticipationData", item);
          }
          resolve();
        } else {
          // handle case where no matching items found
          resolve();
        }
      })
      .catch((error) => {
        reject(error);
      });
  });
}

async function userEmail() {
	const member = await currentMember.getMember();
    const userEmail = member.loginEmail;

	return userEmail
}

function refreshRepeater(email){
	
	console.log("Setting filter on #datasetRepeater")
	$w("#datasetRepeater").setFilter(wixData.filter().eq("email", email))
		.then(() => {
			$w("#datasetRepeater").refresh
			//$w("#repeaterMyRank").show()
			$w("#tableMyRank").show()
		})
}

export function radioGroupSort_change(event) {
	/*This is used to sort the table tableSelfTapeMayLeaderboard by the indicated options*/ 
	if ($w("#radioGroupSort").value === 'market_az')
	//Sort by Market
   {
        //$w("#datasetSelfTapeMayParticipation").setSort(wixData.sort().ascending("market"));
		$w("#datasetSTMLeaderboard").setSort( wixData.sort()
			.ascending("market")
			.descending("maxTimestamp")
			//.ascending("leaderBoardRank")
  			.descending("numSelftapes")
  			//.ascending("_updatedDate")
		);
    } 
	else if ($w("#radioGroupSort").value === 'market_za') 
  {
        //$w("#datasetSelfTapeMayParticipation").setSort(wixData.sort().descending("yearsParticipatedBefore"));
		$w("#datasetSTMLeaderboard").setSort( wixData.sort()
			.descending("market")
			.descending("maxTimestamp")
			//.ascending("leaderBoardRank")
  			.descending("numSelftapes")
  			//.ascending("_updatedDate")
		);
    } 
	else if ($w("#radioGroupSort").value === 'years_participated_lowhigh') 
  {
		$w("#datasetSTMLeaderboard").setSort( wixData.sort()
			.ascending("numYearsParticipated")
			.descending("maxTimestamp")
			//.ascending("leaderBoardRank")
  			.descending("numSelftapes")
  			//.ascending("_updatedDate")
		);
    }
	else if ($w("#radioGroupSort").value === 'years_participated_highlow') 
  {
		$w("#datasetSTMLeaderboard").setSort( wixData.sort()
			.descending("numYearsParticipated")
			.descending("maxTimestamp")
			//.ascending("leaderBoardRank")
  			.descending("numSelftapes")
  			//.ascending("_updatedDate")
		);
    }
	else if ($w("#radioGroupSort").value === 'selfTapesHighLow') 
  {
		$w("#datasetSTMLeaderboard").setSort( wixData.sort()
			.descending("numSelftapes")
			//.descending("numYearsParticipated")
			.descending("maxTimestamp")
			//.ascending("leaderBoardRank")
  			//.ascending("_updatedDate")
		);
    }
}

export function buttonResetSort_click(event) {
	/**This should reset the sort of the table tableSelfTapeMayLeaderboard back to the originally intended sort order */

	$w("#datasetSTMLeaderboard").setSort( wixData.sort()
		.descending("maxTimestamp")
		.descending("userRank")
	);

	$w("#radioGroupSort").value = ""
}

export function buttonResetFilter_click(event) {
	/**This should reset all of the filter options back to default/starting position */
	var filter = wixData.filter();
	filter = filter.gt("numSelftapes", 0);
	//filter = filter.ne("excludeFromLeaderboard", true);
	$w("#datasetSTMLeaderboard").setFilter(filter);
	$w("#rangeSliderSelfTapes").value=[0,45];
	$w("#inputInstagram").value = "";
	$w("#dropdownMarket").value = "";
	$w("#checkboxCampaign").checked = false;
	$w("#datasetSTMLeaderboard").setSort( wixData.sort()
		.descending("maxTimestamp")
		.descending("userRank")
	);
}

export function buttonFilterSlider_click(event) {
	/**This slider will allow the users to filter the table based on the range of self tapes completed that have been selected with the slider */
	let sliderMin = $w("#rangeSliderSelfTapes").value[0]
	let sliderMax = $w("#rangeSliderSelfTapes").value[1]
	let marketValue = $w("#dropdownMarket").value
	let instagramFilter = $w('#inputInstagram').value
	let campaignFlag = $w("#checkboxCampaign").checked
	//let campaignFlagBool = $w("#checkboxCampaign").value === "true"
	console.log("Instagram handle value" + instagramFilter)
	console.log("Slider min value: " + sliderMin)
	console.log("Slider max value: " + sliderMax)
	console.log("Market value is: " + marketValue)
	
	// init the filter
	//HUGE credit to the answer given here: https://www.wix.com/velo/forum/coding-with-velo/add-a-filter-to-dataset-but-also-keep-the-previous-filter
	 var filter = wixData.filter();

	//Filter for Self Tapes
	if (sliderMin == 0 && sliderMax == 45) {
		//do nothing
		filter = filter.gt("numSelftapes", 0)
		console.log("I did nothing to filter slider")
	} else {
		//Filter for self tape #
		//This if statement is to make sure the minimum values showing up when filtered are 1
		//because I don't want people with a 0 self tapes to show up
		//Since the filter is sliderMin - 1 then 2 will force the absolute minimum of the sliderMin value to be 1
		if (sliderMin == 0) {
			//sliderMin = 2
			sliderMin = 1
		} /*else if (sliderMax == 1) {
			//sliderMin = 2
			sliderMin = 1
		}*/ else {
			//do nothing
		}
		filter = filter.between("numSelftapes", sliderMin, sliderMax + 1);
		//filter = filter.between("selfTapes", sliderMin, sliderMax);
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
		filter = filter.contains("instagram", instagramFilter)
	}
	//Filter for Campaign Sides
	if (campaignFlag) {
		console.log("Applied campaignFlag filter...")
		console.log("campaignFlag value: ", campaignFlag)
		//console.log("campaignFlagBool value: ", campaignFlagBool)
		filter = filter.eq("campaignFlag", "Y")
	} else {
		//do nothing
		console.log("Did nothing...")
		console.log("campaignFlag value: ", campaignFlag)
		//console.log("campaignFlagBool value: ", campaignFlagBool)
	}
	//Apply filter
	//filter = filter.ne("excludeFromLeaderboard", true);
	$w("#datasetSTMLeaderboard").setFilter(filter);	
}


/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function buttonRefreshLeaderboard_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
	/************************************************************************* */
	//Rank the entire population based on self tapes recorded and updated date
	//This is working as expected 27-apr-2022
	rankLeaderboard();
	console.log("Leaderboard refreshed");
	/************************************************************************* */
}