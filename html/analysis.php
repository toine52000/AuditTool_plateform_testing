<?php

/* Ajoute une redirection pour que vous puissiez lire stderr. */
chdir('/var/www/analysis/');
ob_implicit_flush(true);
ob_end_flush();

$cmd = "./snap_analysis.py";

$descriptorspec = array(
   0 => array("pipe", "r"),   // stdin is a pipe that the child will read from
   1 => array("pipe", "w"),   // stdout is a pipe that the child will write to
   2 => array("pipe", "w")    // stderr is a pipe that the child will write to
);
flush();
$process = proc_open($cmd, $descriptorspec, $pipes, realpath('./'), array());
echo "<pre>";
if (is_resource($process)) {
    while ($s = fgets($pipes[1]) or $e = fgets($pipes[2])) {
        print $s;
	print $e;
        flush();
    }
}
echo "</pre>";



?>