# LLM RAG Chatbot over custom data with ui using streamlit

<h2> Large Langugate Model</h2> 
Language models have exploded on the internet ever since ChatGPT came out, and rightfully so. They can write essays, code entire programs, and even make memes. 
<br/>
<b> Limitations of Large Language models </b>    
i) They have limitations in tasks requiring external knowledge (for example, our knowledge base that is our private data) and factual information. For ex, if i ask Language model how much I spent this month, LLM wont be able to tel as its not trained on that data     
      
ii)  Language models become far more valuable if they can generate insights from any data that we provide, rather than just their original training data.

Since retraining those large language models from scratch costs millions of dollars and takes months, we need better ways to give our existing LLMs access to our custom data. RAG addresses the issue. 

       
<h3> Why RAG   </h3>    
Retrieval-augmented generation (RAG) integrates external information retrieval into the process of generating responses by Large Language Models (LLMs). It searches a database for information beyond its pre-trained knowledge base, significantly improving the accuracy and relevance of the generated responses..     <br/>

![image](https://github.com/padmapria/LM-RAG-Chatbot-over-custom-data/assets/31624929/9fb2e6bd-6998-47fd-aebd-cdd8663eb673)


The image above shows how a basic RAG system works. Before forwarding the question to the LLM, we have a layer that searches our knowledge base for the “relevant knowledge” to answer the user query. Specifically, in this case, the spending data from the last month. Our LLM can now generate a relevant non-hallucinated response about our budget.   

As your data grows, you’ll need efficient ways to identify the most relevant information for your LLM’s limited memory. This is where you’ll want a proper way to store and retrieve the specific data you’ll need for your query, without needing the LLM to remember it.    

      
<h3>Where is RAG being used?</h3>    
We can find RAG models being applied in many areas today, especially those who need factual accuracy and knowledge depth, as they are more knowledgeable and able to provide contextual responses        
         
<b>Real-World Applications:</b>   
<br/>
<b>Question answering:</b> This is perhaps the most prominent use case for RAG models. They power advanced question-answering systems that can retrieve relevant information from large knowledge bases and then generate fluent answers.   

<b>Language generation:</b> RAG enables more factual and contextualized text generation for contextualized text summarization from multiple sources   

<b>Data-to-text generation:</b> By retrieving relevant structured data, RAG models can generate product/business intelligence reports from databases or describing insights from data visualizations and charts    

<b>Multimedia understanding:</b> RAG isn’t limited to text - it can retrieve multimodal information like images, video, and audio to enhance understanding. Answering questions about images/videos by retrieving relevant textual context.  

Refer the site for more details   
https://qdrant.tech/articles/what-is-rag-in-ai/

<h2> Components of This Application</h2> 
<b>Elasticsearch</b><br/>
Elasticsearch is a powerful open-source search and analytics engine.<br/>
In this application, Elasticsearch is used to store and index data.<br/>
The RAG system queries the data from Elasticsearch to find relevant information needed to answer user queries.<br/>
<br/>
<br/>
<b>Streamlit</b><br/>
Streamlit is an open-source app framework for Machine Learning and Data Science projects that allows you to build interactive web applications quickly.<br/>
In this application, Streamlit is used to develop the user interface (UI), providing a user-friendly way to interact with the RAG system.<br/>
<br/>
<br/>
<b>Docker</b><br/>
The application is deployed in Docker as a Docker app, so you don't need to install any libraries on your computer.    
<br/>
**Note:** OpenAI immediately revokes the API key once it detects that the key has been exposed publicly. Therefore, do not expose your API key.

<br/>

Generate your OpenAI API key here: [Click Here](https://platform.openai.com/account/api-keys)

1. Clone this git repository from command prompt
git clone https://github.com/padmapria/LLM-RAG-Chatbot-over-custom-data-streamlit-App.git    
cd LLM-RAG-Chatbot-over-custom-data-with-streamlit-ui    

2. Create a `.env` file inside the 'app' folder and store the key as follows:     
OPENAI_API_KEY='YOUR_API_KEY_HERE'
ELASTIC_SEARCH_PWD=DkIedPPSCb

. Refer to the key in `rag.py` by:  
```python   
from dotenv import load_dotenv   
load_dotenv()   
openai_api_key = os.getenv("OPENAI_API_KEY")    
ELAST_SEARCH_PWD = os.getenv('ELASTIC_SEARCH_PWD')   
```
3. Install Docker Desktop on your computer and start Docker Desktop    

4. Start the application by running the command from the command prompt 
docker compose up -d



 

