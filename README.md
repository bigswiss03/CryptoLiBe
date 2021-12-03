# CryptoLiBe
Il progetto `CryptoLiBe`, elaborato dalla classe 4ABCDE (fu 3ABCDE) FaM del Liceo di Bellinzona (AS 2020-2021; 2021-2022), prevede la creazione di un Bot che acquisti e venda in modo automatico criptovalute.
## Installazione
Perché il Bot funzioni correttamente è necessario soddisfare alcuni requisiti:

* Installare `Python`. Recarsi nella [pagina di downlad](https://www.python.org/downloads/windows) (scegliere Python 3.8.10) e seguire il processo guidato di download e installazione.
* Installare alcuni pacchetti. Aprire il `Prompt dei comandi` (basta digitare `cmd` nella barra di ricerca di Windows) e digitare il comando `pip install youtube_dl pafy numpy opencv-python`.

I procedimenti appena descritti differiranno un po' se si utilizza un Mac.

## Risoluzione di problemi // Debug
### Errore `dislike_count`
L'errore è causato dal pacchetto `pafy`, non debitamente aggiornato dai suoi sviluppatori.<br>
Come risolvere il problema? Procediamo per step.
1. Ottenere l'errore e copiare l'indirizzo per la cartella che contiene il pacchetto `pafy`. Nel mio caso:
```
C:\Users\Giacomo\AppData\Local\Programs\Python\Python38\lib\site-packages\pafy\
```
2. Andate in quella cartella e aprite il file `backend_youtube_dl.py`, dal quale dovete eliminare la riga seguente
```
self._dislikes = self._ydl_info['dislike_count']
```
4. Salvate 
