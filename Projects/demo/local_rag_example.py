import chromadb
import logging
import uuid
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from openai import OpenAI

# Configuration parameters
BASE_URL = "http://localhost:11434"
API_KEY = "Welcome01"
STORAGE_PATH = "./vector_store"
EMBEDDING_MODEL = "mixedbread-ai/mxbai-embed-large-v1"
LLM_MODEL = "dolphin-mistral:7b"
QUESTION = "Which level 3 spells would be useful for a DND 5th edition eldritch knight elf focused on ranged combat?"
TOKEN_LENGTH = 16384

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize embedding model
embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)

# Hardcoded JSON documents
documents = [
    {"id": str(uuid.uuid4()), "text": "Fireball: A powerful level 3 spell for dealing damage at range.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Counterspell: Useful for negating enemy spells at a distance.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Blink: Provides a defensive mechanism by teleporting the caster randomly.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Haste: Enhances speed and combat effectiveness, but not specifically ranged.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Water Breathing: Allows the caster to breathe underwater, situationally useful.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Fly: Grants the ability to fly, which can be advantageous for ranged attacks.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Protection from Energy: Provides resistance to damage types, useful for defense.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Clairvoyance: Allows seeing and hearing from a distance, but not directly useful in combat.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Leomund's Tiny Hut: Creates a shelter, useful for resting but not combat.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Dispel Magic: Removes magical effects, can be useful in various situations.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Magic Circle: Protects against certain types of creatures, situationally useful.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Phantom Steed: Summons a horse-like creature for travel.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Slow: Reduces the speed and reaction times of enemies, useful for controlling combat.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Feign Death: Makes the caster appear dead, useful for deception.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Animate Dead: Reanimates corpses to serve the caster, not specifically ranged.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Tongues: Allows the caster to speak and understand any language.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Remove Curse: Removes curses from a target, situationally useful.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Stinking Cloud: Creates a cloud of gas that incapacitates enemies, useful for control.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Bestow Curse: Places a debilitating effect on a target.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Lightning Bolt: A powerful ranged attack spell.", "source": "spell_guide.html"},
    {"id": str(uuid.uuid4()), "text": "Hypnotic Pattern: Charms and incapacitates enemies in an area.", "source": "spell_guide.html"},
]

def transform_query(query: str) -> str:
    """Transform query for retrieval."""
    return f'Represent this sentence for searching relevant passages: {query}'

def get_query_embedding(query):
    transformed_query = transform_query(query)
    return embed_model.get_query_embedding(transformed_query)

def get_text_embeddings(texts):
    return embed_model.get_text_embedding_batch(texts, show_progress=True)

def generate_response(contexts, questions, llm_model):
    client = OpenAI(base_url=(BASE_URL + "/v1/"), api_key=API_KEY)
    responses = []
    for context, question in zip(contexts, questions):
        prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
        try:
            response = client.chat.completions.create(
                model=llm_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=TOKEN_LENGTH,
                temperature=0.1
            )
            result_text = response.choices[0].message.content.strip()
            responses.append(result_text)
        except Exception as e:
            logger.error(f"Error generating answer: {e}", exc_info=True)
            raise
    return responses

def index_documents(documents):
    client = chromadb.PersistentClient(path=STORAGE_PATH)
    collection_name = "documents"
    
    # Remove existing collection if it exists
    try:
        existing_collection = client.get_collection(name=collection_name)
        client.delete_collection(existing_collection.id)
        logger.info(f"Existing collection '{collection_name}' deleted.")
    except chromadb.CollectionNotFound:
        logger.info(f"No existing collection '{collection_name}' found.")

    # Create new collection
    collection = client.create_collection(name=collection_name)
    texts = [doc["text"] for doc in documents]
    embeddings = get_text_embeddings(texts)
    metadatas = [{"source": doc["source"]} for doc in documents]
    ids = [doc["id"] for doc in documents]
    collection.add(documents=texts, metadatas=metadatas, embeddings=embeddings, ids=ids)
    return collection

def query_vector_store(collection, query, top_k=5):
    embedding = get_query_embedding(query)
    results = collection.query(query_embeddings=[embedding], n_results=top_k, include=["documents", "metadatas"])
    return results

def main():
    collection = index_documents(documents)
    results = query_vector_store(collection, QUESTION, top_k=5)

    if results and 'documents' in results:
        contexts = " ".join([doc for docs in results['documents'] for doc in docs])
        answer = generate_response([contexts], [QUESTION], LLM_MODEL)
        logger.info(f"Question: {QUESTION}\nAnswer: {answer[0]}")
    else:
        logger.info("No relevant documents found.")

if __name__ == "__main__":
    main()
