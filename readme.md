# Real Estate Listing Generator

A Python project that generate, store, search, and enhance real estate property listings based on your preferences, using LLMs (OpenAI), sentence embeddings, and ChromaDB.

## Setup & Installation

1. Clone the repository and open the project directory.
2. Create and activate a virtual environment:
```bash
cd personalized_real_estate_agent

python3 -m venv venv

source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Run

Run the program from your terminal:

```bash
python3 HomeMatch.py
```

## Listings generation
The program comes with a pre-generated set of listings. You can generate new listings by answering yes to the prompt that asks if you want to generate a new listing, addtionally, you can choose the number of listings you want to generate and the temperature of the generation.

## Semantic Search
The program will ask you a series of questions to understand your preferences for the property you are looking for. The program will use your answers to search for the most relevant listings in the database. The program will return a list of the most relevant listings based on your answers.

## Augmentation
The listing descriptions retrieved from the database are augmented to better highlight how the property meets your preferences. This feature tends to hallucinate a little bit, but I left it as it is, because it's better showcasing the augmentation itself for the purpose of this exercise.

### Example of the augmentation:
```python
user_preferences = {
    'size': 'A comfortable three-bedroom house with a spacious kitchen and a cozy living room.',
    'important_factors': 'A quiet neighborhood, good local schools, and convenient shopping options.',
    'amenities': 'A backyard for gardening, a two-car garage, and a modern, energy-efficient heating system.',
    'transport': 'Easy access to a reliable bus line, proximity to a major highway, and bike-friendly roads.',
    'urbanity': 'A balance between suburban tranquility and access to urban amenities like restaurants and theaters.'
}
```

***ORIGINAL PROPERTY DESCRIPTION:***
Step into classic elegance with this sophisticated townhouse in the heart of Cobblestone Square. The grand entrance welcomes
you to a spacious interior featuring intricate moldings, coffered ceilings, and rich hardwood floors throughout. Entertain in
style with a formal dining room, gourmet kitchen outfitted with high-end appliances, and a cozy family room complete with a
fireplace perfect for cool evenings. Retreat to the luxurious primary suite including a sitting area, walk-in closet, and spa-like
en-suite bathroom. Enjoy outdoor living on the charming brick patio nestled amidst lush gardens—a true oasis in the city.

***ORIGINAL NEIGHBORHOOD DESCRIPTION:***
Cobblestone Square exudes historic charm combined with modern conveniences, boasting boutique shops, trendy cafes, and cultural
landmarks within walking distance. Residents can explore cobblestone streets lined with unique architecture while also having access
to parks for leisurely strolls or picnics. The vibrant energy of this neighborhood makes it an ideal place for those seeking luxury
living in a prime location.


***AUGMENTED PROPERTY DESCRIPTION:***
Discover a blend of classic charm and modern comfort in this elegant townhouse nestled in the sought-after Cobblestone Square neighborhood.
Step inside to find a spacious interior adorned with intricate moldings, coffered ceilings, and luxurious hardwood floors, embodying a perfect
mix of sophistication and coziness. Entertain effortlessly in the formal dining room and gourmet kitchen equipped with high-end appliances,
ideal for culinary enthusiasts. Unwind in the cozy family room by the fireplace, offering a warm ambiance for relaxing evenings.

Retreat to the opulent primary suite, featuring a sitting area, walk-in closet, and a spa-like en-suite bathroom, providing a serene sanctuary
within your home. Step outside to the charming brick patio surrounded by lush gardens, creating a private urban oasis for outdoor enjoyment.

Cobblestone Square offers a historic yet vibrant neighborhood setting, with boutique shops, trendy cafes, and cultural landmarks just a stroll
away. Explore the unique architecture and cobblestone streets while enjoying nearby parks for leisurely activities. Experience luxury living in
a prime location that perfectly balances suburban tranquility with urban amenities like restaurants and theaters.

This impeccable townhouse presents an opportunity to live in a comfortable five-bedroom property with three bathrooms, ideal for a family seeking
a spacious kitchen, cozy living spaces, and a backyard for gardening. With convenient shopping options, good local schools, and a quiet neighborhood
setting, this home meets the criteria for a modern, energy-efficient heating system and a two-car garage. Easy access to transportation options,
including a reliable bus line, proximity to a major highway, and bike-friendly roads, ensures convenience for daily commuting needs. Embrace the
perfect harmony of luxury living and practicality in this exquisite property.



