import time
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

def generate_real_estate_listings(num_properties=10, temperature=1):
    # Initialize LangChain's OpenAI LLM with your endpoint
    client = ChatOpenAI(
        openai_api_base="https://openai.vocareum.com/v1",
        openai_api_key="voc-558633062126677400528667f8c21cb5ff28.91749773",
        temperature=temperature,
        model="gpt-3.5-turbo",
        frequency_penalty=0.7,
        presence_penalty=0.7
    )

    listings = []

    # LangChain Prompt: will receive a string with 'previous_listings'
    template = """You are a professional real estate copywriter specializing in creating appealing property listings.
{previous_listings}
Generate a unique real estate listing with the following format:

Neighborhood: [Unique neighborhood name]
Price: [Price between $300,000 and $2,000,000]
Bedrooms: [Number between 1 and 6]
Bathrooms: [Number between 1 and 5]
House Size: [Size between 700 and 5,000 sqft]

Description: [A detailed, engaging description of the property highlighting its unique features, approximately 100-150 words]

Neighborhood Description: [A brief description of the neighborhood, including nearby amenities, approximately 50-75 words]

Examples for reference:

Neighborhood: Mariner’s Row
Price: €73,000
Bedrooms: 1
Bathrooms: 1
Home Size: 33m²

Description:
Experience effortless living in this streamlined, nautical-inspired studio tucked along the canal lanes of Mariner’s Row. Clever storage solutions maximize every inch of space, with built-in bookshelves and an elevated sleeping loft overlooking the water. Tall casement windows bathe the open-plan main room in northern light, while a compact designer kitchenette features ceramic tiling and stainless fittings. Step onto the Juliet balcony and watch the boats pass by, or relax by the cozy electric fireplace. Perfect for a solo professional or creative, this rare find blends harbour charm with contemporary flair.

Neighborhood Description:
Mariner’s Row is a lively district in a historic port city. Cobbled walkways connect quirky bookshops, artisan bakeries, and a floating weekly market. Residents enjoy picturesque vistas, tranquil cycling paths beside the canals, and a calendar packed with maritime festivals. Everything you need, from tram stops to trendy galleries, is just steps away.

Neighborhood: Sonnenfeld Vineyards
Price: €374,000
Bedrooms: 3
Bathrooms: 2
Home Size: 106m²

Description:
Nestled among rolling grape fields, this sun-washed farmhouse in Sonnenfeld Vineyards radiates rustic elegance. Wide-plank oak floors, exposed limestone walls, and a central fireplace fill the airy living spaces with warmth. The gourmet country kitchen boasts vintage tilework and leads directly to a pergola-shaded terrace—ideal for alfresco dining. Upstairs, the primary suite reveals panoramic views of surrounding vineyards, while a bespoke wine cellar downstairs offers the perfect tasting nook. Embrace country sophistication with modern comforts in a storybook wine-country retreat.

Neighborhood Description:
Sonnenfeld Vineyards is famed for its boutique wineries, cycling trails, and local harvest celebrations. Enjoy easy access to organic grocers, quiet picnic spots between rows of vines, and a friendly weekly farmer’s market. The tranquil ambiance suits families and anyone wishing to savor a slower, idyllic lifestyle.

Neighborhood: Steeplegate Arts Quarter
Price: €462,000
Bedrooms: 4
Bathrooms: 3
Home Size: 141m²

Description:
Discover urban artistry in this light-filled, loft-style residence perched atop a converted workshop in Steeplegate Arts Quarter. Boasting original steel beams, exposed brickwork, and expansive factory windows, this home celebrates industrial chic style with a splash of color from custom murals. The vast main space flows from a chef’s island kitchen to a sunroom and reading nook overlooking a private rooftop patio, lush with potted olive trees. Three bedrooms feature gallery-worthy picture rails, while the fourth is perfect for a studio or music room. Smart climate control and underfloor heating balance comfort with style.

Neighborhood Description:
Steeplegate Arts Quarter pulses with creative energy. Home to avant-garde galleries, jazz cafés, independent theaters, and weekend flea markets, the neighborhood buzzes day and night. Everything from boutique fabric shops to quirky record stores is just around the corner—making this the ultimate address for inspired city dwellers.

IMPORTANT:
• All features, locations, amenities, and styles must be totally unique—do not repeat or paraphrase from the three sample listings or prior generated output.
• Each listing must introduce a fresh architectural style, new setting (urban historic, mountain, vineyard, coastal, alpine village, art quarter, etc.), and one-of-a-kind amenities.
• Avoid any similarities to past descriptions: do not use overlaps in details, adjectives, or “template” language.
• Ensure a full range of size and room diversity: some listings must showcase compact, cozy homes (e.g., 1-2 bedrooms, 30-50m², single bathroom); others should highlight family or larger homes up to the allowed max. Choose combinations not clustering around a single size.
• All details must fit European standards (currency, meters, local lifestyle, etc.).

"""
    prompt = PromptTemplate(
        input_variables=["previous_listings"],
        template=template
    )

    chain = prompt | client

    print(f"Generating {num_properties} real estate listings...")

    for i in range(num_properties):
        print(f"Generating listing {i+1}/{num_properties}...")

        if listings:
            # Use last 5 generated listings for reference to avoid prompt overflow
            prev_window = "\n\n".join([f"Previous Listing {j+1}:\n{l}" for j, l in enumerate(listings[-5:])])
            previous_listings = f"Below are previous generated listings, do NOT repeat elements from these:\n\n{prev_window}\n"
        else:
            previous_listings = ""

        generated = chain.invoke({"previous_listings": previous_listings})
        listings.append(generated.content)
        print(f"Listing {i+1} generated successfully!")
        time.sleep(0.05)

    with open("Listings.txt", "w", encoding="utf-8") as file:
        for i, listing in enumerate(listings, 1):
            file.write(f"Listing {i}:\n\n")
            file.write(listing)
            file.write("\n\n" + "-"*50 + "\n\n")

    print("All listings have been successfully saved to Listings.txt")
    return f"Generated {num_properties} real estate listings and saved them to Listings.txt"

