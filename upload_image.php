 <?php
    header('Content-Type: application/json');
    $command = escapeshellcmd('python3 rmdir.py');
    $output = shell_exec($command);
    echo $output;

    if (isset($_FILES['upload']) && $_FILES['upload']['error'] == 0) {
        #$ext = explode('.',$_FILES['upload']['name']);
        #$extension = $ext[1];
        #echo $extension;
        #$full_local_path = '/var/www/html/numrecog/'.$newname.'.'.$extension ;
        if (move_uploaded_file($_FILES['upload']['tmp_name'], "/var/www/html/numrecog/image.png")) {
            #var_dump($_FILES);
        }else{
            #var_dump($_FILES);
        }
    }else{
        #var_dump($_FILES);
    }


    
?>

