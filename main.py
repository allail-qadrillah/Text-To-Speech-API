from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
import uvicorn
from gtts import gTTS
import tempfile
import json

app = FastAPI()

@app.get('/')
def main():

  languages   = open('languages.json', 'r')
  languages  = json.loads(languages.read())
 
  return {'status' : True,
         '/speak' : {
           'text' : 'string',
           'lang' : languages 
         }}

@app.get('/speak')
async def textToSpeech(text: str = Query(..., min_length=1),
                       lang: str = Query("id")):
          try:
            tts = gTTS(text, lang=lang)
  
            with tempfile.NamedTemporaryFile() as fp:
              filePath = fp.name + '.mp3'
              tts.save(filePath)
              return FileResponse(filePath)
          except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
            
if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)




