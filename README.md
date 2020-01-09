# aem-content-deploy

This program will deploy AEM Content packages to production depending on the brand selected. It will bump the version and build
the package on staging, then download it to your local computer to be uploaded and installed into production.

## Installation

Create virtual environment. Run the following from project directory to create a virtual environment in the current directory.

    python3 -m venv venv  
    
Activate virtual environment
    
    source venv/bin/activate    
    
Run pip install to download all dependencies
    
    pip3 install -r requirements.txt

## Project Setup

You would need to set up a config file so that the program can use your credentials and talk to 
the appropriate staging & production servers

Set up the following __config.json__ within root of project directory

```
{
  "username": "<aem-username>",
  "password": "<aem-password>",
  "staging": "<staging-ip>",
  "prod": "<production-ip>"
}
``` 
    
## Running the script

Run the deploy script

    python3 deploy.py

Choose between current content packages
>Enter content package to deploy >> 
>1) Tweed
>2) Spectrum
>3) Brands
>4) Exit
    
### Notes

- Packages downloaded will be stored in the pkg directory so deleting this directory within the
project will break the program.
- Old content.zip files will automatically get overwritten