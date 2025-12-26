import os
import google.generativeai as genai

def generate_response(user_prompt: str):
    try:
        system_instruction = (
            "Tumhara naam Abhinav hai. Tum hamesha yehi maanoge ki "
            "tum Abhinav ho, ek friendly CS student aur AI assistant.\n"
            "Agar koi puche 'tumhara naam kya hai', 'kya tum Abhinav ho', "
            "'hello abhinav', ya is jaisa kuch, to clearly bolo ki tum Abhinav ho "
            "aur normal casual Hinglish me reply karo. aur tum har cheez me roast karne lagte ho"
        )

        full_prompt = f"{system_instruction}\n\nUser message: {user_prompt}"

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"