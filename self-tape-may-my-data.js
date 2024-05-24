// Velo API Reference: https://www.wix.com/velo/reference/api-overview/introduction
import wixData from 'wix-data';
import { currentMember } from 'wix-members';

$w.onReady(function () {

	// Write your Javascript code here using the Velo framework API

	// Print hello world:
	// console.log("Hello world!");

	// Call functions on page elements, e.g.:
	// $w("#button1").label = "Click me!";

	// Click "Run", or Preview your site, to execute your code
	let email = userEmail()
		.then((email) => {
			console.log(email)
			refreshMyData(email)
		})
});

async function userEmail() {
	const member = await currentMember.getMember();
    const userEmail = member.loginEmail;

	return userEmail
}

function refreshMyData(email){

console.log("Setting filter on #datasetMyData")
$w("#datasetMyData").setFilter(wixData.filter().eq("email", email))
	.then(() => {
		$w("#datasetMyData").refresh
		//$w("#repeaterMyRank").show()
		$w("#tableMyData").show()
	})
}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function buttonSomethingDoesntLookRight_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
	$w('#boxSomethingDoesntLookRight').show()
	$w('#textPrivateIG').hide()
	$w('#vectorImagePrivateIG').hide()
}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function buttonSubmit_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
	
	let email = userEmail()
	.then((email) => {
		let postURL = $w('#inputPostURL').value
		console.log("postURL: " + postURL)
		let postDateTime = $w('#datePostDate').value
		console.log("postDateTime: " + postDateTime)
		console.log("email: " + email)
		wixData.insert("missingData", {
		"url": postURL,
		"dateTime": new Date(postDateTime),
		"email": email
		})
	})
	.then((results) => {
		console.log("Data inserted to missingData");
	})
	.catch((err) => {
		console.log(err);
	});

	// Show the text box
	$w('#imageSaved').show();

	// Hide the text box after 3 seconds
	setTimeout(() => {
		$w('#imageSaved').hide()
		$w('#boxSomethingDoesntLookRight').hide();
		$w('#textPrivateIG').show()
		$w('#vectorImagePrivateIG').show()
	}, 2000);


}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function buttonManualData_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
	$w('#boxManualData').show();
	$w('#textPrivateIG').hide()
	$w('#vectorImagePrivateIG').hide()

	let email = userEmail()
		.then((email) => {
			//console.log(email)
			//refreshMyData(email)
			console.log("userEmail to query user instagram: ", email)
			wixData.query("gcpOperationalDB/viewSTMParticipantData")
				.eq("email", email)
				.find()
				.then(results => {
					if (results.items.length > 0) {
						const item = results.items[0]; // get the first item in the array
						$w('#inputInstagram').value = item.instagram
						$w('#inputInstagram').enable()
					} else {
						console.log("Something went wrong!!  Instagram account doesn't exist for " + userEmail)
						// handle case where no results are found
					}
				})
			.catch(error => {
				console.log(error);
			});
		})
	
}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function buttonSubmitData_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
	//$w('#mobileTextUpdating').show()

	// Get the value from the input field
	const inputInstagram = $w('#inputInstagram').value;

	// Specify the required prefix
	const prefix = 'https://www.instagram.com/p/';

	// Check if the input starts with the required prefix
	//if (!inputInstagram.startsWith(prefix)) {
	//	$w('#textURLMatchWarning').show();
	//	// Hide the text box after 3 seconds
	//	setTimeout(() => {
	//		$w('#textURLMatchWarning').hide()
	//	}, 2000);
	//	return; // Exit the function
	//	//throw new Error('The Instagram URL must start with ' + prefix);
	//}

	// Continue with the rest of your code if no error is thrown

	let instagramHandleURLCheck = $w('#inputInstagram').value
	instagramHandleURLCheck = instagramHandleURLCheck.replace(/@/g, "")
	//instagramHandleURLCheck = 'www.instagram.com/' + instagramHandleURLCheck
	
	let instagramURL = $w('#inputURL').value
	if (instagramURL == "") {
		// show #textPostURLRequired for 2 seconds
		$w('#textPostURLRequired').show();
		// Hide the text box after 3 seconds
		setTimeout(() => {
			$w('#textPostURLRequired').hide()
		}, 2000);
	} else if (instagramURL.includes(instagramHandleURLCheck) ) {
		$w('#textURLMatchWarning').show();
		// Hide the text box after 3 seconds
		setTimeout(() => {
			$w('#textURLMatchWarning').hide()
		}, 2000);
	} else {
		console.log("instagramURL: ", instagramURL)
	$w('#textAddingRecord').show()
	$w('#imageCheckManualData').hide()
	wixData.query("gcpOperationalDB/viewSTMInstagramData")
		.limit(3)
  		.eq("url", instagramURL)
  		.find()
		.then(results => {
			console.log("Query has finished and returned results...")
			console.log(results.items.length)
			if (results.items.length > 0) {
				$w('#textAddingRecord').hide()
				$w('#textAlert').show()
			} else {
				console.log("Creating a new record...")
				let recordDate = new Date()
				console.log("recordDate: ", recordDate)
				let instagramHandle = $w('#inputInstagram').value
				console.log(instagramHandle)
				let campaign = $w('#checkboxCampaign').checked
				console.log(campaign)
				let hashtag0 = "selftapemay"
				console.log(hashtag0)
				let hashtag1 = ""
				console.log(hashtag1)
				if (campaign) {
					hashtag1 = "selftapemaylotr"
				} else {
					hashtag1 = ""
				}
				console.log(campaign)

				const toInsert = {
					"id": instagramURL,
					"ownerUsername": instagramHandle,
					"timestamp": recordDate,
					"url": instagramURL,
					"hashtag_0": hashtag0,
					"hashtag_1": hashtag1,
					"campaignFlag": campaign
				};
				wixData.insert("gcpOperationalDB/tblInstagramData", toInsert)
					.then((results) => {
						console.log(results); //see item below
						// Show the text box
						$w('#textAddingRecord').hide()
						$w('#imageCheckManualData').show();

						// Hide the text box after 3 seconds
						setTimeout(() => {
							$w('#imageCheckManualData').hide()
							$w('#boxManualData').hide();
							$w('#textPrivateIG').show()
							$w('#vectorImagePrivateIG').show()
						}, 2000);
					})
					.catch((err) => {
						console.log(err);
					});
			}
		});
	}
}


/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function buttonCancel_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
	$w('#boxSomethingDoesntLookRight').hide()
	$w('#textPrivateIG').show()
	$w('#vectorImagePrivateIG').show()
}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function buttonCancelManualData_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
	$w('#boxManualData').hide();
	$w('#textPrivateIG').show()
	$w('#vectorImagePrivateIG').show()
}