<?php
/**
 * RIVO ELC — Enquiry Form Mailer
 * Uses PHP built-in mail() — no composer or library needed.
 * Works on any standard PHP web hosting.
 */

// ── Only accept POST requests ───────────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: contact.html');
    exit;
}

// ── Sanitize inputs ─────────────────────────────────────────────────────────
function clean(string $v): string {
    return htmlspecialchars(strip_tags(trim($v)), ENT_QUOTES, 'UTF-8');
}

$child_name   = clean($_POST['child-name']   ?? '');
$child_dob    = clean($_POST['child-dob']    ?? '');
$child_age    = clean($_POST['child-age']    ?? '');
$mother_name  = clean($_POST['mother-name']  ?? '');
$father_name  = clean($_POST['father-name']  ?? '');
$phone        = clean($_POST['phone']        ?? '');
$email        = filter_var(trim($_POST['email'] ?? ''), FILTER_SANITIZE_EMAIL);
$relationship = clean($_POST['relationship'] ?? '');
$centre       = clean($_POST['centre']       ?? '');

// ── Validate required fields ────────────────────────────────────────────────
if (empty($child_name) || empty($child_age) || empty($mother_name) ||
    empty($father_name) || empty($phone) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    header('Location: contact.html?status=error');
    exit;
}

// ── Build the email ─────────────────────────────────────────────────────────
$to      = 'info@rivoelc.com';
$subject = "New Enquiry: {$child_name} ({$child_age}) — RIVO ELC";

$body = "
New Admission Enquiry — RIVO Early Learning Centre
Submitted: " . date('d M Y, h:i A') . "

---------------------------------------
CHILD DETAILS
---------------------------------------
Name         : {$child_name}
Date of Birth: {$child_dob}
Age          : {$child_age}

---------------------------------------
PARENT / GUARDIAN DETAILS
---------------------------------------
Mother's Name : {$mother_name}
Father's Name : {$father_name}
Relationship  : {$relationship}

---------------------------------------
CONTACT DETAILS
---------------------------------------
Phone  : {$phone}
Email  : {$email}

---------------------------------------
PREFERRED RIVO CENTRE
---------------------------------------
{$centre}

---------------------------------------
Reply directly to this email to contact the parent.
";

$headers  = "From: RIVO Website <info@rivoelc.com>\r\n";
$headers .= "Reply-To: {$email}\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "X-Mailer: PHP/" . phpversion() . "\r\n";

// ── Send & redirect ─────────────────────────────────────────────────────────
if (mail($to, $subject, $body, $headers)) {
    header('Location: contact.html?status=success');
} else {
    header('Location: contact.html?status=error');
}
exit;
