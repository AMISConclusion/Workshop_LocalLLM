import logging
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.schema import Document
from llama_index.llms import HuggingFaceLLM
import chromadb
from chromadb.config import Settings

# Configuration parameters
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "gpt-3.5-turbo"
QUESTION = "Which level 3 spells would be useful for a DND 5th edition eldritch knight elf focused on ranged combat?"
LOGGING_LEVEL = logging.INFO

# Configure logging
logging.basicConfig(level=LOGGING_LEVEL)
logger = logging.getLogger(__name__)

# Initialize embedding model
embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
llm = HuggingFaceLLM(model_name=LLM_MODEL)

# Hardcoded JSON documents
DOCUMENTS = [
    {"id": 1, "content": "Fireball is a powerful level 3 spell that deals significant damage in an area."},
    {"id": 2, "content": "Fly allows the caster to gain a flying speed for a duration."},
    {"id": 3, "content": "Counterspell can stop other casters from successfully casting their spells."},
    {"id": 4, "content": "Dispel Magic removes magical effects from an object or creature."},
    {"id": 5, "content": "Haste grants the target increased speed and additional actions in combat."},
    {"id": 6, "content": "Protection from Energy grants resistance to a chosen type of energy."},
    {"id": 7, "content": "Fear causes enemies to run away in panic, leaving them vulnerable."},
    {"id": 8, "content": "Major Image creates a large, detailed illusion that can move and make noise."},
    {"id": 9, "content": "Sleet Storm creates a storm of sleet that obscures vision and makes the ground slippery."},
    {"id": 10, "content": "Water Breathing allows a number of creatures to breathe underwater."},
    {"id": 11, "content": "Bestow Curse imposes a debilitating curse on a creature, affecting its abilities."},
    {"id": 12, "content": "Blink lets the caster shift to the Ethereal Plane and return unpredictably."},
    {"id": 13, "content": "Daylight creates a bright light that dispels darkness and affects creatures sensitive to light."},
    {"id": 14, "content": "Animate Dead raises undead minions to serve the caster."},
    {"id": 15, "content": "Call Lightning summons a storm cloud that can strike enemies with lightning bolts."},
    {"id": 16, "content": "Vampiric Touch allows the caster to drain life from a target and heal themselves."},
    {"id": 17, "content": "Phantom Steed creates a magical steed for fast travel."},
    {"id": 18, "content": "Stinking Cloud creates a cloud of gas that incapacitates those within it."},
    {"id": 19, "content": "Slow reduces the speed and reactions of enemies within an area."},
    {"id": 20, "content": "Hypnotic Pattern charms and incapacitates creatures that can see it."}
]

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./chromadb_store")
collection = client.get_or_create_collection(name="documents")

def index_documents(documents):
    """Index documents into ChromaDB."""
    texts = [doc['content'] for doc in documents]
    metadatas = [{"id": doc['id']} for doc in documents]
    embeddings = embed_model.get_text_embedding_batch(texts)
    
    collection.add(
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings
    )

def query_vector_store(query, top_k=5):
    """Query the indexed documents and return the most relevant ones."""
    query_embedding = embed_model.get_query_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results

def generate_answer(context, question):
    """Generate an answer from the LLM given a context and a question."""
    prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
    response = llm.generate(prompt, max_tokens=150)
    return response['choices'][0]['text'].strip()

def main():
    index_documents(DOCUMENTS)
    
    logger.info(f"Querying vector store with question: {QUESTION}")
    results = query_vector_store(QUESTION, top_k=5)

    if results:
        context = " ".join([doc for doc in results['documents']])
        answer = generate_answer(context, QUESTION)
        logger.info(f"Question: {QUESTION}\nAnswer: {answer}")
    else:
        logger.info("No relevant documents found.")

if __name__ == "__main__":
    main()
