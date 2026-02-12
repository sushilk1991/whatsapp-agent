<?php
// Waitlist handler - add to your server
header('Content-Type: application/json');

$email = $_POST['email'] ?? '';
$name = $_POST['name'] ?? '';

// Validate
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo json_encode(['success' => false, 'message' => 'Invalid email']);
    exit;
}

// Save to file (use database in production)
$waitlist_file = 'waitlist.json';
$waitlist = file_exists($waitlist_file) ? json_decode(file_get_contents($waitlist_file), true) : [];
$waitlist[] = ['email' => $email, 'name' => $name, 'date' => date('Y-m-d H:i:s')];
file_put_contents($waitlist_file, json_encode($waitlist, JSON_PRETTY_PRINT));

echo json_encode(['success' => true, 'message' => 'You\'re on the list! We\'ll notify you when we launch.']);
?>
