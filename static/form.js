function validateField(element) {
  let field=$(element).val();
  if(field =="") {
    element.style["border-bottom"] ="2px solid red";
  } else {
    element.style["border-bottom"] ="2px solid green";
  }
}

function validateEmail(element) {
  let field=$(element).val();
  if (field == "")
    element.style["border-bottom"] ="2px solid red";
	else if (!((field.indexOf(".") > 0) && (field.indexOf("@") > 0)) || /[^a-zA-Z0-9.@_-]/.test(field))
		element.style["border-bottom"] ="2px solid red";
	else element.style["border-bottom"] ="2px solid green";
}

function validatePhone(element) {
  let field = $(element).val();
  if (field =="" || /[^0-9-]/.test(field))
    element.style["border-bottom"] ="2px solid red";
  else element.style["border-bottom"] ="2px solid green";
}

function validateLocation(element) {
  let field = $(element).val();
  if (field == "" || /[^a-zA-Z0-9.-\s]/.test(field))
    element.style["border-bottom"] ="2px solid red";
  else element.style["border-bottom"] ="2px solid green";
}

function validateCity(element) {
  let field = $(element).val();
  if (field =="" || /[^a-zA-Z\s]/.test(field)) {
    element.style["border-bottom"] ="2px solid red";
  }
  else element.style["border-bottom"] ="2px solid green";
}

function validateState(element) {
  let field = $(element).val();
  if (field =="" || /[^a-zA-Z]/.test(field) || field.length > 2) {
    element.style["border-bottom"] ="2px solid red";
    element.placeholder= "2 chars."
  }
  else element.style["border-bottom"] ="2px solid green";
}

function validateZip(element) {
  let field = $(element).val();
  if (field =="" || /[^0-9]/.test(field))
    element.style["border-bottom"] ="2px solid red";
  else element.style["border-bottom"] ="2px solid green";
}

function validateUsername(element) {
  let field = $(element).val();
  if (field == "" || /[^a-zA-Z0-9._-]/.test(field) || field.length < 5) {
    element.style["border-bottom"] ="2px solid red";
    element.placeholder ="Username must be at least 5 characters";
  }
  else element.style["border-bottom"] ="2px solid green";
}

function validatePassword(element) {
  let field = $(element).val();
  if (field == "" || /[^a-zA-Z0-9._-]/.test(field) || field.length < 8) {
    element.style["border-bottom"] ="2px solid red";
    element.placeholder ="Passwords must be at least 8 characters";
  }
  else element.style["border-bottom"] ="2px solid green";
}

function authUser(element) {
  let field = $(element).val();
  if (field == "" || /[^a-zA-Z0-9._-]/.test(field)) {
    element.style["border-bottom"] ="2px solid red";
  }
  else element.style["border-bottom"] ="2px solid green";
}
