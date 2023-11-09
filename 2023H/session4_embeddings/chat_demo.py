import torch
import psycopg2

import chainlit as cl
import pandas as pd

from chainlit import user_session
from transformers import AutoModelForSeq2SeqLM
from transformers import AutoTokenizer
from transformers import GenerationConfig
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer, util

# Last inn modellen
model_name='google/flan-t5-base'
original_model = AutoModelForSeq2SeqLM.from_pretrained(model_name, torch_dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

model_embedding = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

# Sett opp tilgang til PostgreSQL database
conn = psycopg2.connect(user="svalbard", 
                       password="", 
                       host="svalbard.postgres.database.azure.com", 
                       port=5432, 
                       database="postgres")

register_vector(conn)
cur = conn.cursor()

def ask_question(query: str, tableName: str):

    emb = model_embedding.encode(query)
    df = pd.read_sql(f"SELECT id, content, embedding <-> '{list(emb)}' AS distance FROM {tableName};", conn)
  
    content = list(df.sort_values('distance').iloc[0:2].content)
    content = '. '.join(content)
    
    prompt = f"""
    Answer the question using the content, never use anything out of the context.
    Content: {content}

    Question: {query}
    """

    inputs = tokenizer(prompt, return_tensors='pt')
    output = tokenizer.decode(
        model.generate(
            inputs["input_ids"], 
            max_new_tokens=100,
            temperature=0,
            top_k=3,
        )[0], 
        skip_special_tokens=True
    )

    return output.capitalize()



@cl.on_chat_start
async def main():
    res = await cl.AskUserMessage(content="Hva heter tabellen din?", timeout=60).send()
    if res:
        user_session.set("tableName", res['content'])
        await cl.Message(
            content=f"Da har jeg koblet meg på **{res['content']}** tabellen i databasen, spør meg noen spørsmål 🤖",
        ).send()

@cl.on_message
async def main(message: str, message_id: str):
    # do something
    tableName = user_session.get("tableName")

    result = ask_question(message, tableName)

    msg = cl.Message(
        content=result, disable_human_feedback=True
    )

    await msg.send()
