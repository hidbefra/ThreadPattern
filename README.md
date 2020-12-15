# ThreadPattern
Thread pattern
Deutsch:
    Dieses Projekt dient zum schwarz weiss bilder in Fadenbilder zu verwandeln. 

    Die berechung der Fäden basiert auf python mit openCV. 
    Produziert werden die Fadenbilder mit einem KUKA KR6 R900.

    Vorgehensweise:
      Bild auswählen und mit ThreadPattern.py zu einem Fadenbild verwandeln. Das ergebnis liegt in ausgabe.txt

      Mit dehm Roboter den Ring als Basis erfassen. Nulpunkt der Basis ist egal. Nur die XY-Ebene ist muss parallel zum Ring sein.

      Mindestens drei Punkte am Ring erfassen und mit circle-fit.py den Kreismittelpunkt erstellen.

      Eintragen des Kreismitelpunkt in Fadenlegen.dat in der Variablen KM. Orientierung A, B, C anpassen an den eigenen Greifer.
      Punkte[*] aus ausgabe.txt kopieren

Englisch
    This project is used to turn black and white pictures into thread pictures.

    The calculation of the threads is based on python with openCV.
    The thread patterns are produced with a KUKA KR6 R900.

    Method:
      Select an image and use ThreadPattern.py to transform it into a thread image. The result is in ausgabe.txt

      Grasp the ring as a base with the robot. The zero point of the base does not matter. Only the XY plane must be parallel to the ring.

      Record at least three points on the ring and create the center of the circle with circle-fit.py.

      Enter the circle center point in Fadenlegen.dat in the variable KM. Orientation A, B, C adapt to your own gripper.
      Copy points [*] from ausgabe.txt

![alt text](https://github.com/hidbefra/ThreadPattern/blob/main/herz-blur3.png?raw=true)
