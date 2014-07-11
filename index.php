<?php

if(isset($_GET["pin"]) && !empty($_GET["pin"]))
{
	$pin = $_GET["pin"];

	if($pin == "3441")
	{
		echo "welcome";
	}
	else
	{
		echo "go away";
	}
}
else
{
	include("form.html");
}

#EOF