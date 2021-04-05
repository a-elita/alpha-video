---
id: doc3
title: Install
sidebar_label: Install
---

Once Docker is fully installed and running. Open a terminal on your device. I use powershell on windows. 

There is a few different versions of the docker image use the command bellow that matches your language. 

English: ``` docker run -d --restart unless-stopped --name alpha-video -p 5000:5000 -e subdomain=changeme andrewstech/alpha-video:latest ```


More lanugages to come.

That command downloads the latest version of the code and runs it in a virtual environment.

The part of the command which says changeme, change this to somthing unique to you. If you choose something generic like youtube then someone else will probably have already claimed the domain. A good example is andrewstech7863 . After you have changed that then run the command. It should start downloading multiple files and give you an output such as ``` 3493783796b56777987287120c5e3d4defa418d58825d22aa7b1a7c96dfa6604 ```. This means the code has been installed. Now we need to see if our unique domain was avalible.

Run ``` docker logs ``` followed by the number you just copyed. For example ``` docker logs 3493783796b56777987287120c5e3d4defa418d58825d22aa7b1a7c96dfa6604 ```.

This should show the logs of the skill and at the botten you should see the line ``` your url is: ```





