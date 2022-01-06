# NYCU-LA-final-project

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)  
![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)

## Installation 

`$ git clone https://github.com/SiriusKoan/NYCU-LA-final-project.git`  
`$ cd NYCU-LA-final-project`  
`$ pipenv shell`  
`$ pipenv install`  
`$ exit`  
`$ pipenv run python3 PicrypterBOT.py`



## Functionality

This telegram bot is devised to help people **encrypt and decrypt confidential photos** with user-specified passwords, through *linear algebra* techniques.



## Bot Introduction

`/start` : Show greeting and the customized keyboard.

`/end` : Clear data.

`/encrypt` : Encrypt the image with the password.

`/dncrypt` : Decrypt the image with the password. 

`Text Message` : Store as the password.

`Image File Message` :  Store as an image file.



## Manual

1.  Type in `/start` to get the customized keyboard.

2. Press the `/image` button and send the **image file**.

   *Note* : Remember to press `Send as File` and **DO NOT** check *compression*.

3. Press the `/password` button and enter the password.

4. Press the `/encrypt` / `decrypt`button and wait for a response.

   + `Warning! Fail to encrypt!`

     This warning arises when you haven not entered the password or send the image file. Please make sure previous steps are finished. 

   + `Wait a moment...`

     Your image is being encrypted or decrypted now! 

     Wait about 5 ~ 10 seconds, the bot will send back the encrypted / decrypted image.

     *Note* : If there is no response for a too long period of time, *Time Out* may have occurred due to some server error or the file size is overwhelming. Please do *step 2 to 4* again or try another smaller image (or compress it before hand). 

5. Get the Image File!
6. Type in `/end` to clear your data.
