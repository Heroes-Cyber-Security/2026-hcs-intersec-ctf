<?php
session_start();

header('Content-Type: application/json');

$key = $_GET['key'] ?? '';
$progress = $_SESSION['upload_progress_' . $key] ?? null;

echo json_encode($progress);
