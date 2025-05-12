from real_estate_listing_generator import generate_real_estate_listings
import chromadb
import re
import os
from sentence_transformers import SentenceTransformer
import numpy as np
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma as LangChroma
from langchain.schema import Document

DEFAULT_API_BASE = "https://openai.vocareum.com/v1"

# Ask user for API key and (optionally) base URL
def get_openai_credentials():
    api_key = ""
    while not api_key:
        api_key = input("Enter your OPENAI_API_KEY (required): ").strip()
        if not api_key:
            print("OPENAI_API_KEY cannot be empty. Please try again.")

    api_base = input(f"Enter your OPENAI_API_BASE (optional, press Enter to use default: {DEFAULT_API_BASE}): ").strip()
    if not api_base:
        api_base = DEFAULT_API_BASE

    return api_key, api_base

OPENAI_API_KEY, OPENAI_API_BASE = get_openai_credentials()
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["OPENAI_API_BASE"] = OPENAI_API_BASE
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Initialize OpenAI client
client = OpenAI(
    base_url=os.environ["OPENAI_API_BASE"],
    api_key=os.environ["OPENAI_API_KEY"],
)

# Initialize ChromaDB
db_client = chromadb.PersistentClient("./chroma_db")
collection = db_client.get_or_create_collection(name="property_listings")

# Preference questions and defaults
questions = [
    "How big do you want your house to be?",
    "What are 3 most important things for you in choosing this property?",
    "Which amenities would you like?",
    "Which transportation options are important to you?",
    "How urban do you want your neighborhood to be?",
]
default_answers = [
    "A comfortable three-bedroom house with a spacious kitchen and a cozy living room.",
    "A quiet neighborhood, good local schools, and convenient shopping options.",
    "A backyard for gardening, a two-car garage, and a modern, energy-efficient heating system.",
    "Easy access to a reliable bus line, proximity to a major highway, and bike-friendly roads.",
    "A balance between suburban tranquility and access to urban amenities like restaurants and theaters."
]

def ask_user_preferences():
    print("\nPlease answer the following questions about your ideal property.\nYou may press Enter to skip a question (a default answer will be used).")
    preferences = []
    for idx, question in enumerate(questions):
        response = input(f"{question} (default: {default_answers[idx]}): ").strip()
        if response == "":
            response = default_answers[idx]
        preferences.append(response)
    return {
        "size": preferences[0],
        "important_factors": preferences[1],
        "amenities": preferences[2],
        "transport": preferences[3],
        "urbanity": preferences[4],
        "full_text": " ".join(preferences),
    }

