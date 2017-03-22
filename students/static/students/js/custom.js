$(document).ready(function() {

	var userData = {};

	$("#registerForm").submit(function(e) {

		// Cache the form's object
		var form = $(this).find("form");
		form.removeClass("has-error");
		if (e.isDefaultPrevented() || $(this).find('.has-error').length) {
			// Form has validation errors.
		} else {
			e.preventDefault();
			userData = convertToJSON(form.serializeArray());
			userData["type_flag"] = 1;
		
			//  Get URL set by Django
			var verifyUrl = form.attr('action');
			
			// Send limited information to the server till the phone number is verified
			var json = {"mobile_number": userData['mobile_number'], "csrfmiddlewaretoken": userData["csrfmiddlewaretoken"], "type_flag": userData["type_flag"]};
			
			// Send AJAX to initiate the verification process
			$.ajax({
				url: verifyUrl,
				type: 'POST',
				data: json,
				dataType: "json",
				success: function(data) {
					if(data == userData["type_flag"]) {
						var verifyForm = $("#verifyForm");
						verifyForm.removeClass("hidden");
						form.parents(".row").addClass("hidden");
						verifyForm.validator();
					} else {
						form.addClass("has-error");
					}
				},
				error: function(e) {
					form.addClass("has-error");
				}
			});
		}
	});

	$("#verifyForm .btn.btn-primary").click(function(e) {
		// Cache the form's object
		var form = $(this).parents("form");
		form.removeClass("has-error");
		if (e.isDefaultPrevented() || $(this).find('.has-error').length) {
			// Form has validation errors.
		} else {
			e.preventDefault();
			var verifyData = convertToJSON(form.serializeArray());

			//  Get URL set by Django
			var verifyUrl = form.attr('action');

			json = jQuery.extend(verifyData, userData);

			if(json["type_flag"] == "1") {
				$.ajax({
					url: verifyUrl,
					type: 'POST',
					data: json,
					dataType: "json",
					success: function(data) {
						window.location.href = data.url;
					},
					error: function(e) {
						form.addClass("has-error");
					}
				});
			} else if (json["type_flag"] == "2") {
				var input = $("<input>").attr("type", "hidden").attr("name", "mobile_number").val(userData["mobile_number"]);
				var input2 = $("<input>").attr("type", "hidden").attr("name", "type_flag").val(userData["type_flag"]);
				form.append($(input));
				form.append($(input2));
				form.submit();
			}
		}
	});

	$("#getInfoForm").submit(function(e) {

		// Cache the form's object
		var form = $(this).find("form");
		form.removeClass("has-error");
		if (e.isDefaultPrevented() || $(this).find('.has-error').length) {
			// Form has validation errors.
		} else {
			e.preventDefault();
			userData = convertToJSON(form.serializeArray());
			userData["type_flag"] = 2;
		
			//  Get URL set by Django
			var verifyUrl = form.attr('action');
			
			// Send AJAX to initiate the verification process
			$.ajax({
				url: verifyUrl,
				type: 'POST',
				data: userData,
				dataType: "json",
				success: function(data) {
					if(data == userData["type_flag"]) {
						var verifyForm = $("#verifyForm");
						verifyForm.removeClass("hidden");
						form.parents(".row").addClass("hidden");
						verifyForm.validator();
					} else {
						form.addClass("has-error");
					}
				},
				error: function(e) {
					form.addClass("has-error");
				}
			});
		}
	});
});

function convertToJSON(array) {
	var jsonObject = {};
	for (var i = 0; i < array.length; i++){
		jsonObject[array[i]['name']] = array[i]['value'];
	}
	return jsonObject;
}