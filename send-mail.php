<?php
/**
 * RIVO ELC — Enquiry Form Mailer
 * Receives POST data from the contact form and sends it to info@rivoelc.com
 */

// ── Configuration ──────────────────────────────────────────────────────────
define('TO_EMAIL',   'info@rivoelc.com');
define('TO_NAME',    'RIVO Early Learning Centre');
define('FROM_EMAIL', 'noreply@rivoelc.com');   // must be on your hosting domain
define('FROM_NAME',  'RIVO Website Enquiry');
define('REDIRECT',   'contact.html');
// ───────────────────────────────────────────────────────────────────────────

// Only accept POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: ' . REDIRECT . '?status=error');
    exit;
}

// ── Helper: sanitize input ──────────────────────────────────────────────────
function clean(string $value): string {
    return htmlspecialchars(strip_tags(trim($value)), ENT_QUOTES, 'UTF-8');
}

// ── Collect & sanitize fields ───────────────────────────────────────────────
$child_name   = clean($_POST['child-name']   ?? '');
$child_dob    = clean($_POST['child-dob']    ?? '');
$child_age    = clean($_POST['child-age']    ?? '');
$mother_name  = clean($_POST['mother-name']  ?? '');
$father_name  = clean($_POST['father-name']  ?? '');
$phone        = clean($_POST['phone']        ?? '');
$email        = clean($_POST['email']        ?? '');
$relationship = clean($_POST['relationship'] ?? '');
$centre       = clean($_POST['centre']       ?? '');

// ── Basic server-side validation ────────────────────────────────────────────
$errors = [];

if (empty($child_name))  $errors[] = 'Child name is required.';
if (empty($child_age))   $errors[] = 'Child age is required.';
if (empty($mother_name)) $errors[] = "Mother's name is required.";
if (empty($father_name)) $errors[] = "Father's name is required.";
if (empty($phone))       $errors[] = 'Phone number is required.';
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'A valid email address is required.';

if (!empty($errors)) {
    // Redirect back with error (you can add flash-message support later)
    header('Location: ' . REDIRECT . '?status=error');
    exit;
}

// ── Build email body ────────────────────────────────────────────────────────
$submitted_on = date('d M Y, h:i A');

$body = "
New Enquiry Received — RIVO Early Learning Centre
==================================================
Submitted on : {$submitted_on}

CHILD DETAILS
-------------
Name         : {$child_name}
Date of Birth: {$child_dob}
Age          : {$child_age}

PARENT / GUARDIAN DETAILS
--------------------------
Mother's Name : {$mother_name}
Father's Name : {$father_name}
Relationship  : {$relationship}

CONTACT DETAILS
---------------
Phone   : {$phone}
Email   : {$email}

PREFERRED CENTRE
----------------
{$centre}

==================================================
This message was sent automatically from the RIVO website enquiry form.
";

// ── Email headers ───────────────────────────────────────────────────────────
$subject = "New Admission Enquiry — {$child_name} ({$child_age})";

$headers  = "From: " . FROM_NAME . " <" . FROM_EMAIL . ">\r\n";
$headers .= "Reply-To: {$email}\r\n";
$headers .= "X-Mailer: PHP/" . phpversion() . "\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

// ── Send ────────────────────────────────────────────────────────────────────
$sent = mail(TO_NAME . ' <' . TO_EMAIL . '>', $subject, $body, $headers);

// ── Redirect with result ────────────────────────────────────────────────────
if ($sent) {
    header('Location: ' . REDIRECT . '?status=success');
} else {
    header('Location: ' . REDIRECT . '?status=error');
}
exit;