def augment_listing_with_llm(listing, user_preferences):
    property_description = listing.metadata.get('description', '')
    neighborhood_description = listing.metadata.get('neighborhood_description', '')
    original_description = f"PROPERTY DESCRIPTION:\n{property_description}\n\nNEIGHBORHOOD DESCRIPTION:\n{neighborhood_description}"


    if isinstance(user_preferences, str):
        pref_text = user_preferences
        user_preferences = {
            'full_text': pref_text,
            'size': pref_text,
            'important_factors': pref_text,
            'amenities': pref_text,
            'transport': pref_text,
            'urbanity': pref_text,
        }

    prompt = f"""
    You are a real estate agent helping match a buyer with their ideal property.

    PROPERTY DESCRIPTION:
    {property_description}

    NEIGHBORHOOD DESCRIPTION:
    {neighborhood_description}

    FACTS ABOUT THE PROPERTY:
    - Neighborhood: {listing.metadata.get('neighborhood', 'N/A')}
    - Price: {listing.metadata.get('price', 'N/A')}
    - Bedrooms: {listing.metadata.get('bedrooms', 'N/A')}
    - Bathrooms: {listing.metadata.get('bathrooms', 'N/A')}
    - Size: {listing.metadata.get('size', 'N/A')}

    BUYER PREFERENCES:
    - Size preference: {user_preferences.get('size', '')}
    - Important factors: {user_preferences.get('important_factors', '')}
    - Desired amenities: {user_preferences.get('amenities', '')}
    - Transportation needs: {user_preferences.get('transport', '')}
    - Neighborhood style: {user_preferences.get('urbanity', '')}

    TASK: Rewrite the property description to subtly emphasize aspects that align with the buyer's preferences.
    Use neighborhood description to enhance the property description.
    DO NOT add any features that aren't mentioned in the original description or facts.
    DO NOT change any factual information about the property.
    DO highlight aspects of the property that match what the buyer is looking for.
    Keep a similar length to the original description.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful real estate copywriter."},
                      {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300,
        )

        augmented_description = response.choices[0].message.content.strip()
        return original_description, augmented_description

    except Exception as e:
        print(f"Error during LLM augmentation: {str(e)}")
        return original_description, original_description


# Function to perform semantic search using user preferences
def perform_semantic_search(user_pref_text, top_n=5):
    results = collection.get()
    if not results.get('ids'):
        print("No listings found in the collection. Please add listings first.")
        return []

    documents = [Document(page_content=doc, metadata=meta)
                for doc, meta in zip(results['documents'], results['metadatas'])]
    print(f"Searching through {len(documents)} property listings...")

    try:
        embeddings = OpenAIEmbeddings()
        db = LangChroma.from_documents(documents, embeddings)

        similar_docs = db.similarity_search(user_pref_text, k=top_n)

        print("\n----- Top Matching Properties -----")

        for i, doc in enumerate(similar_docs):
            print(f"\n{'-'*50}")
            print(f"Listing #{i+1}: {doc.metadata.get('neighborhood', 'N/A')} - {doc.metadata.get('price', 'N/A')}")
            print(f"Bedrooms: {doc.metadata.get('bedrooms', 'N/A')} | Bathrooms: {doc.metadata.get('bathrooms', 'N/A')} | Size: {doc.metadata.get('size', 'N/A')}")

            original_desc, augmented_desc = augment_listing_with_llm(doc, user_pref_text)

            print("\nOriginal Description:")
            print(original_desc)

            print("\nEnhanced Description with neighborhood context and user preferences:")
            print(augmented_desc)

        return similar_docs

    except Exception as e:
        print(f"Error with semantic search: {str(e)}")
        return []


# Function to process the Listings.txt file and extract property listings
def process_listings_file():
    with open('Listings.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    listings = []
    for block in re.split(r'-{10,}', text):
        if 'Listing' not in block:
            continue

        extract = lambda pattern: re.search(pattern, block)
        metadata = {
            'neighborhood': extract(r'Neighborhood: (.+)').group(1).strip() if extract(r'Neighborhood: (.+)') else '',
            'price': extract(r'Price: (.+)').group(1).strip() if extract(r'Price: (.+)') else '',
            'bedrooms': extract(r'Bedrooms: (\d+)').group(1).strip() if extract(r'Bedrooms: (\d+)') else '',
            'bathrooms': extract(r'Bathrooms: (\d+)').group(1).strip() if extract(r'Bathrooms: (\d+)') else '',
            'size': extract(r'(Home Size|House Size): (.+)').group(2).strip() if extract(r'(Home Size|House Size): (.+)') else '',
            'description': extract(r'Description:\n(.+?)\n\n').group(1).strip() if extract(r'Description:\n(.+?)\n\n') else '',
            'neighborhood_description': extract(r'Neighborhood Description:\n(.+?)\n\n').group(1).strip() if extract(r'Neighborhood Description:\n(.+?)\n\n') else '',
            'full_text': block.strip(),
        }
        listings.append(metadata)

    return listings

# Main function to handle user input and process listings
def main():
    existing_data = collection.get()
    if existing_data.get('ids'):
        reuse = input(f"Collection contains {len(existing_data['ids'])} listings. Use them? (yes/no): ").lower() == "yes"
        if reuse:
            preferences = ask_user_preferences()
            perform_semantic_search(preferences["full_text"])
            return
        else:
            collection.delete(ids=existing_data['ids'])

    if input("Generate new real estate listings? (yes/no): ").lower() == "yes":
        try:
            num_properties = max(1, int(input("Number of properties to generate: ")))
            temperature = max(0, min(2, float(input("Temperature (0.0-2.0): "))))
            generate_real_estate_listings(openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE, num_properties=num_properties, temperature=temperature)
        except ValueError:
            generate_real_estate_listings(openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE)

    listings = process_listings_file()
    if not listings:
        print("No valid listings found in Listings.txt.")
        return

    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    docs = [listing['full_text'] for listing in listings]
    embeddings = model.encode(docs)

    collection.add(
        ids=[f"listing_{i+1}" for i in range(len(listings))],
        embeddings=embeddings.tolist(),
        documents=docs,
        metadatas=listings,
    )
    print(f"Added {len(listings)} listings to collection")

    preferences = ask_user_preferences()
    perform_semantic_search(preferences["full_text"])

if __name__ == "__main__":
    main()
