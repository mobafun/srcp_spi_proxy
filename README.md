# model-rail-control

_english version below_

Python-Proxy zur Steuerung von Modellbahnanlagen

Bei diesem Python-Programm handelt es sich um einen Rückmelde-Decoder-Anschluss-Proxy.
Das ganze ist gedacht für Modellbahnanlagen die mit RocRail gesteuert werden und als Software-Zentrale den SRCP-Daemon verwenden.
Dieser Proxy schaltet sich zwischen diese beiden Programme und füttert RocRail mit Sensordaten eines MCP23S17.

== english ==

Python code controlling my model rail

This python project is a tiny feedback sensor integration proxy.
It is suited for model railroad layouts, that are controlled with rocrail and use the SRCP daemon as software control center.
This proxy is interposed between those two software packages and provides feedback sensor data for a MCP23S17 port expander to RocRail. 

## References
Python-Skript zur Steuerung des MCP23S17 am Raspberry Pi (Teil 2)[http://erik-bartmann.de/programmierung/downloads2.html#RasPi]



