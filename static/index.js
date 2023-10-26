function get_data() {
	const submitButton = document.getElementById('submitButton');
	const textInput = document.getElementById('textInput');
	const imageInput = document.getElementById('imageInput');

	submitButton.addEventListener('click', function (e) {
		e.preventDefault();

		let text = textInput.value;
		let image = imageInput.files[0];
		console.log(image);

		const formData = new FormData();
		formData.append('text', text);
		formData.append('image', image);

		fetch(`/`, {
			method: 'POST',
			body: formData,
		}).then((response) => {
			if (response.ok) {
				window.location.reload();
			}
		});
	});
}

get_data();
