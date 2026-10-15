from google import genai
from 
api_key="AQ.Ab8RN6KWhKNVI9Z2YExhX9EUfoaVQv-aOxbviwxmiIhOEqtI9w"

#STEP1:authenticate

client=genai.Client(api_key=api_key)

prompt= 


        # Step 4: Call Gemini 2.5 Flash
    response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

    print(response.text)

response=client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
      

)

print(response.text)