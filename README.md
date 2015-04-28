# Trinity - Web Application URL Collector

<table>
    <tr>
        <th>Version</th>
        <td>0.1</td>
    </tr>
    <tr>
        <th>Blog</th>
        <td><a http://securityhorror.blogspot.com/">http://securityhorror.blogspot.com/</a></td>
    </tr>
    <tr>
        <th>Github</th>
        <td><a https://github.com/rekcahemal/Trinity">https://github.com/rekcahemal/Trinity</a></td>
     <tr/>
    <tr>
       <th>Author</th>
       <td><a href="mailto:rekcahemal@gmail.com">GERASIMOS KASSARAS</a> (<a href="http://twitter.com/lamehacker">@lamehacker</a>)</td>
    </tr>
    <tr>
        <th>Copyright</th>
        <td>2013 Gerasimos Kassaras</td>
    </tr>
    <tr>
        <th>License</th>
        <td><a href="file.LICENSE.html">Apache License Version 2.0</a></td>
    </tr>
</table>


## Synopsis

Trinity is an Open Source,free url collector written for training purposes. 

### Trinity offers:

#### A stable, efficient, high-performance simple python url collector.

Trinity is a simple proof of concept python script that collects urls from sites that need no authentication nor use SSL.

#### Simplicity

In order to run Trinity to collect the urls from your site set the variables to the desired site url:

urlList = ["http://www.example.com/"] # Later on this url is going to be fed through command parser.
host = 'http://www.example.com/'
domain = 'www.example.com'

#### In simple terms

## Features

### General

Collects urls from:

 - a HTML tags.
 - link HTML tags.
 - script HTML tags.
 - meta HTML tags.

### Crawler

The crawler Trinity is using is http://www.crummy.com/software/BeautifulSoup/


### HTML Parser

Is based in BeautifulSoup soup version 4.

Documentation found in: http://www.crummy.com/software/BeautifulSoup/
Download: http://www.crummy.com/software/BeautifulSoup/bs4/download/

## Installation

You have to install BeautifulSoup. Instruction about that found here:
http://www.crummy.com/software/BeautifulSoup/bs4/doc/

## License

Trinity is licensed under the Apache License Version 2.0.<br/>

## Disclaimer

This is free software and you are allowed to use it as you see fit.
However, neither the development team nor any of our contributors can held
responsible for your actions or for any damage caused by the use of this software.
