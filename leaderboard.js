// API Reference: https://www.wix.com/velo/reference/api-overview/introduction
// “Hello, World!” Example: https://learn-code.wix.com/en/article/1-hello-world
import wixData from 'wix-data';

$w.onReady(function () {
	// Write your JavaScript here

	// To select an element by ID use: $w('#elementID')
	
	// Click 'Preview' to run your code

});

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function buttonFilterInstagram_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
	let instagramFilter = $w('#inputInstagram').value
	console.log("Instagram handle value" + instagramFilter)
	$w("#datasetSelfTapeMayParticipation").setFilter(wixData.filter().eq("instagramHandle", instagramFilter));
	
	$w("#datasetSelfTapeMayParticipation").refresh()
		.then( () => {
		console.log("Done refreshing datasetSelfTapeParticipant");
	} );
}

/**
*	Adds an event handler that runs when an input element's value
 is changed.
	[Read more](https://www.wix.com/corvid/reference/$w.ValueMixin.html#onChange)
*	 @param {$w.Event} event
*/
export function radioGroupSort_change(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
	if ($w("#radioGroupSort").value === 'market_az')
	//Sort by Market
   {
        //$w("#datasetSelfTapeMayParticipation").setSort(wixData.sort().ascending("market"));
		$w("#datasetSelfTapeMayParticipation").setSort( wixData.sort()
			.ascending("market")
			.descending("leaderBoardRank")
  			.descending("selfTapes")
  			.ascending("_updatedDate")
		);
    } 
	else if ($w("#radioGroupSort").value === 'market_za') 
  {
        //$w("#datasetSelfTapeMayParticipation").setSort(wixData.sort().descending("yearsParticipatedBefore"));
		$w("#datasetSelfTapeMayParticipation").setSort( wixData.sort()
			.descending("market")
			.descending("leaderBoardRank")
  			.descending("selfTapes")
  			.ascending("_updatedDate")
		);
    } 
	else if ($w("#radioGroupSort").value === 'years_participated_lowhigh') 
  {
        //$w("#datasetSelfTapeMayParticipation").setSort(wixData.sort().descending("yearsParticipatedBefore"));
		$w("#datasetSelfTapeMayParticipation").setSort( wixData.sort()
			.ascending("yearsParticipatedBefore")
			.descending("leaderBoardRank")
  			.descending("selfTapes")
  			.ascending("_updatedDate")
		);
    }
	else if ($w("#radioGroupSort").value === 'years_participated_highlow') 
  {
        //$w("#datasetSelfTapeMayParticipation").setSort(wixData.sort().descending("yearsParticipatedBefore"));
		$w("#datasetSelfTapeMayParticipation").setSort( wixData.sort()
			.descending("yearsParticipatedBefore")
			.descending("leaderBoardRank")
  			.descending("selfTapes")
  			.ascending("_updatedDate")
		);
    }
}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function buttonResetSort_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
	//$w("#datasetSelfTapeMayParticipation").setSort(wixData.sort().descending("selfTapes"), wixData.sort().ascending("_updatedDate"));

	$w("#datasetSelfTapeMayParticipation").setSort( wixData.sort()
		.descending("leaderBoardRank")
  		.descending("selfTapes")
  		.ascending("_updatedDate")
);
}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function buttonResetFilter_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
	$w("#datasetSelfTapeMayParticipation").setFilter(wixData.filter());
	$w("#rangeSliderSelfTapes").value=[0,16];
	$w("#inputInstagram").value = "";
}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function buttonFilterSlider_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
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
