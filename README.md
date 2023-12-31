# In-Browser OCR based on Streamlit and Tesseract

## Core Functionality
* The very basic functionality is in `do_ocr` function of `mytessapp.py`
* The dependencies are reflected in `Dockerfile`

## HOWTO
* Build the image: `podman build -t mytess_streamlitapp_img .`
* Run the app: `podman run -p 8888:8888 -v ./config-cont:/app/config -v ./data-cont:/app/data -v ./output-cont:/app/output -d mytess_streamlitapp_img`
    * Tesseract config params are in `.env` file locally accessible via `./config-cont/.env` (reasonable defaults are already set)
    * Uploaded picture files are locally accessible (and also can be cleaned up) via `./data-cont`
    * Results of OCR are locally accessible (and also can be cleaned up) via `./output-cont`
* Upload the input data and see the results locally in a browser via `localhost:8888`
* Stop the app/release the resources: `podman stop <CONTAINER_NAME> && podman rm <CONTAINER_NAME>`

## Useful podman/docker commands
* List (running) containers (also to find out container names and ids): `podman ps -a`
* Show log messages for a given container: `podman logs <CONTAINER_NAME>`
* Stop given container (normally before rm-command): `podman stop <CONTAINER_NAME>`
* Remove given container/release resources: `podman rm <CONTAINER_NAME>`
* Get a command prompt inside a running container: `podman exec -it <CONTAINER_NAME> "bash"`
