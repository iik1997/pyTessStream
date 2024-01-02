#!/bin/bash
cont_name="$(podman ps -a | grep mytess_streamlitapp_img | tr -s ' ' | tr ' ' "\n" | tail -1)"
if [ -n "$cont_name" ]; then
	echo Restarting mytess_streamlitapp_img...
	podman restart "${cont_name}"
	echo ...done
else
	echo mytess_streamlitapp_img is not running
fi
