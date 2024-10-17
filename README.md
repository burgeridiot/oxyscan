# Oxyscan 
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/burgeridiot/oxyscan/blob/master/README.md)
[![pt-pt](https://img.shields.io/badge/lang-pt--pt-green.svg)](https://github.com/burgeridiot/oxyscan/blob/master/README-pt-pt.md)

Oxyscan is a simple Python app built with Flet designed to work with hospitals that handle lots of oxygen bottles and that can't keep up with all of them. It allows you to:
- Add oxygen bottles on your device, with location, condition and even the patient using it available as additional information you can add.
- Save a localized list of bottles, and upload them to a database later if you are in a area without network.
- Not worry about setting up new devices for the app, as you can import a list of current bottles from said database, allowing you to just install the app on a new device and start immediately using it.
- Host your own Oxyscan server for free as this uses SQL for its database.

This app will require Android 4.0 +.


## Compiling
*side-note:* This app requires you to manually compile it. Why? It's related to how every hospital has their own server. Oxyscan does not come bundled with a main server or a server explorer as this could allow malicious actors to access servers with ease. Hence, having to manually compile it (because you gotta alter the server configurations.)

To compile, you will require:

- Flet + PyMySQL
- Flutter
- Android Studio (On Windows, unsure what else is needed on MacOS/Linux)
- Anything else that is requested to you by Flutter Doctor during compilation. (To check independently of compilation, download Flutter and run `flutter doctor -v`).

Simply download `oxyscan.py`, extract it to a folder, open your terminal in said folder and type in: `flet build apk --module-name oxyscan.py`. This process takes about a minute or so, but if you have all of the requirements then it should be successful. After that, it's ready to be installed in any device!


## Setting up a server
To set up a server, you simply need:
- MySQL and its prerequisites (if you are new, I suggest getting MySQL Workbench as well, as a visual interface is easier to work with.)

For anyone who's an expert in MySQL, this should be an easy task, but if it is your first time:

- If you haven't installed MySQL already, configure an additional user named "oxyscan_release" and grant it DB Admin permissions.
- Note down the port that you chose during MySQL's installation and the IP of your machine, and note down the password and user you created in the previous step.
- Boot up MySQL, and create a database named oxyscan.
- Replace the example `user` and `password` in the Python file with the ones you created as well as the `ip` and the `port`.
- Inside of the database, create a table named "garrafas", and add the columns: `garrafa_ID` (INT), `garrafa_Lote` (INT), `garrafa_Localizacao` (I used LONGTEXT, but you can use VARCHAR() as well) and `garrafa_Utente` (VARCHAR(120)).
And that's all you need to do.

Current Progress: `35%`
