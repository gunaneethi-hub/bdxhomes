/**
 * BDX Smart Homes — Website Lead & Job Application Intake
 *
 * SETUP
 * 1. Create a Google Sheet (any name) — this script will create the tabs it needs.
 * 2. Extensions -> Apps Script, delete the placeholder code, paste this file in.
 * 3. Deploy -> New deployment -> type "Web app".
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 4. Copy the deployed /exec URL and paste it into SCRIPT_URL in form-submit.js.
 * 5. Re-deploy (new version) any time you edit this file — the /exec URL stays the same
 *    as long as you use "Manage deployments" -> edit -> new version, rather than
 *    creating a brand new deployment.
 */

var NOTIFY_EMAIL = 'bdxhomes@gmail.com';
var LEADS_SHEET = 'Leads';
var APPLICATIONS_SHEET = 'Applications';
var RESUME_FOLDER_NAME = 'BDX Website Resumes';

function doPost(e) {
  try {
    var p = e.parameter;
    if (p.form_type === 'application') {
      handleApplication(p);
    } else {
      handleLead(p);
    }
    return ContentService.createTextOutput('ok');
  } catch (err) {
    return ContentService.createTextOutput('error: ' + err.message);
  }
}

function getSheet_(name, headerRow) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    sheet.appendRow(headerRow);
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function handleLead(p) {
  var sheet = getSheet_(LEADS_SHEET, ['Timestamp', 'Source Page', 'Name', 'Phone', 'Email', 'Service Interest']);
  sheet.appendRow([
    new Date(),
    p.source_page || '',
    p.name || '',
    p.phone || '',
    p.email || '',
    p.service || ''
  ]);

  MailApp.sendEmail({
    to: NOTIFY_EMAIL,
    subject: 'New website lead: ' + (p.name || 'Unknown') + ' — ' + (p.source_page || ''),
    body:
      'Name: ' + (p.name || '') + '\n' +
      'Phone: ' + (p.phone || '') + '\n' +
      'Email: ' + (p.email || '') + '\n' +
      'Service: ' + (p.service || '') + '\n' +
      'Source: ' + (p.source_page || '') + '\n' +
      'Time: ' + new Date()
  });
}

function handleApplication(p) {
  var sheet = getSheet_(APPLICATIONS_SHEET, ['Timestamp', 'Source Page', 'Name', 'Phone', 'Email', 'Role', 'Resume Link']);

  var resumeLink = '';
  if (p.resume_data && p.resume_name) {
    var folder = getOrCreateFolder_(RESUME_FOLDER_NAME);
    var base64 = p.resume_data.indexOf(',') > -1 ? p.resume_data.split(',').pop() : p.resume_data;
    var bytes = Utilities.base64Decode(base64);
    var blob = Utilities.newBlob(bytes, p.resume_type || 'application/octet-stream', p.resume_name);
    var file = folder.createFile(blob);
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    resumeLink = file.getUrl();
  }

  sheet.appendRow([
    new Date(),
    p.source_page || '',
    p.name || '',
    p.phone || '',
    p.email || '',
    p.role || '',
    resumeLink
  ]);

  MailApp.sendEmail({
    to: NOTIFY_EMAIL,
    subject: 'New job application: ' + (p.name || 'Unknown') + ' — ' + (p.role || ''),
    body:
      'Name: ' + (p.name || '') + '\n' +
      'Phone: ' + (p.phone || '') + '\n' +
      'Email: ' + (p.email || '') + '\n' +
      'Role: ' + (p.role || '') + '\n' +
      'Resume: ' + (resumeLink || '(not attached)') + '\n' +
      'Source: ' + (p.source_page || '') + '\n' +
      'Time: ' + new Date()
  });
}

function getOrCreateFolder_(name) {
  var folders = DriveApp.getFoldersByName(name);
  if (folders.hasNext()) return folders.next();
  return DriveApp.createFolder(name);
}
