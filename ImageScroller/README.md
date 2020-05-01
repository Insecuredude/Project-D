# Readme ImageScroller

### imageScroller.py
Met imageScroller.py kan je van een bepaalde Ecosia pagina de afbeeldingen in een urls.txt bestand schrijven. De URL kan je als argument meegeven. Als er geen url als argument wordt meegegeven, zal de code "https://www.ecosia.org/images?q=plastic+bottle" als url gebruiken.

-> imageScroller.py --url my_url

### download_images.py
download_images.py download de afbeeldingen van een bepaald bestand en plaats die in een output directory. De input en output directory moeten als argumenten meegegeven worden. Deze moeten ook allebei al bestaan. Het script maakt zelf geen directories aan. 

-> download_images.py --urls my_input --output my_output

### trash_images.tar
trash_images.tar bevat alle afbeeldingen tot nu toe. Dit bestand gaat gebruikt worden als dataset voor het trainen en testen van het Machine Learning algoritme. Om verschillende afvalsoorten te herkennen is het noodzakelijk om alle afbeeldingen een label te geven. Elke afvalsoort moet dus in de trash_images directory een eigen directory hebben.
