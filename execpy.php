 <?php
    header('Content-Type: application/json');
    $command = escapeshellcmd('python3 rmdir.py');
    $output = shell_exec($command);
    echo $output;

    $command = escapeshellcmd('python3 ocr_c.py');
    $output = shell_exec($command);
    echo $output;

    $command = escapeshellcmd('python3 code.py');
    $output = shell_exec($command);
    echo $output;


    
?>

