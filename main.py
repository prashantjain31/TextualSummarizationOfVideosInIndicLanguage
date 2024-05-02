from pytube import YouTube
import whisper
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
text_splitter = CharacterTextSplitter()
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
import requests
from gtts import gTTS

def download_youtube_audio(youtube_url):
    try:
        # Create a YouTube object
        yt = YouTube(youtube_url)

        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Download the audio stream
        audio_stream.download(output_path='./file/', filename='audio.wav')

        print("Audio downloaded successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")

# Example usage:
# youtube_url = "https://www.youtube.com/watch?v=mN-0jnKw6WY"
# output_path = "./file/"

# download_youtube_audio(youtube_url, output_path)

def transcribe_audio(model_name="base", verbose=True):
  # Load the Whisper model
  model = whisper.load_model(model_name)

  # Transcribe the audio
  result = model.transcribe(".\\file\\audio.wav", verbose=verbose)

  # Return the transcribed text
  with open('.\\file\\transcript.txt', 'w+') as f:
    for items in result['text']:
        f.write('%s' %items)
    print("File written successfully")
  f.close()
  
# Example usage
# audio_file = ".\\file\\audio.wav"
# transcription = transcribe_audio(audio_file)

# Initialize OpenAI with temperature (optional)
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="")

def summarize_txt():
  with open('./file/transcript.txt', encoding='utf-8') as f:
    state_of_the_union = f.read()
  texts = text_splitter.split_text(state_of_the_union)
  docs = [Document(page_content=t) for t in texts]
  chain = load_summarize_chain(llm, chain_type="map_reduce")
  return chain.run(docs)

summary = summarize_txt()
print(summary)

def translate(targetLanguage, summary):
    url = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"

    # Define the request payload
    payload = {
        "pipelineTasks": [
            {
                "taskType": "translation",
                "config": {
                    "language": {
                        "sourceLanguage": "en",
                        "targetLanguage": targetLanguage
                    },
                    "serviceId": "ai4bharat/indictrans-v2-all-gpu--t4"
                }
            }
        ],
        "inputData": {
            "input": [
                {
                    "source": summary
                }
            ]
        }
    }

    headers = {
        "Authorization": "",
        "Content-Type": "application/json"
    }

    # Send the POST request
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response
        print("Response:")
        print(response.json())
        return response.json()['pipelineResponse'][0]['output'][0]['target']
    else:
        # Print error message if request was unsuccessful
        print("Error:", response.status_code)
        print(response.text)

def save_summary_as_audio(translated_summary, language_code):
    tts = gTTS(translated_summary, lang=language_code, tld='co.in')
    tts.save('summary.wav')

# translated_summary =translate('kn', summary)
# print(translated_summary)
