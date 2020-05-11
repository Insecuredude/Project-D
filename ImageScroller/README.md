# README ImageScroller

### imageScroller.py
Met imageScroller.py kan je van een bepaalde Ecosia pagina de afbeeldingen in een urls.txt bestand schrijven. De URL kan je als argument meegeven. Als er geen url als argument wordt meegegeven, zal de code "https://www.ecosia.org/images?q=plastic+bottle" als url gebruiken.

-> imageScroller.py --url my_url

### download_images.py
download_images.py download de afbeeldingen van een bepaald bestand en plaats die in een output directory. De input en output directory moeten als argumenten meegegeven worden. Deze moeten ook allebei al bestaan. Het script maakt zelf geen directories aan. 

-> download_images.py --urls my_input --output my_output

### trash_images.tar
trash_images.tar bevat alle afbeeldingen tot nu toe. Dit bestand gaat gebruikt worden als dataset voor het trainen en testen van het Machine Learning algoritme. Om verschillende afvalsoorten te herkennen is het noodzakelijk om alle afbeeldingen een label te geven. Elke afvalsoort moet dus in de trash_images directory een eigen directory hebben.


### categorized_trash_images.tar
categorized_strash_images.tar bevat alle afbeeldingen tot nu toe. Deze afbeeldingen zijn gecategorizeerd met verschillende labels. Elke afbeelding heeft maar 1 label.
De afkortingen van de mappen/labels hebben de volgende betekenis:

bottles:

* BIH_CB: "Bottle in Hand, Colored Background"
    Afbeeldingen met een hand met een gekleurde achtergrond
* BIH_TC: "Bottle in Hand, Trash Can"
    Afbeeldingen met een hand met een afvalbak
* BIH_WB: "Bottle in Hand, White Background"
    Afbeeldingen met een hand met een witte achtergrond
* MB_CB: "Multiple Bottles, Colored Background"
    Meerdere flesjes met een gekleurde achtergrond
* MB_WB: "Multiple Bottles, White Background"
    Meerdere flesjes met een witte achtergrond
* SB_CB: "Single Bottle, Colored Background"
    Een flesje met een gekleurde achtergrond
* SB_WB: "Single Bottle, White Background"
    Een flesje met een witte achtergrond

cans:

* CIH_CB: "Can in Hand, Colored Background"
    Afbeeldingen met een hand met een gekleurde achtergrond
* CIH_WB: "Can in Hand, White Background"
    Afbeeldingen met een hand met een witte achtergrond
* MC_CB: "Multiple Cans, Colored Background"
    Meerdere blikjes met een gekleurde achtergrond
* MC_WB: "Multiple Cans, White Background"
    Meerdere blikjes met een witte achtergrond
* SC_CB: "Single Can, Colored Background"
    Een blikje met een gekleurde achtergrond
* SC_WB: "Single Can, White Background"
    Een blikje met een witte achtergrond
