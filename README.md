# Project Library Manager (PLM)
### A simple library manager for simple projects


![](https://github.com/Ardethian/PLM/blob/master/plm.gif?)


### What is PLM?
PLM is a plugin for Sublime Text 3 that saves you time by downloading your predefined libraries/frameworks and adding them to the ```<head>``` tag of your .html file without having to open your browser.


I created PLM after noticing that I've been practically doing the same thing over and over again - downloading the same libraries for various seperate projects.

With PLM, you just need to set up your own list of libraries using the plugin User Settings, like so:
```
"libraries": [
    {
        "name": "jQuery",
        "version": "1.8.2",
        "source": "https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.js"
    }
]
```

and watch the magic happen.

### Attachments
You can also add attachments for each library. For example, if you need both Bootstrap's CSS and JS files, you can just edit the plugin's user settings and add something like the following:

```
"libraries": [
    {
        "name": "Bootstrap (CSS + JS)",
        "version": "3.3.7",
        "source": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
        "attachments": [
            "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
        ]
    }
]
```

### Default folder name
As you can tell, the name of the default folder for downloaded libraries is "plm_libs". 

You can change that by adding the following to your plugin User Settings:
```
"includes_dirname": "myLibraries",
```