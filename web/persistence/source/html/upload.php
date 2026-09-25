<?php
session_start();

const UPLOAD_DIR = '/var/www/uploads/';

function back(string $message): void
{
    header('Location: index.php?message=' . urlencode($message));
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST' || !isset($_FILES['attachment'])) {
    back('No file was submitted.');
}

$file = $_FILES['attachment'];

if ($file['error'] !== UPLOAD_ERR_OK) {
    back('Upload failed during transfer.');
}

$mime = (new finfo(FILEINFO_MIME_TYPE))->file($file['tmp_name']);
$dimensions = @getimagesize($file['tmp_name']);
$extension = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));

$allowedMime = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
$allowedExt = ['jpg', 'jpeg', 'png', 'gif', 'webp'];

if (!in_array($mime, $allowedMime, true)) {
    back('Rejected: unsupported MIME type (' . $mime . ').');
}

if ($dimensions === false) {
    back('Rejected: file is not a valid image.');
}

if (!in_array($extension, $allowedExt, true)) {
    back('Rejected: unsupported file extension.');
}

$content = file_get_contents($file['tmp_name']);

if (preg_match('/<\?|<script|eval\(|system\(|base64_decode\(/i', $content)) {
    back('Rejected: suspicious content detected.');
}

$storedName = bin2hex(random_bytes(16)) . '.' . $extension;

if (!move_uploaded_file($file['tmp_name'], UPLOAD_DIR . $storedName)) {
    back('Failed to store the uploaded file.');
}

$_SESSION['last_upload'] = $storedName;

back('Success: attachment stored securely.');
