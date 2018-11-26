<?php $out = array();
                    foreach (glob('numimg/*.jpg') as $filename) {
                        $p = pathinfo($filename);
                        $out[] = $p['filename'];
                    }
echo json_encode($out); ?>;