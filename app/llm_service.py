from google import genai
from dotenv import load_dotenv
from google.genai.errors import ServerError, ClientError
load_dotenv()

client=genai.Client()
model_name="gemini-3.8-flash"

def ask_llm(user_message):
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=user_message,
            config={
                "system_instruction": "You are a ShopEase customer support assistant. Do not invent order information. If you don't know the answer, say 'I don't know'.",
            }
        )
        return response.text
    except ServerError:
        return "I'm sorry, the AI service is temporarily unavailable. Please try again in a moment."
    except ClientError:
        return "I'm sorry, the AI service is temporarily unavailable. Please try again later."
    except Exception:
        return "I'm sorry, something went wrong while processing your request."


def generate_final_response(user_message, agent_result):
    prompt = f"""
You are the ShopEase customer support assistant.

The customer asked:
{user_message}

The system retrieved the following verified result:
{agent_result}

Generate a clear and helpful response to the customer.

Rules:
- Use only the information in the verified result.
- Do not invent order, customer, refund, ticket, or policy information.
- Do not change any values from the verified result.
- If the result indicates failure, explain the failure clearly.
- Keep the response concise and professional.
"""

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text

    except ServerError:
        return "I'm sorry, the AI service is temporarily unavailable. Please try again in a moment."

    except ClientError:
        return "I'm sorry, there was a problem with the AI request. Please try again later."

    except Exception:
        return "I'm sorry, something went wrong while generating the response."