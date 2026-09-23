<?php

$KEY      = 'REDACTED_ON_SERVER';
$FLAG_ENC = 'REDACTED_ON_SERVER';

if ($_SERVER['REQUEST_METHOD'] !== 'POST' || parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH) !== '/api/claim') {
    return false; // let the built-in server serve static files
}

header('Content-Type: application/json');

function fail(string $msg): void {
    echo json_encode(['msg' => $msg]);
    exit;
}

$in = json_decode(file_get_contents('php://input'), true);
if (!is_array($in)) fail('hey, no ☝️ no ☝️ no ☝️ yah');

$score     = $in['score']     ?? null;
$eats      = $in['eats']      ?? null;
$integrity = $in['integrity'] ?? null;
$sig       = $in['sig']       ?? null;

if ($score !== 999999)         fail('hey, no ☝️ no ☝️ no ☝️ yah');
if ($eats !== 111111)          fail('hey, no ☝️ no ☝️ no ☝️ yah');
if ($integrity !== 0x71800FC4) fail('hey, no ☝️ no ☝️ no ☝️ yah');

$sigInput = implode('|', [$score, $eats, $integrity, 'HCS{coba_submit_flag_ini_siapa_tau_bukan_decoy_xixixi}']);
if (!is_string($sig) || !hash_equals(hash('sha256', $sigInput), $sig)) fail('hey, no ☝️ no ☝️ no ☝️ yah');

$out = '';
for ($i = 0; $i < strlen($FLAG_ENC); $i++) {
    $out .= $FLAG_ENC[$i] ^ $KEY[$i % strlen($KEY)];
}
echo json_encode(['flag' => $out]);
