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
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/

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
  			.descending("selfTapes")
  			.ascending("_updatedDate")
		);
    } 
	else if ($w("#radioGroupSort").value === 'market_za') 
  {
        //$w("#datasetSelfTapeMayParticipation").setSort(wixData.sort().descending("yearsParticipatedBefore"));
		$w("#datasetSelfTapeMayParticipation").setSort( wixData.sort()
			.descending("market")
  			.descending("selfTapes")
  			.ascending("_updatedDate")
		);
    } 
	else if ($w("#radioGroupSort").value === 'years_participated_lowhigh') 
  {
        //$w("#datasetSelfTapeMayParticipation").setSort(wixData.sort().descending("yearsParticipatedBefore"));
		$w("#datasetSelfTapeMayParticipation").setSort( wixData.sort()
			.ascending("yearsParticipatedBefore")
  			.descending("selfTapes")
  			.ascending("_updatedDate")
		);
    }
	else if ($w("#radioGroupSort").value === 'years_participated_highlow') 
  {
        //$w("#datasetSelfTapeMayParticipation").setSort(wixData.sort().descending("yearsParticipatedBefore"));
		$w("#datasetSelfTapeMayParticipation").setSort( wixData.sort()
			.descending("yearsParticipatedBefore")
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
}
