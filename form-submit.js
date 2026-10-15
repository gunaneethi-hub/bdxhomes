// BDX Smart Homes — shared lead/application intake helper.
// Posts form data to the Google Apps Script Web App via a hidden iframe form
// submission, so it works without CORS and without leaving the page.
//
// SETUP: after deploying the Apps Script (see google-apps-script/Code.gs) as
// a Web App, paste its /exec URL below.
(function () {
  var SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbxcqeitpE87T1YqRKNm3pad1XeE4pR7QGGmebTG6NQxngpge3WrHapXixIxQLmRzrbR/exec';

  function targetIframe() {
    var iframe = document.getElementById('bdx-form-target');
    if (!iframe) {
      iframe = document.createElement('iframe');
      iframe.name = 'bdx-form-target';
      iframe.id = 'bdx-form-target';
      iframe.style.display = 'none';
      document.body.appendChild(iframe);
    }
    return iframe;
  }

  // Submits an arbitrary field map to the intake sheet.
  window.bdxSubmitLead = function (data) {
    if (!SCRIPT_URL || SCRIPT_URL.indexOf('PASTE_YOUR') === 0) {
      return false;
    }
    targetIframe();
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = SCRIPT_URL;
    form.target = 'bdx-form-target';
    form.style.display = 'none';
    Object.keys(data).forEach(function (key) {
      var input = document.createElement('input');
      input.type = 'hidden';
      input.name = key;
      input.value = data[key] == null ? '' : data[key];
      form.appendChild(input);
    });
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
    return true;
  };

  // Convenience for the standard lead forms (name/phone/email/service).
  // Silently aborts if the honeypot field was filled in (bot traffic).
  window.bdxSubmitFormLead = function (formEl) {
    var honeypot = formEl.querySelector('[name="website"]');
    if (honeypot && honeypot.value) return false;

    var nameField = formEl.querySelector('[name="name"]');
    var phoneField = formEl.querySelector('[name="phone"]');
    var emailField = formEl.querySelector('[name="email"]');
    var serviceField = formEl.querySelector('[name="service"]');
    var formTypeField = formEl.querySelector('[name="form_type"]');
    var sourceField = formEl.querySelector('[name="source_page"]');

    return window.bdxSubmitLead({
      form_type: formTypeField ? formTypeField.value : 'lead',
      source_page: sourceField ? sourceField.value : document.title,
      name: nameField ? nameField.value.trim() : '',
      phone: phoneField ? phoneField.value.trim() : '',
      email: emailField ? emailField.value.trim() : '',
      service: serviceField ? serviceField.value : ''
    });
  };
})();
